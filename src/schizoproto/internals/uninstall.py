# ~/schizoproto/src/schizoproto/internals/uninstall.py
"""
Internal uninstall functionality for schizoproto.

This module provides functions to unregister the schizo:// protocol
and clean up any persistent data. It is strictly for development and
testing purposes and should not be included in distribution builds.

WARNING: This module will be excluded from distribution packages.
"""
from __future__ import annotations
import os, sys, shutil, platform, typing as t
from pathlib import Path

from schizoproto.logs import log
from schizoproto.config import DEVMODE, SCHIZOPROTODIR
from schizoproto.core.protocol.globals import PREFIX
from schizoproto.core.protocol.registration.common import SHELL
from schizoproto.core.protocol.registration.methods import detect


class unregister:
    """Unregister the protocol across various systems"""

    @staticmethod
    def _windows() -> bool:
        import winreg
        try:
            # Remove registry entries
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, "schizo\\shell\\open\\command")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, "schizo\\shell\\open")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, "schizo\\shell")
            winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, "schizo")
            return True
        except Exception as e:
            log.error(f"Failed to unregister Windows protocol: {str(e)}")
            return False

    @staticmethod
    def _macos() -> bool:
        try:
            os.system(
                "defaults delete com.apple.LaunchServices LSHandlers "
                "-dict-add LSHandlerURLScheme schizo"
            )
            return True
        except Exception as e:
            log.error(f"Failed to unregister MacOS protocol: {str(e)}")
            return False

    @staticmethod
    def _linux() -> bool:
        try:
            desktopfile = Path.home() / ".local/share/applications/schizoproto.desktop"
            if desktopfile.exists():
                os.remove(desktopfile)
            os.system("update-mime-database ~/.local/share/mime")
            return True
        except Exception as e:
            log.error(f"Failed to unregister Linux protocol: {str(e)}")
            return False

    @classmethod
    def protocol(cls) -> bool:
        platformsystem = detect()
        match platformsystem:
            case "windows":
                return cls._windows()
            case "darwin":
                return cls._macos()
            case "linux":
                return cls._linux()
            case _:
                log.error(f"Unsupported platform for unregistration: {platformsystem}")
                return False


def cleanpersistentdata() -> bool:
    try:
        if os.path.exists(SCHIZOPROTODIR):
            shutil.rmtree(SCHIZOPROTODIR)

        # Clean browser localStorage (for development mode)
        # This would require browser extension interaction, so we'll just log it
        log.info("Browser localStorage cleanup requires manual intervention")
        # at least log steps
        return True
    except Exception as e:
        log.error(f"Failed to clean persistent data: {str(e)}")
        return False


def run(force: bool = False) -> bool:
    """
    Run the complete uninstall process.

    Args:
        force: Force uninstallation even in production mode

    Returns:
        bool: True if successful, False otherwise
    """
    if (not DEVMODE) and (not force):
        log.error("Uninstall aborted: Not a development build")
        return False

    log.info(f"(schizoproto://) starting uninstall")

    unregistersuccess = unregister.protocol()
    if not unregistersuccess:
        log.warning(f"(schizoproto://) protocol unregistration failed or partially succeeded")

    datasuccess = cleanpersistentdata()
    if not datasuccess:
        log.warning("(schizoproto://) data cleanup failed or partially succeeded")

    status = "success" if (unregistersuccess and datasuccess) else ("partial success" if (datasuccess or unregistersuccess) else "failed")

    log.info(f"(schizo://) uninstall completed with status: {status}")
    return (unregistersuccess and datasuccess)
