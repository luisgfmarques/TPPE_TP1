import pytest
from ..functions import (
    return_ultima_faixas,
    calcula_imposto_efetivo,
    calcula_valor_imposto,
)


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
    "valortotal, valorimposto, expected_imposto_efetivo",
    [
        (1000, 100, 10),
        (1000, 0, 0),
        (1000, 1000, 100),
        (1000, 500, 50),
        (1000, 200, 20),
    ],
)
def test_calcula_imposto_efetivo(valortotal, valorimposto, expected_imposto_efetivo):
    assert calcula_imposto_efetivo(valortotal, valorimposto) == expected_imposto_efetivo


@pytest.mark.parametrize(
    "base_calculo, valor_imposto",
    [
        (1000, 0),
        (2000, 7.20),
        (3000, 95.20),
        (4000, 263.87),
        (5000, 505.64),
        (6000, 780.64),
        (7000, 1055.64),
        (8000, 1330.64),
        (9000, 1605.64),
        (10000, 1880.64),
    ],
)
def test_calcula_valor_imposto(base_calculo, valor_imposto):
    assert valor_imposto == pytest.approx(calcula_valor_imposto(base_calculo)[0], 0.001)
