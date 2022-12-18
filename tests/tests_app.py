import pytest
from ..functions import return_ultima_faixas


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
