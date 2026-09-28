import pytest
from app.schemas import EntradaPredicao
from pydantic import ValidationError

def test_aceita_entrada_valida():
    entrada = EntradaPredicao(
        renda=5000,
        divida=4500,
        numero_atrasos=5
    )
    assert entrada.renda == 5000
    assert entrada.divida == 4500
    assert entrada.numero_atrasos == 5

def test_rejeita_renda_zero():
    with pytest.raises(ValidationError):
        EntradaPredicao(
            renda=0,
            divida=4500,
            numero_atrasos=5
        )

def test_rejeita_divida_negativa():
    with pytest.raises(ValidationError):
        EntradaPredicao(
            renda=5000,
            divida=-1,
            numero_atrasos=5
        )

def test_rejeita_numero_atrasos_negativo():
    with pytest.raises(ValidationError):
        EntradaPredicao(
            renda=5000,
            divida=4500,
            numero_atrasos=-1
        )