from ..target.arch import BnArchAdapter


class Arm32Arch(BnArchAdapter):
    BASE_POINTER_CANDIDATES = ("fp", "r11")

    def __init__(self, view):
        super().__init__(view)

    def get_base_pointer_reg(self):
        if self._bp:
            return self._bp
        for name in Arm32Arch.BASE_POINTER_CANDIDATES:
            if name in self._regs:
                return name
        return super().get_base_pointer_reg()
