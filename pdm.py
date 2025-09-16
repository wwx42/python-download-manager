#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple Python Downloader with Progress Bar
Author: Mahdi Mohammadkhani
GitHub-ready version
"""

# ---------------- modules ----------------
import requests
from tqdm import tqdm
import os
import sys

# ---------------- configuration ----------------
# Folder where downloads will be saved
DOWNLOAD_FOLDER = input("Enter download directory: ")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ---------------- helper functions ----------------
def clear_terminal():
    """Clear terminal screen on Windows or Linux/macOS."""
    os.system("cls" if sys.platform == "win32" else "clear")


def get_filename_from_url(url: str) -> str:
    """Extract a clean filename from a URL (remove query parameters)."""
    return url.split("/")[-1].split("?")[0]


# ---------------- main program ----------------
def main():
    links = []

    # Step 1: Collect download links from user
    while True:
        file_input = input("Enter download link (type 'start' to begin download): ").strip()
        if file_input.lower() == "start":
            clear_terminal()
            break
        elif file_input:
            links.append(file_input)

    if not links:
        print("No links provided. Exiting.")
        return

    # Step 2: Download each file
    for link in links:
        filename = get_filename_from_url(link)
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        print(f"⬇️  {filename} is downloading...")

        try:
            # Send HTTP GET request with streaming
            with requests.get(link, stream=True, timeout=(5, 60)) as response:
                response.raise_for_status()  # Raise error for bad HTTP status

                total_size = int(response.headers.get('content-length', 0))
                print(f"📦 Download size: {total_size / 10**6:.2f} MB")

                chunk_size = 1024 * 8  # 8KB chunks
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as progress_bar:
                    with open(filepath, "wb") as f:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                progress_bar.update(len(chunk))

            print(f"✅ {filename} download completed.\n")
            clear_terminal()

        except requests.exceptions.RequestException as e:
            print(f"❌ Error downloading {filename}: {e}")

    print("Sincerely,\nMade by Mahdi Mohammadkhani :)")

# ---------------- run ----------------
if __name__ == "__main__":
    main()