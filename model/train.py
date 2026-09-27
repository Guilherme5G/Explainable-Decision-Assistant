import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

def gerar_dados_sinteticos(n_amostras=1000, random_state=42):
    rng = np.random.default_rng(random_state) # gera valores aleatorios sinteticos

    renda = rng.uniform(low=1500, high=15000, size=n_amostras)

    divida = rng.uniform(low=0, high=15000, size=n_amostras)

    numero_atrasos = rng.integers(low=0, high=9, size=n_amostras)

    proporcao_divida = divida / renda

    risco = ((proporcao_divida > 0.7) & (numero_atrasos >= 3)).astype(int)

    X = pd.DataFrame({
        "renda": renda,
        "divida": divida,                  #criando coluna x como um dataframe
        "numero_atrasos": numero_atrasos
    })

    y = pd.Series(risco, name="risco")   # criando como uma pd.series

    return X, y

def separar_dados(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    return X_train, X_test, y_train, y_test


def avaliar_profundidade(X_train, y_train):
    profundidades = [2, 3, 4, 5, None]

    for profundidade in profundidades:
        modelo = DecisionTreeClassifier(max_depth=profundidade, random_state=42)
        scores = cross_val_score(
            modelo, X_train, y_train, cv=5, scoring="accuracy"
        )
        print(profundidade)
        print(scores.mean())
        print(scores.std())

def treinar_modelo(X_train, y_train, max_depth=5):
    modelo = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    modelo.fit(X_train, y_train)
    return modelo

def avaliar_modelo(modelo, X_test, y_test):
    previsoes = modelo.predict(X_test)

    acuracia = accuracy_score(y_test, previsoes)
    matriz = confusion_matrix(y_test, previsoes)

    print("Accuracy:", acuracia)
    print("Matriz de confusão:")
    print(matriz)

def salvar_modelo(modelo):
    pasta_atual = Path(__file__).resolve().parent
    caminho_modelo = pasta_atual / "model.joblib"

    joblib.dump(modelo, caminho_modelo)
    return caminho_modelo

def main():
    X, y = gerar_dados_sinteticos()
    X_train, X_test, y_train, y_test = separar_dados(X, y)

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    avaliar_profundidade(X_train, y_train)

    modelo = treinar_modelo(X_train, y_train)
    print("Profundidade real:", modelo.get_depth())
    print("Número de folhas:", modelo.get_n_leaves())

    avaliar_modelo(modelo, X_test, y_test)

    caminho = salvar_modelo(modelo)
    print("Modelo salvo em:", caminho)

if __name__ == "__main__":
    main()
