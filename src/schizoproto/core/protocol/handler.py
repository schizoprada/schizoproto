# ~/schizoproto/src/schizoproto/core/protocol/handler.py
"""
schizo:// protocol core handler.

This module defines the foundational functionality for the schizo:// URI protocol.
It handles protocol recognition, URI parsing, and dispatching to appropriate handlers.
"""

from __future__ import annotations
import re, urllib.parse, typing as t

from schizoproto.core.protocol.globals import _handlers, PREFIX, DEFAULT

class SchizoParse:
    """
    Parsed schizo:// URI container.
    Holds the components of a parsed URI for easy access.
    """
    def __init__(
        self,
        raw: str,
        endpoint: str,
        params: t.Dict[str, str],
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
    if not isprada(uri):
        return None

    path = uri[len(PREFIX):]

    endpointpart, querypart = path.split('?', 1) if ('?' in path) else (path, "")

    fragment = ""
    if ('#' in endpointpart):
        endpointpart, fragment = endpointpart.split('#', 1)
    elif ('#' in querypart):
        querypart, fragment = querypart.split('#', 1)

    endpoint = (endpointpart.strip() or DEFAULT.ENDPOINT)

    params = {}
    if querypart:
        queryparams = urllib.parse.parse_qs(querypart)
        params = {k:v[0] if (len(v) == 1) else v for k,v in queryparams.items()} # should update to handle lists

    return SchizoParse(
        uri, endpoint, params, fragment
    )


def register(endpoint: str, handler: t.Callable) -> None:
    """
    Register a handler function for a specific endpoint.

    Args:
        endpoint: The endpoint name to register
        handler: Function to handle requests to this endpoint
    """
    _handlers[endpoint] = handler

def handle(uri: str, **context) -> t.Any:
    """
    Process a schizo:// URI through the appropriate handler.

    Args:
        uri: The URI to process
        **context: Additional context for handlers

    Returns:
        Any: Result from the handler function
    """
    parsed = parse(uri)
    if not parsed:
        raise ValueError(f"Invalid schizo:// URI: {uri}")

    handler = _handlers.get(parsed.endpoint, _handlers.get(DEFAULT.ENDPOINT))
    if not handler:
        raise NotImplementedError(f"No handler for endpoint: {parsed.endpoint}")

    return handler(parsed, **context)


def _defaulthandler(parsed: SchizoParse, **context) -> t.Dict[str, t.Any]:
    """Default handler for testing the protocol."""
    return {
        "status": "processed",
        "endpoint": parsed.endpoint,
        "params": parsed.params,
        "message": "schizo:// protocol acknowledged"
    }

register(DEFAULT.ENDPOINT, _defaulthandler)
