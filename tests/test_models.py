import pytest
from pydantic import ValidationError

from todoreels_py.models import ReelScript, BriefSchema

VALID = {
    "question": "¿Por qué cayó la población?",
    "questionType": "why",
    "hook": "No fueron las espadas.",
    "scenes": [
        {
            "id": "scene-1",
            "narration": "Texto",
            "screenText": "Texto",
            "visualDescription": "Mapa",
        }
    ],
    "conclusion": "Fue la viruela.",
}


def test_valid_script_parses_camel_case_json():
    script = ReelScript.model_validate(VALID)
    assert script.question_type == "why"
    assert script.scenes[0].screen_text == "Texto"


def test_hook_over_80_chars_is_rejected():
    with pytest.raises(ValidationError):
        ReelScript.model_validate({**VALID, "hook": "x" * 81})


def test_brief_accepts_valid_json_and_rejects_bad_certainty():
    data = {
        "topic": "La catástrofe demográfica en América",
        "context": "La llegada de los europeos en 1492.",
        "curiosityGap": "¿Por qué cayó la población indígena?",
        "payoff": "Enfermedades, guerras y esclavitud.",
        "facts": [
            {"fact": "La población cayó tras 1492.", "source": "https://a.example"},
            {"fact": "Hubo enfermedades europeas.", "source": "https://b.example"},
        ],
        "scores": {"curiosity": 8, "clarity": 9, "visual": 7, "evidence": 9},
        "fitsDuration": True,
        "certainty": "high",
        "verdict": "go",
        "reason": "Buen gancho.",
    }
    assert BriefSchema.model_validate(data).certainty == "high"

    with pytest.raises(ValidationError):
        BriefSchema.model_validate({**data, "certainty": 0.9})