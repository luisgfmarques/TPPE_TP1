from .functions import return_ultima_faixas


class PessoaFisicaReceitaFederal:

    name = None
    cpf = None
    rendimentos = []
    soma_rendimentos_tributaveis = 0
    deducao = []
    dependentes = []

    def __init__(self, name: str = None, cpf: str = None):
        self.name = name
        self.cpf = cpf
        self.rendimentos = []
        self.soma_rendimentos_tributaveis = 0
        self.deducao = []
        self.dependentes = []

    def cadastrar_rendimentos(self, valor: float, descricao: str) -> None:
        if valor < 0 or valor is None:
            raise Exception("ValorRendimentoInvalidoException")
        if descricao is None or descricao == "":
            raise Exception("DescricaoEmBrancoException")
        self.rendimentos.append({"valor": valor, "descricao": descricao})
        self.soma_rendimentos_tributaveis += valor

    def insere_deducao(self, valor: float, descricao: str) -> None:
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
        
        total_deducao += len(self.dependentes)*189.59
        return total_deducao

    def base_de_calculo(self):
        total_rendimentos = 0
        for rendimento in self.rendimentos:
            total_rendimentos += rendimento["valor"]
        
        base_calculo = total_rendimentos - self.total_deducoes()
        if base_calculo < 0:
            return  0

        return base_calculo