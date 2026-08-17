#!/usr/bin/env python3
"""
Patches design.html: replaces both localhost:5051 image-generation calls
with the working production endpoint (afrivid-tts worker), which
create.html already uses successfully.

Only the fetch URL changes in each case — request body, headers, and
response handling (.blob()) are left untouched since they already match.

Makes a design.html.bak backup before touching anything.

Run from inside your afrivid project folder (~/projects/afrivid):
    python3 patch_design.py
"""

import shutil
import sys

FILE = "design.html"
OLD_URL = "http://localhost:5051/generate-image"
NEW_URL = "https://afrivid-tts.afrividstudio.workers.dev/generate-image"

def main():
    with open(FILE, "r", encoding="utf-8") as f:
        content = f.read()

    count = content.count(OLD_URL)
    if count == 0:
        print(f"ERROR: Could not find '{OLD_URL}' in {FILE}. No changes made.")
        print("The file may have changed since we last inspected it.")
        sys.exit(1)
    if count != 2:
        print(f"WARNING: Expected exactly 2 occurrences, found {count}.")
        confirm = input("Continue and replace all of them anyway? (y/n): ")
        if confirm.strip().lower() != "y":
            print("Aborted. No changes made.")
            sys.exit(1)

    shutil.copy(FILE, FILE + ".bak")
    print(f"Backup written to {FILE}.bak")

    new_content = content.replace(OLD_URL, NEW_URL)
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"{FILE} patched successfully. Replaced {count} occurrence(s).")
    print("Next: run 'diff design.html.bak design.html' to review, then deploy/publish as usual.")

if __name__ == "__main__":
    main()
