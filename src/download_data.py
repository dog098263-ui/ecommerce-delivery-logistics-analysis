"""
Automated Data Download Script
Project 1: E-commerce Delivery & Logistics Performance Analysis
Downloads and extracts the raw Olist dataset into data/raw/
"""

import os
import sys
import zipfile
import urllib.request
import ssl

RELEASE_URL = "https://github.com/dog098263-ui/ecommerce-delivery-logistics-analysis/releases/download/v1.0.0-data/olist_dataset.zip"


def download_and_extract(project_root: str):
    raw_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    zip_path = os.path.join(raw_dir, "olist_dataset.zip")

    # Check if raw files already exist
    orders_csv = os.path.join(raw_dir, "olist_orders_dataset.csv")
    if os.path.exists(orders_csv):
        print(f"✓ Raw dataset already present in: {raw_dir}")
        return

    print(f"Downloading Olist raw dataset from GitHub Releases (~42 MB)...")
    print(f"URL: {RELEASE_URL}")

    ctx = ssl.create_default_context()
    # Handle local certificate verification fallbacks if needed
    if os.path.exists("/etc/ssl/cert.pem"):
        ctx.load_verify_locations("/etc/ssl/cert.pem")

    def progress_bar(blocks_transferred, block_size, total_size):
        transferred = blocks_transferred * block_size
        pct = (transferred / total_size) * 100 if total_size > 0 else 0
        sys.stdout.write(f"\r  Downloading: {pct:5.1f}% [{transferred / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB]")
        sys.stdout.flush()

    try:
        urllib.request.urlretrieve(RELEASE_URL, zip_path, reporthook=progress_bar)
        print("\n✓ Download completed.")
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print("\nManual Alternative:")
        print("1. Download olist_dataset.zip manually from:")
        print("   https://github.com/dog098263-ui/ecommerce-delivery-logistics-analysis/releases/tag/v1.0.0-data")
        print(f"2. Extract the CSV files directly into: {raw_dir}")
        return

    print("Extracting CSV files into data/raw/...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(raw_dir)
    os.remove(zip_path)
    print("✓ Dataset extracted successfully! You can now run: python3 src/ingest_and_clean.py")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))
    download_and_extract(project_root)
