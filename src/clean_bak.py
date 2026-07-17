import shutil
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def get_bak_dir():
    """Return the path of the 'bak' folder next to this script."""
    return Path(__file__).resolve().parent / 'bak'

def clean_bak():
    bak_dir = get_bak_dir()

    # 1. If the directory doesn't exist, nothing to do
    if not bak_dir.exists():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Cleanup Complete", "Backup directory does not exist. Nothing to clean.")
        root.destroy()
        return

    # 2. Confirmation dialog
    root = tk.Tk()
    root.withdraw()
    confirm = messagebox.askyesno(
        "Confirm Cleanup",
        f"Are you sure you want to permanently delete the entire backup directory?\n\n{bak_dir}\n\nThis action cannot be undone."
    )
    root.destroy()

    if not confirm:
        return

    # 3. Delete the directory tree
    try:
        shutil.rmtree(bak_dir)
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Cleanup Complete", "Backup directory has been successfully deleted.")
        root.destroy()
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Cleanup Failed", f"Failed to delete backup directory:\n{e}")
        root.destroy()

if __name__ == '__main__':
    clean_bak()
