import builtins
import os
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
prompt_module = types.ModuleType("rich.prompt")
prompt_module.Prompt = lambda *a, **k: None
panel_module = types.ModuleType("rich.panel")
panel_module.Panel = lambda *a, **k: None

sys.modules.setdefault("rich.console", console_module)
sys.modules.setdefault("rich.markdown", markdown_module)
sys.modules.setdefault("rich.prompt", prompt_module)
sys.modules.setdefault("rich.panel", panel_module)
sys.modules.setdefault("rich", types.ModuleType("rich"))
sys.modules["rich"].console = console_module
sys.modules["rich"].markdown = markdown_module
sys.modules["rich"].prompt = prompt_module
sys.modules["rich"].panel = panel_module

from pathlib import Path
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from py_doctor import utils


def test_log_filename_posix(tmp_path, monkeypatch):
    monkeypatch.setattr(utils, "LOG_DIR", tmp_path)
    monkeypatch.setattr(time, "strftime", lambda fmt: "ts")
    utils.garantir_logs()

    project = tmp_path / "proj"
    project.mkdir()

    utils.logar("msg", project, "geral")

    geral = tmp_path / "pydoctor_main_ts.log"
    local = project / ".pydoctor_geral.log"
    assert geral.read_text(encoding="utf-8").strip() == "ts [INFO] - msg"
    assert local.read_text(encoding="utf-8") == "msg"


def test_log_filename_windows(monkeypatch, tmp_path):
    monkeypatch.setattr(utils, "LOG_DIR", tmp_path)
    monkeypatch.setattr(time, "strftime", lambda fmt: "ts")
    utils.garantir_logs()

    project = tmp_path / "proj_win"
    project.mkdir()

    utils.logar("msg", project, "geral")

    assert (tmp_path / "pydoctor_main_ts.log").exists()
    assert (project / ".pydoctor_geral.log").exists()
