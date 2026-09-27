def explicar_decisao(modelo, entrada):
    caminho = modelo.decision_path(entrada)
    folha = modelo.apply(entrada)[0]

    regras = []
    for no in caminho.indices:
        if no == folha:
            continue

        indice_feature = modelo.tree_.feature[no]
        limite = modelo.tree_.threshold[no]

        nome_feature = entrada.columns[indice_feature]
        valor = entrada.iloc[0, indice_feature]

        if valor <= limite:
            operador = "<="
        else:
            operador = ">"

        regra = (
            f"{nome_feature} {operador} {limite:.2f} "
            f"(valor informado: {valor:.2f})"
        )
        regras.append(regra)

    return {
        "regras": regras,
        "folha": int(folha)
    }