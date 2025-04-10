# ~/schizoproto/src/schizoproto/core/protocol/globals.py
"""
Globally shared components
"""
from __future__ import annotations
import typing as t

_handlers: t.Dict[str, t.Callable] = {}

PREFIX: str = "schizo://"

class DEFAULT:
    ENDPOINT: str = "default"
