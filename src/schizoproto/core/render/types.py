# ~/schizoproto/src/schizoproto/core/render/types.py
"""
Core type definitions for the schizo:// render system.

This module defines the fundamental types, enums, and dataclasses
used throughout the render module.
"""
from __future__ import annotations
import enum, random, typing as t, dataclasses as dc

class MutationType(enum.Enum):
    TEXTSWAP = "textswap"
    DOMSHIFT = "domshift"
    STYLEGLITCH = "styleglitch"
    AUDIOINJECT = "audioinject"
    TIMEWARP = "timewarp"
    MEMORYECHO = "memoryecho"
    METACORRUPT = "metacorrupt"
    PIEVENT = "pievent"
    # add more

class ContentType(enum.Enum):
    TEXT = "text"
    HTML = "html"
    JSON = "json"
    URI = "uri"

class MutationMood(enum.Enum):
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    PARANOID = "paranoid"
    MANIC = "manic"
    MELANCHOLIC = "melancholic"
    HAUNTING = "haunting"
    # expand
    # HUMOROUS
    # etc

@dc.dataclass
class RenderOptions:
    drift: float = 0.14
    corruption: float = 0.3
    piprob: float = 0.0314
    mood: MutationMood = MutationMood.NEUTRAL
    mutables: t.Set[MutationType] = dc.field(
        default_factory=lambda: {MutationType.TEXTSWAP, MutationType.STYLEGLITCH}
    )
    seed: t.Optional[int] = None
    options: t.Dict[str, t.Any] = dc.field(default_factory=dict)


    def __post_init__(self):
        if isinstance(self.mood, str):
            try:
                self.mood = MutationMood[self.mood.upper()]
            except KeyError:
                self.mood = MutationMood.NEUTRAL

        if self.seed is not None:
            random.seed(self.seed) # what


@dc.dataclass
class UserState:
    """User state information for personalized mutations."""
    interactioncount: int = 0
    firstsintime: t.Optional[float] = None
    lastinteraction: t.Optional[float] = None
    emotions: t.Dict[str, float] = dc.field(default_factory=dict)
    interests: t.Dict[str, float] = dc.field(default_factory=dict)
    vulnerabilities: t.Dict[str, float] = dc.field(default_factory=dict)
    flags: t.Set[str] = dc.field(default_factory=set)


@dc.dataclass
class MutationHistory:
    """History of mutations applied to content."""
    records: t.List[t.Dict[str, t.Any]] = dc.field(default_factory=list)
    bytype: t.Dict[str, int] = dc.field(default_factory=dict)
    lastapplied: t.Optional[float] = None

    def add(self, mutationtype: str, details: t.Dict[str, t.Any]) -> None:
        """Add a mutation record to history."""
        timestamp = __import__('time').time()
        record = {
            "type": mutationtype,
            "timestamp": timestamp,
            "details": details
        }
        self.records.append(record)
        self.bytype[mutationtype] = self.bytype.get(mutationtype, 0) + 1
        self.lastapplied = timestamp

    def getlast(self, count: int = 1) -> t.List[t.Dict[str, t.Any]]:
        """Get the last N mutation records."""
        return self.records[-count:] if self.records else []

    def countbytype(self, mutationtype: str) -> int:
        """Count mutations of a specific type."""
        return self.bytype.get(mutationtype, 0)

@dc.dataclass
class MutationContext:
    contenttype: ContentType
    contentlength: int = 0
    complexity: float = 0.5
    userstate: UserState = dc.field(default_factory=UserState)
    history: MutationHistory = dc.field(default_factory=MutationHistory)
    metadata: t.Dict[str, t.Any] = dc.field(default_factory=dict)

    @classmethod
    def FromContent(cls, content: t.Any, typeof: t.Union[str, ContentType]) -> MutationContext:
        if isinstance(typeof, str):
            try:
                typeof = ContentType[typeof.upper()]
            except Exception as e:
                typeof = ContentType.TEXT

        contentlength = 0
        if isinstance(content, str):
            contentlength = len(content)
        elif isinstance(content, (list, dict)):
            contentlength = len(str(content))

        return cls(
            contenttype=typeof,
            contentlength=contentlength
        )

@dc.dataclass
class MutationResult:
    original: t.Any
    result: t.Any
    mutationtype: MutationType
    details: t.Dict[str, t.Any] = dc.field(default_factory=dict)
    timestamp: float = dc.field(default_factory=lambda: __import__('time').time())
