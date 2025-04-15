# ~/schizoproto/src/schizoproto/core/render/mutators/text.py
"""
Text mutation components for schizo:// render engine.

This module provides mutators that handle text-based content corruption,
including character manipulation, word hallucination, and semantic drift.
"""
from __future__ import annotations
import random, typing as t, dataclasses as dc

from schizoproto.logs import log
from schizoproto.core.render.base import Mutator
from schizoproto.core.render.types import (
    MutationType as MT, MutationContext as MC, RenderOptions as RO,
    MutationMood as MM
)
from schizoproto.core.render.mutators.subs import SubstitutionEngine

class DEFAULT:
    # note:
        # make these configurable via config
    MOODMODSMAP = {
        MM.NEUTRAL: 1.0,
        MM.ANXIOUS: 1.2,
        MM.PARANOID: 1.5,
        MM.MANIC: 2.0,
        MM.MELANCHOLIC: 0.8,
        MM.HAUNTING: 1.3
    }

    CHARSUBS = {
        'a': ['@', '4', 'α'],
        'e': ['3', 'ε', '€'],
        'i': ['1', '!', 'ι'],
        'o': ['0', 'θ', 'σ'],
        's': ['5', '$', 'δ'],
        't': ['7', '+', 'τ'],
        # expand with more substitutions
    }

@dc.dataclass
class TextMutationParams:
    """Configurations for text mutation"""
    corruptionrate: float = 0.14
    subweight: float = 0.5 # substitution weight
    delweight: float = 0.3 # deletion weight
    insertweight: float = 0.2 # insertion weight
    maxrepeats: int = 3
    preservecase: bool = True # preserve casing
    preservepunct: bool = True # preserve punctuation

class TextMutator(Mutator):
    """Base class for text-based mutations"""

    def __init__(self,
        options: RO,
        params: t.Optional[TextMutationParams] = None,
        moodsmap: t.Optional[t.Dict[MM, float]] = None,
        subsengine: t.Optional[SubstitutionEngine] = None,
        **kwargs):
        super().__init__(options, **kwargs)
        self.mutationtype = MT.TEXTSWAP
        self.params = (params or TextMutationParams())
        self.moodsmap = (moodsmap or DEFAULT.MOODMODSMAP)
        self.subsengine = (subsengine or SubstitutionEngine())



    def _getmoodmod(self, context: MC) -> float:
        """Get mutation probability modifier based on current mood."""
        return self.moodsmap.get(self.options.mood, 1.0)

    def shouldmutate(self, context: MC) -> bool:
        """Determine if mutation should occur based on drift and context."""
        if context.contenttype.value != "text":
            return False

        basechance = (self.options.drift * self.params.corruptionrate)
        moodmod = self._getmoodmod(context)

        return (random.random() < (basechance * moodmod))


class CharacterCorruptor(TextMutator):
    """Mutates text at the character level."""

    def __init__(self,
        options: RO,
        params: t.Optional[TextMutationParams] = None,
        moodsmap: t.Optional[t.Dict[MM, float]] = None,
        charsubsmap: t.Optional[t.Dict[str, t.List[str]]] = None,
        **kwargs):
        super().__init__(options, params, moodsmap, **kwargs)
        self.charsubs = (charsubsmap or DEFAULT.CHARSUBS)

    def _shouldmutatechar(self, position: int, context: MC) -> bool:
        basechance = self.params.corruptionrate
        posmod = min((position/100), 2.0)
        return (random.random() < (basechance * posmod))


    def mutate(self, content: t.Any, context: MC) -> t.Any:
        """Apply character-level mutations to text content."""
        if not isinstance(content, str):
            return content

        result = list(content)
        for i in range(len(result)):
            if not self._shouldmutatechar(i, context):
                continue
            char = result[i].lower()
            try:
                subs = self.subsengine.getcharsubs(char, self.options.mood)
                if subs:
                    result[i] = random.choice(subs)
            except Exception as e:
                log.error(f"CharacterCorruptor.mutate | exception: {str(e)}")

        return ''.join(result)


class WordHallucinator(TextMutator):
    """Introduces and transforms words using NLP-based substitutions."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutationtype = MT.TEXTSWAP

    def _shouldhallucinate(self, position: int, context: MC) -> bool:
        """Determine if hallucination should occur at position."""
        basechance = (self.params.corruptionrate * self.params.insertweight)
        posmod = min((position/50), 1.5)  # Position influence
        return (random.random() < (basechance * posmod))

    def mutate(self, content: t.Any, context: MC) -> t.Any:
        """Apply word-level mutations to text content."""
        if not isinstance(content, str):
            return content

        words = content.split()
        result = []

        for i, word in enumerate(words):
            result.append(word)

            if self.shouldmutate(context):
                try:
                    subs = self.subsengine.getwordsubs(
                        word,
                        self.options.mood,
                        context
                    )
                    if subs:
                        result[-1] = random.choice(subs)
                except Exception as e:
                    log.error(f"Exception substituting words: {str(e)}")

            if self._shouldhallucinate(i, context):
                try:
                    hallucinations = self.subsengine.getwordsubs(
                        word,
                        self.options.mood,
                        context
                    )
                    if hallucinations:
                        result.append(random.choice(hallucinations))
                except Exception as e:
                    log.error(f"Excpetion hallucinating words: {str(e)}")

        return ' '.join(result)


class SentenceShifter(TextMutator):
    """Manipulates sentence structure and flow using NLP analysis."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mutationtype = MT.TEXTSWAP

    def _shouldshift(self, position: int, totalsentences: int, context: MC) -> bool:
        """Determine if sentence shift should occur at position."""
        if totalsentences < 2:
            return False

        basechance = (self.params.corruptionrate * self.params.subweight)
        posmod = min((position/totalsentences), 1.5)
        return (random.random() < (basechance * posmod))

    def _getshiftrange(self, position: int, totalsentences: int) -> tuple[int, int]:
        """Calculate range of sentences to consider for shifting."""
        maxrange = min(3, totalsentences - position)  # Max 3 sentences at once
        shiftsize = random.randint(1, maxrange)
        return (position, (position + shiftsize))


    def mutate(self, content: t.Any, context: MC) -> t.Any:
        """Apply sentence-level mutations to text content."""
        if not isinstance(content, str):
            return content

        try:
            # Split into sentences using nltk
            sentences = self.subsengine.tokenizer(content)
            if len(sentences) < 2:
                return content

            result = sentences.copy()
            for i in range(len(sentences)):
                if not self._shouldshift(i, len(sentences), context):
                    continue

                try:
                    # Get range to shift
                    start, end = self._getshiftrange(i, len(sentences))

                    # Extract segment to manipulate
                    segment = result[start:end]

                    # Apply transformations based on mood
                    match self.options.mood:
                        case MM.ANXIOUS:
                            # Repeat last sentence
                            segment.append(segment[-1])
                        case MM.PARANOID:
                            # Reverse order
                            segment.reverse()
                        case MM.MANIC:
                            # Shuffle segment
                            random.shuffle(segment)
                        case MM.MELANCHOLIC:
                            # Drop random sentence
                            if len(segment) > 1:
                                segment.pop(random.randint(0, len(segment)-1))
                        case MM.HAUNTING:
                            # Insert generated sentence
                            try:
                                ctxword = segment[0].split()[0]  # First word for context
                                hallucinations = self.subsengine.getwordsubs(
                                    ctxword,
                                    self.options.mood,
                                    context
                                )
                                if hallucinations:
                                    segment.insert(
                                        random.randint(0, len(segment)),
                                        random.choice(hallucinations)
                                    )
                            except Exception as e:
                                log.error(f"Sentence hallucination failed: {e}")

                    # Replace segment in result
                    result[start:end] = segment

                except Exception as e:
                    log.error(f"Sentence shift operation failed: {e}")
                    continue

            return ' '.join(result)

        except Exception as e:
            log.error(f"Sentence shifting failed: {e}")
            return content
