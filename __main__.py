# py-doctor/__main__.py

import os
import sys
import datetime
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# Ajuste de path para execução direta (caso rodando fora de pacotes instalados)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from py_doctor.checker import diagnosticar_projeto
from py_doctor.cleaner import limpar_pycache
from py_doctor.utils import obter_workspace, LOG_DIR, garantir_logs

console = Console()

# Início do log de execução
garantir_logs()
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = os.path.join(LOG_DIR, f"exec_log_{timestamp}.txt")
log_file = open(log_path, "w", encoding="utf-8")


def registrar_log(texto):
    log_file.write(f"{datetime.datetime.now().isoformat()} - {texto}\n")
    log_file.flush()


def listar_projetos(workspace):
    pasta_python = os.path.join(workspace, "python")
    console.print(f"\n[cyan]🔍 Procurando projetos em:[/] {pasta_python}\n")
    registrar_log(f"Verificando subpastas diretas em: {pasta_python}")

    if not os.path.isdir(pasta_python):
        console.print(
            f"[red]❌ Subdiretório 'python/' não encontrado dentro do workspace.[/]"
        )
        registrar_log("Subdiretório 'python/' não encontrado.")
        return []

    projetos = []
    for nome in sorted(os.listdir(pasta_python)):
        caminho = os.path.join(pasta_python, nome)
        if not os.path.isdir(caminho):
            continue
        arquivos = os.listdir(caminho)
        if any(f.endswith(".py") for f in arquivos) or "requirements.txt" in arquivos:
            projetos.append(caminho)

    registrar_log(f"Projetos encontrados: {len(projetos)}")
    return projetos


def exibir_tabela_projetos(projetos):
    table = Table(title="Projetos Python Detectados", show_lines=True)
    table.add_column("ID", style="bold green", justify="right")
    table.add_column("Caminho", style="cyan")

    for i, caminho in enumerate(projetos, start=1):
        table.add_row(str(i), caminho)

    console.print(table)


def menu_acao(projeto):
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
    console.print(
        "\n[bold magenta]===[/] [bold white]🛠 Py-Doctor: Diagnóstico de Projetos Python[/] [bold magenta]===\n[/]"
    )

    workspace = obter_workspace()
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
        log_file.close()

