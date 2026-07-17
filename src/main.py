import os
import shutil
import time
import configparser
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime

# ---------- Configuration Loader ----------
def load_config(config_file='config.ini'):
    """Read and parse the configuration file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found. Please create it first.")

    # Disable interpolation so that '%' in paths (e.g. %USERPROFILE%) won't cause errors
    config = configparser.ConfigParser(interpolation=None)
    config.read(config_file, encoding='utf-8')

    directory = config.get('scan', 'directory')
    patterns_str = config.get('scan', 'patterns', fallback='*.ppt, *.pptx')
    patterns = [p.strip() for p in patterns_str.split(',') if p.strip()]
    recursive = config.getboolean('scan', 'recursive', fallback=False)
    creation_days = config.getfloat('time', 'creation_days', fallback=0)
    access_days = config.getfloat('time', 'access_days', fallback=0)

    return {
        'directory': directory,
        'patterns': patterns,
        'recursive': recursive,
        'creation_days': creation_days,
        'access_days': access_days
    }

# ---------- File Time Utilities ----------
def get_file_times(file_path):
    """Return (creation_time, last_access_time) as Unix timestamps."""
    stat = file_path.stat()
    return stat.st_ctime, stat.st_atime

# ---------- Backup Directory Helpers ----------
def ensure_backup_dir(backup_root):
    """Create backup directory if it doesn't exist."""
    backup_root.mkdir(parents=True, exist_ok=True)

def generate_backup_name(file_path, backup_root):
    """Generate a unique name inside backup directory to avoid overwrites."""
    base_name = file_path.name
    stem = file_path.stem
    suffix = file_path.suffix
    dest = backup_root / base_name
    counter = 1
    while dest.exists():
        dest = backup_root / f"{stem}_{counter}{suffix}"
        counter += 1
    return dest

# ---------- Case-insensitive Path Check ----------
def is_in_backup_dir(file_path, backup_root):
    """
    Return True if file_path is located inside backup_root.
    Uses case-insensitive comparison for Windows compatibility.
    """
    return os.path.normcase(str(file_path.resolve())).startswith(
        os.path.normcase(str(backup_root.resolve()))
    )

# ---------- Safe File Move ----------
def safe_move(src, dst):
    """
    Move a file safely:
      - Try os.rename first (fast, same drive).
      - If that fails (cross-drive), copy the file, verify size, then delete source.
    Returns (success: bool, error_message: str)
    """
    try:
        os.rename(str(src), str(dst))
        return True, ""
    except OSError:
        # Cross-drive or permission issue – copy then verify
        try:
            shutil.copy2(src, dst)
            if Path(src).stat().st_size == Path(dst).stat().st_size:
                os.remove(src)
                return True, ""
            else:
                # Size mismatch – delete incomplete destination and keep source
                os.remove(dst)
                return False, "File size mismatch after copy – source preserved."
        except Exception as e:
            return False, str(e)

# ---------- Popup Summary ----------
def show_popup(moved_files, failed_files):
    """Display a popup window summarising moved and failed files."""
    root = tk.Tk()
    root.withdraw()

    if not moved_files and not failed_files:
        messagebox.showinfo("Operation Complete", "No files needed to be moved.")
    else:
        lines = []
        if moved_files:
            lines.append(f"Successfully moved {len(moved_files)} file(s):")
            max_show = 20
            for i, (src_name, _) in enumerate(moved_files):
                if i < max_show:
                    lines.append(f"  ✓ {src_name}")
                else:
                    lines.append(f"  ... and {len(moved_files) - max_show} more")
                    break
        if failed_files:
            if lines:
                lines.append("")  # empty line separator
            lines.append(f"Failed to move {len(failed_files)} file(s):")
            max_show = 15
            for i, (name, reason) in enumerate(failed_files):
                if i < max_show:
                    lines.append(f"  ✗ {name} ({reason})")
                else:
                    lines.append(f"  ... and {len(failed_files) - max_show} more")
                    break
        messagebox.showinfo("Operation Complete", "\n".join(lines))
    root.destroy()

# ---------- Main Logic ----------
def main():
    cfg = load_config()

    # Expand environment variables in the target directory (e.g. %USERPROFILE%)
    raw_dir = cfg['directory']
    expanded_dir = os.path.expandvars(raw_dir)
    target_dir = Path(expanded_dir)
    if not target_dir.is_dir():
        raise NotADirectoryError(f"Target directory does not exist or is not accessible: {target_dir}")

    patterns = cfg['patterns']
    recursive = cfg['recursive']
    creation_days = cfg['creation_days']
    access_days = cfg['access_days']

    now = time.time()
    # If a day threshold is 0, that filter is disabled (no cutoff)
    creation_cutoff = now - creation_days * 86400 if creation_days > 0 else None
    access_cutoff   = now - access_days * 86400   if access_days > 0   else None

    script_dir = Path(__file__).resolve().parent
    backup_root = script_dir / 'bak'
    ensure_backup_dir(backup_root)

    print(f"Scan directory: {target_dir}")
    print(f"Backup directory: {backup_root}")
    print(f"Creation time threshold: {'unlimited' if creation_days==0 else f'{creation_days} days ago'}")
    print(f"Access time threshold: {'unlimited' if access_days==0 else f'{access_days} days ago'}")
    print("-" * 50)

    moved_files = []   # list of (original_filename, destination_path)
    failed_files = []  # list of (original_filename, error_message)

    for pattern in patterns:
        files = target_dir.rglob(pattern) if recursive else target_dir.glob(pattern)
        for file in files:
            if not file.is_file():
                continue

            # Exclude files that are inside the backup directory itself
            if recursive and is_in_backup_dir(file, backup_root):
                continue

            try:
                ctime, atime = get_file_times(file)
            except OSError as e:
                print(f"[Skipped] Unable to read file times: {file} - {e}")
                continue

            # Time filter: condition ignored if days == 0
            creation_ok = (creation_days == 0) or (ctime < creation_cutoff)
            access_ok   = (access_days == 0)   or (atime < access_cutoff)

            if creation_ok and access_ok:
                dest = generate_backup_name(file, backup_root)
                success, reason = safe_move(file, dest)
                if success:
                    print(f"[Moved] {file.name} -> {dest}")
                    moved_files.append((file.name, dest))
                else:
                    print(f"[Move Failed] {file.name}: {reason}")
                    failed_files.append((file.name, reason))

    print("-" * 50)
    print(f"Operation finished. Successfully moved {len(moved_files)} file(s), failed {len(failed_files)} file(s).")
    show_popup(moved_files, failed_files)

if __name__ == '__main__':
    main()