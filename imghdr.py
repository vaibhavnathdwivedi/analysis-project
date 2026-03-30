from io import BytesIO

try:
    from PIL import Image
except ImportError:
    Image = None


def what(filename, h=None):
    """Approximate replacement for Python stdlib imghdr.what."""
    if Image is None:
        return None

    if h is None:
        try:
            with open(filename, "rb") as f:
                h = f.read(32)
        except Exception:
            return None

    if isinstance(h, (bytes, bytearray)):
        try:
            # Try reading from full file path first for better detection.
            if filename and hasattr(filename, "__str__"):
                path = str(filename)
                if path and isinstance(path, str):
                    try:
                        with Image.open(path) as img:
                            return img.format.lower()
                    except Exception:
                        pass
            with Image.open(BytesIO(h)) as img:
                return img.format.lower()
        except Exception:
            return None

    return None
