"""
Render PPTX slides to PNG images using PowerPoint COM / win32com for Visual QA.
"""

import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECK_PATH = ROOT / "UniHack_ELIO_Prototype_Submission.pptx"
SLIDES_DIR = ROOT / "artifacts" / "slide_images"
SLIDES_DIR.mkdir(parents=True, exist_ok=True)

def export_slides():
    import win32com.client
    
    abs_deck = str(DECK_PATH.resolve())
    abs_out = str(SLIDES_DIR.resolve())
    
    print(f"Opening presentation: {abs_deck}")
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    # Open presentation in read-only / minimized mode
    prs = powerpoint.Presentations.Open(abs_deck, WithWindow=False)
    
    try:
        print(f"Exporting {prs.Slides.Count} slides to: {abs_out}")
        prs.Export(abs_out, "PNG", 1920, 1080)
        print("Export completed successfully!")
    finally:
        prs.Close()
        powerpoint.Quit()

if __name__ == '__main__':
    try:
        export_slides()
    except Exception as e:
        print(f"Error exporting slides: {e}")
        sys.exit(1)
