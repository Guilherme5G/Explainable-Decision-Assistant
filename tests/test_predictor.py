import pytest
from app.predictor import carregar_modelo, criar_entrada, prever

def test_previsao_retorna_probabilidades_validas():
    modelo = carregar_modelo()
    entrada = criar_entrada(
        renda=5000,
        divida=4500,
        numero_atrasos=5
    )

    resultado = prever(modelo, entrada)
    assert resultado["classe"] in (0, 1)

    soma = (
        resultado["probabilidade_classe_0"] +
        resultado["probabilidade_classe_1"]
    )
    assert soma == pytest.approx(1.0)


def test_preve_classe_um_para_entrada_de_maior_risco():
    modelo = carregar_modelo()
    entrada = criar_entrada(
        renda=5000,
        divida=4500,
        numero_atrasos=5
    )
    resultado = prever(modelo, entrada)
    assert resultado["classe"] == 1