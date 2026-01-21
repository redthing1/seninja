from ..utility.expr_wrap_util import symbolic


class CallConvAdapter(object):
    def __init__(self, calling_convention, arch_adapter=None):
        self.calling_convention = calling_convention
        self.arch = arch_adapter

    def arg_reg_names(self):
        if self.calling_convention is None:
            return []
        return list(self.calling_convention.int_arg_regs)

    def return_reg_names(self):
        if self.calling_convention is None:
            return []
        return list(self.calling_convention.int_return_regs)

    def get_arg(self, state, k, size_bytes):
        arg_regs = self.arg_reg_names()
        if k - 1 < len(arg_regs):
            res = getattr(state.regs, arg_regs[k - 1])
            return res.Extract(size_bytes * 8 - 1, 0)

        stack_pointer = getattr(state.regs, state.arch.get_stack_pointer_reg())
        assert not symbolic(stack_pointer)
        offset_words = k - len(arg_regs)
        return state.mem.load(
            stack_pointer + (state.arch.bits() // 8) * offset_words,
            size_bytes,
            state.arch.endness(),
        )

    def set_return(self, state, value):
        regs = self.return_reg_names()
        if not regs:
            if self.arch is not None:
                self.arch.save_result_value(state, self.calling_convention, value)
            return
        setattr(state.regs, regs[0], value)


class AbiResolver(object):
    def __init__(self, view, arch_adapter=None):
        self.view = view
        self.arch = arch_adapter

    def _default_calling_convention(self):
        if self.view is None:
            return None
        return self.view.platform.default_calling_convention

    def resolve_for_function(self, function):
        cc = function.calling_convention if function is not None else self._default_calling_convention()
        return CallConvAdapter(cc, self.arch)

    def get_arg(self, state, function, k, size_bytes):
        cc = self.resolve_for_function(function)
        return cc.get_arg(state, k, size_bytes)
