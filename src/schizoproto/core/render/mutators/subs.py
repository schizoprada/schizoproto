# ~/schizoproto/src/schizoproto/core/render/mutators/subs.py
"""
Substitution engine for schizo:// render system.

This module provides NLP-driven text substitution capabilities for the
schizo:// protocol's content mutation system. It combines multiple approaches:

- Character-level substitutions with mood-based modifications
- Word-level replacements using WordNet synonyms
- Contextual text generation using transformer models
- Mood-influenced content corruption

The SubstitutionEngine class serves as the core component for generating
textual alternatives, which are then used by various mutators to create
progressive content drift and emotional manipulation effects.

Example:
    engine = SubstitutionEngine()

    # Character substitutions
    chars = engine.getcharsubs('a', MutationMood.PARANOID)
    # => ['@', '4', 'α', '#', '@', '$']

    # Word substitutions
    words = engine.getwordsubs('watch', MutationMood.ANXIOUS, context)
    # => ['observe', 'monitor', 'stalk', 'follow', 'lurk']

Note:
    Requires NLTK data and transformer models. Will attempt to download
    required NLTK components on first initialization.
"""
from __future__ import annotations
import random, typing as t, collections as co, dataclasses as dc

import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize as wordtokenize
from transformers import pipeline

from schizoproto.logs import log
from schizoproto.core.render.base import Mutator
from schizoproto.core.render.types import (
    MutationType as MT, MutationContext as MC, RenderOptions as RO,
    MutationMood as MM
)

class DEFAULT:
    class NLTK:
        DATA = ('tokenizers/punkt', 'corpora/wordnet')

    class TRANSFORMERS:
        MODEL = "distilgpt2"
        MAXLEN = 20
        NUMSEQS = 3

    class MOOD:
        MODS = {
            MM.ANXIOUS: ['!', '?', '*'],
            MM.PARANOID: ['#', '@', '$'],
            MM.MANIC: ['1', '0', '+'],
            MM.MELANCHOLIC: ['_', '-', '.'],
            MM.HAUNTING: ['~', '`', '^']
        }

    class CHARS:
        SUBS = {
            'a': ['@', '4', 'α'],
            'e': ['3', 'ε', '€'],
            'i': ['1', '!', 'ι'],
            'o': ['0', 'θ', 'σ'],
            's': ['5', '$', 'δ'],
            't': ['7', '+', 'τ'],
            # expand with more substitutions
        }

    class PROMPTS:
        WORDSUB = "Replace '{word}' with a {mood} word:"

class SubstitutionEngine:
    """Dynamic substitution engine using NLP"""
    def __init__(self,
        nltkdata: t.Optional[t.Sequence[str]] = None,
        transformermodel: t.Optional[str] = None,
        tokenizer: t.Optional[t.Callable] = None,
        moodsmap: t.Optional[t.Dict[MM, float]] = None,
        charsubsmap: t.Optional[t.Dict[str, t.List[str]]] = None,
        **kwargs) -> None:
        self.nltkdata = (nltkdata or DEFAULT.NLTK.DATA)
        self.transformermodel = (transformermodel or DEFAULT.TRANSFORMERS.MODEL)
        self._ensurenltk()
        self.generator = pipeline('text-generation', model=self.transformermodel)
        self.tokenizer = (tokenizer or wordtokenize)
        self.moodsmap = (moodsmap or DEFAULT.MOOD.MODS)
        self.charsubsmap = (charsubsmap or DEFAULT.CHARS.SUBS)

    def _ensurenltk(self) -> None:
        for entry in self.nltkdata:
            try:
                nltk.data.find(entry)
            except LookupError:
                try:
                    entrydata = entry.split('/')
                    download = entrydata[1]
                    nltk.download(download)
                except Exception as e:
                    log.error(f"SubstitutionEngine._ensurenltk | exception: {str(e)}")
                    raise e

    def getcharsubs(self, char: str, mood: MM) -> t.List[str]:
        """Get character substitutions using visual/phonetic similarity"""
        basesubs = self.charsubsmap.get(char, [char])
        moodsubs = self.moodsmap.get(mood, [])
        return list(set(basesubs + moodsubs))

    def getwordsubs(self, word: str, mood: MM, context: MC, limit: int = 5) -> t.List[str]:
        """Get contextual word substitutions based on mood"""

        synsets = wordnet.synsets(word)
        alternatives = set()

        for syn in synsets:
            if syn is not None:
                alternatives.update(lemma.name() for lemma in syn.lemmas())

        prompt = f"Replace '{word}' with a {mood.value} word:" # should probably make this configurable
        try:
            generated = self.generator(prompt, max_length=20, num_return_sequences=3)
            for g in generated:
                if g is not None:
                    tokens = self.tokenizer(g['generated_text'])
                    alternatives.update(tokens)
        except Exception as e:
            log.error(f"SubstitutionEngine.getwordsubs | exception: {str(e)}")

        return (list(alternatives)[:limit])
