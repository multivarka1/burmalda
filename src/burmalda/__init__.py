"""Print ``Burmalda`` when a Python program crashes."""

from __future__ import annotations

from contextlib import contextmanager
from types import TracebackType
from typing import Callable, Iterator, Optional, Type
import sys

__all__ = ["__version__", "burmalda", "install", "uninstall"]

__version__ = "0.1.0"

ExcHook = Callable[[Type[BaseException], BaseException, Optional[TracebackType]], None]

_previous_hook: Optional[ExcHook] = None
_installed_hook: Optional[ExcHook] = None


def install(message: str = "Burmalda") -> ExcHook:
    """Install a global exception hook that prints *message* on crashes.

    The hook handles unhandled exceptions, prints the message to stderr, and
    then calls the exception hook that was active before installation.
    """

    global _previous_hook, _installed_hook

    if _installed_hook is not None:
        return sys.excepthook

    previous_hook = sys.excepthook

    def burmalda_hook(
        exc_type: Type[BaseException],
        exc: BaseException,
        traceback: Optional[TracebackType],
    ) -> None:
        print(message, file=sys.stderr)
        previous_hook(exc_type, exc, traceback)

    _previous_hook = previous_hook
    _installed_hook = burmalda_hook
    sys.excepthook = burmalda_hook
    return previous_hook


def uninstall() -> bool:
    """Restore the exception hook that was active before :func:`install`.

    Returns ``True`` when a hook was removed, otherwise ``False``.
    """

    global _previous_hook, _installed_hook

    if _installed_hook is None:
        return False

    if sys.excepthook is _installed_hook and _previous_hook is not None:
        sys.excepthook = _previous_hook

    _previous_hook = None
    _installed_hook = None
    return True


@contextmanager
def burmalda(message: str = "Burmalda") -> Iterator[None]:
    """Temporarily install the Burmalda exception hook."""

    install(message=message)
    try:
        yield
    finally:
        uninstall()
