# ~/schizoproto/src/schizoproto/core/protocol/registration/methods.py
"""
Protocol registration mechanisms for schizo://

This module provides utilities to register the schizo:// protocol
with browsers and operating systems.
"""
from __future__ import annotations
from re import L
import os, sys, json, platform, typing as t

from schizoproto.core.protocol.registration.common import HTML, JS, SHELL, MANIFEST

def detect() -> str:
    return platform.system().lower()


def browserjs() -> str:
    """
    Get JavaScript code to register the protocol in a browser context.

    Returns:
        str: JavaScript code for protocol registration
    """


    return JS.REGISTER


def systemcommand() -> t.Optional[str]:
    """
    Get the appropriate system command to register the protocol.

    Returns:
        Optional[str]: Shell command to register the protocol or None if not supported
    """
    platform = detect()
    return SHELL.Match(platform)

def browserextensionmanifest() -> t.Dict:
    """
    Generate a Chrome/Firefox extension manifest.json content.

    Returns:
        Dict: Extension manifest structure
    """
    return MANIFEST.BROWSEREXTENSION


def browserextensionjs() -> t.Dict[str, str]:
    """
    Generate JavaScript files for a browser extension.

    Returns:
        Dict[str, str]: Mapping of filename to JS content
    """
    return {
        'background.js': JS.EXTENSIONS.BACKGROUND,
        'content.js': JS.EXTENSIONS.CONTENT,
        'handler.js': JS.EXTENSIONS.HANDLER
    }


def creatextensionfiles(directory: str) -> t.List[str]:
    """
    Create all necessary files for a browser extension.

    Args:
        directory: Path to create the extension files

    Returns:
        List[str]: List of created file paths
    """
    os.makedirs(directory, exist_ok=True)

    manifestpath = os.path.join(directory, 'manifest.json')
    with open (manifestpath, 'w') as f:
        json.dump(browserextensionmanifest(), f, indent=2)

    jsfiles = browserextensionjs()
    createdfiles = [manifestpath]

    for filename, content in jsfiles.items():
        filepath = os.path.join(directory, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        createdfiles.append(filepath)

    handlerpath = os.path.join(directory, 'handler.html')
    popuppath = os.path.join(directory, 'popup.html')
    with open(handlerpath, 'w') as f:
        f.write(HTML.HANDLER)
    createdfiles.append(handlerpath)
    with open(popuppath, 'w') as f:
        f.write(HTML.POPUP)
    createdfiles.append(popuppath)

    return createdfiles
