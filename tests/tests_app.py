import pytest
from ..functions import return_ultima_faixas


def test_return_ultima_faixa():
    assert return_ultima_faixas(2000)["aliquota"] == 7.5
    assert return_ultima_faixas(2000)["faixa"] == 2
    assert return_ultima_faixas(50000)["aliquota"] == 27.5
    assert return_ultima_faixas(50000)["faixa"] == 5
