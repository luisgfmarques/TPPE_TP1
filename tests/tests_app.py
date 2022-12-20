import pytest
from ..functions import return_ultima_faixas
from ..obj import PessoaFisicaReceitaFederal

@pytest.fixture
def pessoa():
    pessoa = PessoaFisicaReceitaFederal()
    return pessoa

@pytest.mark.parametrize(
    "valor, expected_aliquota,expected_faixa",
    [
        (2000, 0.075, 2),
        (50000, 0.275, 5),
        (100000, 0.275, 5),
        (1800, 0, 1),
        (1903.98, 0, 1),
        (1903.99, 0.075, 2),
        (2826.65, 0.075, 2),
        (2826.66, 0.15, 3),
        (3751.05, 0.15, 3),
        (3751.06, 0.225, 4),
        (4664.68, 0.225, 4),
    ],
)
def test_return_ultima_faixa(valor, expected_aliquota, expected_faixa):
    retorno = return_ultima_faixas(valor)
    assert retorno["aliquota"] == expected_aliquota
    assert retorno["faixa"] == expected_faixa


@pytest.mark.parametrize(
    ("valor", "descricao"),
    [(1000, "Salario"), (0000.1, "Alugueis"), (999999999, "VENDA"), (20202.0, "aulas")],
)
def test_cadastro_rendimentos(pessoa, valor, descricao):
    pessoa.cadastrar_rendimentos(valor, descricao)
    assert pessoa.rendimentos[-1]["valor"] == valor
    assert pessoa.rendimentos[-1]["descricao"] == descricao


@pytest.mark.parametrize(
    ("valor", "descricao", "expected_exception"),
    [
        (-1000, "Salario", "ValorRendimentoInvalidoException"),
        (1000, "", "DescricaoEmBrancoException"),
        (None, "Salario", "ValorRendimentoInvalidoException"),
        (1000, None, "DescricaoEmBrancoException"),
    ],
)
def test_cadastro_rendimento_exception(pessoa, valor, descricao, expected_exception):
    with pytest.raises(Exception):
        pessoa.cadastrar_rendimentos(valor, descricao)
        assert Exception == expected_exception


def test_soma_rendimentos(pessoa):
    pessoa.cadastrar_rendimentos(1000, "Salario")
    pessoa.cadastrar_rendimentos(1000, "Salario")
    pessoa.cadastrar_rendimentos(1000, "Salario")
    pessoa.cadastrar_rendimentos(1000, "Salario")
    assert pessoa.soma_rendimentos_tributaveis == 4000


@pytest.mark.parametrize(
    ("valor", "descricao"),
    [
        (1000, "previdencia privada"),
        (1000, "pensao alimenticia"),
        (1000, "funpresp")
    ],
)
def test_insere_deducao(pessoa, valor, descricao):
    pessoa.insere_deducao(valor, descricao)
    assert pessoa.deducao[-1]["valor"] == valor
    assert pessoa.deducao[-1]["descricao"] == descricao

@pytest.mark.parametrize(
    ("valor", "descricao", "expected_exception"),
    [
        (-1000, "previdencia privada", "ValorDeducaoInvalidoException"),
        (1000, "", "DescricaoEmBrancoException"),
        (None, "previdencia privada", "ValorDeducaoInvalidoException"),
        (1000, None, "DescricaoEmBrancoException"),
    ],
)
def test_insere_deducao_exception(pessoa, valor, descricao, expected_exception):
    with pytest.raises(Exception):
        pessoa.insere_deducao(valor, descricao)
        assert Exception == expected_exception

@pytest.mark.parametrize(
    ("nome", "data_nascimento"),
    [
        ("Rafael Fernandes", "01/12/2007"),
        ("Bruno Dias", "01/08/2008"),
        ("Jonas Alves", "02/04/2009")
    ],
)
def test_cadastra_dependentes(pessoa, nome, data_nascimento):
    pessoa.cadastra_dependentes(nome, data_nascimento)
    assert pessoa.dependentes[-1]["nome"] == nome
    assert pessoa.dependentes[-1]["data_nascimento"] == data_nascimento

@pytest.mark.parametrize(
    ("nome", "data_nascimento", "expected_exception"),
    [
        ("", "01/01/2018", "NomeEmBrancoException"),
        (None, "01/01/2018", "NomeEmBrancoException")
    ],
)
def test_cadastra_dependentes_exception(pessoa, nome, data_nascimento, expected_exception):
    with pytest.raises(Exception):
        pessoa.cadastra_dependentes(nome, data_nascimento)
        assert Exception == expected_exception


@pytest.mark.parametrize(
    ("deducoes", "dependentes"),
    [
        ([(1000, "funpresp"), (1000, "Pensao alimenticia"), (1000, "previdencia privada")],
        [("Rafael Fernandes", "01/12/2007"), ("Bruno Dias", "01/08/2008"), ("Jonas Alves", "02/04/2009")]),
        ([(100, "funpresp"), (2000, "Pensao alimenticia"), (5000, "previdencia privada")],
        [("Rafael Dias", "01/12/2007"), ("Bruno Fernandes", "01/08/2008"), ("Jonas Lopes", "02/04/2009")])
    ],
)
def test_total_deducoes(pessoa, deducoes, dependentes):
    total = 0
    for deducao in deducoes:
        pessoa.insere_deducao(deducao[0], deducao[1])
        total += deducao[0]
        assert pessoa.total_deducoes() == float("%0.2f"%total)
    
    for dependente in dependentes:
        pessoa.cadastra_dependentes(dependente[0], dependente[1])
        total += 189.59
        assert pessoa.total_deducoes() == float("%0.2f"%total)

def test_base_calculo(pessoa):
    pessoa.cadastrar_rendimentos(3500, "Salario")
    pessoa.cadastrar_rendimentos(1500, "Aluguel")
    pessoa.insere_deducao(1000, "Pensao alimenticia")
    pessoa.insere_deducao(1000, "Previdencia privada")
    pessoa.cadastra_dependentes("Rafael Dias", "01/12/2007")
    pessoa.cadastra_dependentes("Bruno Fernandes", "01/08/2008")
    assert float("%0.2f"%pessoa.base_de_calculo()) == 2620.82

def test_base_calculo_dois_asserts(pessoa):
    pessoa.cadastrar_rendimentos(3500, "Salario")
    pessoa.cadastrar_rendimentos(1500, "Aluguel")
    pessoa.insere_deducao(1000, "Pensao alimenticia")
    pessoa.insere_deducao(1000, "Previdencia privada")
    pessoa.cadastra_dependentes("Rafael Dias", "01/12/2007")
    pessoa.cadastra_dependentes("Bruno Fernandes", "01/08/2008")
    assert float("%0.2f"%pessoa.base_de_calculo()) == 2620.82
    pessoa.cadastrar_rendimentos(1500, "Aluguel")
    pessoa.insere_deducao(1000, "Pensao alimenticia")
    pessoa.cadastra_dependentes("Bruno Fernandes", "01/08/2008")
    assert float("%0.2f"%pessoa.base_de_calculo()) == 2931.23