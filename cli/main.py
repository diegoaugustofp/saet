"""Ponto de entrada da CLI do SAET.

Requisito: SYS-NFR-040 (interface CLI na primeira versao).
"""


import typer


from saet import __version__
app = typer.Typer(
    name="saet",
    help="SAET - Sistema de Automacao de Estrategias de Trading",
    add_completion=False,
)


@app.callback()
def main(
    version: bool = typer.Option(False, "--version", "-v", help="Exibe a versao do SAET."),
) -> None:
    """SAET - Sistema de Automacao de Estrategias de Trading."""
    if version:
        typer.echo(f"SAET versao {__version__}")
        raise typer.Exit()


@app.command()
def server(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host do servidor API."),
    port: int = typer.Option(8000, "--port", "-p", help="Porta do servidor API."),
    reload: bool = typer.Option(False, "--reload", "-r", help="Habilitar auto-reload."),
) -> None:
    """Inicia o servidor API do SAET."""
    import uvicorn
    typer.echo(f"Iniciando SAET API em {host}:{port}...")
    uvicorn.run(
        "saet.api.app:create_app",
        host=host,
        port=port,
        reload=reload,
        factory=True,
    )


@app.command()
def status() -> None:
    """Exibe o status atual do sistema."""
    typer.echo("SAET Status")
    typer.echo(f"  Versao: {__version__}")
    typer.echo("  Ambiente: nao configurado")
    typer.echo("  Scheduler: parado")
    typer.echo("  Conexao MT5: desconectado")


if __name__ == "__main__":
    app()