from ..target.arch import BnArchAdapter


class RiscVArch(BnArchAdapter):
    ZERO_REG_NAMES = {"zero", "x0"}

    def __init__(self, view):
        super().__init__(view)

    def normalize_reg_write(self, reg_name, value, dest_size_bytes):
        if reg_name in RiscVArch.ZERO_REG_NAMES:
            return None, value
        return reg_name, value

    def is_synthetic_reg(self, reg_name):
        return reg_name in RiscVArch.ZERO_REG_NAMES

    def is_zero_reg(self, reg_name):
        return reg_name in RiscVArch.ZERO_REG_NAMES
