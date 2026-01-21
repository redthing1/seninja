from ..arch.arch_abstract import Arch


class BnArchAdapter(Arch):
    def __init__(self, view):
        self._view = view
        self._arch = view.arch
        self._bits = self._resolve_bits()
        self._endian = self._resolve_endian()
        self._regs = self._build_regs()
        self._reg_names = self._build_reg_names()
        self._flags = self._build_flags()
        self._ip = None
        self._sp = self._normalize_reg_name(self._arch.stack_pointer)
        self._bp = None
        self._lr = self._normalize_reg_name(self._arch.link_reg)

    def _normalize_reg_name(self, reg):
        if reg is None:
            return None
        if isinstance(reg, str):
            return reg
        return getattr(reg, "name", reg)

    def _resolve_bits(self):
        return self._arch.address_size * 8

    def _resolve_endian(self):
        return "little" if self._arch.endianness.name == "LittleEndian" else "big"

    def _iter_reg_infos(self):
        return self._arch.regs.items()

    def _get_full_reg_name(self, reg_info, reg_name):
        full = reg_info.full_width_reg
        if full:
            return full
        return reg_name

    def _get_reg_offset(self, reg_info):
        return reg_info.offset

    def _get_reg_size(self, reg_info):
        return reg_info.size

    def _build_regs(self):
        full_regs = {}
        reg_infos = list(self._iter_reg_infos())
        for reg_name, reg_info in reg_infos:
            full_name = self._get_full_reg_name(reg_info, reg_name)
            if full_name not in full_regs:
                full_info = self._arch.regs[full_name]
                size = self._get_reg_size(full_info)
                full_regs[full_name] = {
                    "size": size,
                    "sub": {},
                }

        for reg_name, reg_info in reg_infos:
            full_name = self._get_full_reg_name(reg_info, reg_name)
            if full_name == reg_name:
                continue
            parent = full_regs.get(full_name)
            if not parent:
                continue
            parent_size = parent["size"]
            sub_size = self._get_reg_size(reg_info)
            bn_offset = self._get_reg_offset(reg_info)
            mem_offset = max(parent_size - sub_size - bn_offset, 0)
            parent["sub"][reg_name] = {
                "offset": mem_offset,
                "size": sub_size,
            }

        curr_addr = 0
        for reg_name in full_regs:
            reg = full_regs[reg_name]
            reg["addr"] = curr_addr
            curr_addr += reg["size"]
        return full_regs

    def _build_reg_names(self):
        return list(self._regs.keys())

    def _build_flags(self):
        names = list(self._arch.flags)
        return {name: 0 for name in names}

    def bits(self):
        return self._bits

    def regs_data(self):
        return self._regs

    def reg_names(self):
        return self._reg_names

    def flags_data(self):
        return self._flags

    def flags_default(self, flag):
        return None

    def endness(self):
        return self._endian

    def getip_reg(self):
        if self._ip:
            return self._ip
        for name in ("pc", "ip", "rip", "eip"):
            if name in self._regs:
                return name
        return next(iter(self._regs.keys()))

    def get_base_pointer_reg(self):
        if self._bp:
            return self._bp
        for name in ("bp", "rbp", "ebp", "fp"):
            if name in self._regs:
                return name
        return None

    def get_stack_pointer_reg(self):
        if self._sp:
            return self._sp
        for name in ("sp", "rsp", "esp"):
            if name in self._regs:
                return name
        return next(iter(self._regs.keys()))

    def save_return_address(self, state, return_address):
        if self._lr and self._lr in self._regs:
            setattr(state.regs, self._lr, return_address)
            return
        state.stack_push(return_address)

    def get_return_address(self, state):
        if self._lr and self._lr in self._regs:
            return getattr(state.regs, self._lr)
        return state.stack_pop()

    def get_argument_regs(self, calling_convention):
        return list(calling_convention.int_arg_regs)

    def save_result_value(self, state, calling_convention, value):
        reg_names = list(calling_convention.int_return_regs)
        if not reg_names:
            return
        reg = reg_names[0]
        setattr(state.regs, reg, value)

    def get_flag_cond_lambda(self, cond: str):
        raise NotImplementedError

    def execute_special_handler(self, disasm_str, sv):
        return False
