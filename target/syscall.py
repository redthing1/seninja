class SyscallAbi(object):
    def get_number(self, state):
        raise NotImplementedError

    def get_arg(self, state, idx: int):
        raise NotImplementedError

    def set_return(self, state, value):
        raise NotImplementedError


class NullSyscallAbi(SyscallAbi):
    def __init__(self, reason="syscall ABI not configured"):
        self.reason = reason

    def get_number(self, state):
        raise NotImplementedError(self.reason)

    def get_arg(self, state, idx: int):
        raise NotImplementedError(self.reason)

    def set_return(self, state, value):
        raise NotImplementedError(self.reason)


class RegSyscallAbi(SyscallAbi):
    def __init__(self, number_reg, arg_regs, return_reg):
        self.number_reg = number_reg
        self.arg_regs = list(arg_regs)
        self.return_reg = return_reg

    def get_number(self, state):
        return getattr(state.regs, self.number_reg)

    def get_arg(self, state, idx: int):
        if idx >= len(self.arg_regs):
            raise NotImplementedError("Syscall argument index out of range")
        return getattr(state.regs, self.arg_regs[idx])

    def set_return(self, state, value):
        setattr(state.regs, self.return_reg, value)

