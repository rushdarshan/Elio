"""
Generate high-resolution, polished diagrams for the UniHack PowerPoint presentation
with colors optimized for the white template background.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART_DIR = ROOT / "artifacts"
ART_DIR.mkdir(exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

def generate_process_flow_diagram():
    fig, ax = plt.subplots(figsize=(11, 4.4), dpi=300)
    # White background matching the slide
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    stages = [
        ("1. INGEST", "6-Col Supplier Feed\nSanitization & Clean", '#0284c7'),
        ("2. IDENTITY", "Brand & Mfr Resolution\nDistributor Blacklist", '#0284c7'),
        ("3. TAXONOMY", "3-Tier UNSPSC Engine\n1,000+ Categories", '#0284c7'),
        ("4. RETRIEVAL", "Manufacturer Specs\n& Evidence Harvest", '#0284c7'),
        ("5. EXTRACTION", "Attribute Value Mining\n& Fraction Parsing", '#0284c7'),
        ("6. DUAL-PASS", "100% Verbatim Span\nVerification Gate", '#16a34a'),
        ("7. DECISION", "Accept / Review / Refuse\nAppend-Only Event Log", '#16a34a'),
        ("8. DESCRIPTIONS", "Universal 5-Variant Pack\nInvoice, Mobile, Web", '#0284c7'),
        ("9. 252-EXPORT", "Formula-Protected\n252-Column Syndication", '#0284c7')
    ]

    # Render as two balanced rows
    y_top = 2.45
    y_bot = 0.45
    w = 1.8
    h = 1.45

    for i, (title, desc, color) in enumerate(stages):
        if i < 5:
            x = 0.35 + i * 2.1
            y = y_top
        else:
            x = 0.35 + (8 - i) * 2.6
            y = y_bot

        # Outer card box with light shadow effect
        shadow = patches.FancyBboxPatch((x + 0.03, y - 0.03), w, h, boxstyle="round,pad=0.08",
                                        linewidth=0, facecolor='#e2e8f0', alpha=0.6)
        ax.add_patch(shadow)

        bg_card = '#f0fdf4' if color == '#16a34a' else '#f8fafc'
        border_card = color
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                      linewidth=1.8, edgecolor=border_card, facecolor=bg_card)
        ax.add_patch(card)

        # Header tag
        ax.text(x + w/2, y + 1.1, title, color=color,
                fontsize=8.5, fontweight='bold', ha='center', va='center')
        # Description
        ax.text(x + w/2, y + 0.52, desc, color='#1e293b',
                fontsize=7.5, ha='center', va='center', linespacing=1.25)

        # Flow Arrows
        if i < 4:
            ax.annotate('', xy=(x + 2.05, y + 0.72), xytext=(x + w + 0.05, y + 0.72),
                        arrowprops=dict(arrowstyle="->", color='#0072ce', lw=2.0))
        elif i == 4:
            # Curve arrow down to stage 6
            ax.annotate('', xy=(x + w/2, y_bot + h + 0.05), xytext=(x + w/2, y_top - 0.05),
                        arrowprops=dict(arrowstyle="->", color='#16a34a', lw=2.0))
        elif i > 4 and i < 8:
            ax.annotate('', xy=(x - 0.25, y + 0.72), xytext=(x - 0.05, y + 0.72),
                        arrowprops=dict(arrowstyle="->", color='#0072ce', lw=2.0))

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.4)
    ax.axis('off')
    plt.tight_layout()
    
    out_path = ART_DIR / "diagram_process_flow.png"
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 4.4), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    layers = [
        ("LAYER 1: MULTI-SOURCE INGESTION & DATA SANITIZATION", 
         [("Supplier CSV / Excel Feed", "6 Columns Ingest (MPN, Desc, Mfr)"), 
          ("Placeholder Filter", "Sanitizes '-- Unbranded --' & generic stubs"), 
          ("Distributor Blacklist", "Blocks entity poisoning from middle-tier names")], 
         2.95, '#f8fafc', '#0072ce'),
        
        ("LAYER 2: 9-STAGE EVIDENCE-GATED ENRICHMENT & LINEAGE DAG", 
         [("Deterministic Normalization", "89 UOM Categories + 63 Fraction Mappings"), 
          ("Dual-Pass Gate", "100% Verbatim Character Span Anchoring"), 
          ("Cryptographic Receipt Engine", "Content-Addressed SHA-256 Hashes (rcpt_<id>)")], 
         1.65, '#f0fdf4', '#16a34a'),
          
        ("LAYER 3: GOVERNANCE, REPLAY & SYNDICATION PROJECTION", 
         [("5-Surface Operations Cockpit", "Pipeline Overview, Evidence Explorer, Custody Drawer"), 
          ("Decision Log & Replay Engine", "100% Byte-Identical Deterministic Replay"), 
          ("252-Column Syndication Export", "Formula Injection Protected UTF-8-SIG Output")], 
         0.35, '#f8fafc', '#0072ce')
    ]

    for title, boxes, y_pos, bg_col, border_col in layers:
        # Layer backdrop shadow
        shadow = patches.FancyBboxPatch((0.33, y_pos - 0.03), 10.35, 1.12, boxstyle="round,pad=0.08",
                                        linewidth=0, facecolor='#e2e8f0', alpha=0.6)
        ax.add_patch(shadow)

        # Layer backdrop
        backdrop = patches.FancyBboxPatch((0.3, y_pos), 10.35, 1.12, boxstyle="round,pad=0.08",
                                          linewidth=1.8, edgecolor=border_col, facecolor=bg_col)
        ax.add_patch(backdrop)
        ax.text(0.55, y_pos + 0.94, title, color=border_col, fontsize=8.5, fontweight='bold')

        # Sub-boxes
        for b_idx, (b_title, b_sub) in enumerate(boxes):
            bx = 0.55 + b_idx * 3.32
            by = y_pos + 0.12
            b_patch = patches.FancyBboxPatch((bx, by), 3.15, 0.72, boxstyle="round,pad=0.05",
                                             linewidth=1, edgecolor='#cbd5e1', facecolor='#ffffff')
            ax.add_patch(b_patch)
            ax.text(bx + 1.57, by + 0.46, b_title, color='#0f172a', fontsize=7.8, fontweight='bold', ha='center')
            ax.text(bx + 1.57, by + 0.20, b_sub, color='#475569', fontsize=6.8, ha='center')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.4)
    ax.axis('off')
    plt.tight_layout()

    out_path = ART_DIR / "diagram_architecture.png"
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == '__main__':
    generate_process_flow_diagram()
    generate_architecture_diagram()
