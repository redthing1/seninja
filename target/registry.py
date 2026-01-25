import inspect

from .arch import BnArchAdapter

_ARCH_FACTORIES = {}
_OS_FACTORIES = {}
_BUILTINS_LOADED = False


def register_arch_adapter(arch_name, factory):
    _ARCH_FACTORIES[arch_name] = factory


def register_os_model(platform_name, factory):
    _OS_FACTORIES[platform_name] = factory


def _load_builtins():
    global _BUILTINS_LOADED
    if _BUILTINS_LOADED:
        return

    from ..arch.arch_x86 import x86Arch
    from ..arch.arch_x86_64 import x8664Arch
    from ..arch.arch_armv7 import ArmV7Arch
    from ..arch.arch_arm32 import Arm32Arch
    from ..arch.arch_aarch64 import AArch64Arch
    from ..arch.arch_riscv import RiscVArch
    from ..os_models.linux import (
        Linuxi386,
        Linuxia64,
        LinuxArmV7,
        LinuxAArch64,
        LinuxRiscV,
    )
    from ..os_models.windows import Windows
    from ..os_models.macos import MacOS

    register_arch_adapter("x86", x86Arch)
    register_arch_adapter("x86_64", x8664Arch)
    register_arch_adapter("armv7", ArmV7Arch)
    register_arch_adapter("armv7eb", Arm32Arch)
    register_arch_adapter("thumb2", Arm32Arch)
    register_arch_adapter("thumb2eb", Arm32Arch)
    register_arch_adapter("aarch64", AArch64Arch)
    register_arch_adapter("riscv32", RiscVArch)
    register_arch_adapter("riscv64", RiscVArch)
    register_arch_adapter("rv32gc", RiscVArch)
    register_arch_adapter("rv64gc", RiscVArch)

    register_os_model("linux-x86", Linuxi386)
    register_os_model("linux-x86_64", Linuxia64)
    register_os_model("linux-armv7", LinuxArmV7)
    register_os_model("linux-armv7eb", LinuxArmV7)
    register_os_model("linux-thumb2", LinuxArmV7)
    register_os_model("linux-thumb2eb", LinuxArmV7)
    register_os_model("linux-aarch64", LinuxAArch64)
    register_os_model("linux-riscv32", LinuxRiscV)
    register_os_model("linux-riscv64", LinuxRiscV)
    register_os_model("linux-rv32gc", LinuxRiscV)
    register_os_model("linux-rv64gc", LinuxRiscV)
    register_os_model("windows-x86", Windows)
    register_os_model("windows-x86_64", Windows)
    register_os_model("mac-x86_64", MacOS)
    register_os_model("mac-aarch64", MacOS)

    _BUILTINS_LOADED = True


def _instantiate(factory, view):
    if factory is None:
        return None
    if inspect.isclass(factory):
        sig = inspect.signature(factory)
        if len(sig.parameters) == 0:
            return factory()
        return factory(view)
    try:
        return factory(view)
    except TypeError:
        return factory()


def resolve_arch_adapter(view):
    _load_builtins()
    arch_name = view.arch.name
    factory = _ARCH_FACTORIES.get(arch_name)
    if factory is None:
        return BnArchAdapter(view)
    return _instantiate(factory, view)


def resolve_os_model(view):
    _load_builtins()
    platform_name = view.platform.name
    factory = _OS_FACTORIES.get(platform_name)
    if factory is None:
        return None
    return _instantiate(factory, view)
