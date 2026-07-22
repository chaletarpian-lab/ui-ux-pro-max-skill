#!/usr/bin/env python3
"""Rend les 11 slides du carrousel Arpian et assemble le PDF LinkedIn.

Usage :
    pip install playwright pillow
    python3 build.py [--chromium /chemin/vers/chrome]

Par defaut le script utilise le Chromium installe par Playwright
(`playwright install chromium`) ; sur Claude Code web, passer
--chromium /opt/pw-browsers/chromium-1194/chrome-linux/chrome.
"""
import argparse
import pathlib

from PIL import Image
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent.resolve()
SLIDE_IDS = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s7b", "s8", "s9", "s10"]

parser = argparse.ArgumentParser()
parser.add_argument("--chromium", default=None, help="chemin de l'executable Chromium")
args = parser.parse_args()

with sync_playwright() as p:
    launch = {"args": ["--no-sandbox", "--allow-file-access-from-files"]}
    if args.chromium:
        launch["executable_path"] = args.chromium
    browser = p.chromium.launch(**launch)
    page = browser.new_page(viewport={"width": 1080, "height": 1350})
    page.goto((HERE / "slides.html").as_uri())
    page.wait_for_timeout(2500)
    for i, sid in enumerate(SLIDE_IDS, 1):
        page.locator(f"#{sid}").screenshot(path=str(HERE / f"slide_{i:02d}.png"))
        print(f"slide_{i:02d}.png")
    browser.close()

images = [Image.open(HERE / f"slide_{i:02d}.png").convert("RGB") for i in range(1, 12)]
images[0].save(HERE / "CarrouselLinkedInArpian.pdf", save_all=True, append_images=images[1:], resolution=96)
print("CarrouselLinkedInArpian.pdf OK")
