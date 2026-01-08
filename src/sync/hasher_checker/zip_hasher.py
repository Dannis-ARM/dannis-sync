from contextlib import redirect_stdout
from io import StringIO
import argparse
import hashlib
import json
import time
from pathlib import Path

def get_zip_files(folder_path):
    """Find all .zip files in a folder, ignoring access errors."""
    try:
        # Correctly search for .zip files as intended
        return list(Path(folder_path).rglob("*"))
    except OSError as e:
        print(f"⚠️ Error scanning directory {folder_path}: {e}")
        return []

def calculate_hash(file_path):
    """Calculate the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except OSError as e:
        print(f"⚠️ Could not read file {file_path} for hashing: {e}")
        return None

def load_hashes(hash_file_path):
    """Loads hashes from a JSON file."""
    if not hash_file_path.exists():
        return {}
    try:
        with open(hash_file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Warning: Could not decode {hash_file_path}. A new one will be created.")
        return {}
    except OSError as e:
        print(f"⚠️ Could not read hash file {hash_file_path}: {e}")
        return {}


def save_hashes(hash_file_path, hashes):
    """Saves hashes to a JSON file."""
    try:
        with open(hash_file_path, "w") as f:
            json.dump(hashes, f, indent=4)
    except OSError as e:
        print(f"⚠️ Could not write to hash file {hash_file_path}: {e}")

def process_file(file_path, hashes):
    """
    Processes a single file to check its hash.
    Returns a status ('unchanged', 'changed', 'new', 'error') and the current hash.
    """
    file_path_str = str(file_path)
    current_hash = calculate_hash(file_path)

    if current_hash is None:
        return 'error', None

    if file_path_str in hashes:
        if hashes[file_path_str] == current_hash:
            return 'unchanged', current_hash
        else:
            return 'changed', current_hash
    else:
        return 'new', current_hash

def print_summary(results):
    """Prints a summary of the hash check results."""
    total_files = sum(len(v) for v in results.values())
    
    print("\n" + "="*50)
    print("📊 Hashing Complete")
    print("="*50)
    print(f"Total files checked: {total_files}")
    print(f"✅ Unchanged: {len(results['unchanged'])}")
    print(f"✨ New files: {len(results['new'])}")
    print(f"⚠️ Modified files: {len(results['modified'])}")
    if results['errors']:
        print(f"❌ Errors: {len(results['errors'])}")
    
    if results['modified']:
        print("\n📄 Files with changed hashes:")
        for file_path in results['modified']:
            print(f"  - {file_path}")

    if results['new']:
        print("\n📄 New files found:")
        for file_path in results['new']:
            print(f"  - {file_path}")
    
    print("="*50)


def check_hashes(folder_path):
    """
    Checks for file changes in a directory based on their hashes.

    Args:
        folder_path (str or Path): The path to the folder to check.

    Returns:
        list: A list of file paths that have been modified.
    """
    print(f"🔍 Starting hash check for *.zip files in '{folder_path}'...")
    
    files_to_check = get_zip_files(folder_path)
    if not files_to_check:
        print("No *.zip files found to check.")
        return []

    hash_file = Path.cwd() / "hashes.json"
    lock_file = Path.cwd() / "hashes.lock"

    # Wait for lock file to be released, with a 30-second timeout
    if lock_file.exists():
        print(f"⏳ Lock file {lock_file} exists, waiting...")
        while True:
            try:
                if not lock_file.exists():
                    print("\n✅ Lock file released.")
                    break
                
                lock_age = time.time() - lock_file.stat().st_mtime
                if lock_age > 30:
                    print(f"\n⚠️ Lock file is {lock_age:.0f}s old. Ignoring and proceeding.")
                    break
                
                print(f"⏳ Waiting... (lock is {lock_age:.0f}s old)", end='\r')
                time.sleep(1)
            except FileNotFoundError:
                # Race condition: file was deleted between exists() and stat()
                print("\n✅ Lock file was released.")
                break

    try:
        lock_file.touch()

        hashes = load_hashes(hash_file)
        
        results = {'unchanged': [], 'modified': [], 'new': [], 'errors': []}
        total_files = len(files_to_check)

        for i, file_path in enumerate(files_to_check):
            progress = f"[{i + 1}/{total_files}]"
            # Use carriage return to show progress on a single line
            print(f"{progress} ⏳ Hashing {file_path.name}...", end='\r')

            status, current_hash = process_file(file_path, hashes)
            
            file_path_str = str(file_path)
            
            # Overwrite the "Hashing..." line with the result
            clear_line = ' ' * 60
            print(f"{progress} {' '*len(file_path.name)} {clear_line}", end='\r')


            if status == 'unchanged':
                print(f"{progress} ✅ Unchanged: {file_path.name}")
                results['unchanged'].append(file_path_str)
            elif status == 'changed':
                print(f"{progress} ⚠️  Changed:   {file_path_str}")
                results['modified'].append(file_path_str)
                hashes[file_path_str] = current_hash
            elif status == 'new':
                print(f"{progress} ✨ New file:  {file_path_str}")
                results['new'].append(file_path_str)
                hashes[file_path_str] = current_hash
            elif status == 'error':
                results['errors'].append(file_path_str)

        save_hashes(hash_file, hashes)
        print_summary(results)
        
        return results['modified'] + results['new']

    finally:
        if lock_file.exists():
            lock_file.unlink()

def main():
    """CLI entry point for the script."""
    parser = argparse.ArgumentParser(description="Check for changes in zip files in a folder and compare hashes.")
    parser.add_argument("folder_path", type=str, help="The path to the folder to check.")
    parser.add_argument("--output-format", type=str, choices=['human', 'bash'], default='human',
                        help="Output format: 'human' for readable logs, 'bash' for machine-readable list of files.")
    args = parser.parse_args()
    
    if args.output_format == 'bash':
        # Temporarily redirect stdout to suppress verbose output
        f = StringIO()
        with redirect_stdout(f):
            changed_files = check_hashes(args.folder_path)
        # Print only the changed files for bash consumption
        for file_path in changed_files:
            print(file_path)
    else: # default 'human'
        modified_files = check_hashes(args.folder_path)
        if modified_files:
            print("\nScript finished. Modified files were found.")
        else:
            print("\nScript finished. No modified files detected.")

if __name__ == "__main__":
    main()