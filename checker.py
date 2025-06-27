# py-doctor/checker.py

"""Ferramentas de diagnóstico e verificação de dependências."""

import os
import subprocess
import time
import ast
from pathlib import Path
from rich.console import Console
from rich.table import Table

import py_doctor.filesystem as fs
from py_doctor.utils import (
    logar,
    mostrar_ultimo_log,
    load_requirements,
    esta_em_modo_teste,
)


console = Console()


def diagnosticar_projeto(caminho_projeto):
    """Menu interativo de diagnóstico para um projeto.

    Args:
        caminho_projeto (str): Caminho do projeto a ser analisado.

    Returns:
        None
    """
    caminho_projeto = Path(caminho_projeto)
    requeridos = load_requirements(caminho_projeto)

    while True:
        console.rule(f"[bold cyan]🔬 Diagnóstico: {caminho_projeto}")
        console.print("[1]: Verificar pacotes instalados com requirements.txt")
        console.print("[2]: Verificar consistência do requirements.txt com o código")
        console.print("[3]: Exibir último log de diagnóstico")
        console.print("[4]: Atualizar automaticamente o requirements.txt")
        console.print("[5]: Restaurar backup do requirements.txt")
        console.print("[0]: Voltar")
        escolha = console.input("Escolha uma opção [1/2/3/4/0]: ").strip()
        if escolha == "1":
            diagnostico_basico(caminho_projeto)
        elif escolha == "2":
            req_path = caminho_projeto / "requirements.txt"
            if req_path.exists():
                requeridos = load_requirements(caminho_projeto)
                verificar_consistencia_requirements(caminho_projeto, requeridos)
            else:
                console.print("[red]requirements.txt não encontrado.")
        elif escolha == "3":
            mostrar_ultimo_log(caminho_projeto, tipo="diagnostico")
        elif escolha == "4":
            atualizar_requirements(caminho_projeto)
            requeridos = load_requirements(caminho_projeto)
        elif escolha == "5":
            restaurar_backup_requirements(caminho_projeto)
            requeridos = load_requirements(caminho_projeto)
        else:
            break

def restaurar_backup_requirements(projeto_path):
    """Restaura o ``requirements.txt`` a partir de um backup.

    Args:
        projeto_path (str): Caminho do projeto alvo.

    Returns:
        None
    """
    projeto_path = Path(projeto_path)
    req_path = projeto_path / "requirements.txt"
    backup = Path(str(req_path) + ".bak")
    if not backup.exists():
        console.print("[red]❌ Nenhum backup encontrado para restaurar.")
        return
    try:
        confirm = (
            console.input(
                "[yellow]Tem certeza que deseja restaurar o backup? Isso sobrescreverá o requirements.txt atual. (s/n): "
            )
            .strip()
            .lower()
        )
        if confirm != "s":
            console.print("[cyan]🛑 Restauração cancelada pelo usuário.")
            return
        backup.replace(req_path)
        console.print(
            f"[green]✔ requirements.txt restaurado com sucesso a partir de {backup}"
        )
    except Exception as e:
        console.print(f"[red]Erro ao restaurar backup: {e}")


def diagnostico_basico(caminho_projeto):
    """Verifica se as dependências declaradas estão instaladas.

    Args:
        caminho_projeto (str): Caminho do projeto.

    Returns:
        None
    """
    caminho_projeto = Path(caminho_projeto)
    req_path = caminho_projeto / "requirements.txt"
    modo_teste = esta_em_modo_teste()
    requeridos = load_requirements(caminho_projeto)
    log = f"Diagnóstico do projeto: {caminho_projeto}\n"
    inicio = time.time()

    if not req_path.exists():
        msg = "[red]❌ Nenhum requirements.txt encontrado.[/]"
        console.print(msg)
        log += "Requisitos não encontrados."
        logar(log, caminho_projeto, tipo="diagnostico")
        return
      

    console.print(
        f"📄 {len(requeridos)} dependência(s) declarada(s) em requirements.txt"
    )
    log += f"Dependências declaradas:\n" + "\n".join(requeridos) + "\n"

    resultado = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, text=True)
    instalados = {
        linha.split("==")[0].lower(): linha
        for linha in resultado.stdout.strip().split("\n")
        if "==" in linha
    }

    faltando = []
    table = Table(title="⚠️ Dependências Faltando ou Incompatíveis", show_lines=True)
    table.add_column("Nome")
    table.add_column("Esperado")
    table.add_column("Instalado")

    for req in requeridos:
        nome = req.split("==")[0].lower().split()[0]
        if nome not in instalados:
            faltando.append(req)
            table.add_row(nome, req, "❌ não encontrado")

    if faltando:
        console.print(table)
        log += f"Faltando:\n" + "\n".join(faltando) + "\n"
        if modo_teste:
            console.print(
                "[yellow]🔒 Modo de teste ativo — nenhuma instalação será feita."
            )
            log += "Modo teste ativo — instalação não executada."
        else:
            console.print("[green]Deseja instalar os pacotes?")
            console.print("[bold green]1[/]: Instalar apenas faltantes")
            console.print("[bold green]2[/]: Instalar todos do requirements.txt")
            console.print("[bold red]0[/]: Cancelar")
            inst = console.input("Escolha uma opção [1/2/0]: ").strip()
            if inst == "1":
                console.print("⬇️ Instalando apenas os pacotes faltantes...")
                resultado = subprocess.call(["pip", "install"] + faltando)
                log += (
                    "Instalado com pip install individual:"
                    + "".join(faltando)
                    + f"Código de saída: {resultado}"
                )
            elif inst == "2":
                console.print("⬇️ Instalando com requirements.txt completo...")
                resultado = subprocess.call(["pip", "install", "-r", str(req_path)])
                log += f"Instalado com pip install -r requirements.txt Código de saída: {resultado}"
            else:
                console.print("[yellow]Instalação cancelada.")
                log += "Usuário optou por não instalar."
    else:
        console.print("[green]✅ Todas as dependências estão presentes.")
        log += "Nenhum pacote faltando."

    duracao = time.time() - inicio
    log += f"Duração do diagnóstico: {duracao:.2f}s"
    logar(log, caminho_projeto, tipo="diagnostico")


def verificar_consistencia_requirements(projeto_path, requeridos):
    """Compara pacotes usados no código com o ``requirements.txt``.

    Args:
        projeto_path (str): Diretório do projeto.
        requeridos (list[str]): Lista de dependências declaradas.

    Returns:
        None
    """
    console.rule("[bold magenta]📊 Verificando consistência do requirements.txt")
    projeto_path = Path(projeto_path)
    requeridos_mod = set([r.split("==")[0].split("@")[0].lower() for r in requeridos])
    usados = set()
    for root, _, files in os.walk(projeto_path):
        for f in files:
            if f.endswith(".py"):
                caminho = Path(root) / f
                try:
                    codigo = fs.read_text(caminho, default="")
                    tree = ast.parse(codigo, filename=str(caminho))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                usados.add(alias.name.split(".")[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                usados.add(node.module.split(".")[0])
                except Exception as e:
                    console.print(f"[yellow]Aviso: erro ao analisar {caminho}: {e}")
    usados = sorted(usados)
    faltando = [
        u for u in usados if u.lower() not in requeridos_mod and not u.startswith("__")
    ]
    extras = [r for r in requeridos_mod if r not in usados]

    if faltando:
        console.print("[red]🔍 Módulos usados mas ausentes no requirements.txt:")
        for m in faltando:
            console.print(f"  - {m}")
    else:
        console.print("[green]✅ Todos os módulos usados estão listados.")

    if extras:
        console.print("[yellow]🧹 Pacotes listados mas não utilizados no código:")
        for m in extras:
            console.print(f"  - {m}")
    else:
        console.print(
            "[green]✅ Nenhum pacote aparentemente desnecessário no requirements.txt"
        )


def atualizar_requirements(projeto_path):
    """Atualiza ``requirements.txt`` adicionando e removendo pacotes.

    Args:
        projeto_path (str): Caminho do projeto.

    Returns:
        None
    """
    projeto_path = Path(projeto_path)
    req_path = projeto_path / "requirements.txt"
    modo_teste = esta_em_modo_teste()
    requeridos = load_requirements(projeto_path)
    if not req_path.exists():
        console.print("[red]❌ requirements.txt não encontrado.")
        return

    requeridos_mod = set([r.split("==")[0].split("@")[0].lower() for r in requeridos])
    usados = set()
    for root, _, files in os.walk(projeto_path):
        for f in files:
            if f.endswith(".py"):
                caminho = Path(root) / f
                try:
                    codigo = fs.read_text(caminho, default="")
                    tree = ast.parse(codigo, filename=str(caminho))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                usados.add(alias.name.split(".")[0])
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                usados.add(node.module.split(".")[0])
                except Exception as e:
                    console.print(f"[yellow]Aviso: erro ao analisar {caminho}: {e}")

    usados = sorted(usados)
    faltando = [
        u for u in usados if u.lower() not in requeridos_mod and not u.startswith("__")
    ]
    extras = [
        r for r in requeridos if r.split("==")[0].split("@")[0].lower() not in usados
    ]

    novo_req = [r for r in requeridos if r not in extras]
    novo_req += [f"{m}" for m in faltando if m not in novo_req]

    if not modo_teste:
        backup = Path(str(req_path) + ".bak")
        req_path.rename(backup)
        fs.write_text(req_path, "\n".join(novo_req) + "\n")
        console.print(
            f"[green]✔ requirements.txt atualizado com sucesso. Backup salvo como: {backup}"
        )
    else:
        console.print("[yellow]🔒 Modo de teste ativo — nenhuma modificação foi feita.")
        console.print("📋 Novo conteúdo sugerido para requirements.txt:")
        for r in novo_req:
            console.print("  - " + r)

    log_text = "Atualização automática de requirements.txt:"
    log_text += f"Pacotes adicionados: {faltando}"
    log_text += f"Pacotes removidos: {extras}"
    log_text += f"Modo de teste: {modo_teste}"
    logar(log_text, projeto_path, tipo="diagnostico")
