from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Theme:
    id: Optional[int]
    title: str


@dataclass
class Question:
    id: Optional[int]
    title: str
    theme_id: int
    answers: list["Answer"] = field(default_factory=list)


@dataclass
class Answer:
    title: str
    is_correct: bool

    @classmethod
    def from_dict(cls, dic: dict):
        return cls(title=dic['title'], is_correct=dic['is_correct'])
