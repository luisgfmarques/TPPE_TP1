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


def calcula_imposto_efetivo(valortotal, valorimposto):
    return round(valorimposto / valortotal * 100, 2)


def calcula_valor_importo(base_calculo: float):
    valores_limite = [
        {"valor": 1903.98, "aliquota": 0},
        {"valor": 922.67, "aliquota": 7.5 / 100},
        {"valor": 924.40, "aliquota": 15 / 100},
        {"valor": 913.63, "aliquota": 22.5 / 100},
        {"valor": base_calculo - 4664.68, "aliquota": 27.5 / 100},
    ]
    valor_calculo = base_calculo
    valor_imposto = 0
    faixa = 0
    valores = []
    while valor_calculo > 0:
        if valor_calculo >= valores_limite[faixa]["valor"]:
            valor_imposto += (
                valores_limite[faixa]["valor"] * valores_limite[faixa]["aliquota"]
            )
            valores.append(
                {
                    "faixa": faixa + 1,
                    "faixa de base de calculo": valores_limite[faixa]["valor"]
                    if valor_calculo > 0
                    else valor_calculo,
                    "aliquota da faixa": str(valores_limite[faixa]["aliquota"] * 100)
                    + "%",
                    " imposto pago nesta faixa": round(
                        valores_limite[faixa]["valor"]
                        * valores_limite[faixa]["aliquota"],
                        4,
                    ),
                }
            )
            valor_calculo -= valores_limite[faixa]["valor"]
            valor_calculo = round(valor_calculo, 3)
        else:
            print("else")
            valor_imposto += valor_calculo * valores_limite[faixa]["aliquota"]
            valores.append(
                {
                    "faixa": faixa + 1,
                    "faixa de base de calculo": valores_limite[faixa]["valor"]
                    if valor_calculo > valores_limite[faixa]["valor"]
                    else valor_calculo,
                    "aliquota da faixa": str(valores_limite[faixa]["aliquota"] * 100)
                    + "%",
                    " imposto pago nesta faixa": round(
                        valor_calculo * valores_limite[faixa]["aliquota"], 4
                    ),
                }
            )
            valor_calculo = 0
        faixa += 1
    valores.append(
        {
            "faixa": "Total",
            "faixa de base de calculo": base_calculo,
            "aliquota da faixa": "-",
            " imposto total": round(valor_imposto, 4),
        }
    )
    return (round(valor_imposto, 2), valores)


if __name__ == "__main__":
    print(calcula_valor_importo(3000))
