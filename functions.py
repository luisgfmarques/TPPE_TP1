from math import inf


def return_ultima_faixas(valor):
    valores_limite = [
        {"valor": 1903.98, "aliquota": 0},
        {"valor": 2826.65, "aliquota": 7.5 / 100},
        {"valor": 3751.05, "aliquota": 15 / 100},
        {"valor": 4664.68, "aliquota": 22.5 / 100},
        {"valor": inf, "aliquota": 27.5 / 100},
    ]
    for i in range(len(valores_limite)):
        if valor <= valores_limite[i]["valor"]:
            return {
                "faixa": i + 1,
                "aliquota": valores_limite[i]["aliquota"],
            }
