from base64 import b64encode
from hashlib import sha256
from json import dumps
from os import environ
from time import monotonic


def logger_with_colors(name: str, level="INFO"):
    """
    Get a logger with colored output.
    """
    from logging import getLogger

    debug = environ.get("DEBUG", "false").lower() == "true"
    if debug:
        level = "DEBUG"

    try:
        from coloredlogs import install

        install(level=level)
    except ImportError:
        pass

    return getLogger(name)


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


def could_be_json(data: str) -> bool:
    """
    Check if a string could be JSON.
    """
    data = data.strip()
    return (data.startswith("{") or data.startswith("[")) and (
        data.endswith("}") or data.endswith("]")
    )
