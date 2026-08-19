import sys
import os
import pprint

# Add parent directory to path so we can import our pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unihack_catalog.stages import run_pipeline
from competitors.uni_hack.competitor_baseline import CompetitorBaselineEnricher

class GauntletCritic:
    """
    A harsh critic that compares our pipeline output against the competitor baseline blind.
    It rates both records on strict catalog quality standards and picks the winner.
    """
    def evaluate(self, our_res: dict, competitor_res: dict) -> tuple:
        """
        Returns (winner_label, score_our, score_comp, gaps_our)
        """
        score_our = 0
        score_comp = 0
        gaps_our = []

        # 1. Entity Resolution Check (separate brand & manufacturer, stable IDs)
        our_identity = our_res.get("identity", {})
        comp_identity = competitor_res.get("identity", {})
        
        our_brand = our_identity.get("brand", {}).get("label")
        our_mfr = our_identity.get("brand", {}).get("parent")
        comp_brand = comp_identity.get("brand", {}).get("label")
        comp_mfr = comp_identity.get("brand", {}).get("parent")
        
        # Award points for separate resolved entities
        if our_brand != our_mfr and our_brand != "Unknown":
            score_our += 2
        else:
            gaps_our.append("Entity: Brand and Manufacturer are not separated as distinct nodes.")
            
        if comp_brand != comp_mfr and comp_brand != "Unknown":
            score_comp += 2

        # stable ID check
        if our_identity.get("brand", {}).get("id") != "B_PENDING" and our_identity.get("brand", {}).get("id") != "B_UNBRANDED":
            score_our += 1
        if comp_identity.get("brand", {}).get("id") != "B01":
            score_comp += 1

        # 2. Provenance / Custody Chain Check
        our_attrs = our_res.get("attributes", [])
        comp_attrs = competitor_res.get("attributes", [])

        our_prov_count = sum(1 for a in our_attrs if isinstance(a.get("source"), dict) and a.get("source").get("url"))
        comp_prov_count = sum(1 for a in comp_attrs if isinstance(a.get("source"), str) and "Regex" in a.get("source"))

        if our_prov_count > 0:
            score_our += our_prov_count * 2
        else:
            gaps_our.append("Provenance: Extracted attributes lack verifiable URL, span, or page coordinates.")
            
        score_comp += comp_prov_count * 0.5 # Regex matches get lower score because they lack source domain citations

        # 3. Description compliance (Check lengths and valid flags)
        our_descs = our_res.get("descriptions", {})
        comp_descs = competitor_res.get("descriptions", {})
        
        # Check lengths: mobile <= 40, invoice <= 30, short <= 80
        limits = {"mobile": 40, "invoice": 30, "short": 80}
        
        for k, limit in limits.items():
            our_d = our_descs.get(k)
            # handle both dict or Pydantic object
            our_text = our_d.get("text") if isinstance(our_d, dict) else getattr(our_d, "text", "")
            our_valid = our_d.get("valid") if isinstance(our_d, dict) else getattr(our_d, "valid", False)
            
            comp_text = comp_descs.get(k, "")
            
            if len(our_text) <= limit and our_valid:
                score_our += 1.5
            else:
                gaps_our.append(f"Descriptions: {k} description exceeds character limit of {limit} (length={len(our_text)}).")
                
            if len(comp_text) <= limit:
                score_comp += 1.5

        # Decide winner
        if score_our > score_comp:
            winner = "OURS"
        elif score_comp > score_our:
            winner = "COMPETITOR"
        else:
            winner = "TIE"

        return winner, score_our, score_comp, gaps_our

    def run_gauntlet(self, test_rows: list):
        print("="*60)
        print("GAUNTLET LOOP BLIND EVALUATION CRITIC")
        print("="*60)
        
        enricher = CompetitorBaselineEnricher()
        
        total_runs = 0
        our_wins = 0
        comp_wins = 0
        ties = 0

        for idx, row in enumerate(test_rows):
            mpn = row["MPN"]
            mfr = row["Manufacturer"]
            desc = row["Description"]
            
            print(f"\n[Row {idx+1}] MPN: {mpn} | Manufacturer: {mfr}")
            print(f"Input text: '{desc}'")
            
            # Run competitor
            comp_output = enricher.enrich_row(mpn, mfr, desc)
            
            # Run our pipeline
            our_output_pydantic, flat_export = run_pipeline(row)
            our_output = our_output_pydantic.model_dump()
            
            # Evaluate blind
            winner, score_our, score_comp, gaps = self.evaluate(our_output, comp_output)
            total_runs += 1
            
            if winner == "OURS":
                our_wins += 1
                status = "WIN"
            elif winner == "COMPETITOR":
                comp_wins += 1
                status = "LOSS"
            else:
                ties += 1
                status = "TIE"
                
            print(f"-> Result: {status} (Ours: {score_our:.1f} pts, Competitor: {score_comp:.1f} pts)")
            if gaps:
                print("   Ours Remaining Gaps:")
                for g in gaps:
                    print(f"   - {g}")
                    
        print("\n" + "="*60)
        print("GAUNTLET LOOP SUMMARY REPORT")
        print("="*60)
        print(f"Total Rows Evaluated: {total_runs}")
        print(f"Our Pipeline Wins:   {our_wins} ({our_wins/total_runs*100:.1f}%)")
        print(f"Competitor Wins:     {comp_wins} ({comp_wins/total_runs*100:.1f}%)")
        print(f"Ties:                {ties} ({ties/total_runs*100:.1f}%)")
        print("="*60)
        
        if our_wins == total_runs:
            print("\nSUCCESS: Our pipeline beat the competitor bar on all test cases!")
            return True
        else:
            print("\nNEEDS WORK: The critic found quality gaps in our pipeline's output.")
            return False

if __name__ == "__main__":
    test_data = [
        {
            "MPN": "K-596-VS",
            "Manufacturer": "Kohler",
            "Description": "Kohler K-596-VS Simplice Kitchen Faucet, Vibrant Stainless, 1.5 gpm, 1/2 in connection"
        },
        {
            "MPN": "Leland 9178-DST",
            "Manufacturer": "Delta Faucet",
            "Description": "Delta Leland Single Handle Pull-Down Kitchen Faucet in Matte Black, 1.8 gpm"
        },
        {
            "MPN": "PVC 00300 0600",
            "Manufacturer": "Charlotte Pipe",
            "Description": "Charlotte Pipe PVC Schedule 40 90 Degree Elbow 1/2 in Socket"
        }
    ]
    critic = GauntletCritic()
    critic.run_gauntlet(test_data)
