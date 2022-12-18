def return_ultima_faixas(valor):
    valores_limite = [1903.98, 2826.65, 3751.05, 4664.68]
    faixas = [1, 2, 3, 4, 5]
    aliquotas = [0, 7.5, 15, 22.5, 27.5]
    for i in range(len(valores_limite)):
        if valor <= valores_limite[i]:
            return {
                "faixa": faixas[i],
                "aliquota": aliquotas[i],
            }
    return {
        "faixa": faixas[-1],
        "aliquota": aliquotas[-1],
    }
