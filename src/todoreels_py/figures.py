import re
from todoreels_py.models import BriefSchema, ReelScript

def extract_figures(text: str) -> list[str]:
    raw_figures = re.findall(r"\d+(?:[.,]\d+)*", text)
    figures = []
    for raw in raw_figures:
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", raw):
            figures.append(raw.replace(".", ""))
        else:
            figures.append(raw.replace(",", ".", 1))
    return figures

def _script_text(script: ReelScript) -> str:
    parts = [script.question, script.hook, script.conclusion]
    for scene in script.scenes:
        parts.extend([scene.narration, scene.screen_text, scene.visual_description])
    return " \n ".join(parts)


def _brief_text(brief: BriefSchema) -> str:
    parts = [brief.topic, brief.context, brief.curiosity_gap, brief.payoff]
    for fact in brief.facts:
        parts.append(fact.fact)
    return " \n ".join(parts)


def find_unsupported_figures(script: ReelScript, brief: BriefSchema) -> list[str]:
    allowed = set(extract_figures(_brief_text(brief)))
    used = extract_figures(_script_text(script))
    unsupported = []
    for figure in used:
        if figure not in allowed and figure not in unsupported:
            unsupported.append(figure)
    return unsupported