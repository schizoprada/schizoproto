# ~/schizoproto/src/schizoproto/core/protocol/registration/methods.py
"""
Protocol registration mechanisms for schizo://

This module provides utilities to register the schizo:// protocol
with browsers and operating systems.
"""
from __future__ import annotations
from re import L
import os, sys, platform, typing as t

def detect() -> str:
    return platform.system().lower()


def browserjs() -> str:
    """
    Get JavaScript code to register the protocol in a browser context.

    Returns:
        str: JavaScript code for protocol registration
    """

    """
        try {
            // Modern approach for PWAs and extensions
            if (navigator.registerProtocolHandler) {
                navigator.registerProtocolHandler(
                    'schizo',
                    window.location.origin + '/handler?uri=%s',
                    'Schizo Protocol Handler'
                );
                console.log('Registered schizo:// protocol handler');
            } else {
                console.warn('This browser does not support protocol registration');
            }
        } catch (e) {
            console.error('Failed to register protocol:', e);
        }
    """
    raise NotImplementedError


def systemcommand() -> t.Optional[str]:
    """
    Get the appropriate system command to register the protocol.

    Returns:
        Optional[str]: Shell command to register the protocol or None if not supported
    """
    raise NotImplementedError

def browserextensionmanifest() -> t.Dict:
    """
    Generate a Chrome/Firefox extension manifest.json content.

    Returns:
        Dict: Extension manifest structure
    """
    raise NotImplementedError


def browserextensionjs() -> t.Dict[str, str]:
    """
    Generate JavaScript files for a browser extension.

    Returns:
        Dict[str, str]: Mapping of filename to JS content
    """
    raise NotImplementedError


def creatextensionfiles(directory: str) -> t.List[str]:
    """
    Create all necessary files for a browser extension.

    Args:
        directory: Path to create the extension files

    Returns:
        List[str]: List of created file paths
    """
    raise NotImplementedError
