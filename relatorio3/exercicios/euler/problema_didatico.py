"""Problema didático para testar o Método de Euler."""

from math import exp


def problema_euler_didatico():
    """Retorna um PVI simples com solução exata conhecida.

    O problema é dy/dt = y, com y(0) = 1.
    A solução exata é y(t) = e^t.
    """
    return {
        "nome": "Problema didático do Método de Euler",
        "descricao": "dy/dt = y, com y(0) = 1",
        "f": lambda t, y: y,
        "t0": 0.0,
        "y0": 1.0,
        "h": 0.1,
        "n": 10,
        "solucao_exata": exp,
    }
