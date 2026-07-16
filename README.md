# CleanOldfiles

A lightweight, configurable Python tool that automatically **moves** old files into a backup directory based on their **creation date** and **last access date**.  
The file types are fully customizable (e.g. `.ppt`, `.docx`, `.xlsx`, `.pdf`, `.log`, …) – you decide what to clean.  
A companion script lets you safely purge the backup folder with one click.  
Already packaged as a **standalone `.exe`** – no Python required.

---

## ✨ Features

- 🧹 **Automatic cleanup** – Move old files to a `bak` folder using flexible time thresholds (creation days, access days).
- 🗃️ **Any file type** – Define your own file patterns in `config.ini` (wildcards like `*.pdf`, `*.tmp`, `*.log` – as many as you want).
- 🔒 **Safe backup** – Files are *moved*, not deleted. You can always recover them from the backup directory.
- 🎛️ **Fully configurable** – All settings live in a clean `config.ini` file (scan directory, file patterns, days, recursion).
- 🌍 **Environment variable support** – Use `%USERPROFILE%`, `%USERNAME%` etc. in your scan path.
- 🪟 **Cross-drive safety** – When moving files between different drives, the tool copies, verifies file size, then deletes the source – zero data loss risk.
- 📢 **Desktop notifications** – Pop‑up window shows exactly which files were moved and which failed (with reasons).
- 🔎 **Recursive scanning** – Optionally scan sub‑folders.
- 📁 **Excludes backup folder** – Won’t accidentally re‑process files already inside `bak`, even on case‑insensitive Windows.
- 🧪 **Standalone `.exe`** – Ready to distribute. Just download `CleanOldfiles.exe` and run it.
- 🗑️ **One‑click backup remover** – Separate script (`clean_bak.py`) deletes the whole `bak` folder after a confirmation pop‑up. Also packable as `.exe`.

---

## 📦 Quick Start

### 1. Using the pre‑built executable (Windows)
1. Download the latest `CleanOldfiles.exe` from [Releases](https://github.com/TUSI-ISUT/CleanOldfiles/releases).
2. Place the `config.ini` file next to it and edit to your needs (see [Configuration](./confing/confing.ini)).
3. Double‑click the `.exe` – it runs silently and shows a summary pop‑up.

### 2. Running from source (Python 3.7+)
```bash
git clone https://github.com/TUSI-ISUT/CleanOldfiles.git
cd CleanOldfiles
python main.py
