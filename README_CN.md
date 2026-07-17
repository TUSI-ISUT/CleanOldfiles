# CleanOldfiles

[简体中文](./README_CN.md)  [English](./README.md)

一个轻量、可配置的 Python 工具，能根据**创建日期**和**最后访问日期**自动将**任意类型的旧文件**移动到备份目录。  
文件类型完全由你决定（例如 `.ppt`、`.docx`、`.xlsx`、`.pdf`、`.log`……），在 `config.ini` 中随意设置即可。  
另有配套脚本，可一键安全清空备份文件夹。  
**已打包为独立 `.exe`**，无需安装 Python 环境，下载即用。

---

## ✨ 功能特性

- 🧹 **自动清理** – 根据灵活的时间阈值（创建天数、访问天数）将旧文件移至 `bak` 文件夹。
- 🗃️ **支持所有文件类型** – 在 `config.ini` 中自定义文件匹配模式（支持通配符，如 `*.pdf`、`*.tmp`、`*.log`，可同时指定多种）。
- 🔒 **安全备份** – 文件是**移动**而非删除，随时可从备份目录恢复。
- 🎛️ **完全可配置** – 所有设置集中在 `config.ini`（扫描目录、文件模式、天数、是否递归）。
- 🌍 **支持环境变量** – 路径中可使用 `%USERPROFILE%`、`%USERNAME%` 等。
- 🪟 **跨盘安全移动** – 跨盘符移动时，先复制并校验大小，再删除源文件，杜绝数据丢失。
- 📢 **桌面弹窗提醒** – 弹窗精确显示移动了哪些文件、哪些失败（含失败原因）。
- 🔎 **递归扫描** – 可选是否扫描子文件夹。
- 📁 **自动排除备份目录** – 避免递归时重复处理 `bak` 内的文件（已处理 Windows 大小写不敏感问题）。
- 🧪 **开箱即用的 `.exe`** – 下载 `CleanOldfiles.exe` 和 `config.ini` 即可运行。
- 🗑️ **一键清空备份** – 运行 `clean_bak.py`（或打包后的 `CleanBak.exe`），确认后直接删除整个 `bak` 目录。

---

## 📦 快速开始

### 1. 使用预编译的可执行文件（Windows）
1. 从 [Releases](https://github.com/yourusername/CleanOldfiles/releases) 下载最新的 `CleanOldfiles.exe`。
2. 将 `config.ini` 放在同一目录，按需修改（参见[配置说明](./config/config_CN.ini)）。
3. 双击 `.exe` 运行，稍候会弹出结果摘要弹窗。

### 2. 从源码运行（Python 3.7+）
```bash
git clone https://github.com/yourusername/CleanOldfiles.git
cd CleanOldfiles
python main.py
