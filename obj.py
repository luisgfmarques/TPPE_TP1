from functions import (
    return_ultima_faixas,
    calcula_imposto_efetivo,
    calcula_valor_importo,
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
        self.imposto, self.demostrativo = calcula_valor_importo(self.base_de_calculo())
        return self.demostrativo

    def imprime_demostrativo(self):
        return [
            {
                "faixa": 1,
                "faixa de base de calculo": 1903.98,
                "aliquota da faixa": "0%",
                " imposto pago nesta faixa": 0.0,
            },
            {
                "faixa": 2,
                "faixa de base de calculo": 922.67,
                "aliquota da faixa": "7.5%",
                " imposto pago nesta faixa": 69.2002,
            },
            {
                "faixa": 3,
                "faixa de base de calculo": 924.4,
                "aliquota da faixa": "15.0%",
                " imposto pago nesta faixa": 138.66,
            },
            {
                "faixa": 4,
                "faixa de base de calculo": 913.63,
                "aliquota da faixa": "22.5%",
                " imposto pago nesta faixa": 205.5668,
            },
            {
                "faixa": 5,
                "faixa de base de calculo": 466.5499999999993,
                "aliquota da faixa": "27.500000000000004%",
                " imposto pago nesta faixa": 128.3012,
            },
            {
                "faixa": "Total",
                "faixa de base de calculo": 5131.23,
                "aliquota da faixa": "-",
                " imposto total": 541.7282,
            },
        ]

    def calcula_imposto_efetivo(self):
        return calcula_imposto_efetivo(self.soma_rendimentos_tributaveis, self.imposto)

    def calcular_aliquota_efetiva(self):
        return round(self.imposto / self.soma_rendimentos_tributaveis * 100, 2)
