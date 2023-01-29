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


class CalculaValores:
    VALORES_LIMITE = [
        {"valor": 1903.98, "aliquota": 0},
        {"valor": 922.67, "aliquota": 7.5 / 100},
        {"valor": 924.40, "aliquota": 15 / 100},
        {"valor": 913.63, "aliquota": 22.5 / 100},
        {"valor": inf, "aliquota": 27.5 / 100},
    ]
    base_de_calculo = 0
    valor_imposto = 0

    def __init__(self, base_de_calculo: float):
        self.base_de_calculo = base_de_calculo

    def calcula_valor_imposto_faixa(self, faixa: int):
        return (
            self.VALORES_LIMITE[faixa]["valor"] * self.VALORES_LIMITE[faixa]["aliquota"]
        )

    def atualiza_valor_calculo(self, valor_calculo: float, faixa: int):
        valor_calculo -= self.VALORES_LIMITE[faixa]["valor"]
        return round(valor_calculo, 3)

    def append_value(self, faixa: int, valor_calculo: float):
        return {
            "faixa": faixa + 1,
            "faixa de base de calculo": self.VALORES_LIMITE[faixa]["valor"]
            if valor_calculo > self.VALORES_LIMITE[faixa]["valor"]
            else valor_calculo,
            "aliquota da faixa": str(round(self.VALORES_LIMITE[faixa]["aliquota"] * 100, 2))
            + "%",
            " imposto pago nesta faixa": (
                round(
                    (
                        self.VALORES_LIMITE[faixa]["valor"]
                        if valor_calculo > self.VALORES_LIMITE[faixa]["valor"]
                        else valor_calculo
                    )
                    * self.VALORES_LIMITE[faixa]["aliquota"],2
                )
            ),
        }

    def adiciona_faixa_total(self):
        return {
            "faixa": "Total",
            "faixa de base de calculo": self.base_de_calculo,
            "aliquota da faixa": "-",
            " imposto total": round(self.valor_imposto, 2),
        }
    
    def calcula_valor_calculo(self, faixa: int, valor_calculo: float):
        valor_limite_da_faixa = self.VALORES_LIMITE[faixa]["valor"] 
        aliquota_da_faixa = self.VALORES_LIMITE[faixa]["aliquota"]

        if valor_calculo >= valor_limite_da_faixa:
            self.valor_imposto += self.calcula_valor_imposto_faixa(faixa)
            valor_calculo = self.atualiza_valor_calculo(valor_calculo, faixa)
        else:
            self.valor_imposto += valor_calculo * aliquota_da_faixa
            valor_calculo = 0
        
        return valor_calculo
    
    def calcula_valor_imposto(self):
        valor_calculo = self.base_de_calculo        
        faixa = 0
        valores = []
        while valor_calculo > 0:
            valores.append(self.append_value(faixa, valor_calculo))
            valor_calculo = self.calcula_valor_calculo(faixa, valor_calculo)
            faixa += 1
        valores.append(self.adiciona_faixa_total())
        return (round(self.valor_imposto, 2), valores)

if __name__ == "__main__":
    pass
