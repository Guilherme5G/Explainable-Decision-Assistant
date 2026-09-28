# Explainable Decision Assistant

Aplicação educacional de Machine Learning que integra uma árvore de decisão explicável com backend FastAPI e frontend web.

O sistema recebe informações sintéticas de renda, dívida e número de atrasos, produz uma classificação de risco e mostra o caminho percorrido pelo modelo para chegar à decisão.

> **Aviso:** este projeto utiliza dados sintéticos e possui finalidade exclusivamente educacional. Ele não deve ser utilizado para decisões financeiras ou de crédito reais.

## Funcionalidades

- Geração reproduzível de dados sintéticos.
- Separação estratificada entre treino e teste.
- Seleção da profundidade da árvore por validação cruzada.
- Preservação do test set para avaliação final.
- Treinamento de uma `DecisionTreeClassifier`.
- Persistência do modelo treinado com Joblib.
- Predição da classe com `predict()`.
- Cálculo das probabilidades com `predict_proba()`.
- Explicação do caminho percorrido na árvore.
- Validação de entrada com Pydantic.
- API REST com FastAPI.
- Documentação interativa com Swagger UI.
- Frontend responsivo em HTML, CSS e JavaScript.
- Estados visuais diferentes para menor e maior risco.
- Testes automatizados de validação, predictor e API.

## Arquitetura

O treinamento acontece offline e gera um artefato reutilizável:

```text
Dados sintéticos
       ↓
   train.py
       ↓
Validação cruzada
       ↓
Treinamento final
       ↓
 model.joblib
```

Durante o uso da aplicação, o modelo salvo é carregado e reutilizado:

```text
Frontend HTML/CSS/JS
          ↓
      POST /predict
          ↓
Validação com Pydantic
          ↓
Predictor → model.joblib
          ↓
Predict + Predict Proba
          ↓
Explainer → decision_path
          ↓
      Resposta JSON
          ↓
Resultado apresentado no frontend
```

O modelo não é treinado novamente a cada requisição.

## Estrutura do projeto

```text
Explainable_Decision_Assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── predictor.py
│   └── explainer.py
│
├── model/
│   ├── train.py
│   └── model.joblib
│
├── static/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── background.jpg
│
├── tests/
│   ├── test_validation.py
│   ├── test_predictor.py
│   └── test_api.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── report.md
```

## Dados sintéticos

O dataset contém 1.000 exemplos e três features:

| Feature | Descrição |
|---|---|
| `renda` | Renda sintética do exemplo |
| `divida` | Dívida sintética do exemplo |
| `numero_atrasos` | Quantidade sintética de atrasos |

O alvo é:

```text
risco = 0 ou 1
```

A regra utilizada para gerar o alvo sintético foi:

```text
risco = 1 quando:

divida / renda > 0.7
E
numero_atrasos >= 3
```

Essa regra é usada apenas para gerar os dados educacionais. A árvore não recebe a regra diretamente: ela aprende aproximações a partir das features e dos exemplos de treinamento.

## Separação dos dados

Os dados foram separados de forma estratificada:

```text
Treino: 80% — 800 exemplos
Teste:  20% — 200 exemplos
```

A estratificação preserva aproximadamente a proporção das classes nos dois conjuntos.

O test set foi mantido fora do processo de escolha de hiperparâmetros. A profundidade do modelo foi escolhida usando somente os dados de treino e validação cruzada.

## Seleção do modelo

Foram comparadas as seguintes configurações:

| `max_depth` | Accuracy média na CV | Desvio-padrão |
|---:|---:|---:|
| 2 | 0.88625 | 0.01829 |
| 3 | 0.90500 | 0.01741 |
| 4 | 0.95500 | 0.00612 |
| 5 | 0.97500 | 0.00395 |
| `None` | 0.98125 | 0.00395 |

Foi escolhido:

```python
DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)
```

Embora `max_depth=None` tenha obtido a maior média, a diferença para `max_depth=5` foi de aproximadamente 0,63 ponto percentual.

A profundidade 5 foi escolhida para limitar a complexidade e manter as explicações mais simples.

## Características do modelo final

```text
Profundidade real: 5
Número de folhas: 13
```

## Avaliação final

O modelo escolhido foi avaliado uma única vez no test set final.

```text
Test accuracy: 0.94
```

Matriz de confusão:

```text
[[109, 10],
 [  2, 79]]
```

Interpretação considerando a classe `1` como maior risco:

| Resultado | Quantidade |
|---|---:|
| Verdadeiros negativos | 109 |
| Falsos positivos | 10 |
| Falsos negativos | 2 |
| Verdadeiros positivos | 79 |

O modelo identificou 79 dos 81 exemplos reais da classe 1 presentes no conjunto de teste.

Esses resultados descrevem somente o dataset sintético utilizado neste projeto. Eles não representam desempenho em dados financeiros reais.

## Explicabilidade

A aplicação utiliza os recursos internos da árvore para identificar o caminho percorrido por cada entrada:

```python
modelo.decision_path(entrada)
modelo.apply(entrada)
```

A resposta mostra:

- A feature analisada.
- O operador utilizado.
- O limite aprendido pela árvore.
- O valor informado pelo usuário.
- A folha final alcançada.

Exemplo:

```text
numero_atrasos > 2.50 (valor informado: 5.00)
divida <= 6958.13 (valor informado: 4500.00)
renda <= 8473.47 (valor informado: 5000.00)
```

As explicações representam os cortes realmente aprendidos pelo modelo, não apenas a regra original usada para gerar os dados.

## Tecnologias

- Python
- NumPy
- Pandas
- Scikit-learn
- Joblib
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- HTTPX
- HTML
- CSS
- JavaScript

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Guilherme5G/Explainable-Decision-Assistant.git
cd Explainable-Decision-Assistant
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar o ambiente virtual

PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Treinar e salvar o modelo

```bash
python model/train.py
```

Esse comando:

- Gera os dados sintéticos.
- Separa treino e teste.
- Executa a validação cruzada.
- Treina a árvore escolhida.
- Avalia o modelo no test set.
- Salva `model/model.joblib`.

### 6. Iniciar a aplicação

```bash
python -m uvicorn app.main:app --reload
```

### 7. Acessar

Aplicação:

```text
http://127.0.0.1:8000/
```

Documentação Swagger:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## API

### `GET /health`

Verifica se a API está ativa e se o modelo foi carregado.

Exemplo de resposta:

```json
{
  "status": "ok",
  "modelo_carregado": true
}
```

### `POST /predict`

Realiza uma previsão e retorna sua explicação.

Exemplo de requisição:

```json
{
  "renda": 5000,
  "divida": 4500,
  "numero_atrasos": 5
}
```

Exemplo de resposta:

```json
{
  "classe": 1,
  "probabilidade_classe_0": 0.3333333333333333,
  "probabilidade_classe_1": 0.6666666666666666,
  "explicacao": {
    "regras": [
      "numero_atrasos > 2.50 (valor informado: 5.00)",
      "divida <= 6958.13 (valor informado: 4500.00)",
      "renda <= 8473.47 (valor informado: 5000.00)",
      "divida > 4340.62 (valor informado: 4500.00)",
      "divida <= 4637.40 (valor informado: 4500.00)"
    ],
    "folha": 9
  }
}
```

## Validação de entrada

A API exige:

```text
renda > 0
divida >= 0
numero_atrasos >= 0
```

`numero_atrasos` deve ser inteiro.

Entradas inválidas são rejeitadas com status HTTP `422` antes de chegarem ao modelo.

## Testes

Execute toda a suíte com:

```bash
python -m pytest -v
```

Resultado atual:

```text
9 passed
```

Os testes cobrem:

- Aceitação de entrada válida.
- Rejeição de renda igual a zero.
- Rejeição de dívida negativa.
- Rejeição de número de atrasos negativo.
- Formato da previsão.
- Soma das probabilidades.
- Previsão de um exemplo conhecido.
- Health check da API.
- Resposta válida do endpoint `/predict`.
- Rejeição HTTP de entrada inválida.

> Dependendo das versões instaladas, a execução pode apresentar um aviso de depreciação interno do FastAPI/Starlette relacionado ao cliente de testes. Esse aviso não representa falha da aplicação.

## Interface

O frontend apresenta:

- Formulário validado pelo navegador.
- Estado de carregamento.
- Tratamento de erros.
- Classe prevista.
- Probabilidades numéricas.
- Barras visuais de probabilidade.
- Caminho da decisão.
- Cores diferentes para menor e maior risco.
- Layout responsivo para desktop e dispositivos móveis.
- Tema escuro com imagem de fundo.

A imagem de fundo utilizada é de Pawel Czerwinski, disponibilizada via Unsplash.

## Limitações

- Os dados são totalmente sintéticos.
- O projeto não foi validado com dados financeiros reais.
- A regra do alvo é artificial e conhecida.
- As probabilidades da árvore correspondem à distribuição das classes nas folhas.
- As probabilidades não foram calibradas.
- Não há autenticação ou controle de usuários.
- Não há banco de dados.
- Não há monitoramento de drift.
- Não há análise de fairness.
- O modelo não deve ser usado para decisões reais.

## Próximos passos

Possíveis evoluções:

- Utilizar um dataset real e devidamente documentado.
- Comparar a árvore com outros modelos.
- Avaliar diferentes métricas além de accuracy.
- Analisar precision, recall e F1 por classe.
- Aplicar poda com `ccp_alpha`.
- Calibrar as probabilidades.
- Criar testes adicionais para o explainer.
- Adicionar monitoramento e logs estruturados.
- Criar container Docker.
- Configurar integração contínua.
- Publicar uma demonstração online.

## Objetivo educacional

Este projeto foi desenvolvido para praticar a integração entre Machine Learning e desenvolvimento de software:

```text
problema
→ dados
→ validação
→ treinamento
→ avaliação
→ persistência
→ API
→ frontend
→ explicabilidade
→ testes
→ documentação
```

O principal objetivo não é construir um sistema de crédito, mas demonstrar um fluxo completo, reproduzível e explicável de Machine Learning aplicado.