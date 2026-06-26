"""Problema de condução de calor em uma haste."""

from math import exp


def solucao_analitica_temperatura(x):
    """Solução analítica usada como referência."""
    return 73.4523 * exp(0.1 * x) - 53.4523 * exp(-0.1 * x) + 20


def obter_problema_haste():
    """Retorna os parâmetros do problema de valor de contorno."""
    return {
        "nome": "Problema de valor de contorno da haste",
        "ta": 20.0,
        "t1": 40.0,
        "t2": 200.0,
        "h_linha": 0.01,
        "comprimento": 10.0,
        "n_internos": 10,
        "chute_1": 10.0,
        "chute_2": 20.0,
        "solucao_analitica": solucao_analitica_temperatura,
    }
