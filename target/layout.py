class DataLayout(object):
    def __init__(self, ptr_bits, endian, long_bits=None, size_t_bits=None,
                 time_t_bits=None, stack_grows_down=True):
        self.ptr_bits = ptr_bits
        self.endian = endian
        self.long_bits = long_bits if long_bits is not None else ptr_bits
        self.size_t_bits = size_t_bits if size_t_bits is not None else ptr_bits
        self.time_t_bits = time_t_bits if time_t_bits is not None else ptr_bits
        self.stack_grows_down = stack_grows_down

    @staticmethod
    def from_view(view):
        arch = view.arch
        ptr_bits = arch.address_size * 8
        endian = "little" if arch.endianness.name == "LittleEndian" else "big"
        return DataLayout(ptr_bits, endian)

    @staticmethod
    def from_arch(arch):
        ptr_bits = arch.bits()
        endian = arch.endness()
        return DataLayout(ptr_bits, endian)
