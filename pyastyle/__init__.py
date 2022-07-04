import sys
import struct

VERSION = sys.version_info[:2]
PLATFORM = sys.platform
ARCH = 'x%d' % (struct.calcsize('P') * 8)

platform = None

try:
    from ._local_arch.pyastyle import *
    platform = "Local arch"
except ImportError:
    if PLATFORM == 'darwin':
        from ._macosx_universal.pyastyle import *
        platform = "MacOS X Universal"
    elif PLATFORM.startswith('linux'):
        if ARCH == 'x64':
            from ._linux_libcpp6_x86_64.pyastyle import *
            platform = "Linux 64 bits"
        elif ARCH == 'x32':
            from ._linux_libcpp6_x86.pyastyle import *
            platform = "Linux 32 bits"
    elif PLATFORM.startswith('win'):
        if ARCH == 'x64':
            from ._win64.pyastyle import *
            platform = "Windows 64 bits"
        elif ARCH == 'x32':
            from ._win32.pyastyle import *
            platform = "Windows 32 bits"

if not platform:
    raise ImportError("Could not find a suitable pyastyle binary for your platform and architecture.")
