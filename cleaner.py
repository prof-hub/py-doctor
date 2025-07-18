# py-doctor/cleaner.py

"""Rotinas de limpeza de arquivos e gestão de logs."""

import os
import time
import shutil
from glob import glob
from pathlib import Path
from rich.console import Console
from rich.table import Table

from py_doctor.utils import LOG_DIR, esta_em_modo_teste, logar


console = Console()


def _remover_caminho(caminho, projeto_path):
    """Remove um caminho e registra erros se ocorrerem."""

    try:
        if caminho.is_dir():
            shutil.rmtree(caminho)
        else:
            caminho.unlink()
        return True
    except PermissionError as e:
        console.print(f"[red]Permissão negada ao remover {caminho}: {e}[/]")
        logar(
            f"Permissão negada ao remover {caminho}: {e}",
            projeto_path,
            tipo="limpeza",
            nivel="ERROR",
        )
    except Exception as e:
        console.print(f"[red]Erro ao remover {caminho}: {e}[/]")
        logar(
            f"Erro ao remover {caminho}: {e}",
            projeto_path,
            tipo="limpeza",
            nivel="ERROR",
        )
    return False


def limpar_pycache(projeto_path):
    """Remove pastas ``__pycache__`` e arquivos temporários.

    Args:
        projeto_path (str): Diretório do projeto que será limpo.

    Returns:
        None
    """

    console.rule(f"[bold red]🧹 Limpando: {projeto_path}")
    projeto_path = Path(projeto_path)
    modo_teste = esta_em_modo_teste()
    removidos = []
    inicio = time.time()

    for root, dirs, files in os.walk(projeto_path):
        for d in dirs:
            if d == "__pycache__":
                caminho = Path(root) / d
                removidos.append(("__pycache__", caminho))
                if not modo_teste:
                    _remover_caminho(caminho, projeto_path)

        for f in files:
            if f.endswith((".pyc", ".pyo", ".log")):
                caminho = Path(root) / f
                removidos.append((f[-4:], caminho))
                if not modo_teste:
                    _remover_caminho(caminho, projeto_path)

    if not removidos:
        console.print("[green]✅ Nada para limpar.")
        logar("Sem resíduos a remover.", projeto_path, tipo="limpeza")
        return

    tabela = Table(title="🧽 Arquivos e pastas removidos", show_lines=True)
    tabela.add_column("Tipo", style="bold")
    tabela.add_column("Caminho", style="dim")

    for tipo, caminho in removidos:
        tabela.add_row(tipo, str(caminho))

    console.print(tabela)

    if modo_teste:
        console.print(
            "[yellow]🔒 Modo de teste ativo — nenhuma exclusão foi realizada."
        )

    texto_log = f"Itens removidos (modo_teste={modo_teste}):\n"
    for tipo, caminho in removidos:
        texto_log += f"[{tipo}] {caminho}\n"

    duracao = time.time() - inicio
    texto_log += f"Duração da limpeza: {duracao:.2f}s\n"
    logar(texto_log, projeto_path, tipo="limpeza")



def arquivar_logs_antigos(dias):
    """Move arquivos ``.log`` antigos para a pasta ``logs_arquivados``.

    Args:
        dias (int): Idade mínima dos logs (em dias) para serem arquivados.

    Returns:
        None
    """

    destino = Path(LOG_DIR) / "logs_arquivados"
    destino.mkdir(parents=True, exist_ok=True)
    limite = time.time() - dias * 86400

    for arquivo in Path(LOG_DIR).glob("*.txt"):
        if arquivo.stat().st_mtime < limite:
            try:
                shutil.move(str(arquivo), str(destino / arquivo.name))
                console.print(f"[blue]Arquivo arquivado:[/] {arquivo}")
            except Exception as e:
                console.print(f"[red]Erro ao arquivar {arquivo}: {e}")
                logar(
                    f"Erro ao arquivar {arquivo}: {e}",
                    LOG_DIR,
                    tipo="limpeza",
                    nivel="ERROR",
                )


