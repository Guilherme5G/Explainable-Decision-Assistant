import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_retorna_status_ok():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {
        "status": "ok",
        "modelo_carregado": True
    }

# teste de integracao, validacao, rota, dataframe, probabilidades,
# explicacao e serializacao JSON.
def test_predict_retorna_predicao_e_explicacao():
    resposta = client.post(
        "/predict",
        json={
            "renda": 5000,
            "divida": 4500,
            "numero_atrasos": 5
        }
    )
    assert resposta.status_code == 200

    corpo = resposta.json()
    assert corpo["classe"] == 1

    soma = (
        corpo["probabilidade_classe_0"] +
        corpo["probabilidade_classe_1"]
    )
    assert soma == pytest.approx(1.0)
    assert len(corpo["explicacao"]["regras"]) > 0
    assert isinstance(corpo["explicacao"]["folha"], int)


def test_predict_rejeita_renda_zero():
    resposta = client.post(
        "/predict",
        json={
            "renda": 0,
            "divida": 4500,
            "numero_atrasos": 5
        }
    )
    assert resposta.status_code == 422

    corpo = resposta.json()
    assert corpo["detail"][0]["loc"] == ["body", "renda"]
