# ~/schizoproto/src/schizoproto/core/render/engine.py
"""
schizo:// render engine.

This module handles the rendering and mutation of content for the schizo:// protocol.
It provides utilities for manipulating DOM and text content to create the
"drift" and "hallucination" effects that are central to the protocol.
"""
from __future__ import annotations
import re, abc, random, typing as t, dataclasses as dc

@dc.dataclass
class RenderOptions:
    """Options for content rendering and mutation."""
    drift: float
    corruption: float
    options: t.Sequence[t.Any]



class Mutator(abc.ABC):
    """Abstract base class for all things mutation."""



    @abc.abstractmethod
    def shouldmutate(self) -> bool:
        """should it"""
        pass
