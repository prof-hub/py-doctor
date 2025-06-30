
    with log_local_path.open("w", encoding="utf-8") as f:
        f.write(conteudo)

def mostrar_ultimo_log(caminho_projeto: Path, tipo: str = "diagnostico"):
    """Exibe o último log de um tipo específico salvo no diretório do projeto."""
    log_path = caminho_projeto / f".pydoctor_{tipo}.log"
    if not log_path.exists():
        console.print(f"[red]Nenhum log do tipo '{tipo}' encontrado em {caminho_projeto.name}[/red]")
        return
