import numpy as np
import pandas as pd

def gerar_dados_sinteticos(n_amostras=1000, random_state=42):
    rng = np.random.default_rng(random_state)

    renda = rng.uniform(low=1500, high=15000, size=n_amostras)

    divida = rng.uniform(low=0, high=15000, size=n_amostras)

    numero_atrasos = rng.integers(low=0, high=9, size=n_amostras)

    print(renda[:5])
    print(divida[:5])
    print(numero_atrasos[:5])


gerar_dados_sinteticos()