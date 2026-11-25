from fastapi import FastAPI

from todoreels_py.figures import find_unsupported_figures
from todoreels_py.models import BriefSchema, CamelModel, ReelScript

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