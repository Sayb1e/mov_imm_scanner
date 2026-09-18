# 开发记录 / Development Notes

本文件记录本插件的架构、关键决策、踩过的坑与扩展指南，方便日后修改。

## 1. 项目结构

```
mov_imm_scanner/
├── ida-plugin.json         # IDA 9.x 插件元数据（入口声明）
├── mov_imm_scanner.py      # 全部逻辑（单文件）
├── README.md               # 用户文档
├── DEVELOPMENT.md          # 本文件：开发记录
└── AGENTS.md               # 给 AI/协作者的约定
```

安装时整个文件夹放进 IDA 的 `plugins\` 下即可。

## 2. IDA 9.x 插件框架要点（重要）

IDA 9.0 起推荐“新框架”，与旧写法不同：

- **必须放在子目录**，并提供 `ida-plugin.json`：
  ```json
  {
    "IDAMetadataDescriptorVersion": 1,
    "plugin": { "name": "MOV Immediate Scanner", "entryPoint": "mov_imm_scanner.py" }
  }
  ```
- `plugin_t.init()` 返回一个 **`plugmod_t` 实例**（不是 `PLUGIN_OK`）。
  运行时调用的是 `plugmod_t.run(arg)`，`plugin_t.run/term` 不再使用。
- 实测：**单文件直接丢在 `plugins\` 根目录不会被自动加载**；用“子目录 + json”才稳定出现于 `Edit > Plugins`。
- `flags` 用 `PLUGIN_KEEP | PLUGIN_MULTI`。

## 3. 关键 API 与坑

- **取选区**：IDA 9.2 的 `ida_kernwin.read_selection()` 变成需要 `(v, p1, p2)`。
  用便捷函数：
  ```python
  ok, start, end = ida_kernwin.read_range_selection(None)  # None = 当前地址窗口
  ```
  代码里保留了对旧版的回退。
- **立即数判断**：`insn.ops[i].type == ida_ua.o_imm`，值在 `.value`。
  只算立即数；`mov rax, offset foo` 属于 `o_mem`，未计入（如需，可在 `collect_immediates` 里加）。
- **遍历地址**：用 `idautils.Heads(start, end)`，只落在指令/数据头，避免从指令中间解码。
- **多菜单项**：一个插件目录只能有 1 个入口。额外菜单项用 `register_action` +
  `ida_kernwin.attach_action_to_menu("Edit/Plugins/", action_name, SETMENU_APP)`。
  - 注意：`idat.exe`（文本模式）无菜单栏，`attach_action_to_menu` 会返回 `False`；
    要用 GUI 版 `ida.exe` 验证（返回 `True` 才算挂上）。
- **文件编码**：所有 `.py`/文本必须 **UTF-8 无 BOM**，否则 IDA 报 `U+FEFF`/中文乱码。

## 4. 代码职责

| 函数 | 作用 |
| :--- | :--- |
| `get_selection_range()` | 取当前选区；无选区时弹框输入起止地址 |
| `collect_immediates(start, end)` | 返回立即数列表（导出用） |
| `scan_range(start, end)` | 明细输出到 Output 窗口 |
| `format_python_array(values)` | 生成 `immediates = [...]` |
| `format_c_array(values)` | 生成 `uint64_t immediates[] = {...};` |
| `export_array(kind)` | 取选区 + 收集 + 按格式输出 |
| `register_actions()` / `unregister_actions()` | 注册/注销两个导出菜单项 |

## 5. 如何扩展

- **支持更多指令**：改 `MOV_MNEMONICS` 元组（如加 `lea`、`push` 等）。
- **新增导出格式**（如 JSON、Rust 数组）：
  1. 加一个 `format_xxx(values)`；
  2. 在 `export_array` 里分支；
  3. 加 `ACTION_*` 常量，在 `register_actions` 注册并 attach 到 `Edit/Plugins/`。
- **导出带地址**：把 `collect_immediates` 改成收集 `(ea, value)`，格式化时一并输出。
- **改 C 类型**：`format_c_array` 里的 `uint64_t` 与 `ULL` 后缀。

## 6. 本地测试方法（无 GUI 也可回归）

用 IDA 命令行跑一个脚本，检查插件是否加载、action 是否注册、导出格式是否正确：

```powershell
# 文本模式（快，但无法测菜单挂载）
& "D:\CTFtools\IDA Professional 9.2\idat.exe" -A -c -S"<检查脚本.py>" -L"<日志>" "<某个.exe/dll>"
# GUI 模式（可测 attach_action_to_menu）
& "D:\CTFtools\IDA Professional 9.2\ida.exe"  -A -c -S"<检查脚本.py>" -L"<日志>" "<某个.exe/dll>"
```

检查脚本可调用 `idaapi.find_plugin("MOV Immediate Scanner", False)`、
`ida_kernwin.get_action_label("mov_imm_scanner:py_array")` 等做断言。

## 7. 发布流程

见仓库根目录 `AGENTS.md`（含代理、gh、push 命令）。

## 8. 变更历史

见 `git log`。提交信息用 `feat:` / `fix:` / `docs:` / `chore:` / `ci:` 前缀。

## 9. TODO / 待办

- [ ] 可选：导出为 JSON / Rust 数组
- [ ] 可选：导出时附带地址（`(ea, value)`）
- [ ] 可选：对 `o_mem`（`mov reg, offset xxx`）的支持开关
- [ ] 可选：兼容 IDA 8.x 的 legacy 版本
