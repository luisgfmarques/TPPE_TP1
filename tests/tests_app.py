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


def test_cadastro_rendimentos(pessoa):
    pessoa.cadastrar_rendimentos(1000, "Salario")
    pessoa.cadastrar_rendimentos(2000, "Alugueis")
    assert pessoa.rendimentos[0]["valor"] == 1000
    assert pessoa.rendimentos[1]["valor"] == 2000
    assert pessoa.soma_rendimentos_tributaveis == 3000
