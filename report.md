# Relatório — Explainable Decision Assistant

## Semana 1 — Dia 7

## 1. Objetivo

O objetivo deste projeto foi integrar os principais conceitos estudados durante a primeira semana em uma aplicação completa de Machine Learning.

O sistema desenvolvido recebe três informações sintéticas:

- Renda.
- Dívida.
- Número de atrasos.

A partir desses valores, uma árvore de decisão retorna:

- Uma classe de risco.
- As probabilidades das duas classes.
- O caminho percorrido pelo modelo até a decisão.

Além do modelo, o projeto inclui validação de entrada, backend, API, frontend responsivo, testes automatizados e documentação.

O projeto possui finalidade exclusivamente educacional e não deve ser utilizado para decisões financeiras reais.

## 2. Arquitetura

O sistema foi separado em dois fluxos principais.

### 2.1. Treinamento offline

```text
Geração de dados sintéticos
→ separação entre treino e teste
→ validação cruzada
→ seleção da profundidade
→ treinamento
→ avaliação final
→ persistência do modelo
```

O treinamento é executado separadamente das requisições do usuário. O modelo resultante é salvo em `model/model.joblib`.

### 2.2. Inferência online

```text
Frontend
→ requisição HTTP
→ validação com Pydantic
→ predictor
→ modelo salvo
→ explicação
→ resposta JSON
→ apresentação do resultado
```

A API carrega o modelo uma vez durante sua inicialização e o reutiliza nas requisições seguintes.

Essa separação evita treinar novamente a árvore sempre que o usuário solicita uma previsão.

## 3. Dados sintéticos

Foram gerados 1.000 exemplos com as features:

```text
renda
divida
numero_atrasos
```

O alvo sintético foi definido pela regra:

```text
risco = 1 quando:

divida / renda > 0.7
E
numero_atrasos >= 3
```

A relação entre dívida e renda foi escolhida porque uma dívida isolada não informa adequadamente seu peso financeiro.

Uma dívida de mesmo valor pode representar situações muito diferentes dependendo da renda.

O operador `E` tornou a classe de maior risco mais restritiva, exigindo simultaneamente uma proporção elevada de dívida e pelo menos três atrasos.

A distribuição gerada foi:

```text
classe 0: 597 exemplos
classe 1: 403 exemplos
```

## 4. Separação dos dados

Foi utilizado um split estratificado:

```text
Treino: 800 exemplos
Teste:  200 exemplos
```

Parâmetros utilizados:

```python
test_size=0.20
random_state=42
stratify=y
```

A estratificação preservou aproximadamente a proporção das classes.

O test set foi mantido fora do processo de seleção de hiperparâmetros. Ele foi utilizado somente depois da escolha da configuração final.

## 5. Validação cruzada

As profundidades avaliadas foram:

```text
[2, 3, 4, 5, None]
```

Foi utilizada validação cruzada com cinco folds e accuracy como métrica.

Resultados:

| Profundidade | Accuracy média | Desvio-padrão |
|---:|---:|---:|
| 2 | 0.88625 | 0.01829 |
| 3 | 0.90500 | 0.01741 |
| 4 | 0.95500 | 0.00612 |
| 5 | 0.97500 | 0.00395 |
| Sem limite | 0.98125 | 0.00395 |

A árvore sem limite obteve a maior accuracy média. Entretanto, sua vantagem sobre `max_depth=5` foi de aproximadamente 0,63 ponto percentual.

Foi escolhida a profundidade 5 porque a diferença de desempenho era pequena e uma árvore limitada oferece:

- Maior controle de complexidade.
- Menor risco de overfitting.
- Explicações potencialmente menores.
- Melhor equilíbrio entre desempenho e interpretabilidade.

## 6. Modelo final

O modelo final foi:

```python
DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)
```

Características observadas:

```text
Profundidade real: 5
Número de folhas: 13
```

O modelo foi treinado apenas com `X_train` e `y_train`.

## 7. Avaliação final

Depois da seleção do modelo por validação cruzada, o test set foi utilizado para a avaliação final.

Resultado:

```text
Accuracy: 0.94
```

Matriz de confusão:

```text
[[109, 10],
 [  2, 79]]
```

Interpretação:

```text
Verdadeiros negativos: 109
Falsos positivos:       10
Falsos negativos:        2
Verdadeiros positivos:  79
```

O modelo identificou 79 dos 81 exemplos reais da classe 1 presentes no test set.

O resultado não foi utilizado para trocar a profundidade ou selecionar outro modelo. Fazer isso transformaria o test set em parte do processo de tuning e reduziria a imparcialidade da avaliação.

## 8. Probabilidades

O método `predict()` retorna a classe majoritária da folha alcançada.

O método `predict_proba()` retorna a distribuição das classes entre as amostras de treino presentes naquela folha.

Em um dos exemplos utilizados:

```text
renda: 5000
divida: 4500
numero_atrasos: 5
```

O modelo retornou:

```text
classe: 1
probabilidade da classe 0: 0.3333
probabilidade da classe 1: 0.6667
```

Essas probabilidades não representam probabilidades financeiras calibradas. Elas refletem somente a distribuição observada na folha da árvore treinada com dados sintéticos.

## 9. Explicabilidade

O caminho da decisão foi obtido com:

```python
modelo.decision_path(entrada)
modelo.apply(entrada)
```

Para cada nó percorrido, o sistema recupera:

- A feature analisada.
- O limite aprendido.
- O operador utilizado.
- O valor informado.
- A folha final.

Exemplo:

```text
numero_atrasos > 2.50 (valor informado: 5.00)
divida <= 6958.13 (valor informado: 4500.00)
renda <= 8473.47 (valor informado: 5000.00)
```

Essa explicação mostra o comportamento real da árvore, que pode ser diferente da regra original utilizada para gerar os dados.

## 10. Backend e validação

O backend foi desenvolvido com FastAPI.

Endpoints criados:

```text
GET  /health
POST /predict
GET  /
```

A entrada é validada por um schema Pydantic com as restrições:

```text
renda > 0
divida >= 0
numero_atrasos >= 0
```

Entradas inválidas são rejeitadas com status HTTP `422` antes de chegarem ao modelo.

O schema de saída garante:

- Classe igual a 0 ou 1.
- Probabilidades entre 0 e 1.
- Lista de regras da explicação.
- Identificação da folha final.

## 11. Frontend

O frontend foi desenvolvido com:

- HTML.
- CSS.
- JavaScript.

Ele oferece:

- Formulário para as três features.
- Validação básica no navegador.
- Estado de carregamento.
- Tratamento de erros.
- Classe prevista.
- Probabilidades numéricas.
- Barras visuais.
- Caminho da decisão.
- Estados visuais para menor e maior risco.
- Layout responsivo.
- Tema escuro com imagem de fundo.

O JavaScript envia os dados para a API com `fetch()` e atualiza a interface com a resposta recebida.

## 12. Testes

Foram criados testes para três camadas.

### 12.1. Validação

- Aceitação de entrada válida.
- Rejeição de renda igual a zero.
- Rejeição de dívida negativa.
- Rejeição de número de atrasos negativo.

### 12.2. Predictor

- Classe dentro do conjunto permitido.
- Probabilidades somando aproximadamente 1.
- Previsão esperada para um exemplo conhecido.

### 12.3. API

- Health check.
- Predição válida.
- Presença da explicação.
- Rejeição HTTP de entrada inválida.

Resultado final:

```text
9 passed
```

Também foi realizada validação manual dos seguintes cenários:

```text
classe 1: ok
classe 0: ok
entrada inválida: ok
mobile: ok
```

## 13. Decisões importantes

As principais decisões tomadas durante o desenvolvimento foram:

1. Separar treinamento e inferência.
2. Salvar o modelo em vez de treiná-lo durante cada requisição.
3. Preservar o test set durante o tuning.
4. Escolher profundidade 5 em vez de uma árvore ilimitada.
5. Separar responsabilidades entre módulos.
6. Validar entradas antes de chamar o modelo.
7. Explicar o caminho real da árvore.
8. Criar testes de diferentes camadas.
9. Informar claramente que os dados são sintéticos.
10. Manter o projeto educacional e não apresentá-lo como sistema financeiro real.

## 14. Dificuldades e aprendizados

Durante o projeto, alguns dos principais aprendizados foram:

- Entender a diferença entre valores escalares, arrays, `DataFrame` e `Series`.
- Retornar valores criados dentro de funções.
- Separar features e target.
- Interpretar probabilidades de uma folha.
- Entender que definir uma função não significa executá-la.
- Carregar e reutilizar um artefato treinado.
- Transformar objetos NumPy em tipos compatíveis com JSON.
- Usar schemas como contratos de entrada e saída.
- Integrar frontend, backend e modelo.
- Criar explicações a partir da estrutura interna da árvore.
- Utilizar testes para validar comportamento automaticamente.
- Organizar commits por marcos do projeto.

## 15. Limitações

O projeto possui limitações importantes:

- Dados completamente sintéticos.
- Regra do alvo criada manualmente.
- Nenhuma validação com dados reais.
- Probabilidades não calibradas.
- Ausência de análise de fairness.
- Ausência de monitoramento de drift.
- Ausência de autenticação.
- Ausência de banco de dados.
- Ausência de observabilidade de produção.
- Uso educacional, sem validade para crédito ou finanças.

## 16. Próximos passos

Possíveis evoluções:

- Usar um dataset real.
- Comparar outros algoritmos.
- Avaliar precision, recall e F1.
- Investigar falsos positivos e falsos negativos.
- Aplicar poda por `ccp_alpha`.
- Calibrar probabilidades.
- Criar testes específicos para o explainer.
- Adicionar logging estruturado.
- Criar imagem Docker.
- Configurar integração contínua.
- Publicar uma demonstração online.
- Monitorar qualidade do modelo ao longo do tempo.

## 17. Conclusão

O projeto atingiu o objetivo de integrar Machine Learning e desenvolvimento de software em uma aplicação funcional.

A Decision Tree foi treinada, avaliada, salva e reutilizada por uma API. O sistema valida entradas, retorna probabilidades, explica o caminho da decisão e apresenta os resultados em uma interface responsiva.

O principal aprendizado foi que construir um produto de Machine Learning envolve mais do que treinar um algoritmo. Também exige:

```text
organização
validação
separação de responsabilidades
persistência
integração
testes
documentação
comunicação das limitações
```

O resultado representa uma base inicial para projetos futuros mais próximos de cenários reais, mantendo boas práticas de avaliação e engenharia.