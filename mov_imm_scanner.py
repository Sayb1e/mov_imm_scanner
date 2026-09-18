import idaapi
import idc
import idautils
import ida_kernwin
import ida_ua
import ida_bytes
import ida_lines


PLUGIN_NAME = "MOV Immediate Scanner"
PLUGIN_COMMENT = "Scan immediate operands of mov-like instructions in a selection"
PLUGIN_HELP = (
    "Select an address range in the disassembly view, then run this plugin.\n"
    "It prints every instruction that moves an immediate value, e.g. mov eax, 1234h."
)
PLUGIN_HOTKEY = "Ctrl-Alt-I"

MOV_MNEMONICS = ("mov", "movzx", "movsx", "movsxd")


def get_selection_range():
    if hasattr(ida_kernwin, "read_range_selection"):
        ok, start, end = ida_kernwin.read_range_selection(None)
    else:
        ok, start, end = ida_kernwin.read_selection()
    if ok:
        return start, end

    start = ida_kernwin.ask_addr(ida_kernwin.get_screen_ea(), "Start address:")
    if start in (None, idaapi.BADADDR):
        return None, None
    end = ida_kernwin.ask_addr(start, "End address (exclusive):")
    if end in (None, idaapi.BADADDR):
        return None, None
    if end < start:
        start, end = end, start
    return start, end


def disasm_line(ea):
    try:
        text = ida_lines.generate_disasm_line(ea, 0)
    except AttributeError:
        text = idc.generate_disasm_line(ea, 0)
    return ida_lines.tag_remove(text or "")


def scan_range(start, end):
    hits = 0
    total = 0
    insn = ida_ua.insn_t()

    for ea in idautils.Heads(start, end):
        if not ida_bytes.is_code(ida_bytes.get_flags(ea)):
            continue
        if ida_ua.decode_insn(insn, ea) == 0:
            continue
        total += 1

        mnem = ida_ua.print_insn_mnem(ea).lower()
        if mnem not in MOV_MNEMONICS:
            continue

        for i, op in enumerate(insn.ops):
            if op.type == ida_ua.o_void:
                break
            if op.type == ida_ua.o_imm:
                hits += 1
                idaapi.msg(
                    "0x%X  op%d = 0x%X   ; %s\n" % (ea, i, op.value, disasm_line(ea))
                )
                break

    idaapi.msg("\n[MOV Imm Scanner] %d immediate mov(s) found in %d instructions.\n" % (hits, total))
    return hits


class MovImmScannerPlugmod(idaapi.plugmod_t):
    def run(self, arg):
        start, end = get_selection_range()
        if start is None:
            idaapi.warning("No address range selected.")
            return
        ida_kernwin.msg("[MOV Imm Scanner] range 0x%X - 0x%X\n" % (start, end))
        scan_range(start, end)

    def __del__(self):
        pass


class MovImmScannerPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP | idaapi.PLUGIN_MULTI
    comment = PLUGIN_COMMENT
    help = PLUGIN_HELP
    wanted_name = PLUGIN_NAME
    wanted_hotkey = PLUGIN_HOTKEY

    def init(self):
        return MovImmScannerPlugmod()

    def run(self, arg):
        pass

    def term(self):
        pass


def PLUGIN_ENTRY():
    return MovImmScannerPlugin()
