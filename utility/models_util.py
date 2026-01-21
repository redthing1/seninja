from .bninja_util import get_function


def get_arg_k(state, k, size, view):

    ip = state.get_ip()
    func = get_function(view, ip)
    if not hasattr(state, "abi") or state.abi is None:
        raise Exception("Missing ABI resolver for argument access")
    return state.abi.get_arg(state, func, k, size)
