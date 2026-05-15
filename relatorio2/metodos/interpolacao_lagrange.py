"""Interpolacao por polinomios de Lagrange."""

from __future__ import annotations

from pathlib import Path

try:
    from metodos.io_utils import Ponto, ler_pontos_txt, salvar_csv
    from metodos.polinomios import (
        avaliar_polinomio,
        formatar_polinomio,
        multiplicar_polinomios,
        somar_polinomios,
    )
except ModuleNotFoundError:
    from io_utils import Ponto, ler_pontos_txt, salvar_csv
    from polinomios import (
        avaliar_polinomio,
        formatar_polinomio,
        multiplicar_polinomios,
        somar_polinomios,
    )


def coeficientes_lagrange(pontos: list[Ponto]) -> list[float]:
    """Monta o polinomio interpolador usando a forma de Lagrange."""
    polinomio = [0.0]

    for i, (xi, yi) in enumerate(pontos):
        base = [1.0]
        denominador = 1.0

        for j, (xj, _) in enumerate(pontos):
            if i == j:
                continue

            base = multiplicar_polinomios(base, [-xj, 1.0])
            denominador *= xi - xj

        termo = [(yi / denominador) * coef for coef in base]
        polinomio = somar_polinomios(polinomio, termo)

    return polinomio


def interpolar_lagrange(pontos: list[Ponto], x: float) -> float:
    """Calcula o valor interpolado em x."""
    coeficientes = coeficientes_lagrange(pontos)
    return avaliar_polinomio(coeficientes, x)


def executar_lagrange(
    arquivo_entrada: str | Path = "input/interpolacao_lagrange.txt",
    arquivo_saida: str | Path = "output/interpolacao_lagrange.csv",
) -> list[float]:
    """Le pontos e valores de consulta de um TXT e salva resultado em CSV."""
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

    coeficientes = coeficientes_lagrange(pontos)
    linhas = [("polinomio", formatar_polinomio(coeficientes))]

    for x in consultas:
        linhas.append((x, avaliar_polinomio(coeficientes, x)))

    salvar_csv(arquivo_saida, ("x", "p(x)"), linhas)
    return coeficientes


if __name__ == "__main__":
    coeficientes = executar_lagrange()
    print("Interpolacao de Lagrange concluida.")
    print(f"P(x) = {formatar_polinomio(coeficientes)}")
