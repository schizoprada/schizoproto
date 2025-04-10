# ~/schizoproto/src/schizoproto/core/render/base.py
"""
Abstract base classes for the schizo:// render system.

This module defines the core interfaces and abstract base classes
that form the foundation of the render module.
"""
from __future__ import annotations
import abc, typing as t
from datetime import datetime

from schizoproto.core.render.types import (
    MutationType, ContentType, MutationMood,
    RenderOptions, MutationHistory, UserState,
    MutationContext, MutationResult
)

class Mutator(abc.ABC):
    """Abstract base class for content mutation."""

    def __init__(self, options: RenderOptions, **kwargs):
        self.options = options
        self.history: MutationHistory = MutationHistory()
        self.mutationtype: MutationType = MutationType.TEXTSWAP # override in subclasses

    @abc.abstractmethod
    def shouldmutate(self, context: MutationContext) -> bool:
        """
        Determine if mutation should occur based on context and options.

        Args:
            context: Contextual information for the mutation decision

        Returns:
            bool: True if mutation should be applied
        """
        pass


    @abc.abstractmethod
    def mutate(self, content: t.Any, context: MutationContext) -> t.Any:
        """
        Apply mutation to the content.

        Args:
            content: The content to mutate
            context: Contextual information for the mutation

        Returns:
            Any: The mutated content
        """
        pass

    def recordmutation(self, original: t.Any, result: t.Any, details: t.Optional[t.Dict[str, t.Any]] = None) -> MutationResult:
        """
        Record a mutation for future reference.

        Args:
            original: Original content before mutation
            result: Content after mutation
            details: Additional details about the mutation

        Returns:
            MutationResult: Record of the mutation
        """
        mutdetails = (details or {})

        # Create the mutation result
        mutation = MutationResult(
            original=original,
            result=result,
            mutationtype=self.mutationtype,
            details=mutdetails
        )

        # Add to history
        self.history.add(
            mutationtype=self.mutationtype.value,
            details={
                "result_sample": str(result)[:100] if isinstance(result, str) else "non-string",
                **mutdetails
            }
        )

        return mutation


class ContentTarget(abc.ABC):
    """
    Specifies which parts of content should be affected by mutations.
    Handles selection and replacement of content elements.
    """
    def __init__(self, options: RenderOptions) -> None:
        self.options = options

    @abc.abstractmethod
    def select(self, content: t.Any, context: MutationContext) -> t.List[t.Tuple[t.Any, t.Any]]:
        """
        Select targetable elements from content.

        Args:
            content: The content to select elements from
            context: Contextual information for selection

        Returns:
            List[Tuple[Any, Any]]: List of (selector, element) pairs
        """
        pass

    @abc.abstractmethod
    def replace(self, content: t.Any, replacements: t.List[t.Tuple[t.Any, t.Any]], context: MutationContext) -> t.Any:
        """
        Replace targeted elements with their mutated versions.

        Args:
            content: The original content
            replacements: List of (selector, replacement) pairs
            context: Contextual information for replacement

        Returns:
            Any: The content with replacements applied
        """
        pass


class MutationStrategy(abc.ABC):
    """
    Defines a high-level strategy for mutation.
    Combines multiple mutators and targets to achieve a specific effect.
    """

    def __init__(self, options: RenderOptions):
        self.options = options
        self.mutators: t.List[Mutator] = []
        self.targets: t.Dict[ContentType, ContentTarget] = {}

    @abc.abstractmethod
    def apply(self, content: t.Any, context: MutationContext) -> t.Any:
        """
        Apply the mutation strategy to content.

        Args:
            content: The content to mutate
            context: Contextual information for mutation

        Returns:
            Any: The mutated content
        """
        pass


class RenderListener(abc.ABC):
    """
    Listener for render events.
    Can be used to hook into the rendering process.
    """

    @abc.abstractmethod
    def onrenderstart(self, content: t.Any, context: MutationContext) -> None:
        """Called when rendering begins."""
        pass

    @abc.abstractmethod
    def onrenderend(self, original: t.Any, result: t.Any, context: MutationContext) -> None:
        """Called when rendering completes."""
        pass

    @abc.abstractmethod
    def onmutation(self, mutation: MutationResult) -> None:
        """Called when a mutation is applied."""
        pass
