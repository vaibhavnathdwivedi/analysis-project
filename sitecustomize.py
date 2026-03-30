import os
import sys

# Ensure repository root is first in sys.path so local modules are available.
root = os.path.abspath(os.getcwd())
if root not in sys.path:
    sys.path.insert(0, root)

try:
    import imghdr
except ModuleNotFoundError:
    # Load fallback local imghdr if present, otherwise stub.
    import importlib.util
    import pathlib
    import types

    fallback_path = pathlib.Path(root) / "imghdr.py"
    if fallback_path.exists():
        spec = importlib.util.spec_from_file_location("imghdr", str(fallback_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules["imghdr"] = module
    else:
        fallback = types.ModuleType("imghdr")

        def what(filename, h=None):
            return None

        fallback.what = what
        sys.modules["imghdr"] = fallback
