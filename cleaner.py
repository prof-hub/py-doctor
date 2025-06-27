# py-doctor/cleaner.py

import os
import time
import shutil
from glob import glob
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from py_doctor.utils import logar, esta_em_modo_teste, LOG_DIR
from py_doctor import filesystem as fs

console = Console()


def limpar_pycache(projeto_path):
    console.rule(f"[bold red]🧹 Limpando: {projeto_path}")
    modo_teste = esta_em_modo_teste()
    removidos = []
    inicio = time.time()

    for root, dirs, files in os.walk(projeto_path):
        for d in dirs:
            if d == "__pycache__":
                caminho = os.path.join(root, d)
                removidos.append(("__pycache__", caminho))
                if not modo_teste:
                    try:
                        fs.remove_path(caminho)
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

        for f in files:
            if f.endswith((".pyc", ".pyo", ".log")):
                caminho = os.path.join(root, f)
                removidos.append((f[-4:], caminho))
                if not modo_teste:
                    try:
                        fs.remove_path(caminho)
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

    if not removidos:
        console.print("[green]✅ Nada para limpar.")
        logar("Sem resíduos a remover.", projeto_path, tipo="limpeza")
        return

    tabela = Table(title="🧽 Arquivos e pastas removidos", show_lines=True)
    tabela.add_column("Tipo", style="bold")
    tabela.add_column("Caminho", style="dim")

    for tipo, caminho in removidos:
        tabela.add_row(tipo, caminho)

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


def mostrar_ultimo_log(projeto_path, tipo="limpeza"):
    safe_name = projeto_path.replace(os.sep, "_")
    padrao = f"logs/{tipo}_log_{safe_name}_*.txt"
    arquivos = sorted(glob(padrao), reverse=True)
    if not arquivos:
        console.print(f"[red]Nenhum log encontrado para:[/] {projeto_path}")
        return

    ultimo = arquivos[0]
    console.rule(f"📜 Último log de {tipo}")
    conteudo = fs.read_text(ultimo, default="")
    console.print(Markdown(conteudo))


def arquivar_logs_antigos(dias):
    """Move arquivos .log antigos para a pasta ``logs_arquivados``."""

    destino = os.path.join(LOG_DIR, "logs_arquivados")
    os.makedirs(destino, exist_ok=True)
    limite = time.time() - dias * 86400

    for arquivo in glob(os.path.join(LOG_DIR, "*.log")):
        if os.path.getmtime(arquivo) < limite:
            try:
                shutil.move(arquivo, os.path.join(destino, os.path.basename(arquivo)))
                console.print(f"[blue]Arquivo arquivado:[/] {arquivo}")
            except Exception as e:
                console.print(f"[red]Erro ao arquivar {arquivo}: {e}")
                logar(
                    f"Erro ao arquivar {arquivo}: {e}",
                    "logs",
                    tipo="limpeza",
                    nivel="ERROR",
                )

