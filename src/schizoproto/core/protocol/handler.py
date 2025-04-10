# ~/schizoproto/src/schizoproto/core/protocol/handler.py
"""
schizo:// protocol core handler.

This module defines the foundational functionality for the schizo:// URI protocol.
It handles protocol recognition, URI parsing, and dispatching to appropriate handlers.
"""

from __future__ import annotations
import re, urllib.parse, typing as t

PREFIX = "schizo://"

class DEFAULT:
    ENDPOINT = "default"



class SchizoParse:
    """
    Parsed schizo:// URI container.
    Holds the components of a parsed URI for easy access.
    """
    def __init__(
        self,
        raw: str,
        endpoint: str,
        params: Dict[str, str],
        fragment: str = ""
    ):
        self.raw = raw
        self.endpoint = endpoint
        self.params = params
        self.fragment = fragment

    def __repr__(self) -> str:
        return f"SchizoParse(endpoint='{self.endpoint}', params={self.params})"


def isprada(uri: str) -> bool:
    """
    Check if a URI string uses the schizo:// protocol.

    Args:
        uri: The URI string to check

    Returns:
        bool: True if the URI uses the schizo:// protocol
    """
    return uri.lower().startswith(PREFIX)



def parse(uri: str) -> t.Optional[SchizoParse]:
    """
    Parse a schizo:// URI into its components.

    Args:
        uri: The URI string to parse

    Returns:
        SchizoParse: Parsed URI object or None if invalid
    """
    raise NotImplementedError


def register(endpoint: str, handler: t.Callable) -> None:
    """
    Register a handler function for a specific endpoint.

    Args:
        endpoint: The endpoint name to register
        handler: Function to handle requests to this endpoint
    """
    raise NotImplementedError

def handle(uri: str, **context) -> t.Any:
    """
    Process a schizo:// URI through the appropriate handler.

    Args:
        uri: The URI to process
        **context: Additional context for handlers

    Returns:
        Any: Result from the handler function
    """
    raise NotImplementedError
