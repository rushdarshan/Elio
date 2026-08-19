import os
import math
import pandas as pd
from typing import Dict, List, Any

RAW_DIR = r"c:\Users\rushd\Downloads\Jesus WIn\data\raw"

# =============================================================================
# FALLBACK IS THE PERMANENT PATH (no Excel files exist in the demo).
# Module-level vocabularies below are the source of truth. ReferenceLoader
# methods keep their Excel-first shape but now fall back to these.
# =============================================================================

# --- 1. Taxonomy keywords -----------------------------------------------------
# keyword -> (dept, class_, fine, classpath)
# Match rule: case-insensitive substring; longest keyword wins, so resolve
# text like "PDSH4816AF Dishwasher SS - Display Only" by iterating
# TAXONOMY_KEYWORDS sorted by len(keyword) descending (see match_taxonomy).
AEC = "Appliances & Consumer Electronics"

TAXONOMY_KEYWORDS: Dict[str, tuple] = {
    # Appliances (seeded from gold: dept/class/fine/classpath of FRIGIDAIRE & Whirlpool rows)
    "dishwasher": ("Appliances", "Large Appliances", "Dishwashers", f"{AEC}>Kitchen Appliances>Built-In Dishwashers"),
    "refrigerator": ("Appliances", "Large Appliances", "Refrigerators", f"{AEC}>Kitchen Appliances>Refrigerators"),
    "fridge": ("Appliances", "Large Appliances", "Refrigerators", f"{AEC}>Kitchen Appliances>Refrigerators"),
    "range": ("Appliances", "Large Appliances", "Ranges", f"{AEC}>Kitchen Appliances>Ranges"),
    "oven": ("Appliances", "Large Appliances", "Ovens", f"{AEC}>Kitchen Appliances>Ovens"),
    "microwave": ("Appliances", "Small Appliances", "Microwaves", f"{AEC}>Kitchen Appliances>Microwaves"),
    "washer": ("Appliances", "Large Appliances", "Washers", f"{AEC}>Laundry Appliances>Washers"),
    "dryer": ("Appliances", "Large Appliances", "Dryers", f"{AEC}>Laundry Appliances>Dryers"),
    "water heater": ("Appliances", "Large Appliances", "Water Heaters", f"{AEC}>Water Heaters>Tank & Tankless Water Heaters"),
    "disposal": ("Appliances", "Large Appliances", "Disposals", f"{AEC}>Kitchen Appliances>Garbage Disposals"),
    # Plumbing fixtures
    "faucet": ("Plumbing", "Faucets", "Kitchen & Bath Sink Faucets", "Plumbing>Faucets>Kitchen & Bath Sink Faucets"),
    "sink": ("Plumbing", "Sinks", "Kitchen & Bath Sinks", "Plumbing>Sinks>Kitchen & Bath Sinks"),
    "shower": ("Plumbing", "Showers", "Shower Systems", "Plumbing>Showers>Shower Systems"),
    "tub": ("Plumbing", "Bath", "Bathtubs", "Plumbing>Bathtubs>Bathtubs"),
    "lavatory": ("Plumbing", "Lavatories", "Lavatories", "Plumbing>Lavatories>Lavatories"),
    "toilet": ("Plumbing", "Toilets", "Toilets", "Plumbing>Toilets>Toilets"),
    "bidet": ("Plumbing", "Toilets", "Bidets", "Plumbing>Toilets>Bidets"),
    # Valves
    "ball valve": ("Plumbing", "Valves", "Ball Valves", "Plumbing>Valves>Ball Valves"),
    "gate valve": ("Plumbing", "Valves", "Gate Valves", "Plumbing>Valves>Gate Valves"),
    "check valve": ("Plumbing", "Valves", "Check Valves", "Plumbing>Valves>Check Valves"),
    "valve": ("Plumbing", "Valves", "Valves", "Plumbing>Valves>Valves"),
    # Fittings
    "elbow": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "fitting": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "coupling": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "tee": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "flange": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "nipple": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "adapter": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "reducer": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "cap": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "union": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    "bushing": ("Plumbing", "Fittings", "Pipe Fittings", "Plumbing>Fittings>Pipe Fittings"),
    # Pipe
    "pvc": ("Plumbing", "Pipe", "PVC Pipe", "Plumbing>Pipe>PVC Pipe"),
    "cpvc": ("Plumbing", "Pipe", "CPVC Pipe", "Plumbing>Pipe>CPVC Pipe"),
    "pex": ("Plumbing", "Pipe", "PEX Tubing", "Plumbing>Pipe>PEX Tubing"),
    "pipe": ("Plumbing", "Pipe", "Pipe & Tubing", "Plumbing>Pipe>Pipe & Tubing"),
    "drain": ("Plumbing", "Drains", "Drains", "Plumbing>Drains>Drains"),
    "trap": ("Plumbing", "Drains", "Traps", "Plumbing>Drains>Traps"),
    # --- Real held-out categories (mined from the 1000-row sample) ---
    # Power tool accessories
    "cut-off": ("Hardware & Tools", "Power Tool Accessories", "Cut-Off Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Cut-Off Wheels & Discs"),
    "cutoff": ("Hardware & Tools", "Power Tool Accessories", "Cut-Off Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Cut-Off Wheels & Discs"),
    "cut off": ("Hardware & Tools", "Power Tool Accessories", "Cut-Off Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Cut-Off Wheels & Discs"),
    "disc": ("Hardware & Tools", "Power Tool Accessories", "Cut-Off Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Cut-Off Wheels & Discs"),
    "wheel": ("Hardware & Tools", "Power Tool Accessories", "Grinding Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Grinding Wheels & Discs"),
    "grinding": ("Hardware & Tools", "Power Tool Accessories", "Grinding Wheels & Discs", "Hardware & Tools>Power Tool Accessories>Grinding Wheels & Discs"),
    "flap": ("Hardware & Tools", "Power Tool Accessories", "Flap Discs & Wheels", "Hardware & Tools>Power Tool Accessories>Flap Discs & Wheels"),
    "masonry": ("Hardware & Tools", "Power Tool Accessories", "Masonry Cutting Discs", "Hardware & Tools>Power Tool Accessories>Masonry Cutting Discs"),
    "diamond": ("Hardware & Tools", "Power Tool Accessories", "Diamond Cutting Discs", "Hardware & Tools>Power Tool Accessories>Diamond Cutting Discs"),
    "blade": ("Hardware & Tools", "Power Tool Accessories", "Saw Blades", "Hardware & Tools>Power Tool Accessories>Saw Blades"),
    "teeth": ("Hardware & Tools", "Power Tool Accessories", "Saw Blades", "Hardware & Tools>Power Tool Accessories>Saw Blades"),
    "saw blade": ("Hardware & Tools", "Power Tool Accessories", "Saw Blades", "Hardware & Tools>Power Tool Accessories>Saw Blades"),
    "saw stop": ("Hardware & Tools", "Power Tools", "Table Saws", "Hardware & Tools>Power Tools>Table Saws"),
    "saw": ("Hardware & Tools", "Power Tools", "Saws", "Hardware & Tools>Power Tools>Saws"),
    "sanding": ("Hardware & Tools", "Power Tool Accessories", "Sanding Belts & Sheets", "Hardware & Tools>Power Tool Accessories>Sanding Belts & Sheets"),
    "belt": ("Hardware & Tools", "Power Tool Accessories", "Sanding Belts & Sheets", "Hardware & Tools>Power Tool Accessories>Sanding Belts & Sheets"),
    "abrasive": ("Hardware & Tools", "Power Tool Accessories", "Sanding Belts & Sheets", "Hardware & Tools>Power Tool Accessories>Sanding Belts & Sheets"),
    "stikit": ("Hardware & Tools", "Power Tool Accessories", "Sanding Belts & Sheets", "Hardware & Tools>Power Tool Accessories>Sanding Belts & Sheets"),
    "cubitron": ("Hardware & Tools", "Power Tool Accessories", "Sanding Belts & Sheets", "Hardware & Tools>Power Tool Accessories>Sanding Belts & Sheets"),
    "hole saw": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "step bit": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "brad": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "countersink": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "reamer": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "auger": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "bit": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "drill": ("Hardware & Tools", "Power Tool Accessories", "Drill Bits", "Hardware & Tools>Power Tool Accessories>Drill Bits"),
    "router": ("Hardware & Tools", "Power Tool Accessories", "Router Bits", "Hardware & Tools>Power Tool Accessories>Router Bits"),
    "socket adapter": ("Hardware & Tools", "Power Tool Accessories", "Sockets & Adapters", "Hardware & Tools>Power Tool Accessories>Sockets & Adapters"),
    "socket": ("Hardware & Tools", "Power Tool Accessories", "Sockets & Adapters", "Hardware & Tools>Power Tool Accessories>Sockets & Adapters"),
    "eyewear": ("Hardware & Tools", "Safety", "Safety Eyewear", "Hardware & Tools>Safety>Safety Eyewear"),
    "goggle": ("Hardware & Tools", "Safety", "Safety Eyewear", "Hardware & Tools>Safety>Safety Eyewear"),
    "tape": ("Hardware & Tools", "Measuring Tools", "Tape Measures", "Hardware & Tools>Measuring Tools>Tape Measures"),
    "clamp": ("Hardware & Tools", "Woodworking Tools", "Clamps & Jigs", "Hardware & Tools>Woodworking Tools>Clamps & Jigs"),
    "jig": ("Hardware & Tools", "Woodworking Tools", "Clamps & Jigs", "Hardware & Tools>Woodworking Tools>Clamps & Jigs"),
    "kreg": ("Hardware & Tools", "Woodworking Tools", "Clamps & Jigs", "Hardware & Tools>Woodworking Tools>Clamps & Jigs"),
    "workbench": ("Hardware & Tools", "Woodworking Tools", "Workbenches", "Hardware & Tools>Woodworking Tools>Workbenches"),
    # Lighting
    "ceiling fan": ("Lighting", "Ceiling Fans", "Ceiling Fans", "Lighting>Ceiling Fans>Ceiling Fans"),
    "fan": ("Lighting", "Ceiling Fans", "Ceiling Fans", "Lighting>Ceiling Fans>Ceiling Fans"),
    "pendant": ("Lighting", "Light Fixtures", "Pendant Lighting", "Lighting>Light Fixtures>Pendant Lighting"),
    "chandelier": ("Lighting", "Light Fixtures", "Chandeliers", "Lighting>Light Fixtures>Chandeliers"),
    "vanity": ("Lighting", "Light Fixtures", "Vanity Lighting", "Lighting>Light Fixtures>Vanity Lighting"),
    "flush mount": ("Lighting", "Light Fixtures", "Flush Mount Fixtures", "Lighting>Light Fixtures>Flush Mount Fixtures"),
    "recessed": ("Lighting", "Light Fixtures", "Recessed Lighting", "Lighting>Light Fixtures>Recessed Lighting"),
    "fixture": ("Lighting", "Light Fixtures", "Ceiling Fixtures", "Lighting>Light Fixtures>Ceiling Fixtures"),
    "lamp": ("Lighting", "Light Fixtures", "Lamps", "Lighting>Light Fixtures>Lamps"),
    "fluorescent": ("Lighting", "Light Bulbs", "Fluorescent Bulbs", "Lighting>Light Bulbs>Fluorescent Bulbs"),
    "cfl": ("Lighting", "Light Bulbs", "Fluorescent Bulbs", "Lighting>Light Bulbs>Fluorescent Bulbs"),
    "incandescent": ("Lighting", "Light Bulbs", "Incandescent Bulbs", "Lighting>Light Bulbs>Incandescent Bulbs"),
    "halogen": ("Lighting", "Light Bulbs", "Halogen Bulbs", "Lighting>Light Bulbs>Halogen Bulbs"),
    "t8": ("Lighting", "Light Bulbs", "Fluorescent Bulbs", "Lighting>Light Bulbs>Fluorescent Bulbs"),
    "t12": ("Lighting", "Light Bulbs", "Fluorescent Bulbs", "Lighting>Light Bulbs>Fluorescent Bulbs"),
    "e26": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "mr16": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "par30": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "par38": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "lumen": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "lumens": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "bulb": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "led": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    "watt": ("Lighting", "Light Bulbs", "LED Bulbs", "Lighting>Light Bulbs>LED Bulbs"),
    # Electrical
    "wire": ("Electrical", "Wire & Cable", "Building Wire", "Electrical>Wire & Cable>Building Wire"),
    "cable": ("Electrical", "Wire & Cable", "Building Wire", "Electrical>Wire & Cable>Building Wire"),
    "outlet": ("Electrical", "Devices", "Receptacles", "Electrical>Devices>Receptacles"),
    "receptacle": ("Electrical", "Devices", "Receptacles", "Electrical>Devices>Receptacles"),
    "switch": ("Electrical", "Devices", "Switches", "Electrical>Devices>Switches"),
    "gfci": ("Electrical", "Devices", "Receptacles", "Electrical>Devices>Receptacles"),
    "dimmer": ("Electrical", "Devices", "Dimmers", "Electrical>Devices>Dimmers"),
    # Building materials
    "lumber": ("Building Materials", "Lumber & Composites", "Lumber Boards", "Building Materials>Lumber & Composites>Lumber Boards"),
    "stud": ("Building Materials", "Framing Lumber", "Studs", "Building Materials>Framing Lumber>Studs"),
    "board": ("Building Materials", "Lumber & Composites", "Boards & Planks", "Building Materials>Lumber & Composites>Boards & Planks"),
    "plywood": ("Building Materials", "Plywood & Panels", "Plywood", "Building Materials>Plywood & Panels>Plywood"),
    "osb": ("Building Materials", "Plywood & Panels", "OSB Panels", "Building Materials>Plywood & Panels>OSB Panels"),
    "decking": ("Building Materials", "Decking", "Composite Decking", "Building Materials>Decking>Composite Decking"),
    "trex": ("Building Materials", "Decking", "Composite Decking", "Building Materials>Decking>Composite Decking"),
    "timbertech": ("Building Materials", "Decking", "Composite Decking", "Building Materials>Decking>Composite Decking"),
    "moulding": ("Building Materials", "Moulding & Trim", "Moulding", "Building Materials>Moulding & Trim>Moulding"),
    "molding": ("Building Materials", "Moulding & Trim", "Moulding", "Building Materials>Moulding & Trim>Moulding"),
    "trim": ("Building Materials", "Moulding & Trim", "Trim", "Building Materials>Moulding & Trim>Trim"),
    "fascia": ("Building Materials", "Moulding & Trim", "Fascia", "Building Materials>Moulding & Trim>Fascia"),
    "siding": ("Building Materials", "Siding", "Exterior Siding", "Building Materials>Siding>Exterior Siding"),
    "smartside": ("Building Materials", "Siding", "Exterior Siding", "Building Materials>Siding>Exterior Siding"),
    "hardie": ("Building Materials", "Siding", "Exterior Siding", "Building Materials>Siding>Exterior Siding"),
    "lattice": ("Building Materials", "Lattice & Fencing", "Lattice", "Building Materials>Lattice & Fencing>Lattice"),
    "drywall": ("Building Materials", "Drywall", "Drywall Panels", "Building Materials>Drywall>Drywall Panels"),
    "joist": ("Building Materials", "Framing Lumber", "Joists", "Building Materials>Framing Lumber>Joists"),
    "cast stone": ("Building Materials", "Concrete & Masonry", "Cast Stone", "Building Materials>Concrete & Masonry>Cast Stone"),
    "concrete": ("Building Materials", "Concrete & Masonry", "Concrete Products", "Building Materials>Concrete & Masonry>Concrete Products"),
    "cement": ("Building Materials", "Concrete & Masonry", "Concrete Products", "Building Materials>Concrete & Masonry>Concrete Products"),
    "window": ("Building Materials", "Windows & Doors", "Windows", "Building Materials>Windows & Doors>Windows"),
    "door": ("Building Materials", "Windows & Doors", "Doors", "Building Materials>Windows & Doors>Doors"),
}


def match_taxonomy(text: str) -> tuple:
    """Longest-keyword substring match. 'Dishwasher' wins over 'washer'."""
    t = str(text).lower()
    for kw, entry in sorted(TAXONOMY_KEYWORDS.items(), key=lambda kv: len(kv[0]), reverse=True):
        if kw in t:
            return entry
    return ("Other", "Other", "Other", "")


# --- 2. Brand vocabulary ------------------------------------------------------
# canonical brand (gold casing incl. ®) -> {manufacturer, mfr_url[, alias_of]}
BRAND_VOCAB: Dict[str, dict] = {
    # Gold-seeded
    "FRIGIDAIRE®": {"manufacturer": "Rheem Manufacturing",
                    "mfr_url": "https://www.frigidaire.com/en/p/owner-center/product-support/{mpn}"},
    "Whirlpool": {"manufacturer": "Whirlpool Corporation", "mfr_url": "https://www.whirlpool.com"},
    "Whirlpool®": {"manufacturer": "Whirlpool Corporation", "mfr_url": "https://www.whirlpool.com", "alias_of": "Whirlpool"},
    # Plumbing brands
    "Kohler": {"manufacturer": "Kohler Co.", "mfr_url": "https://www.kohler.com"},
    "Delta Faucet": {"manufacturer": "Delta Faucet Company", "mfr_url": "https://www.deltafaucet.com"},
    "Moen": {"manufacturer": "Moen Incorporated", "mfr_url": "https://www.moen.com"},
    "American Standard": {"manufacturer": "American Standard Brands", "mfr_url": "https://www.americanstandard-us.com"},
    "Charlotte Pipe": {"manufacturer": "Charlotte Pipe and Foundry Company", "mfr_url": "https://www.charlottepipe.com"},
    "Mueller": {"manufacturer": "Mueller Industries", "mfr_url": "https://www.muellerindustries.com"},
    "Watts": {"manufacturer": "Watts Water Technologies", "mfr_url": "https://www.watts.com"},
    "NIBCO": {"manufacturer": "NIBCO Inc.", "mfr_url": "https://www.nibco.com"},
    "SharkBite": {"manufacturer": "Reliance Worldwide Corporation", "mfr_url": "https://www.sharkbite.com"},
    "PEX": {"manufacturer": "Uponor", "mfr_url": "https://www.uponor.com"},
    "Grohe": {"manufacturer": "Grohe AG", "mfr_url": "https://www.grohe.us"},
    "Hansgrohe": {"manufacturer": "Hansgrohe SE", "mfr_url": "https://www.hansgrohe-usa.com"},
    "Pfister": {"manufacturer": "Pfister Faucets", "mfr_url": "https://www.pfisterfaucets.com"},
    "Kingston Brass": {"manufacturer": "Kingston Brass", "mfr_url": "https://www.kingstonbrass.com"},
    "Glacier Bay": {"manufacturer": "The Home Depot", "mfr_url": "https://www.homedepot.com"},
    "Danco": {"manufacturer": "Danco Inc.", "mfr_url": "https://www.danco.com"},
    "Fluidmaster": {"manufacturer": "Fluidmaster Inc.", "mfr_url": "https://www.fluidmaster.com"},
    "Sloan": {"manufacturer": "Sloan Valve Company", "mfr_url": "https://www.sloan.com"},
    "TOTO": {"manufacturer": "TOTO USA", "mfr_url": "https://www.totousa.com"},
    "JAG Plumbing Products": {"manufacturer": "JAG Plumbing Products", "mfr_url": "https://www.jagplumbing.com"},
    "Zoeller": {"manufacturer": "Zoeller Company", "mfr_url": "https://www.zoeller.com"},
    "Liberty Pumps": {"manufacturer": "Liberty Pumps Inc.", "mfr_url": "https://www.libertypumps.com"},
    "Zurn": {"manufacturer": "Zurn Elkay Water Solutions", "mfr_url": "https://www.zurn.com"},
    "Crane": {"manufacturer": "American Standard Brands", "mfr_url": "https://www.craneplumbing.com"},
    "Chicago Faucets": {"manufacturer": "Geberit Group", "mfr_url": "https://www.chicagofaucets.com"},
    # Appliance brands
    "GE Appliances": {"manufacturer": "GE Appliances (Haier)", "mfr_url": "https://www.geappliances.com"},
    "LG": {"manufacturer": "LG Electronics", "mfr_url": "https://www.lg.com"},
    "Samsung": {"manufacturer": "Samsung Electronics", "mfr_url": "https://www.samsung.com"},
    "Bosch": {"manufacturer": "BSH Home Appliances", "mfr_url": "https://www.bosch-home.com"},
    "Maytag": {"manufacturer": "Whirlpool Corporation", "mfr_url": "https://www.maytag.com"},
    "Hotpoint": {"manufacturer": "GE Appliances (Haier)", "mfr_url": "https://www.hotpoint.com"},
    "Amana": {"manufacturer": "Whirlpool Corporation", "mfr_url": "https://www.amana.com"},
    "KitchenAid": {"manufacturer": "Whirlpool Corporation", "mfr_url": "https://www.kitchenaid.com"},
    "Electrolux": {"manufacturer": "Electrolux Group", "mfr_url": "https://www.electrolux.com"},
    "Viking": {"manufacturer": "Viking Range LLC", "mfr_url": "https://www.vikingrange.com"},
    "Dacor": {"manufacturer": "Dacor (Samsung)", "mfr_url": "https://www.dacor.com"},
    "Fisher & Paykel": {"manufacturer": "Fisher & Paykel Appliances", "mfr_url": "https://www.fisherpaykel.com"},
    "Midea": {"manufacturer": "Midea Group", "mfr_url": "https://www.midea.com"},
    "Rinnai": {"manufacturer": "Rinnai America", "mfr_url": "https://www.rinnai.us"},
    # Water heaters
    "Rheem": {"manufacturer": "Rheem Manufacturing Company", "mfr_url": "https://www.rheem.com"},
    "Bradford White": {"manufacturer": "Bradford White Corporation", "mfr_url": "https://www.bradfordwhite.com"},
    "AO Smith": {"manufacturer": "A. O. Smith Corporation", "mfr_url": "https://www.aosmith.com"},
    "State": {"manufacturer": "A. O. Smith Corporation", "mfr_url": "https://www.statewaterheaters.com"},
    # Aliases (no ® / alternate casing / common shorthands)
    "Frigidaire": {"manufacturer": "Rheem Manufacturing", "mfr_url": "https://www.frigidaire.com", "alias_of": "FRIGIDAIRE®"},
    # --- Real held-out manufacturers (mined from the 1000-row sample) ---
    # Manufacturer-name keys match Part_Manuf text ("Freud Inc (2435)" -> "Freud Inc").
    "Phillips Lighting": {"manufacturer": "Phillips Lighting", "mfr_url": "https://www.lighting.philips.com"},
    "Philips": {"manufacturer": "Phillips Lighting", "mfr_url": "https://www.lighting.philips.com", "alias_of": "Philips"},
    "Milwaukee Accessory": {"manufacturer": "Milwaukee Tool", "mfr_url": "https://www.milwaukeetool.com", "supplier": True},
    "Milwaukee": {"manufacturer": "Milwaukee Tool", "mfr_url": "https://www.milwaukeetool.com"},
    "Milw": {"manufacturer": "Milwaukee Tool", "mfr_url": "https://www.milwaukeetool.com", "alias_of": "Milwaukee"},
    "Wera": {"manufacturer": "Wera Tools", "mfr_url": "https://www.wera.de"},
    "CertainTeed": {"manufacturer": "CertainTeed (Saint-Gobain)", "mfr_url": "https://www.certainteed.com"},
    "Cooper Lighting": {"manufacturer": "Cooper Lighting (Eaton)", "mfr_url": "https://www.cooperlighting.com"},
    "ACG Brands": {"manufacturer": "ACG Brands", "mfr_url": ""},
    "Senco": {"manufacturer": "Senco Products", "mfr_url": "https://www.senco.com"},
    "National Nail": {"manufacturer": "National Nail Corp", "mfr_url": "https://www.nationalnail.com"},
    "Prebena": {"manufacturer": "Prebena", "mfr_url": "https://www.prebena.com"},
    "Marshalltown": {"manufacturer": "Marshalltown Trowel", "mfr_url": "https://www.marshalltown.com"},
    "Ohio Firewatch Protection": {"manufacturer": "Ohio Firewatch Protection", "mfr_url": ""},
    "First Alert": {"manufacturer": "BRK Brands", "mfr_url": "https://www.firstalert.com"},
    "Boise Cascade Building Materials": {"manufacturer": "Boise Cascade Company", "mfr_url": "https://www.bc.com"},
    "Boise Cascade": {"manufacturer": "Boise Cascade Company", "mfr_url": "https://www.bc.com"},
    "Appliance Dealers Cooperative": {"manufacturer": "Appliance Dealers Cooperative", "mfr_url": ""},
    "Kichler Lighting": {"manufacturer": "Kichler Lighting", "mfr_url": "https://www.kichler.com"},
    "Kichler": {"manufacturer": "Kichler Lighting", "mfr_url": "https://www.kichler.com"},
    "Parksite": {"manufacturer": "Parksite Inc", "mfr_url": "https://www.parksite.com"},
    "Black & Decker": {"manufacturer": "Stanley Black & Decker", "mfr_url": "https://www.stanleyblackanddecker.com"},
    "DEWALT": {"manufacturer": "Stanley Black & Decker", "mfr_url": "https://www.dewalt.com"},
    "Freud Inc": {"manufacturer": "Freud Inc", "mfr_url": "https://www.freudtools.com"},
    "Freud": {"manufacturer": "Freud Inc", "mfr_url": "https://www.freudtools.com"},
    "Diablo": {"manufacturer": "Freud Inc", "mfr_url": "https://www.freudtools.com"},
    "U S Lumber": {"manufacturer": "US Lumber Group", "mfr_url": "https://www.uslumber.com"},
    "Satco Prod Inc": {"manufacturer": "Satco Products", "mfr_url": "https://www.satco.com"},
    "Satco": {"manufacturer": "Satco Products", "mfr_url": "https://www.satco.com"},
    "Makita Usa Inc": {"manufacturer": "Makita USA", "mfr_url": "https://www.makitatools.com"},
    "Makita": {"manufacturer": "Makita USA", "mfr_url": "https://www.makitatools.com"},
    "Southwire": {"manufacturer": "Southwire Company", "mfr_url": "https://www.southwire.com"},
    "Leviton Mfg Co": {"manufacturer": "Leviton Manufacturing", "mfr_url": "https://www.leviton.com"},
    "Leviton": {"manufacturer": "Leviton Manufacturing", "mfr_url": "https://www.leviton.com"},
    "Festool USA": {"manufacturer": "Festool USA", "mfr_url": "https://www.festool.com"},
    "Festool": {"manufacturer": "Festool USA", "mfr_url": "https://www.festool.com"},
    "Tech Gear 5.7 Inc": {"manufacturer": "Tech Gear 5.7", "mfr_url": ""},
    "Kreg Tool Company": {"manufacturer": "Kreg Tool", "mfr_url": "https://www.kregtool.com"},
    "Kreg": {"manufacturer": "Kreg Tool", "mfr_url": "https://www.kregtool.com"},
    "U S Tape Company": {"manufacturer": "US Tape Company", "mfr_url": "https://www.ustape.com"},
    "Edge Eyewear Inc": {"manufacturer": "Edge Eyewear", "mfr_url": "https://www.edgeeyewear.com"},
    "Mirka Abrasives Inc": {"manufacturer": "Mirka Abrasives", "mfr_url": "https://www.mirka.com"},
    "Mirka": {"manufacturer": "Mirka Abrasives", "mfr_url": "https://www.mirka.com"},
    "Palmer Donavin Mfg Company": {"manufacturer": "Palmer Donavin", "mfr_url": "https://www.palmerdonavin.com"},
    "Hunter Fan Co": {"manufacturer": "Hunter Fan Company", "mfr_url": "https://www.hunterfan.com"},
    "Hunter": {"manufacturer": "Hunter Fan Company", "mfr_url": "https://www.hunterfan.com"},
    "Premier Metals": {"manufacturer": "Premier Metals", "mfr_url": ""},
    "Vessel Tools USA Inc": {"manufacturer": "Vessel Tools", "mfr_url": "https://www.vesseltools.com"},
    "Oliver Machinery Company": {"manufacturer": "Oliver Machinery", "mfr_url": "https://www.olivermachinery.net"},
    "Jam Industrial Supply LLC": {"manufacturer": "JAM Industrial Supply", "mfr_url": ""},
    "3M": {"manufacturer": "3M Company", "mfr_url": "https://www.3m.com"},
    "Bow Products": {"manufacturer": "Bow Products", "mfr_url": ""},
    "Prime Wire & Cable": {"manufacturer": "Prime Wire & Cable", "mfr_url": "https://www.primewire.com"},
    "Prime": {"manufacturer": "Prime Wire & Cable", "mfr_url": "https://www.primewire.com"},
    "Saw Stop LLC": {"manufacturer": "SawStop", "mfr_url": "https://www.sawstop.com"},
    "SawStop": {"manufacturer": "SawStop", "mfr_url": "https://www.sawstop.com"},
    "United Window & Door Manufacturing": {"manufacturer": "United Window & Door", "mfr_url": "https://www.unitedwindow.com"},
    "United Window & Door": {"manufacturer": "United Window & Door", "mfr_url": "https://www.unitedwindow.com"},
    "Robt Bosch Tool Corp": {"manufacturer": "Robert Bosch Tool", "mfr_url": "https://www.boschtools.com"},
    "Woodpeckers Inc": {"manufacturer": "Woodpeckers", "mfr_url": "https://www.woodpeck.com"},
    "Rees Cast Stone Company": {"manufacturer": "Rees Cast Stone", "mfr_url": ""},
    "Westwood Lumber Sales": {"manufacturer": "Westwood Lumber", "mfr_url": ""},
    "Whiteside Machine & Repair Co": {"manufacturer": "Whiteside Machine", "mfr_url": "https://www.whitesiderouterbits.com"},
    "Square D Con Prod Dv": {"manufacturer": "Schneider Electric", "mfr_url": "https://www.se.com"},
    "Square D": {"manufacturer": "Schneider Electric", "mfr_url": "https://www.se.com"},
    "CMT USA Inc": {"manufacturer": "CMT USA", "mfr_url": "https://www.cmtusa.com"},
    "Fenton Bros Electric Inc": {"manufacturer": "Fenton Bros Electric", "mfr_url": ""},
    "Velux America Inc": {"manufacturer": "VELUX America", "mfr_url": "https://www.velux.us"},
    "VELUX": {"manufacturer": "VELUX America", "mfr_url": "https://www.velux.us"},
    "JPW Industries": {"manufacturer": "JPW Industries", "mfr_url": "https://www.jettools.com"},
    "TREX": {"manufacturer": "Trex Company", "mfr_url": "https://www.trex.com"},
    "TIMBERTECH": {"manufacturer": "AZEK Company", "mfr_url": "https://www.timbertech.com"},
    "LP SMARTSIDE": {"manufacturer": "Louisiana-Pacific Corporation", "mfr_url": "https://lpcorp.com"},
    "JAMESHARDIE": {"manufacturer": "James Hardie", "mfr_url": "https://www.jameshardie.com"},
    "ANDERSEN": {"manufacturer": "Andersen Windows", "mfr_url": "https://www.andersenwindows.com"},
    "HAGER": {"manufacturer": "Hager Companies", "mfr_url": "https://www.hagerco.com"},
    "PROVIA": {"manufacturer": "Provia Doors & Windows", "mfr_url": "https://www.provia.com"},
    "Feit Electric": {"manufacturer": "Feit Electric", "mfr_url": "https://www.feit.com"},
    "Wiz": {"manufacturer": "Wiz Connected", "mfr_url": "https://www.wizconnected.com"},
    "Dremel": {"manufacturer": "Robert Bosch Tool", "mfr_url": "https://www.dremel.com"},
    "Schumacher": {"manufacturer": "Schumacher Electric", "mfr_url": "https://www.schumacherelectric.com"},
    "Carlon": {"manufacturer": "Thomas & Betts", "mfr_url": "https://www.tnb.com"},
    "Nicholson": {"manufacturer": "Apex Tool Group", "mfr_url": "https://www.apextoolgroup.com"},
    "IRWIN": {"manufacturer": "Apex Tool Group", "mfr_url": "https://www.irwin.com"},
    "Lenox": {"manufacturer": "Stanley Black & Decker", "mfr_url": "https://www.lenox.com"},
    "RIDGID": {"manufacturer": "Emerson Electric", "mfr_url": "https://www.ridgid.com"},
    "Ryobi": {"manufacturer": "Techtronic Industries", "mfr_url": "https://www.ryobitools.com"},
    "Stanley": {"manufacturer": "Stanley Black & Decker", "mfr_url": "https://www.stanleytools.com"},
    "Crescent": {"manufacturer": "Apex Tool Group", "mfr_url": "https://www.crescenttool.com"},
    "Klein Tools": {"manufacturer": "Klein Tools", "mfr_url": "https://www.kleintools.com"},
    "GE": {"manufacturer": "GE Lighting (Savant)", "mfr_url": "https://www.gelighting.com"},
    "Sylvania": {"manufacturer": "Sylvania Lighting", "mfr_url": "https://www.sylvania.com"},
    "OSRAM": {"manufacturer": "OSRAM", "mfr_url": "https://www.osram.com"},
    "Cree": {"manufacturer": "Cree Lighting", "mfr_url": "https://www.creelighting.com"},
    "Utilitech": {"manufacturer": "Lowes Companies", "mfr_url": "https://www.lowes.com"},
    "Halo": {"manufacturer": "Eaton Corporation", "mfr_url": "https://www.eaton.com"},
    "Eaton": {"manufacturer": "Eaton Corporation", "mfr_url": "https://www.eaton.com"},
    "Bosch Tool": {"manufacturer": "Robert Bosch Tool", "mfr_url": "https://www.boschtools.com"},
}

BRAND_ALIASES: Dict[str, str] = {
    "FRIGIDAIRE": "FRIGIDAIRE®",
    "WHIRLPOOL": "Whirlpool",
    "KOHLER": "Kohler",
    "DELTA": "Delta Faucet",
    "AMERICAN STANDARD": "American Standard",
    "GE": "GE Appliances",
    "A O SMITH": "AO Smith",
    "A.O. SMITH": "AO Smith",
    "FISHER PAYKEL": "Fisher & Paykel",
    "CHICAGO FAUCET": "Chicago Faucets",
}


# --- 3. UOM map ---------------------------------------------------------------
# alias (lowercase) -> canonical approved abbreviation. Prefer word-boundary
# matching over substring when resolving (single letters like "v"/"w" are
# substrings of many words).
UOM_MAP: Dict[str, str] = {
    # Length
    "in": "in", "inch": "in", "inches": "in", "in.": "in", "ins": "in", '"': "in",
    "ft": "ft", "foot": "ft", "feet": "ft", "ft.": "ft", "'": "ft",
    "cm": "cm", "centimeter": "cm", "centimeters": "cm",
    "mm": "mm", "millimeter": "mm", "millimeters": "mm",
    "m": "m", "meter": "m", "meters": "m", "m.": "m",
    "sq ft": "sq ft", "sqft": "sq ft", "square foot": "sq ft", "square feet": "sq ft",
    "cu ft": "cu ft", "cubic foot": "cu ft", "cubic feet": "cu ft",
    # Volume
    "gal": "gal", "gallon": "gal", "gallons": "gal", "gals": "gal", "gal.": "gal",
    "qt": "qt", "quart": "qt", "quarts": "qt",
    "pt": "pt", "pint": "pt", "pints": "pt",
    "l": "L", "liter": "L", "liters": "L", "ml": "mL", "milliliter": "mL", "milliliters": "mL",
    # Mass
    "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb", "lb.": "lb", "lbm": "lb",
    "oz": "oz", "ounce": "oz", "ounces": "oz", "oz.": "oz",
    "g": "g", "gram": "g", "grams": "g", "kg": "kg", "kilogram": "kg", "kilograms": "kg",
    # Electrical
    "v": "V", "volt": "V", "volts": "V", "v.": "V",
    "a": "A", "amp": "A", "amps": "A", "ampere": "A", "amperes": "A", "a.": "A",
    "w": "W", "watt": "W", "watts": "W", "w.": "W",
    "kw": "kW", "kilowatt": "kW", "kilowatts": "kW",
    "hz": "Hz", "hertz": "Hz", "khz": "kHz", "mhz": "MHz",
    "kwh": "kW-hr", "kw-hr": "kW-hr", "kilowatt-hour": "kW-hr", "kilowatt-hours": "kW-hr",
    # Flow / pressure / sound
    "gpm": "gpm", "gallons per minute": "gpm", "gph": "gph",
    "cfm": "cfm", "cubic feet per minute": "cfm",
    "psi": "psi", "p.s.i.": "psi", "pounds per square inch": "psi", "bar": "bar", "kpa": "kPa",
    "dba": "dBA", "db": "dB",
    # Temperature / angle
    "deg": "deg", "degree": "deg", "degrees": "deg", "\u00b0": "deg",
    "btu": "BTU", "btu/hr": "BTU/hr", "btuh": "BTU/hr",
    # Packaging
    "ea": "ea", "each": "ea",
    "pk": "pk", "pkg": "pk", "pack": "pk", "package": "pk",
    "pc": "pc", "pcs": "pc", "piece": "pc", "pieces": "pc",
    "ct": "ct", "count": "ct", "dz": "dz", "dozen": "dz", "bx": "bx", "box": "bx",
    "set": "set", "pr": "pr", "pair": "pr",
}


# --- 4. Fraction lookup -------------------------------------------------------
def _build_fraction_tables() -> tuple:
    to_dec, to_frac = {}, {}
    for n in range(1, 64):
        g = math.gcd(n, 64)
        num, den = n // g, 64 // g
        frac = f"{num}/{den}"
        to_dec[frac] = n / 64
        to_frac[n / 64] = frac  # n/64 is exactly representable in binary
    return to_dec, to_frac


FRACTION_TO_DECIMAL, DECIMAL_TO_FRACTION = _build_fraction_tables()


def fraction_lookup(decimal_str: str) -> str:
    """'0.5' -> '1/2', '50.25' -> '50-1/4'. '' if not a neat 1/64 fraction."""
    try:
        x = float(str(decimal_str).strip())
    except (ValueError, TypeError):
        return ""
    nearest = round(x * 64) / 64
    if abs(x - nearest) > 1e-9:
        return ""
    whole = int(nearest)
    frac = nearest - whole
    if frac == 0:
        return str(whole)
    frac_str = DECIMAL_TO_FRACTION[frac]
    return frac_str if whole == 0 else f"{whole}-{frac_str}"


# --- 5. Attribute LOV ---------------------------------------------------------
# Merges the historical faucet/fittings LOVs with values seeded from gold
# (Series, Number of Wash Cycles, Voltage Rating, Amperage Rating, Mounting
# Type, Sound Level, Material) plus faucet/fitting attribute labels.
MOCK_FAUCETS_LOV = {
    "Finish": ["Chrome", "Matte Black", "Vibrant Stainless", "Brushed Nickel", "Oil Rubbed Bronze", "Polished Chrome"],
    "Flow Rate": ["1.2 gpm", "1.5 gpm", "1.8 gpm", "2.2 gpm"],
    "Handle Type": ["Single Handle", "Double Handle", "Sensor-Activated", "Touchless"],
    "Spout Type": ["Pull-down", "Pull-out", "Gooseneck", "High-arc"],
    "Installation Holes": ["1 Hole", "2 Holes", "3 Holes", "4 Holes"]
}

MOCK_FITTINGS_LOV = {
    "Material": ["PVC", "Copper", "Brass", "PEX", "CPVC", "ABS", "Carbon Steel", "Stainless Steel"],
    "Fitting Type": ["Elbow", "Coupling", "Tee", "Adapter", "Union", "Cap", "Bushing", "Plug"],
    "Connection Type": ["FIP", "MIP", "NPT", "Sweat", "Push-to-Connect", "Compression", "Socket", "Threaded"],
    "Schedule": ["Schedule 40", "Schedule 80", "SDR 21"],
    "Size": ["1/2 in", "3/4 in", "1 in", "1-1/4 in", "1-1/2 in", "2 in", "3 in", "4 in"]
}

ATTRIBUTE_LOV: Dict[str, list] = {
    **MOCK_FAUCETS_LOV,
    **MOCK_FITTINGS_LOV,
    # Gold-seeded (dishwasher rows)
    "Series": ["Professional Series", "Eco Series"],
    "Number of Wash Cycles": ["5", "10", "12", "15"],
    "Voltage Rating": ["120 V", "240 V"],
    "Amperage Rating": ["10 A", "15 A"],
    "Mounting Type": ["Leg", "Built-in"],
    "Sound Level": ["39 dBA", "41 dBA", "44 dBA", "47 dBA", "50 dBA"],
    "Color": ["Stainless Steel", "White", "Black", "Bisque"],
    # Expanded materials / finishes
    "Material": ["Stainless Steel", "Brass", "Chrome", "PVC", "Copper", "PEX", "CPVC",
                 "ABS", "Carbon Steel", "Cast Iron", "Chrome-Plated Brass", "Zinc"],
    "Finish": ["Chrome", "Matte Black", "Vibrant Stainless", "Brushed Nickel",
               "Oil Rubbed Bronze", "Polished Chrome", "Polished Nickel",
               "Brushed Bronze", "Stainless Steel"],
    # Faucet / fitting attribute labels
    "Connection Size": ["1/2 in", "3/4 in", "1 in", "1-1/4 in", "1-1/2 in", "2 in", "3 in", "4 in"],
    "Valve Type": ["Ball", "Cartridge", "Ceramic Disc", "Compression", "Pressure Balanced", "Thermostatic"],
    "Body Material": ["Brass", "Zinc", "Stainless Steel", "Plastic", "Copper"],
    "End Connection": ["FIP", "MIP", "NPT", "Sweat", "Push-to-Connect", "Compression", "Socket", "Threaded", "Slip"],
    "Material Construction": ["Stainless Steel", "Brass", "Chrome-Plated Brass", "PVC", "ABS"],
    # Category extractor vocabulary (power-tool accessories / lighting / lumber / electrical)
    "Diameter": [], "Arbor Size": [], "Grit": [], "Quantity": [], "Type": [], "Thickness": [],
    "Shank Type": ["Hex", "Square"], "Number of Teeth": [], "Wattage": [],
    "Luminous Flux": [], "Color Temperature": [], "Base Type": [], "Bulb Shape": [],
    "Wire Gauge": [], "Number of Conductors": [], "Length": [], "Nominal Size": [],
    "Grade": [], "Species": [], "Gauge": [],
}


def get_taxonomy_keywords() -> Dict[str, tuple]:
    return TAXONOMY_KEYWORDS


def get_brand_vocab() -> Dict[str, dict]:
    return BRAND_VOCAB


def get_uom_map() -> Dict[str, str]:
    return UOM_MAP


def get_attribute_lov() -> Dict[str, list]:
    return ATTRIBUTE_LOV


def load_all() -> dict:
    """All five resolution assets in one dict."""
    return {
        "taxonomy_keywords": TAXONOMY_KEYWORDS,
        "brand_vocab": BRAND_VOCAB,
        "uom_map": UOM_MAP,
        "fraction_lookup": fraction_lookup,
        "fractions": {"to_decimal": FRACTION_TO_DECIMAL, "to_fraction": DECIMAL_TO_FRACTION},
        "attribute_lov": ATTRIBUTE_LOV,
    }


# =============================================================================
# Legacy Excel-first loader (kept for stages.py compatibility; Excel files do
# not exist in the demo, so the permanent fallbacks below now source from the
# canonical vocabularies above).
# =============================================================================

# Backward-compat mocks (kept for any external importers)
MOCK_MANUFACTURERS_BRANDS = None  # replaced by derived data below
MOCK_UOMS = None
MOCK_DECIMALS = None
MOCK_GOLD_SET = [
    {
        "mpn": "K-596-VS",
        "raw_manufacturer": "Kohler",
        "raw_text": "Kohler K-596-VS Simplice Kitchen Faucet, Vibrant Stainless, 1.5 gpm, 1/2 in connection",
        "brand": "Simplice",
        "manufacturer": "Kohler Co.",
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Kitchen Faucets",
        "attributes": {
            "Finish": "Vibrant Stainless",
            "Flow Rate": "1.5 gpm",
            "Spout Type": "Pull-down",
            "Size": "1/2 in"
        }
    },
    {
        "mpn": "Leland 9178-DST",
        "raw_manufacturer": "Delta Faucet",
        "raw_text": "Delta Leland Single Handle Pull-Down Kitchen Faucet in Matte Black, 1.8 gpm",
        "brand": "Leland",
        "manufacturer": "Delta Faucet Company",
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Kitchen Faucets",
        "attributes": {
            "Finish": "Matte Black",
            "Flow Rate": "1.8 gpm",
            "Spout Type": "Pull-down",
            "Handle Type": "Single Handle"
        }
    },
    {
        "mpn": "7594SRS",
        "raw_manufacturer": "Moen",
        "raw_text": "Moen Arbor Pulldown Kitchen Faucet, Spot Resist Stainless, 1.5 gpm",
        "brand": "Arbor",
        "manufacturer": "Moen Incorporated",
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Kitchen Faucets",
        "attributes": {
            "Finish": "Vibrant Stainless",
            "Flow Rate": "1.5 gpm",
            "Spout Type": "Pull-down"
        }
    },
    {
        "mpn": "PVC 00300 0600",
        "raw_manufacturer": "Charlotte Pipe",
        "raw_text": "Charlotte Pipe PVC Schedule 40 90 Degree Elbow 1/2 in Socket",
        "brand": "Charlotte Pipe",
        "manufacturer": "Charlotte Pipe and Foundry Company",
        "dept": "Plumbing",
        "class": "Fittings",
        "fine": "Pipe Fittings",
        "attributes": {
            "Material": "PVC",
            "Fitting Type": "Elbow",
            "Schedule": "Schedule 40",
            "Size": "1/2 in",
            "Connection Type": "Socket"
        }
    },
    {
        "mpn": "401-007",
        "raw_manufacturer": "Spears",
        "raw_text": "Spears PVC Schedule 40 Tee Fitting, 3/4 in Slip x Slip x Slip",
        "brand": "Spears",
        "manufacturer": "Spears Manufacturing",
        "dept": "Plumbing",
        "class": "Fittings",
        "fine": "Pipe Fittings",
        "attributes": {
            "Material": "PVC",
            "Fitting Type": "Tee",
            "Schedule": "Schedule 40",
            "Size": "3/4 in",
            "Connection Type": "Socket"
        }
    }
]


def _derive_brand_refs() -> Dict[str, Any]:
    brands, mfrs = {}, {}
    for brand, info in BRAND_VOCAB.items():
        mfr = info["manufacturer"]
        domain = info["mfr_url"].replace("https://", "").replace("http://", "").rstrip("/")
        brands[brand] = {"parent": mfr, "id": f"B_{brand.replace(' ', '_').upper()}"}
        if mfr not in mfrs:
            mfrs[mfr] = {"id": f"M_{mfr.replace(' ', '_').upper()}", "domains": [domain]}
    return {"brands": brands, "manufacturers": mfrs}


class ReferenceLoader:
    def __init__(self):
        self.raw_dir = RAW_DIR
        self._ensure_raw_dir()

    # ponytail: thin delegators — stages.py calls these via _safe(); the
    # canonical vocabularies above are the permanent source (Excel files
    # do not exist in the demo).
    def get_taxonomy_keywords(self) -> Dict[str, tuple]:
        return TAXONOMY_KEYWORDS

    def get_brand_vocab(self) -> Dict[str, dict]:
        return BRAND_VOCAB

    def get_uom_map(self) -> Dict[str, str]:
        return UOM_MAP

    def get_attribute_lov(self) -> Dict[str, list]:
        return ATTRIBUTE_LOV

    def _ensure_raw_dir(self):
        if not os.path.exists(self.raw_dir):
            os.makedirs(self.raw_dir)

    def load_brands_manufacturers(self) -> Dict[str, Any]:
        file_path = os.path.join(self.raw_dir, "UniCat_Manufacturer_and_Brand_List.xlsx")
        if os.path.exists(file_path):
            try:
                # Expect columns: Manufacturer, Brand, Official Domain
                df = pd.read_excel(file_path)
                brands = {}
                mfrs = {}
                for _, row in df.iterrows():
                    mfr = str(row.get("Manufacturer", "")).strip()
                    brand = str(row.get("Brand", "")).strip()
                    domain = str(row.get("Official Domain", "")).strip()
                    if mfr:
                        mfrs[mfr] = {"id": f"M_{mfr.replace(' ', '_').upper()}", "domains": [domain] if domain else []}
                        if brand:
                            brands[brand] = {"parent": mfr, "id": f"B_{brand.replace(' ', '_').upper()}"}
                return {"brands": brands, "manufacturers": mfrs}
            except Exception as e:
                print(f"Error loading brands/mfrs file: {e}. Falling back to vocab data.")
        return _derive_brand_refs()

    def load_faucets_lov(self) -> Dict[str, List[str]]:
        file_path = os.path.join(self.raw_dir, "FAUCETS_LOV.xlsx")
        if os.path.exists(file_path):
            try:
                # Load LOV sheets or columns
                xls = pd.ExcelFile(file_path)
                lovs = {}
                for sheet in xls.sheet_names:
                    df = pd.read_excel(xls, sheet)
                    # Use the first column values
                    lovs[sheet] = df.iloc[:, 0].dropna().astype(str).tolist()
                return lovs
            except Exception as e:
                print(f"Error loading faucets LOV file: {e}. Falling back to vocab data.")
        return {k: ATTRIBUTE_LOV[k] for k in ["Finish", "Flow Rate", "Handle Type", "Spout Type", "Installation Holes"] if k in ATTRIBUTE_LOV}

    def load_fittings_lov(self) -> Dict[str, List[str]]:
        file_path = os.path.join(self.raw_dir, "Fittings_LOV.xlsx")
        if os.path.exists(file_path):
            try:
                xls = pd.ExcelFile(file_path)
                lovs = {}
                for sheet in xls.sheet_names:
                    df = pd.read_excel(xls, sheet)
                    lovs[sheet] = df.iloc[:, 0].dropna().astype(str).tolist()
                return lovs
            except Exception as e:
                print(f"Error loading fittings LOV file: {e}. Falling back to vocab data.")
        return {k: ATTRIBUTE_LOV[k] for k in ["Material", "Fitting Type", "Connection Type", "Schedule", "Size"] if k in ATTRIBUTE_LOV}

    def load_uom_standards(self) -> Dict[str, str]:
        file_path = os.path.join(self.raw_dir, "Unilog_Master_UOM_Standards_Abbreviations_and_Terms.xlsx")
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                # Expect columns: Abbreviation, Standard
                uoms = {}
                for _, row in df.iterrows():
                    abbr = str(row.iloc[0]).strip().lower()
                    std = str(row.iloc[1]).strip()
                    if abbr:
                        uoms[abbr] = std
                return uoms
            except Exception as e:
                print(f"Error loading UOM standards file: {e}. Falling back to vocab data.")
        return dict(UOM_MAP)

    def load_decimal_fractions(self) -> Dict[str, float]:
        file_path = os.path.join(self.raw_dir, "Decimal_Fraction.xlsx")
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                # Expect columns: Fraction, Decimal
                decimals = {}
                for _, row in df.iterrows():
                    frac = str(row.iloc[0]).strip()
                    dec = float(row.iloc[1])
                    if frac:
                        decimals[frac] = dec
                return decimals
            except Exception as e:
                print(f"Error loading decimal fractions file: {e}. Falling back to vocab data.")
        return dict(FRACTION_TO_DECIMAL)

    def load_gold_set(self) -> List[Dict[str, Any]]:
        # Preferred: the actual UniHack gold workbook (2 rows x 252 cols).
        csv_path = os.path.join(self.raw_dir, "Unihack_ Expected Output - Delivery Format.csv")
        if not os.path.exists(csv_path):
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(root, "Unihack_ Expected Output - Delivery Format.csv")
        file_path = os.path.join(self.raw_dir, "Unilog-Sample_200_Items-Input-vs-Output.xlsx")
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path, encoding="utf-8-sig")
                gold_set = []
                for _, row in df.iterrows():
                    mpn = str(row.get("Mfg_Part_Num", "")).strip()
                    populated = {}
                    for col in df.columns:
                        v = row.get(col)
                        if pd.isna(v):
                            continue
                        s = str(v).strip()
                        if s == "" or s == "nan":
                            continue
                        if col in ("PART_NUMBER", "SKU - MY_PART_NUMBER",
                                   "Mfg_Part_Num", "Part_Desc", "E1_Brand",
                                   "Unilog_Brand", "DIB_Brand", "Part_Manuf"):
                            continue
                        populated[col] = s
                    gold_set.append({
                        "mpn": mpn,
                        "brand": str(row.get("BRAND_NAME", "")).strip(),
                        "manufacturer": str(row.get("MANUFACTURER_NAME", "")).strip(),
                        "dept": str(row.get("Dept", "")).strip(),
                        "class": str(row.get("Class", "")).strip(),
                        "fine": str(row.get("Fine", "")).strip(),
                        "attributes": {},
                        "populated": populated,
                    })
                if gold_set:
                    return gold_set
            except Exception as e:
                print(f"Error loading Gold Set CSV: {e}. Falling back.")
        if os.path.exists(file_path):
            try:
                # Load ground truth inputs vs outputs
                df = pd.read_excel(file_path)
                gold_set = []
                for _, row in df.iterrows():
                    gold_set.append({
                        "mpn": str(row.get("MPN", "")).strip(),
                        "raw_manufacturer": str(row.get("Manufacturer", "")).strip(),
                        "raw_text": str(row.get("Description", "")).strip(),
                        "brand": str(row.get("Expected Brand", "")).strip(),
                        "manufacturer": str(row.get("Expected Manufacturer", "")).strip(),
                        "dept": str(row.get("Expected Dept", "")).strip(),
                        "class": str(row.get("Expected Class", "")).strip(),
                        "fine": str(row.get("Expected Fine", "")).strip(),
                        "attributes": {} # Load expected attribute key-value pairs if available
                    })
                return gold_set
            except Exception as e:
                print(f"Error loading Gold Set file: {e}. Falling back to mock gold set.")
        return MOCK_GOLD_SET


if __name__ == "__main__":
    print("Taxonomy 'dishwasher':", get_taxonomy_keywords()["dishwasher"])
    print("Taxonomy match 'PDSH4816AF Dishwasher SS - Display Only':", match_taxonomy("PDSH4816AF Dishwasher SS - Display Only"))
    print("Brand 'FRIGIDAIRE®':", get_brand_vocab()["FRIGIDAIRE®"])
    print("Brand alias 'FRIGIDAIRE' ->", get_brand_vocab()["Frigidaire"]["alias_of"])
    print("UOM 'IN.':", get_uom_map()["in."])
    print("Fraction 50.25:", fraction_lookup("50.25"))
    print("Attribute LOV 'Series':", get_attribute_lov()["Series"])
    loader = ReferenceLoader()
    print("Fallback brands loaded count:", len(loader.load_brands_manufacturers()["brands"]))
    print("Fallback faucets LOVs loaded keys:", list(loader.load_faucets_lov().keys()))
    print("Fallback UOMs count:", len(loader.load_uom_standards()))