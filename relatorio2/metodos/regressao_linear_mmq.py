"""Regressao linear por minimos quadrados.

O modulo implementa as formulas do metodo sem usar bibliotecas prontas de
regressao. As bibliotecas importadas sao apenas auxiliares da linguagem.
"""

from __future__ import annotations

import math
from pathlib import Path

try:
    from metodos.io_utils import Ponto, ler_pontos_txt, salvar_csv
except ModuleNotFoundError:
    # Permite executar este arquivo diretamente pela pasta metodos/.
    from io_utils import Ponto, ler_pontos_txt, salvar_csv


def ler_dados_txt(caminho_arquivo: str | Path) -> list[Ponto]:
    """Mantem compatibilidade com o nome usado nos scripts antigos."""
    return ler_pontos_txt(caminho_arquivo)


def calcular_regressao_mmq(pontos: list[Ponto]) -> tuple[float, float]:
    """Calcula os coeficientes ``a`` e ``b`` da reta ``y = ax + b``."""
    n = len(pontos)
    if n == 0:
        raise ValueError("A regressao precisa de pelo menos um ponto.")

    soma_x = soma_y = soma_xy = soma_x2 = 0.0
    for x, y in pontos:
        soma_x += x
        soma_y += y
        soma_xy += x * y
        soma_x2 += x * x

    denominador = n * soma_x2 - soma_x * soma_x
    if denominador == 0:
        raise ValueError("Nao e possivel ajustar reta: todos os valores de x sao iguais.")

    a = (n * soma_xy - soma_x * soma_y) / denominador
    b = (soma_y - a * soma_x) / n

    return a, b


def calcular_coeficiente_correlacao(pontos: list[Ponto], *_: float) -> float:
    """Calcula o coeficiente de correlacao de Pearson."""
    n = len(pontos)
    if n == 0:
        raise ValueError("O calculo da correlacao precisa de pelo menos um ponto.")

    soma_x = soma_y = soma_xy = soma_x2 = soma_y2 = 0.0
    for x, y in pontos:
        soma_x += x
        soma_y += y
        soma_xy += x * y
        soma_x2 += x * x
        soma_y2 += y * y

    numerador = n * soma_xy - soma_x * soma_y
    variacao_x = n * soma_x2 - soma_x * soma_x
    variacao_y = n * soma_y2 - soma_y * soma_y
    denominador = math.sqrt(variacao_x * variacao_y)

    if denominador == 0:
        return 0.0

    return numerador / denominador


def calcular_coeficiente_determinacao(pontos: list[Ponto], a: float, b: float) -> float:
    """Calcula R2 a partir da soma total e da soma residual dos quadrados."""
    n = len(pontos)
    if n == 0:
        raise ValueError("O calculo de R2 precisa de pelo menos um ponto.")

    media_y = sum(y for _, y in pontos) / n
    soma_total = sum((y - media_y) ** 2 for _, y in pontos)
    soma_residual = sum((y - (a * x + b)) ** 2 for x, y in pontos)

    if soma_total == 0:
        return 1.0 if soma_residual == 0 else 0.0

    return 1.0 - soma_residual / soma_total


def calcular_desvio_padrao_residuos(pontos: list[Ponto], a: float, b: float) -> float:
    """Calcula o desvio padrao amostral dos residuos da regressao."""
    n = len(pontos)
    if n <= 2:
        return 0.0

    soma_quadrados_residuos = sum((y - (a * x + b)) ** 2 for x, y in pontos)
    variancia_residuos = soma_quadrados_residuos / (n - 2)

    return math.sqrt(variancia_residuos)


def salvar_resultados_csv(
    caminho_arquivo: str | Path,
    pontos: list[Ponto],
    a: float,
    b: float,
    r: float | None = None,
    r2: float | None = None,
    desvio_padrao_residuos: float | None = None,
) -> None:
    """Salva pontos, predicoes, residuos e indicadores em CSV UTF-8."""
    linhas: list[tuple[object, ...]] = []

    for x, y in pontos:
        y_predito = a * x + b
        residuo = y - y_predito
        linhas.append((x, y, y_predito, residuo))

    linhas.extend(
        [
            (),
            ("Coeficiente Angular (a)", a),
            ("Coeficiente Linear (b)", b),
            ("Coeficiente de Correlacao (r)", r),
            ("Coeficiente de Determinacao (R2)", r2),
            ("Desvio Padrao dos Residuos", desvio_padrao_residuos),
        ]
    )

    salvar_csv(caminho_arquivo, ("x", "y_original", "y_predito", "residuo"), linhas)


def executar_regressao(
    arquivo_entrada: str | Path = "input/dados_valid.txt",
    arquivo_saida: str | Path = "output/resultado_regressao.csv",
) -> tuple[float, float, float, float, float]:
    """Executa o fluxo completo de leitura, calculo e escrita dos resultados."""
    pontos = ler_dados_txt(arquivo_entrada)
    a, b = calcular_regressao_mmq(pontos)
    r = calcular_coeficiente_correlacao(pontos)
    r2 = calcular_coeficiente_determinacao(pontos, a, b)
    desvio = calcular_desvio_padrao_residuos(pontos, a, b)

    salvar_resultados_csv(arquivo_saida, pontos, a, b, r, r2, desvio)

    return a, b, r, r2, desvio


if __name__ == "__main__":
    coef_a, coef_b, correlacao, determinacao, desvio_residuos = executar_regressao()

    print(f"Regressao concluida: y = {coef_a:.4f}x + {coef_b:.4f}")
    print(f"Coeficiente de correlacao (r): {correlacao:.4f}")
    print(f"Coeficiente de determinacao (R2): {determinacao:.4f}")
    print(f"Desvio padrao dos residuos: {desvio_residuos:.4f}")
    print("Resultados salvos em output/resultado_regressao.csv")
