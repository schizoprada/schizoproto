# ~/schizoproto/src/schizoproto/core/render/engine.py
"""
schizo:// render engine.

This module handles the rendering and mutation of content for the schizo:// protocol.
It provides utilities for manipulating DOM and text content to create the
"drift" and "hallucination" effects that are central to the protocol.
"""
from __future__ import annotations
import random, typing as t, dataclasses as dc
from datetime import datetime

from schizoproto.logs import log
from schizoproto.core.render.types import (
    MutationType, ContentType, MutationMood,
    RenderOptions, MutationHistory, UserState,
    MutationContext, MutationResult
)
from schizoproto.core.render.base import (
    Mutator, ContentTarget, MutationStrategy, RenderListener
)

@dc.dataclass
class EngineOptions:
    logic: t.Any = random # for use later


class RenderEngine:
    """
    Main engine that orchestrates the content mutation process.
    Applies appropriate mutations based on content type and context.
    """
    def __init__(self, options: t.Optional[RenderOptions] = None):
        """
        Initialize the render engine with options.

        Args:
            options: Configuration options for rendering
        """
        self.options = (options or RenderOptions())
        self.mutators: t.Dict[MutationType, t.List[Mutator]] = {}
        self.targets: t.Dict[ContentType, t.List[ContentTarget]] = {}
        self.strategies: t.List[MutationStrategy] = []
        self.listeners: t.List[RenderListener] = []
        self.history: MutationHistory = MutationHistory()

    def _resolvecontenttype(self, typeof: t.Union[str, ContentType]) -> ContentType:
        """Convert string content type to enum if needed."""
        if isinstance(typeof, str):
            try:
                return ContentType[typeof.upper()]
            except KeyError:
                log.warning(f"unknown content type ({typeof}), defaulting to TEXT")
                return ContentType.TEXT
        return typeof

    def _notifylisteners(self, event: str, original: t.Any, result: t.Any, context: MutationContext, mutation: t.Optional[MutationResult] = None) -> None:
        """Notify registered listeners about render events."""
        for listener in self.listeners:
            try:
                if event == 'start':
                    listener.onrenderstart(original, context)
                elif event == 'end':
                    listener.onrenderend(original, result, context)
                elif (event == 'mutation') and mutation:
                    listener.onmutation(mutation)
            except Exception as e:
                log.error(f"({event} listener) error: {str(e)}")

    def _shouldtriggerpievent(self) -> bool:
        """Determine if a π-event should be triggered based on probability."""
        return (random.random() < self.options.piprob)

    def _handlepievent(self, content: t.Any, context: MutationContext) -> t.Any:
        """Notify registered listeners about render events."""
        log.info(f"pi-day babyyyy")
        context.metadata['pievent'] = True

        mutators = self.mutators.get(MutationType.PIEVENT, [])
        if not mutators:
            return content

        mutator = random.choice(mutators)

        try:
            result = mutator.mutate(content, context)
            mutation = mutator.recordmutation(content, result, {"event": "pievent"})
            self.history.add(
                mutationtype=MutationType.PIEVENT.value,
                details={"pievent": True}
            )
            self._notifylisteners('mutation', content, result, context, mutation)
            return result
        except Exception as e:
            log.error(f"exception applying pi-event: {str(e)}")
            return content

    def _applystrategies(self, content: t.Any, context: MutationContext) -> t.Any:
        """Apply registered mutation strategies to content."""
        if not self.strategies:
            return content

        strategy = random.choice(self.strategies)
        try:
            result = strategy.apply(content, context)
            if (result != content):
                return result
        except Exception as e:
            log.error(f"error applying mutation strategy: {str(e)}")

        return content

    def _getactivemutationtypes(self) -> t.List[MutationType]:
        """Determine which mutation types are active based on drift."""
        return [
            mtype for mtype in self.options.mutables
            if random.random() < self.options.drift
        ]

    def _applyelementmutations(self,
        selectedelements: t.List[t.Tuple[t.Any, t.Any]],
        activemutationtypes: t.List[MutationType],
        context: MutationContext,
        typeof: ContentType) -> t.List[t.Tuple[t.Any, t.Any]]:
        """Apply appropriate mutations to selected elements."""
        replacements = []

        for selector, element in selectedelements:
            for mtype in activemutationtypes:
                typemutators = self.mutators.get(mtype, [])
                if not typemutators:
                    continue

                mutator = random.choice(typemutators)

                if not mutator.shouldmutate(context):
                    continue

                try:
                    mutatedelement = mutator.mutate(element, context)
                    mutation = mutator.recordmutation(element, mutatedelement, {"selector": selector})
                    self.history.add(
                        mutationtype=mtype.value,
                        details={"selector": str(selector), "contenttype": typeof.value}
                    )
                    self._notifylisteners('mutation', element, mutatedelement, context, mutation)

                    replacements.append((selector, mutatedelement))
                    break # one mutation per element
                except Exception as e:
                    log.error(f"error applying mutation: {str(e)}")

        return replacements

    def _renderbytypes(self, content: t.Any, typeof: ContentType, context: MutationContext) -> t.Any:
        """
        Render content using type-specific mutators.

        Args:
            content: Content to render
            typeof: Type of the content
            context: Mutation context

        Returns:
            Any: Rendered content
        """
        result = content

        applicabletargets = self.targets.get(typeof, [])
        if not applicabletargets:
            log.warning(f"no targets registered for content type: {typeof}")
            return result

        activemutationtypes = self._getactivemutationtypes()
        if not activemutationtypes:
            log.warning(f"")
            return result

        for target in applicabletargets:
            try:
                selectedelements = target.select(result, context)
                if not selectedelements:
                    continue

                replacements = self._applyelementmutations(
                    selectedelements,
                    activemutationtypes,
                    context,
                    typeof
                )

                if replacements:
                    result = target.replace(result, replacements, context)

            except Exception as e:
                log.error(f"")

        return result


    def render(self, content: t.Any, typeof: t.Union[str, ContentType], extracontext: t.Optional[t.Dict[str, t.Any]] = None) -> t.Any:
        """
        Render content with appropriate mutations.

        Args:
            content: The content to render and potentially mutate
            contenttype: Type of content (e.g., "text", "html", "json")
            extracontext: Additional context for mutation decisions

        Returns:
            Any: Rendered (potentially mutated) content
        """

        typeof = self._resolvecontenttype(typeof)
        context = MutationContext.FromContent(content, typeof)
        if extracontext:
            context.metadata.update(extracontext)

        self._notifylisteners('start', content, None, context)

        mutated = content
        if self._shouldtriggerpievent():
            mutated = self._handlepievent(mutated, context)
        mutated = self._applystrategies(mutated, context)
        mutated = self._renderbytypes(mutated, typeof, context)

        self._notifylisteners('end', content, mutated, context)
        return mutated


    def registermutator(self, mutator: Mutator) -> RenderEngine:
        """
        Register a mutator with the engine.

        Args:
            mutator: Mutator instance to register
        """
        if (mutator.mutationtype not in self.mutators):
            self.mutators[mutator.mutationtype] = []
        self.mutators[mutator.mutationtype].append(mutator)
        return self


    def registertarget(self, target: ContentTarget, typeof: ContentType) -> RenderEngine:
        """
        Register a content target with the engine.

        Args:
            target: ContentTarget instance to register
            contenttype: Content type this target handles
        """
        if (typeof not in self.targets):
            self.targets[typeof] = []
        self.targets[typeof].append(target)
        return self

    def registerstrategy(self, strategy: MutationStrategy) -> RenderEngine:
        """
        Register a mutation strategy with the engine.

        Args:
            strategy: MutationStrategy instance to register
        """
        self.strategies.append(strategy)
        return self

    def registerlistener(self, listener: RenderListener) -> RenderEngine:
        """
        Register a render listener with the engine.

        Args:
            listener: RenderListener instance to register
        """
        self.listeners.append(listener)
        return self
