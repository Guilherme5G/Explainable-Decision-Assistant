from fastapi import FastAPI
from app.predictor import carregar_modelo, criar_entrada, prever
from app.explainer import explicar_decisao
from app.schemas import SaidaPredicao, EntradaPredicao

app = FastAPI(
    title="Explainable Decision Assistant",
    version="1.0.0",
)
modelo = carregar_modelo()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "modelo_carregado": modelo is not None
    }

@app.post("/predict", response_model=SaidaPredicao)
def predict(dados: EntradaPredicao):
    entrada = criar_entrada(
        renda=dados.renda,
        divida=dados.divida,
        numero_atrasos=dados.numero_atrasos
    )

    resultado = prever(modelo, entrada)
    explicacao = explicar_decisao(modelo, entrada)

    resultado["explicacao"] = explicacao
    return resultado