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


def append_value(faixa: int, valores_limite: list, valor_calculo: float):
    return {
        "faixa": faixa + 1,
        "faixa de base de calculo": valores_limite[faixa]["valor"]
        if valor_calculo > valores_limite[faixa]["valor"]
        else valor_calculo,
        "aliquota da faixa": str(round(valores_limite[faixa]["aliquota"] * 100, 2))
        + "%",
        " imposto pago nesta faixa": (
            round(
                (
                    valores_limite[faixa]["valor"]
                    if valor_calculo > valores_limite[faixa]["valor"]
                    else valor_calculo
                )
                * valores_limite[faixa]["aliquota"],2
            )
        ),
    }


class CalculaValores:
    VALORES_LIMITE = [
        {"valor": 1903.98, "aliquota": 0},
        {"valor": 922.67, "aliquota": 7.5 / 100},
        {"valor": 924.40, "aliquota": 15 / 100},
        {"valor": 913.63, "aliquota": 22.5 / 100},
        {"valor": inf, "aliquota": 27.5 / 100},
    ]
    base_de_calculo = 0
    valor_calculo = 0

    def __init__(self, base_de_calculo: float, valor_calculo: float = 0):
        self.base_de_calculo = base_de_calculo
        self.valor_calculo = valor_calculo if valor_calculo else base_de_calculo

    def calcula_valor_imposto_faixa(self, faixa: int):
        return (
            self.VALORES_LIMITE[faixa]["valor"] * self.VALORES_LIMITE[faixa]["aliquota"]
        )

    def atualiza_valor_calculo(self, valor_calculo: float, faixa: int):
        valor_calculo -= self.VALORES_LIMITE[faixa]["valor"]
        return round(valor_calculo, 3)


def adiciona_faixa_total(base_calculo: float, valor_imposto: float):
    return {
        "faixa": "Total",
        "faixa de base de calculo": base_calculo,
        "aliquota da faixa": "-",
        " imposto total": round(valor_imposto, 2),
    }


def calcula_valor_imposto(base_calculo: float):
    calcula = CalculaValores(base_calculo)
    valor_calculo = base_calculo
    valor_imposto = 0
    faixa = 0
    valores = []
    while valor_calculo > 0:
        valores.append(append_value(faixa, calcula.VALORES_LIMITE, valor_calculo))
        if valor_calculo >= calcula.VALORES_LIMITE[faixa]["valor"]:
            valor_imposto += calcula.calcula_valor_imposto_faixa(faixa)
            valor_calculo = calcula.atualiza_valor_calculo(valor_calculo, faixa)
        else:
            valor_imposto += valor_calculo * calcula.VALORES_LIMITE[faixa]["aliquota"]
            valor_calculo = 0
        faixa += 1
    valores.append(adiciona_faixa_total(base_calculo, valor_imposto))
    return (round(valor_imposto, 2), valores)


if __name__ == "__main__":
    pass
