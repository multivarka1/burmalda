from __future__ import annotations

import sys

import burmalda


def teardown_function() -> None:
    burmalda.uninstall()


def test_install_prints_burmalda_before_previous_hook(capsys) -> None:
    calls = []

    def previous_hook(exc_type, exc, traceback) -> None:
        calls.append((exc_type, exc, traceback))

    original_hook = sys.excepthook
    sys.excepthook = previous_hook
    try:
        old_hook = burmalda.install()
        exc = RuntimeError("boom")

        sys.excepthook(RuntimeError, exc, None)

        assert old_hook is previous_hook
        assert calls == [(RuntimeError, exc, None)]
        assert capsys.readouterr().err == "Burmalda\n"
    finally:
        burmalda.uninstall()
        sys.excepthook = original_hook


def test_uninstall_restores_previous_hook() -> None:
    original_hook = sys.excepthook

    burmalda.install()
    assert sys.excepthook is not original_hook

    assert burmalda.uninstall() is True
    assert sys.excepthook is original_hook


def test_context_manager_restores_previous_hook() -> None:
    original_hook = sys.excepthook

    with burmalda.burmalda():
        assert sys.excepthook is not original_hook

    assert sys.excepthook is original_hook
