# MOV 立即数扫描器

一个 IDA Pro 插件（IDAPython）：扫描用户选中的地址范围，把所有向寄存器写入立即数的
`mov` 类指令打印到 Output 窗口。

## 功能

- 扫描用户在反汇编视图中选中的地址范围
- 未选中任何范围时，弹出起止地址输入框
- 匹配 `mov`、`movzx`、`movsx`、`movsxd`
- 打印地址、操作数序号、立即数以及反汇编文本
- 结果输出到 IDA 的 Output 窗口
- 快捷键：`Ctrl-Alt-I`

## 环境要求

- IDA Pro 9.x
- IDAPython

插件基于 IDA 9.x 插件框架（`plugmod_t` + `ida-plugin.json`），以独立插件目录的形式安装。

## 安装

1. 将 `mov_imm_scanner` 文件夹复制到 IDA 插件目录：
   - `<IDA 安装目录>\plugins\mov_imm_scanner\`
   - 或 `%APPDATA%\Hex-Rays\IDA Pro\plugins\mov_imm_scanner\`
2. 重启 IDA。

该目录中必须同时包含 `mov_imm_scanner.py` 和 `ida-plugin.json`。

## 使用

1. 打开数据库，切换到反汇编视图。
2. 选中一段地址范围。
3. 执行 `Edit > Plugins > MOV Immediate Scanner`，或按 `Ctrl-Alt-I`。
4. 结果会打印在 Output 窗口。

如果未选中任何范围，插件会提示输入起始和结束地址。

## 输出示例

```
[MOV Imm Scanner] range 0x140001000 - 0x140003000
0x14000BEF4  op1 = 0x4000   ; mov ecx, 4000h
0x140027B51  op1 = 0x7      ; mov ecx, 7
0x140027CEF  op1 = 0x5A4D   ; mov eax, 5A4Dh

[MOV Imm Scanner] 3 immediate mov(s) found in 697 instructions.
```

## 说明

- 只统计真正的立即数（`o_imm`）。`mov rax, offset foo`（内存/符号引用，`o_mem`）
  不在统计范围内。
- 通过 `idautils.Heads` 遍历地址，因此不会从指令中间开始解码。
- 在体积较小或分析不充分的二进制上，解码到的指令数量可能偏少；
  请确保自动分析已经完成。

## 测试环境

- IDA Pro 9.2.0.250908 (Windows)

## 许可证

暂未选择许可证。
