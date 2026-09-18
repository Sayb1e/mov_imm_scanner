# MOV Immediate Scanner

An IDA Pro plugin (IDAPython) that scans a user-selected address range and prints
every `mov`-like instruction that assigns an immediate value to the Output window.

## Features

- Scans the address range selected by the user
- Falls back to prompting for start/end addresses when nothing is selected
- Matches `mov`, `movzx`, `movsx`, `movsxd`
- Prints address, operand index, immediate value and the disassembly line
- Output goes to the IDA Output window
- Hotkey: `Ctrl-Alt-I`

## Requirements

- IDA Pro 9.x
- IDAPython

The plugin uses the IDA 9.x plugin framework (`plugmod_t` + `ida-plugin.json`),
so it is installed as a self-contained plugin directory.

## Installation

1. Copy the `mov_imm_scanner` folder into your IDA plugins directory:
   - `<IDA install dir>\plugins\mov_imm_scanner\`
   - or `%APPDATA%\Hex-Rays\IDA Pro\plugins\mov_imm_scanner\`
2. Restart IDA.

The folder must contain both `mov_imm_scanner.py` and `ida-plugin.json`.

## Usage

1. Open a database and switch to the disassembly view.
2. Select an address range.
3. Run `Edit > Plugins > MOV Immediate Scanner`, or press `Ctrl-Alt-I`.
4. Results are printed to the Output window.

If nothing is selected, the plugin asks for the start and end address.

## Example output

```
[MOV Imm Scanner] range 0x140001000 - 0x140003000
0x14000BEF4  op1 = 0x4000   ; mov ecx, 4000h
0x140027B51  op1 = 0x7      ; mov ecx, 7
0x140027CEF  op1 = 0x5A4D   ; mov eax, 5A4Dh

[MOV Imm Scanner] 3 immediate mov(s) found in 697 instructions.
```

## Notes

- Only true immediates (`o_imm`) are reported. `mov rax, offset foo`
  (a memory/symbol reference, `o_mem`) is intentionally excluded.
- The range is iterated with `idautils.Heads`, so decoding never starts
  in the middle of an instruction.
- On a small or lightly analyzed binary the number of decoded instructions
  may be low; make sure auto-analysis has finished.

## Tested with

- IDA Pro 9.2.0.250908 (Windows)

## License

No license has been chosen yet.
