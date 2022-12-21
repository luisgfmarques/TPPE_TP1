import pytest
from ..obj import PessoaFisicaReceitaFederal


@pytest.fixture
def pessoa():
    pessoa = PessoaFisicaReceitaFederal()
    return pessoa


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
    [(1000, "previdencia privada"), (1000, "pensao alimenticia"), (1000, "funpresp")],
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
        ("Jonas Alves", "02/04/2009"),
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
        (None, "01/01/2018", "NomeEmBrancoException"),
    ],
)
def test_cadastra_dependentes_exception(
    pessoa, nome, data_nascimento, expected_exception
):
    with pytest.raises(Exception):
        pessoa.cadastra_dependentes(nome, data_nascimento)
        assert Exception == expected_exception


@pytest.mark.parametrize(
    ("deducoes", "dependentes"),
    [
        (
            [
                (1000, "funpresp"),
                (1000, "Pensao alimenticia"),
                (1000, "previdencia privada"),
            ],
            [
                ("Rafael Fernandes", "01/12/2007"),
                ("Bruno Dias", "01/08/2008"),
                ("Jonas Alves", "02/04/2009"),
            ],
        ),
        (
            [
                (100, "funpresp"),
                (2000, "Pensao alimenticia"),
                (5000, "previdencia privada"),
            ],
            [
                ("Rafael Dias", "01/12/2007"),
                ("Bruno Fernandes", "01/08/2008"),
                ("Jonas Lopes", "02/04/2009"),
            ],
        ),
    ],
)
def test_total_deducoes(pessoa, deducoes, dependentes):
    total = 0
    for deducao in deducoes:
        pessoa.insere_deducao(deducao[0], deducao[1])
        total += deducao[0]
        assert pessoa.total_deducoes() == float("%0.2f" % total)

    for dependente in dependentes:
        pessoa.cadastra_dependentes(dependente[0], dependente[1])
        total += 189.59
        assert pessoa.total_deducoes() == float("%0.2f" % total)


@pytest.mark.parametrize(
    ("rendimentos", "deducoes", "dependentes"),
    [
        (
            [(3000, "Salario"), (1500, "aluguel"), (1500, "Juros")],
            [
                (1000, "funpresp"),
                (1000, "Pensao alimenticia"),
                (1000, "previdencia privada"),
            ],
            [
                ("Rafael Fernandes", "01/12/2007"),
                ("Bruno Dias", "01/08/2008"),
                ("Jonas Alves", "02/04/2009"),
            ],
        ),
        (
            [(3500, "Salario"), (1200, "aluguel"), (500, "Juros")],
            [
                (100, "funpresp"),
                (2000, "Pensao alimenticia"),
                (5000, "previdencia privada"),
            ],
            [
                ("Rafael Dias", "01/12/2007"),
                ("Bruno Fernandes", "01/08/2008"),
                ("Jonas Lopes", "02/04/2009"),
            ],
        ),
    ],
)
def test_base_de_calculo(pessoa, rendimentos, deducoes, dependentes):
    for rendimento in rendimentos:
        pessoa.cadastrar_rendimentos(rendimento[0], rendimento[1])
        base_de_calculo = pessoa.soma_rendimentos_tributaveis
        assert pessoa.base_de_calculo() == float("%0.2f" % base_de_calculo)

    for deducao in deducoes:
        pessoa.insere_deducao(deducao[0], deducao[1])
        base_de_calculo = pessoa.soma_rendimentos_tributaveis - pessoa.total_deducoes()
        if base_de_calculo < 0:
            base_de_calculo = 0
        assert pessoa.base_de_calculo() == float("%0.2f" % base_de_calculo)

    for dependente in dependentes:
        pessoa.cadastra_dependentes(dependente[0], dependente[1])
        base_de_calculo = pessoa.soma_rendimentos_tributaveis - pessoa.total_deducoes()
        if base_de_calculo < 0:
            base_de_calculo = 0
        assert pessoa.base_de_calculo() == float("%0.2f" % base_de_calculo)


def test_base_de_calculo_exception(pessoa):
    with pytest.raises(Exception):
        pessoa.base_de_calculo()
        assert Exception == "BaseDeCalculoException"


@pytest.mark.parametrize(
    ("rendimentos", "deducoes", "dependentes", "imposto"),
    [
        (
            [(3000, "Salario"), (1500, "aluguel"), (1500, "Juros")],
            [
                (1000, "funpresp"),
                (1000, "Pensao alimenticia"),
                (1000, "previdencia privada"),
            ],
            [
                ("Rafael Fernandes", "01/12/2007"),
                ("Bruno Dias", "01/08/2008"),
                ("Jonas Alves", "02/04/2009"),
            ],
            39.54,
        ),
        (
            [(3500, "Salario"), (1200, "aluguel"), (500, "Juros")],
            [
                (100, "funpresp"),
                (2000, "Pensao alimenticia"),
                (5000, "previdencia privada"),
            ],
            [
                ("Rafael Dias", "01/12/2007"),
                ("Bruno Fernandes", "01/08/2008"),
                ("Jonas Lopes", "02/04/2009"),
            ],
            0.0,
        ),
        (
            [(30000, "Salario"), (5000, "aluguel"), (3000, "dividendos")],
            [
                (2000, "Pensao alimenticia"),
                (2000, "previdencia privada"),
                (3000, "debitos com saude privada"),
            ],
            [
                ("Rafael Bandeirantes", "29/12/2017"),
                ("Jonas Lopes Batista", "02/04/2009"),
            ],
            7551.37,
        ),
    ],
)
def test_calcula_imposto(pessoa, rendimentos, deducoes, dependentes, imposto):
    [pessoa.cadastrar_rendimentos(valor, descricao) for valor, descricao in rendimentos]
    [pessoa.insere_deducao(dedu, text) for dedu, text in deducoes]
    [
        pessoa.cadastra_dependentes(nome, data_nascimento)
        for nome, data_nascimento in dependentes
    ]
    pessoa.calcula_imposto()
    assert pessoa.imposto == float("%0.2f" % imposto)


@pytest.mark.parametrize(
    ("rendimentos", "deducoes", "dependentes", "aliquota_efetiva"),
    [
        (
            [(3000, "Salario"), (1500, "aluguel"), (1500, "Juros")],
            [
                (1000, "funpresp"),
                (1000, "Pensao alimenticia"),
                (1000, "previdencia privada"),
            ],
            [
                ("Rafael Fernandes", "01/12/2007"),
                ("Bruno Dias", "01/08/2008"),
                ("Jonas Alves", "02/04/2009"),
            ],
            0.66,
        ),
        (
            [(3500, "Salario"), (1200, "aluguel"), (500, "Juros")],
            [
                (100, "funpresp"),
                (2000, "Pensao alimenticia"),
                (5000, "previdencia privada"),
            ],
            [
                ("Rafael Dias", "01/12/2007"),
                ("Bruno Fernandes", "01/08/2008"),
                ("Jonas Lopes", "02/04/2009"),
            ],
            0.0,
        ),
        (
            [(30000, "Salario"), (5000, "aluguel"), (3000, "dividendos")],
            [
                (2000, "Pensao alimenticia"),
                (2000, "previdencia privada"),
                (3000, "debitos com saude privada"),
            ],
            [
                ("Rafael Bandeirantes", "29/12/2017"),
                ("Jonas Lopes Batista", "02/04/2009"),
            ],
            19.87,
        ),
    ],
)
def test_calcular_aliquota_efeticva(
    pessoa, rendimentos, deducoes, dependentes, aliquota_efetiva
):
    [pessoa.cadastrar_rendimentos(valor, descricao) for valor, descricao in rendimentos]
    [pessoa.insere_deducao(dedu, text) for dedu, text in deducoes]
    [
        pessoa.cadastra_dependentes(nome, data_nascimento)
        for nome, data_nascimento in dependentes
    ]
    pessoa.calcula_imposto()
    assert pessoa.calcular_aliquota_efetiva() == float("%0.2f" % aliquota_efetiva)
