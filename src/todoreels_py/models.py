from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

QuestionType = Literal[
    "who", "what", "when", "where", "why",
    "how", "purpose", "consequence", "comparison", "hypothetical",
]


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ScriptScene(CamelModel):
    id: str = Field(min_length=1)
    narration: str = Field(min_length=1, max_length=100)
    screen_text: str = Field(min_length=1, max_length=45)
    visual_description: str = Field(min_length=1, max_length=180)


class ReelScript(CamelModel):
    question: str = Field(min_length=5, max_length=120)
    question_type: QuestionType
    hook: str = Field(min_length=1, max_length=80)
    scenes: list[ScriptScene] = Field(min_length=1, max_length=3)
    conclusion: str = Field(min_length=1, max_length=100)
    

class Facts(CamelModel):
    fact: str = Field(min_length=5, max_length=240)
    source: str = Field(min_length=4)

class Scores(CamelModel):
    curiosity: float =  Field(ge=0, le=10)
    clarity: float =  Field(ge=0, le=10)
    visual: float =  Field(ge=0, le=10)
    evidence: float =  Field(ge=0, le=10)
    

class BriefSchema(CamelModel):
    topic: str = Field(min_length=8, max_length=160)
    context: str = Field(min_length=10, max_length=300)
    curiosity_gap: str = Field(min_length=8, max_length=120)
    payoff: str = Field(min_length=8, max_length=200)
    facts: list[Facts] = Field(min_length=2, max_length=6)
    scores: Scores
    fits_duration: bool
    certainty: Literal['high', 'medium', 'low']
    verdict: Literal['go', 'reject']
    reason: str = Field(max_length=400)




