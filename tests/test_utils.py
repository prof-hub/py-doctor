import builtins
import os
import ntpath
import sys
import types

# Provide minimal rich stubs so utils can be imported without the real package
console_module = types.ModuleType("rich.console")

class DummyConsole:
    def print(self, *a, **k):
        pass

    def rule(self, *a, **k):
        pass

console_module.Console = DummyConsole

markdown_module = types.ModuleType("rich.markdown")
markdown_module.Markdown = lambda x: x

sys.modules.setdefault("rich.console", console_module)
sys.modules.setdefault("rich.markdown", markdown_module)
sys.modules.setdefault("rich", types.ModuleType("rich"))
sys.modules["rich"].console = console_module
sys.modules["rich"].markdown = markdown_module

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import utils


def test_log_filename_posix(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "LOG_DIR", tmp_path)
    monkeypatch.setattr(utils, "timestamp", lambda: "ts")
    utils.garantir_logs()

    projeto = f"dir{os.sep}proj"
    expected = f"geral_log_{projeto.replace(os.sep, '_')}_ts.txt"
    caminho = utils.logar("msg", projeto)
    assert caminho == os.path.join(tmp_path, expected)
    with open(caminho, "r", encoding="utf-8") as f:
        assert f.read() == "[INFO] msg\n"


def test_log_filename_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(utils, "LOG_DIR", str(tmp_path))
    monkeypatch.setattr(utils.os, "sep", "\\")
    monkeypatch.setattr(utils.os, "path", ntpath)
    monkeypatch.setattr(utils, "timestamp", lambda: "ts")
    utils.garantir_logs()

    projeto = "dir\\proj"
    safe_proj = projeto.replace("\\", "_")
    expected = f"geral_log_{safe_proj}_ts.txt"
    expected_path = ntpath.join(str(tmp_path), expected)
    opened = {}

    def dummy_open(path, mode="w", encoding=None):
        opened["path"] = path
        class Dummy:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc, tb):
                pass
            def write(self, data):
                pass
        return Dummy()

    monkeypatch.setattr(builtins, "open", dummy_open)

    caminho = utils.logar("msg", projeto)
    assert caminho == expected_path
    assert opened["path"] == expected_path
