from fastapi import FastAPI
from pydantic import Field

from todoreels_py.figures import find_unsupported_figures
from todoreels_py.models import BriefSchema, CamelModel, ReelScript
from todoreels_py.llm import ask_llm

app = FastAPI(title="TODOreels API")


class FigureCheckRequest(CamelModel):
    script: ReelScript
    brief: BriefSchema


class FigureCheckResponse(CamelModel):
    unsupported_figures: list[str]


@app.post("/check-figures")
def check_figures(request: FigureCheckRequest) -> FigureCheckResponse:
    return FigureCheckResponse(
        unsupported_figures=find_unsupported_figures(request.script, request.brief)
    )


class AskRequest(CamelModel):
    prompt: str = Field(min_length=1, max_length=2000)


class AskResponse(CamelModel):
    answer: str


@app.post("/ask")
async def ask(request: AskRequest) -> AskResponse:
    return AskResponse(answer=await ask_llm(request.prompt))