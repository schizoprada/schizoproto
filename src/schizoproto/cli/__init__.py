# ~/schizoproto/src/schizoproto/cli/__init__.py
"""
Command-line interface for schizoproto.
"""
import sys, importlib, typer, typing as t

from schizoproto.logs import log
from schizoproto.config import DEVMODE


app = typer.Typer(
    name="schizoproto",
    help="A parasitic transport protocol for drift-based systems and behavioral hauntings"
)

try:
    from schizoproto.cli.commands import uninstall
    if DEVMODE:
        app.add_typer(uninstall.app, name="uninstall")
except ImportError as e:
    if DEVMODE:
        log.error(f"Failed to import command: {str(e)}")


def main():
    """Main entry point for the CLI"""
    try:
        app()
    except Exception as e:
        log.error(f"CLI error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
