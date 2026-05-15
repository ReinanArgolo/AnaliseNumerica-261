"""Minimos quadrados discreto para polinomios de qualquer grau."""

from __future__ import annotations

from pathlib import Path

try:
    from metodos.io_utils import Ponto, ler_pontos_txt, salvar_csv
    from metodos.polinomios import avaliar_polinomio, formatar_polinomio
    from metodos.sistemas_lineares import resolver_sistema_gauss
except ModuleNotFoundError:
    from io_utils import Ponto, ler_pontos_txt, salvar_csv
    from polinomios import avaliar_polinomio, formatar_polinomio
    from sistemas_lineares import resolver_sistema_gauss


def ajustar_polinomio_mmq(pontos: list[Ponto], grau: int) -> list[float]:
    """Ajusta um polinomio de grau informado usando minimos quadrados."""
    if grau < 0:
        raise ValueError("O grau do polinomio deve ser maior ou igual a zero.")

    if len(pontos) < grau + 1:
        raise ValueError("Quantidade de pontos insuficiente para o grau escolhido.")

    tamanho = grau + 1
    matriz = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    vetor = [0.0 for _ in range(tamanho)]

    # Monta as equacoes normais:
    # sum(c_j * x_i^(j+k)) = sum(y_i * x_i^k)
    for k in range(tamanho):
        for j in range(tamanho):
            matriz[k][j] = sum(x ** (j + k) for x, _ in pontos)

        vetor[k] = sum(y * (x**k) for x, y in pontos)

    return resolver_sistema_gauss(matriz, vetor)


def salvar_resultado_discreto(
    caminho_saida: str | Path,
    pontos: list[Ponto],
    coeficientes: list[float],
) -> None:
    """Salva coeficientes, estimativas e residuos em CSV UTF-8."""
    linhas: list[tuple[object, ...]] = []

    for x, y in pontos:
        estimado = avaliar_polinomio(coeficientes, x)
        residuo = y - estimado
        linhas.append((x, y, estimado, residuo))

    linhas.append(())
    linhas.append(("Polinomio", formatar_polinomio(coeficientes)))

    for grau, coeficiente in enumerate(coeficientes):
        linhas.append((f"c{grau}", coeficiente))

    salvar_csv(caminho_saida, ("x", "y", "y_estimado", "residuo"), linhas)


def executar_mmq_discreto(
    arquivo_entrada: str | Path = "input/mmq_discreto.txt",
    arquivo_saida: str | Path = "output/mmq_discreto.csv",
    grau: int = 2,
) -> list[float]:
    """Executa leitura, ajuste e escrita do caso discreto."""
    pontos = ler_pontos_txt(arquivo_entrada)
    coeficientes = ajustar_polinomio_mmq(pontos, grau)
    salvar_resultado_discreto(arquivo_saida, pontos, coeficientes)
    return coeficientes


if __name__ == "__main__":
    grau_escolhido = 2
    coeficientes_ajustados = executar_mmq_discreto(grau=grau_escolhido)

    print(f"MMQ discreto concluido para grau {grau_escolhido}.")
    print(f"P(x) = {formatar_polinomio(coeficientes_ajustados)}")
    print("Resultados salvos em output/mmq_discreto.csv")
