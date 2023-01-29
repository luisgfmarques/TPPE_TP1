try:
    from .functions import (
        return_ultima_faixas,
        calcula_imposto_efetivo,
        CalculaValores,
    )
except (ModuleNotFoundError, ImportError):
    from functions import (
        return_ultima_faixas,
        calcula_imposto_efetivo,
        CalculaValores,
    )


class PessoaFisicaReceitaFederal:

    name = None
    cpf = None
    rendimentos = []
    soma_rendimentos_tributaveis = 0
    deducao = []
    dependentes = []
    imposto = 0

    def __init__(self, name: str = None, cpf: str = None):
        self.name = name
        self.cpf = cpf
        self.rendimentos = []
        self.soma_rendimentos_tributaveis = 0
        self.deducao = []
        self.dependentes = []
        self.demostrativo = None

    def cadastrar_rendimentos(self, valor: float, descricao: str):
        if valor < 0 or valor is None:
            raise Exception("ValorRendimentoInvalidoException")
        if descricao is None or descricao == "":
            raise Exception("DescricaoEmBrancoException")
        self.rendimentos.append({"valor": valor, "descricao": descricao})
        self.soma_rendimentos_tributaveis += valor

    def insere_deducao(self, valor: float, descricao: str):
        if valor < 0 or valor is None:
            raise Exception("ValorDeducaoInvalidoException")
        if descricao is None or descricao == "":
            raise Exception("DescricaoEmBrancoException")
        self.deducao.append({"valor": valor, "descricao": descricao})

    def cadastra_dependentes(self, nome: str, data_nascimento: str):
        if nome is None or nome == "":
            raise Exception("NomeEmBrancoException")
        self.dependentes.append({"nome": nome, "data_nascimento": data_nascimento})

    def total_deducoes(self):
        total_deducao = 0
        for val in self.deducao:
            total_deducao += val["valor"]

        total_deducao += len(self.dependentes) * 189.59
        return total_deducao

    def base_de_calculo(self):
        base_calculo = self.soma_rendimentos_tributaveis - self.total_deducoes()
        if base_calculo < 0:
            return 0

        return base_calculo

    def calcula_imposto(self):
        calc = CalculaValores(self.base_de_calculo())
        self.imposto, self.demostrativo = calc.calcula_valor_imposto()
        return self.demostrativo

    def imprime_demostrativo(self):
        return self.demostrativo

    def calcula_imposto_efetivo(self):
        return calcula_imposto_efetivo(self.soma_rendimentos_tributaveis, self.imposto)

    def calcular_aliquota_efetiva(self):
        return round(self.imposto / self.soma_rendimentos_tributaveis * 100, 2)


class CalculaValorImposto:
    base_calculo = 0
    valores_limite = [
        {"valor": 1903.98, "aliquota": 0},
        {"valor": 922.67, "aliquota": 7.5 / 100},
        {"valor": 924.40, "aliquota": 15 / 100},
        {"valor": 913.63, "aliquota": 22.5 / 100},
        {"valor": base_calculo - 4664.68, "aliquota": 27.5 / 100},
    ]
    valores = []
    valor_imposto = 0

    def __init__(self, base_calculo: int = 0):
        self.base_calculo = base_calculo
        self.valores_limite = [
            {"valor": 1903.98, "aliquota": 0},
            {"valor": 922.67, "aliquota": 7.5 / 100},
            {"valor": 924.40, "aliquota": 15 / 100},
            {"valor": 913.63, "aliquota": 22.5 / 100},
            {"valor": base_calculo - 4664.68, "aliquota": 27.5 / 100},
        ]
        self.valores = []
        self.valor_imposto = 0

    def append_value(self, faixa: int, valor_calculo: float):
        return {
            "faixa": faixa + 1,
            "faixa de base de calculo": self.valores_limite[faixa]["valor"]
            if valor_calculo > self.valores_limite[faixa]["valor"]
            else valor_calculo,
            "aliquota da faixa": str(self.valores_limite[faixa]["aliquota"] * 100)
            + "%",
            " imposto pago nesta faixa": (
                (
                    self.valores_limite[faixa]["valor"]
                    if valor_calculo > self.valores_limite[faixa]["valor"]
                    else valor_calculo
                )
                * self.valores_limite[faixa]["aliquota"]
            ),
        }

    def calcula_valor_imposto_faixa(self, faixa: int):
        return (
            self.valores_limite[faixa]["valor"] * self.valores_limite[faixa]["aliquota"]
        )

    def atualiza_valor_calculo(self, valor_calculo: float, faixa: int):
        valor_calculo -= self.valores_limite[faixa]["valor"]
        return round(valor_calculo, 3)

    def adiciona_faixa_total(self):
        return {
            "faixa": "Total",
            "faixa de base de calculo": self.base_calculo,
            "aliquota da faixa": "-",
            " imposto total": round(self.valor_imposto, 4),
        }

    def calcula_valor_imposto(self):
        valor_calculo = self.base_calculo
        faixa = 0

        while valor_calculo > 0:
            self.valores.append(self.append_value(faixa, valor_calculo))
            if valor_calculo >= self.valores_limite[faixa]["valor"]:
                self.valor_imposto += self.calcula_valor_imposto_faixa(faixa)
                valor_calculo = self.atualiza_valor_calculo(valor_calculo, faixa)
            else:
                self.valor_imposto += (
                    valor_calculo * self.valores_limite[faixa]["aliquota"]
                )
                valor_calculo = 0
            faixa += 1
        self.valores.append(self.adiciona_faixa_total())
        return (round(self.valor_imposto, 2), self.valores)
