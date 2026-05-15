"""Interpolacao por diferencas divididas de Newton."""

from __future__ import annotations

from pathlib import Path

try:
    from metodos.io_utils import Ponto, salvar_csv
    from metodos.polinomios import (
        avaliar_polinomio,
        formatar_polinomio,
        multiplicar_polinomios,
        somar_polinomios,
    )
except ModuleNotFoundError:
    from io_utils import Ponto, salvar_csv
    from polinomios import (
        avaliar_polinomio,
        formatar_polinomio,
        multiplicar_polinomios,
        somar_polinomios,
    )


def diferencas_divididas(pontos: list[Ponto]) -> list[float]:
    """Calcula os coeficientes da forma de Newton."""
    coeficientes = [y for _, y in pontos]
    n = len(pontos)

    for ordem in range(1, n):
        for i in range(n - 1, ordem - 1, -1):
            xi = pontos[i][0]
            xj = pontos[i - ordem][0]
            coeficientes[i] = (coeficientes[i] - coeficientes[i - 1]) / (xi - xj)

    return coeficientes


def avaliar_newton(pontos: list[Ponto], coeficientes: list[float], x: float) -> float:
    """Avalia o polinomio de Newton no ponto x."""
    n = len(coeficientes)
    valor = coeficientes[n - 1]

    for i in range(n - 2, -1, -1):
        valor = valor * (x - pontos[i][0]) + coeficientes[i]

    return valor


def coeficientes_newton_em_potencias(pontos: list[Ponto]) -> list[float]:
    """Converte a forma de Newton para potencias de x."""
    difs = diferencas_divididas(pontos)
    polinomio = [difs[0]]
    base = [1.0]

    for i in range(1, len(difs)):
        base = multiplicar_polinomios(base, [-pontos[i - 1][0], 1.0])
        termo = [difs[i] * coef for coef in base]
        polinomio = somar_polinomios(polinomio, termo)

    return polinomio


def executar_newton(
    arquivo_entrada: str | Path = "input/interpolacao_newton.txt",
    arquivo_saida: str | Path = "output/interpolacao_newton.csv",
) -> list[float]:
    """Le pontos e consultas de TXT e salva valores interpolados."""
    pontos: list[Ponto] = []
    consultas: list[float] = []

    with Path(arquivo_entrada).open("r", encoding="utf-8") as arquivo:
        modo = "pontos"
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            if linha.lower() == "[consultas]":
                modo = "consultas"
                continue

            partes = linha.replace(",", " ").replace(";", " ").split()
            if modo == "pontos":
                pontos.append((float(partes[0]), float(partes[1])))
            else:
                consultas.append(float(partes[0]))

    difs = diferencas_divididas(pontos)
    coef_potencias = coeficientes_newton_em_potencias(pontos)
    linhas = [("polinomio", formatar_polinomio(coef_potencias))]

    for x in consultas:
        linhas.append((x, avaliar_newton(pontos, difs, x)))

    salvar_csv(arquivo_saida, ("x", "p(x)"), linhas)
    return coef_potencias


if __name__ == "__main__":
    coeficientes = executar_newton()
    print("Interpolacao de Newton concluida.")
    print(f"P(x) = {formatar_polinomio(coeficientes)}")
