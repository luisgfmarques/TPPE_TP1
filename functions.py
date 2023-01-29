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
        "aliquota da faixa": str(valores_limite[faixa]["aliquota"] * 100) + "%",
        " imposto pago nesta faixa": (
            (
                valores_limite[faixa]["valor"]
                if valor_calculo > valores_limite[faixa]["valor"]
                else valor_calculo
            )
            * valores_limite[faixa]["aliquota"]
        ),
    }


class CalculaValores:
    valores_limite = []
    base_de_calculo = 0

    def __init__(self, base_de_calculo: float):
        self.base_de_calculo = base_de_calculo
        self.valores_limite = [
            {"valor": 1903.98, "aliquota": 0},
            {"valor": 2826.65, "aliquota": 7.5 / 100},
            {"valor": 3751.05, "aliquota": 15 / 100},
            {"valor": 4664.68, "aliquota": 22.5 / 100},
            {"valor": base_de_calculo - 4664.68, "aliquota": 27.5 / 100},
        ]

    def calcula_valor_imposto_faixa(self, valores_limite: list, faixa: int):
        return valores_limite[faixa]["valor"] * valores_limite[faixa]["aliquota"]

    def atualiza_valor_calculo(self, valor_calculo: float, faixa: int):
        valor_calculo -= self.valores_limite[faixa]["valor"]
        return round(valor_calculo, 3)


def adiciona_faixa_total(base_calculo: float, valor_imposto: float):
    return {
        "faixa": "Total",
        "faixa de base de calculo": base_calculo,
        "aliquota da faixa": "-",
        " imposto total": round(valor_imposto, 4),
    }


def calcula_valor_imposto(base_calculo: float):
    valores = CalculaValores(base_calculo)
    valor_calculo = base_calculo
    valor_imposto = 0
    faixa = 0
    valores = []
    while valor_calculo > 0:
        valores.append(append_value(faixa, valores.valores_limite, valor_calculo))
        if valor_calculo >= valores.valores_limite[faixa]["valor"]:
            valor_imposto += CalculaValores.calcula_valor_imposto_faixa(
                valores.valores_limite, faixa
            )
            valor_calculo = CalculaValores.atualiza_valor_calculo(
                valor_calculo, valores.valores_limite, faixa
            )
        else:
            valor_imposto += valor_calculo * valores.valores_limite[faixa]["aliquota"]
            valor_calculo = 0
        faixa += 1
    valores.append(adiciona_faixa_total(base_calculo, valor_imposto))
    return (round(valor_imposto, 2), valores)


if __name__ == "__main__":
    print(calcula_valor_imposto(3000))
