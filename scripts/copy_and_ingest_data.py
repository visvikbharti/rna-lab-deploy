#!/usr/bin/env python
"""
Script to copy sample data from original repo to deployment repo and ingest it.
"""

import os
import sys
import shutil
import argparse
import pathlib
from datetime import datetime

# Get script directory and project directories
script_dir = pathlib.Path(__file__).resolve().parent
deploy_dir = script_dir.parent
original_dir = pathlib.Path('/Users/vishalbharti/Downloads/rna-lab-navigator')

def copy_sample_data():
    """Copy sample data from original repo to deployment repo."""
    # Create directories if they don't exist
    deploy_data_dir = deploy_dir / "data"
    deploy_sample_dir = deploy_data_dir / "sample_docs"
    
    os.makedirs(deploy_data_dir, exist_ok=True)
    os.makedirs(deploy_sample_dir, exist_ok=True)
    
    # Copy each category of documents
    for category in ["theses", "papers", "community_protocols", "troubleshooting"]:
        src_dir = original_dir / "data" / "sample_docs" / category
        dst_dir = deploy_sample_dir / category
        
        if not src_dir.exists():
            print(f"Source directory {src_dir} does not exist, skipping.")
            continue
        
        os.makedirs(dst_dir, exist_ok=True)
        
        # Copy files
        for file_path in src_dir.glob("*"):
            if file_path.is_file():
                print(f"Copying {file_path.name} to {dst_dir}")
                shutil.copy2(file_path, dst_dir)
    
    print("Sample data copied successfully.")

def copy_ingest_script():
    """Copy ingestion script from original repo to deployment repo."""
    src_script = original_dir / "scripts" / "ingest_sample_docs.py"
    dst_scripts_dir = deploy_dir / "scripts"
    dst_script = dst_scripts_dir / "ingest_sample_docs.py"
    
    if not src_script.exists():
        print(f"Source script {src_script} does not exist.")
        return False
    
    os.makedirs(dst_scripts_dir, exist_ok=True)
    
    # Copy script
    print(f"Copying {src_script} to {dst_script}")
    shutil.copy2(src_script, dst_script)
    
    # Adjust paths in script if needed (could be more sophisticated)
    with open(dst_script, 'r') as f:
        content = f.read()
    
    # Ensure script can find the backend directory
    adjusted_content = content.replace(
        "sys.path.append(str(project_dir))",
        "sys.path.append(str(project_dir))\nsys.path.append(str(project_dir / 'backend'))"
    )
    
    with open(dst_script, 'w') as f:
        f.write(adjusted_content)
    
    print("Ingestion script copied and adjusted successfully.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Copy and prepare sample data for deployment")
    parser.add_argument("--copy-only", action="store_true", help="Only copy files, don't ingest")
    args = parser.parse_args()
    
    # Copy sample data
    copy_sample_data()
    
    # Copy ingestion script
    if copy_ingest_script() and not args.copy_only:
        # Run ingestion script
        print("Running ingestion script...")
        os.chdir(deploy_dir)
        os.system(f"python scripts/ingest_sample_docs.py --purge")
    
    print("Done!")

if __name__ == "__main__":
    main()