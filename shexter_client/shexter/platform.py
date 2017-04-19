import sys
from enum import Enum

# Platform - an instance of the Platform enum. Tracks the running platform.
glob_platform = None


class Platform(Enum):
    WIN = 1
    LINUX = 2
    MACOS = 3
    CYGWIN = 4
    OTHER = 5


def get_platform():
    """
    :return:    The user's platform: hopefully one of: linux, win, cyg, macos.
    """
    # persist this data since it won't change during execution
    global glob_platform
    if glob_platform is not None:
        return glob_platform

    platf = sys.platform

    if platf.startswith('win'):
        platform = Platform.WIN
    elif platf.startswith('darwin'):
        print('WARNING: macos is not supported at this time')
        platform = Platform.MACOS
    else:
        if platf.startswith('linux'):
            platform = Platform.LINUX
        elif platf.startswith('cyg'):
            platform = Platform.CYGWIN
        else:
            print('WARNING: Unrecognized (and therefore unsupported) platform ' + platf)
            platform = Platform.OTHER

    return platform
