from .registry import resolve_arch_adapter, resolve_os_model
from .layout import DataLayout
from .abi import AbiResolver
from .syscall import NullSyscallAbi
from ..os_models.null import NullOS


class TargetContext(object):
    def __init__(self, view, arch, abi, syscall_abi, os_model, layout):
        self.view = view
        self.arch = arch
        self.abi = abi
        self.syscall_abi = syscall_abi
        self.os = os_model
        self.layout = layout

    def clone_with(self, os_model=None):
        os_model = os_model if os_model is not None else self.os
        syscall_abi = self.syscall_abi
        return TargetContext(self.view, self.arch, self.abi, syscall_abi, os_model, self.layout)


def resolve_target(view):
    arch = resolve_arch_adapter(view)
    os_model = resolve_os_model(view)
    if os_model is None:
        os_model = NullOS()
    layout = DataLayout.from_view(view)
    abi = AbiResolver(view, arch)
    syscall_abi = os_model.get_syscall_abi(view, arch)

    if syscall_abi is None:
        syscall_abi = NullSyscallAbi(
            "syscall ABI not configured for platform {}".format(view.platform.name)
        )
    return TargetContext(view, arch, abi, syscall_abi, os_model, layout)
