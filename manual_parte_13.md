    while True:
        path_str = Prompt.ask("[bold]📂 Digite o caminho do workspace[/bold]")
        if not path_str:
            console.print("[red]❌ O caminho não pode ser vazio. Tente novamente.[/red]")
            continue
        
        workspace = Path(path_str).expanduser().resolve()
        if workspace.is_dir():
            console.print(f"✅ [green]Workspace definido como:[/green] {workspace}")
            _criar_config_padrao(workspace)
