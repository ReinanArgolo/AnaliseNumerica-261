"""Funcoes auxiliares para trabalhar com polinomios."""

from __future__ import annotations


def avaliar_polinomio(coeficientes: list[float], x: float) -> float:
    """Avalia c0 + c1*x + c2*x^2 + ... no ponto x."""
    valor = 0.0
    potencia = 1.0

    for coeficiente in coeficientes:
        valor += coeficiente * potencia
        potencia *= x

    return valor


def somar_polinomios(p: list[float], q: list[float]) -> list[float]:
    """Soma dois polinomios escritos por coeficientes."""
    tamanho = max(len(p), len(q))
    resultado = [0.0 for _ in range(tamanho)]

    for i in range(tamanho):
        if i < len(p):
            resultado[i] += p[i]
        if i < len(q):
            resultado[i] += q[i]

    return resultado


def multiplicar_polinomios(p: list[float], q: list[float]) -> list[float]:
    """Multiplica dois polinomios escritos por coeficientes."""
    resultado = [0.0 for _ in range(len(p) + len(q) - 1)]

    for i in range(len(p)):
        for j in range(len(q)):
            resultado[i + j] += p[i] * q[j]

    return resultado


def formatar_polinomio(coeficientes: list[float]) -> str:
    """Monta uma representacao simples do polinomio ajustado."""
    partes: list[str] = []

    for grau, coeficiente in enumerate(coeficientes):
        if grau == 0:
            partes.append(f"{coeficiente:.6g}")
        elif grau == 1:
            partes.append(f"{coeficiente:.6g}*x")
        else:
            partes.append(f"{coeficiente:.6g}*x^{grau}")

    return " + ".join(partes)
