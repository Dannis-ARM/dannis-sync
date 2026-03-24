#!/usr/bin/env python3
"""
Copy AGENTS.md to Documents\Cline\Rules directory.
"""

import os
import shutil
from pathlib import Path

def main():
    # Define source and destination paths
    source_file = Path(__file__).parent / "src" / "agents" / "AGENTS.md"
    dest_dir = Path(os.path.expanduser("~")) / "Documents" / "Cline" / "Rules"
    dest_file = dest_dir / "AGENTS.md"
    
    # Check if source file exists
    if not source_file.exists():
        print(f"Error: Source file not found: {source_file}")
        return False
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the file
    shutil.copy2(source_file, dest_file)
    print(f"Successfully copied {source_file} to {dest_file}")
    return True

if __name__ == "__main__":
    main()
