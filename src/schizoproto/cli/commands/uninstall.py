# ~/schizoproto/src/schizoproto/cli/commands/uninstall.py
"""
Uninstall command for schizoproto.
"""
import sys, typer, questionary, typing as t

from schizoproto.logs import log
from schizoproto.config import DEVMODE
from schizoproto.internals.uninstall import run, unregister, cleanpersistentdata

app = typer.Typer(
    name="uninstall",
    help="Uninstall schizoproto protocol (DEVELOPMENT ONLY)"
)


@app.callback(invoke_without_command=True)
def uninstallcmd(
    ctx: typer.Context,
    force: bool = typer.Option(False, "--force", "-f", help="Force uninstall even in production mode"),
    onlyproto: bool = typer.Option(False, "--protocol-only", "-p", help="Only unregister protocol"),
    onlydata: bool = typer.Option(False, "--data-only", "-d", help="Only clean persistent data"),
):
    if not DEVMODE and not force:
        typer.echo("❌ Uninstall aborted: Not in development mode")
        typer.echo("Use --force to override (not recommended)")
        sys.exit(1)

    if (not any((onlyproto, onlydata))) and (not force):
        confirm = questionary.confirm(
            "This will uninstall schizoproto completely. Are you sure?",
            default=False
        ).ask()

        if not confirm:
            typer.echo("Uninstall cancelled")
            sys.exit(0)

    typer.echo("🛑 Uninstalling schizoproto...")

    success = True

    if onlyproto:
        success = unregister.protocol()
        if success:
            typer.echo("✅ Protocol unregistration successful")
        else:
            typer.echo("⚠️ Protocol unregistration failed or partially succeeded")

    elif onlydata:
        success = cleanpersistentdata()
        if success:
            typer.echo("✅ Data cleanup successful")
        else:
            typer.echo("⚠️ Data cleanup failed or partially succeeded")

    else:
        success = run(force=force)
        if success:
            typer.echo("✅ Uninstall completed successfully")
        else:
            typer.echo("⚠️ Uninstall completed with issues")

    if success:
        typer.echo("\nℹ️ Additional Manual Steps:")
        typer.echo("  - Check browser extensions and remove if installed")
        typer.echo("  - Clear browser local storage if needed")

    sys.exit(0 if success else 1)
