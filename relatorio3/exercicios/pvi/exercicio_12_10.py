"""Definição do Exercício 12.10."""

from math import exp


def obter_exercicio_12_10():
    """Retorna os dados do problema de crescimento populacional."""
    p0 = 10000.0
    taxa = 0.075
    return {
        "nome": "Exercício 12.10",
        "variavel": "p",
        "t0": 0.0,
        "tf": 20.0,
        "y0": p0,
        "h": 0.5,
        "taxa": taxa,
        "f": lambda t, p: taxa * p,
        "solucao_exata": lambda t: p0 * exp(taxa * t),
        "descricao": "Crescimento populacional anual modelado por p' = Gp.",
    }
