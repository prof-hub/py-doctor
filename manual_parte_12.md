                return workspace
        except (configparser.Error, KeyError):
            console.print(f"[yellow]⚠️  Aviso: O arquivo '{CONFIG_FILE}' está corrompido ou mal formatado.[/yellow]")

    console.print(Panel(
        f"[bold yellow]Arquivo '{CONFIG_FILE}' não encontrado ou inválido.[/bold yellow]\n\nPor favor, forneça o caminho para a sua pasta de projetos (workspace).",
        title="[cyan]Configuração Necessária[/cyan]",
        border_style="yellow",
    ))

