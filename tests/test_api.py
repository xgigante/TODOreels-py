from fastapi.testclient import TestClient

from todoreels_py.api import app

client = TestClient(app)

PAYLOAD = {
    "script": {
        "question": "¿Por qué cayó la población?",
        "questionType": "why",
        "hook": "De cada 100 personas, 90 desaparecen.",
        "scenes": [
            {
                "id": "scene-1",
                "narration": "Antes de 1492 había entre 10 y 100 millones.",
                "screenText": "10-100 millones",
                "visualDescription": "Mapa con puntos.",
            }
        ],
        "conclusion": "Fue una catástrofe.",
    },
    "brief": {
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
    },
}


def test_check_figures_flags_invented_figure():
    response = client.post("/check-figures", json=PAYLOAD)
    assert response.status_code == 200
    assert response.json() == {"unsupportedFigures": ["90"]}


def test_check_figures_rejects_invalid_brief():
    bad = {**PAYLOAD, "brief": {**PAYLOAD["brief"], "certainty": 0.9}}
    response = client.post("/check-figures", json=bad)
    assert response.status_code == 422