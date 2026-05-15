"""Leitura simples de funcoes digitadas em arquivos TXT."""

from __future__ import annotations

import math


def criar_funcao(expressao: str):
    """Cria uma funcao f(x) a partir de uma expressao em texto."""
    permitidos = {
        "abs": abs,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "exp": math.exp,
        "log": math.log,
        "pi": math.pi,
        "e": math.e,
    }

    def f(x: float) -> float:
        return float(eval(expressao, {"__builtins__": {}}, {**permitidos, "x": x}))

    return f
