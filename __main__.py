# py-doctor/__main__.py

"""Command line interface for Py-Doctor.

This module exposes the interactive menus used to diagnose and clean Python
projects. It can also be executed directly as ``python -m py_doctor``.
"""

import os
import sys

# Ajuste de path para execução direta (caso rodando fora de pacotes instalados)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import datetime
import argparse
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

import py_doctor.filesystem as fs
from py_doctor.utils import (
    LOG_DIR,
    garantir_logs,
    obter_workspace,
    DEFAULT_CONFIG_CREATED,
    CONFIG_FILE,
)

from py_doctor.checker import diagnosticar_projeto
from py_doctor.cleaner import limpar_pycache


console = Console()

# Arquivo de log principal aberto durante a execução
LOG_FILE = None


def abrir_log_file():
    """Cria e abre o arquivo de log de execução."""

    garantir_logs()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(LOG_DIR, f"exec_log_{timestamp}.txt")
    return open(log_path, "w", encoding="utf-8")


def registrar_log(texto):
    """Grava uma mensagem no arquivo de log principal.

    Args:
        texto (str): Conteúdo a ser registrado.

    Returns:
        None
    """

    if LOG_FILE:
        LOG_FILE.write(f"{datetime.datetime.now().isoformat()} - {texto}\n")
        LOG_FILE.flush()


def listar_projetos(workspace, subdir="python"):
    """Varre o diretório informado em busca de subprojetos Python.

    Args:
        workspace (str): Caminho base onde os projetos residem.

    Returns:
        list[str]: Lista de caminhos para projetos encontrados.
    """

    pasta_python = os.path.join(workspace, subdir)
    console.print(f"\n[cyan]🔍 Procurando projetos em:[/] {pasta_python}\n")
    registrar_log(f"Verificando subpastas diretas em: {pasta_python}")

    if not os.path.isdir(pasta_python):
        console.print(
            f"[red]❌ Subdiretório '{subdir}/' não encontrado dentro do workspace.[/]"
        )
        registrar_log(f"Subdiretório '{subdir}/' não encontrado.")
        return []

    projetos = []
    for nome in sorted(fs.list_dir(pasta_python)):
        caminho = os.path.join(pasta_python, nome)
        if not os.path.isdir(caminho):
            continue
        arquivos = fs.list_dir(caminho)
        if any(f.endswith(".py") for f in arquivos) or "requirements.txt" in arquivos:
            projetos.append(caminho)

    registrar_log(f"Projetos encontrados: {len(projetos)}")
    return projetos


def exibir_tabela_projetos(projetos):
    """Exibe em formato de tabela os projetos detectados.

    Args:
        projetos (Iterable[str]): Caminhos para projetos a serem mostrados.

    Returns:
        None
    """

    table = Table(title="Projetos Python Detectados", show_lines=True)
    table.add_column("ID", style="bold green", justify="right")
    table.add_column("Caminho", style="cyan")

    for i, caminho in enumerate(projetos, start=1):
        table.add_row(str(i), caminho)

    console.print(table)


def menu_acao(projeto):
    """Menu de ações para um projeto específico.

    Apresenta opções de diagnóstico e limpeza para ``projeto``.

    Args:
        projeto (str): Caminho do projeto em questão.

    Returns:
        None
    """

    while True:
        console.print(Panel(f"🎯 [bold]Ações para:[/] [yellow]{projeto}[/]"))
        console.print("[bold green][1][/]: Diagnosticar ambiente")
        console.print("[bold green][2][/]: Limpar resíduos (__pycache__, .pyc, .log)")
        console.print("[bold red][0][/]: Voltar")

        escolha = Prompt.ask("Escolha uma ação", choices=["1", "2", "0"])
        registrar_log(f"Ação escolhida para {projeto}: {escolha}")
        if escolha == "1":
            diagnosticar_projeto(projeto)
        elif escolha == "2":
            limpar_pycache(projeto)
        elif escolha == "0":
            registrar_log(f"Retornando do projeto: {projeto}")
            break


def menu():
    """Menu principal da aplicação.

    Returns:
        None
    """

    console.print(
        "\n[bold magenta]===[/] [bold white]🛠 Py-Doctor: Diagnóstico de Projetos Python[/] [bold magenta]===\n[/]"
    )

    workspace = obter_workspace()
    if DEFAULT_CONFIG_CREATED:
        console.print(
            f"[yellow]⚠️ Arquivo de configuração '{CONFIG_FILE}' criado com valores padrão.[/]"
        )
    console.print(f"[dim]ℹ️ Usando configuração de workspace: {workspace}[/]")
    registrar_log(f"Workspace carregado: {workspace}")

    if not os.path.isdir(workspace):
        console.print(f"[red]❌ Diretório de workspace não encontrado:[/] {workspace}")
        registrar_log(f"Workspace não encontrado: {workspace}")
        return

    projetos = listar_projetos(workspace)
    if not projetos:
        console.print("[red]❌ Nenhum projeto Python encontrado.[/]")
        registrar_log("Nenhum projeto encontrado.")
        return

    exibir_tabela_projetos(projetos)
    console.print("[bold red][0][/]: Sair")

    escolha = Prompt.ask(
        "\nEscolha um projeto", choices=[str(i) for i in range(len(projetos) + 1)]
    )
    registrar_log(f"Projeto selecionado: {escolha}")

    if escolha == "0":
        console.print("[blue]Até mais, Capitão![/]")
        registrar_log("Saída do programa pelo menu principal.")
        return

    idx = int(escolha) - 1
    if 0 <= idx < len(projetos):
        menu_acao(projetos[idx])
    else:
        console.print("[red]❌ Escolha inválida.[/]")
        registrar_log("Escolha inválida no menu principal.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Py-Doctor CLI")
    sub = parser.add_subparsers(dest="comando")

    p_diag = sub.add_parser("diagnosticar", help="Rodar diagnóstico do projeto")
    p_diag.add_argument("caminho", help="Caminho para o projeto")

    p_limpar = sub.add_parser("limpar", help="Limpar resíduos do projeto")
    p_limpar.add_argument("caminho", help="Caminho para o projeto")

    args = parser.parse_args()

    LOG_FILE = abrir_log_file()
    try:
        registrar_log("--- INÍCIO DA EXECUÇÃO DO PY-DOCTOR ---")
        if args.comando == "diagnosticar":
            diagnosticar_projeto(args.caminho)
        elif args.comando == "limpar":
            limpar_pycache(args.caminho)
        else:
            menu()
    finally:
        registrar_log("--- FIM DA EXECUÇÃO ---")
        if LOG_FILE:
            LOG_FILE.close()

