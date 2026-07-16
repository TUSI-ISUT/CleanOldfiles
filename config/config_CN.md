⚙️ 配置说明
编辑与程序同目录的 config.ini，所有参数说明如下：

ini
[scan]
# 要扫描的文件夹（支持环境变量）
directory = %USERPROFILE%\Desktop\

# 文件匹配模式 —— 在这里定义你想清理的任意文件类型（英文逗号分隔）
patterns = *.ppt, *.pptx

# 是否扫描子目录？true 或 false
recursive = false

[time]
# 天数：设为 0 表示不限制该条件
creation_days = 3      # 创建时间早于 3 天的文件将被移动
access_days = 2        # 最后访问时间早于 2 天的文件将被移动

时间逻辑
仅当两个条件均满足时，文件才会被移动（阈值>0 时）：

文件创建时间 < 当前时间 - creation_days

文件最后访问时间 < 当前时间 - access_days

若将某个阈值设为 0，则忽略该条件（例如 creation_days = 0 表示“不考虑创建日期”）。

🗂️ 备份与清理
所有被移动的文件存入程序所在目录下的 bak 文件夹（而非被扫描的目标目录）。

若备份目录中已存在同名文件，会自动添加数字后缀（如 _1, _2），避免覆盖。

如需清空整个 bak 目录，运行：
clean_bak.exe
执行前会弹出确认对话框，防止误删。
