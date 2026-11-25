from todoreels_py.figures import extract_figures, find_unsupported_figures
from todoreels_py.models import BriefSchema, ReelScript

def test_extract_figures_normalizes_thousands_and_decimals():
    assert extract_figures("10.000 personas, 3,5 % y 1492") == ["10000", "3.5", "1492"]

BRIEF = BriefSchema.model_validate(
    {
        "topic": "La catástrofe demográfica en América",
        "context": "La llegada de los europeos en 1492.",
        "curiosityGap": "¿Por qué cayó la población indígena?",
        "payoff": "Enfermedades, guerras y esclavitud.",
        "facts": [
            {"fact": "Antes de 1492 había entre 10 y 100 millones.", "source": "https://a.example"},
            {"fact": "La caída se debió a enfermedades.", "source": "https://b.example"},
        ],
        "scores": {"curiosity": 8, "clarity": 9, "visual": 7, "evidence": 9},
        "fitsDuration": True,
        "certainty": "high",
        "verdict": "go",
        "reason": "Buen gancho.",
    }
)


def make_script(hook: str) -> ReelScript:
    return ReelScript.model_validate(
        {
            "question": "¿Por qué cayó la población?",
            "questionType": "why",
            "hook": hook,
            "scenes": [
                {
                    "id": "scene-1",
                    "narration": "Antes de 1492 había entre 10 y 100 millones.",
                    "screenText": "10-100 millones",
                    "visualDescription": "Mapa con puntos.",
                }
            ],
            "conclusion": "Fue una catástrofe.",
        }
    )


def test_find_unsupported_figures_accepts_figures_from_the_brief():
    assert find_unsupported_figures(make_script("Todo cambió en 1492."), BRIEF) == []


def test_find_unsupported_figures_flags_invented_figures():
    script = make_script("De cada 100 personas, 90 desaparecen.")
    assert find_unsupported_figures(script, BRIEF) == ["90"]