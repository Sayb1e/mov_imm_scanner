# AGENTS.md

给 AI/协作者的约定。修改本插件前先读 `DEVELOPMENT.md`。

## 项目

- 仓库：https://github.com/Sayb1e/mov_imm_scanner （MIT）
- 本地：`D:\Objection\mov_imm_scanner`
- 功能：IDA Pro 插件，扫描选中区域的 `mov` 类立即数，支持明细输出 + Python/C 数组导出。

## 环境（本机）

- IDA Pro 9.2：`D:\CTFtools\IDA Professional 9.2\`（GUI 为 `ida.exe`，文本为 `idat.exe`）
- 代理：`127.0.0.1:7897`（访问 GitHub 必开）
- 便携 gh：`C:\Users\Randy\AppData\Local\Temp\opencode\ghcli\bin\gh.exe`
- Git 身份：`Sayb1e` / `sayb1e@qq.com`

## 编码规范

- 所有文件用 **UTF-8 无 BOM**。
- 不写注释，除非确有必要。
- 保持单文件结构（`mov_imm_scanner.py`），不要随意拆文件。
- 不要改 `ida-plugin.json` 的 `entryPoint` 与 `name`（改 `name` 会影响 action 命名空间）。
- 兼容性：优先加回退分支，不要直接删旧 API 调用（见 `get_selection_range`）。

## 必守的框架约束

- 插件必须放在**子目录**里并带 `ida-plugin.json`，单文件放 `plugins\` 根目录不会被加载。
- `plugin_t.init()` 返回 `plugmod_t` 实例；业务逻辑写在 `plugmod_t.run`。
- 额外菜单项通过 `register_action` + `attach_action_to_menu("Edit/Plugins/", ...)` 实现。

## 测试

- 改完先 `python -m py_compile mov_imm_scanner.py` 检查语法。
- 功能回归：用 `idat.exe`（文本）跑检查脚本验证加载/action/格式化；
  验证菜单挂载必须用 `ida.exe`（GUI），看 `attach_action_to_menu` 返回 `True`。
- 最后把改动同步到 IDA 安装目录的插件副本：
  `D:\CTFtools\IDA Professional 9.2\plugins\mov_imm_scanner\`，重启 IDA 实测。

## 发布

```powershell
$env:HTTPS_PROXY="http://127.0.0.1:7897"; $env:HTTP_PROXY="http://127.0.0.1:7897"
git add -A
git commit -m "feat|fix|docs|chore: <描述>"
git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 push origin main
git status -sb; git ls-remote origin refs/heads/main   # 哈希需一致
```

## 不要做

- 未经要求不要改许可证、不要加依赖、不要重写 README 结构。
- 不要使用交互式 rebase / force push。
