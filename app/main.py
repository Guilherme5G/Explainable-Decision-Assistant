from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.predictor import carregar_modelo, criar_entrada, prever
from app.explainer import explicar_decisao
from app.schemas import SaidaPredicao, EntradaPredicao


app = FastAPI(
    title="Explainable Decision Assistant",
    version="1.0.0",
)
modelo = carregar_modelo()

raiz_projeto = Path(__file__).resolve().parent.parent
pasta_static = raiz_projeto / "static"

app.mount(
    "/static",
    StaticFiles(directory=pasta_static),
    name="static"
)

@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(pasta_static / "index.html")

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