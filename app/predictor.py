import joblib
import pandas as pd
from pathlib import Path


def carregar_modelo():
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_modelo = raiz_projeto / "model" / "model.joblib"

    modelo = joblib.load(caminho_modelo)
    return modelo

def criar_entrada(renda, divida, numero_atrasos):
    entrada = pd.DataFrame([{
        "renda": renda,
        "divida": divida,
        "numero_atrasos": numero_atrasos
    }])
    return entrada

def prever(modelo, entrada):
    classe = modelo.predict(entrada)[0]
    probabilidades = modelo.predict_proba(entrada)[0]

    return {
        "classe": int(classe),
        "probabilidade_classe_0": float(probabilidades[0]),
        "probabilidade_classe_1": float(probabilidades[1])
    }
#Teste para saber o modelo usado e as features, para saber se esta reutilizando
'''print(type(modelo).__name__)
print(modelo.feature_names_in_)'''