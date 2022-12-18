import pytest
from ..functions import return_faixas


def test_return_faixas():
    assert return_faixas(2000)["aliquota"] == 7.5
    assert return_faixas(2000)["faixa"] == 2
