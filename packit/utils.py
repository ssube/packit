from base64 import b64encode
from hashlib import sha256
from json import dumps
from time import monotonic


def hash_dict(data: dict):
    """
    Hash a dictionary of data. The result is safe to use as a filename.
    """
    return b64encode(
        sha256(dumps(data, sort_keys=True).encode("utf-8")).digest(),
        altchars=b"-_",
    ).decode("utf-8")


def monotonic_delta(start: float) -> tuple[float, float]:
    """
    Get the time delta from a start time and the current time.
    Returns the delta and the current time.
    """
    last = monotonic()
    return (last - start, last)
