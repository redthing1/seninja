from ..expr import Bool
from .os_file import OsFileHandler


class NullOS(OsFileHandler):
    def __init__(self):
        super().__init__()
        self.stdin_fd = self.open("__stdin", "r--")
        self.stdout_fd = self.open("__stdout", "-w-")

    def get_syscall_by_number(self, n):
        return None

    def get_stdin_stream(self):
        session = self.descriptors_map[self.stdin_fd]
        session_idx = session.seek_idx
        session.seek(0)
        res = session.read(session.symfile.file_size)
        session.seek(session_idx)
        return res

    def get_stdout_stream(self):
        session = self.descriptors_map[self.stdout_fd]
        session_idx = session.seek_idx
        session.seek(0)
        res = session.read(session.symfile.file_size)
        session.seek(session_idx)
        return res

    def copy(self):
        res = NullOS()
        super().copy_to(res)
        res.stdin_fd = self.stdin_fd
        res.stdout_fd = self.stdout_fd
        return res

    def merge(self, other, merge_condition: Bool):
        assert isinstance(other, NullOS)
        pass  # TODO implement this
