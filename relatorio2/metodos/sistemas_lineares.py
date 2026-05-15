"""Funcoes simples para resolver sistemas lineares."""

from __future__ import annotations


def resolver_sistema_gauss(matriz: list[list[float]], vetor: list[float]) -> list[float]:
    """Resolve Ax = b usando eliminacao de Gauss com pivoteamento parcial."""
    n = len(vetor)

    # Copias para nao alterar os dados originais recebidos pela funcao.
    a = [linha[:] for linha in matriz]
    b = vetor[:]

    for coluna in range(n):
        linha_pivo = coluna

        # Escolhe a linha com maior valor absoluto na coluna atual.
        for linha in range(coluna + 1, n):
            if abs(a[linha][coluna]) > abs(a[linha_pivo][coluna]):
                linha_pivo = linha

        if abs(a[linha_pivo][coluna]) < 1e-12:
            raise ValueError("Sistema sem solucao unica.")

        if linha_pivo != coluna:
            a[coluna], a[linha_pivo] = a[linha_pivo], a[coluna]
            b[coluna], b[linha_pivo] = b[linha_pivo], b[coluna]

        # Zera os valores abaixo do pivo.
        for linha in range(coluna + 1, n):
            fator = a[linha][coluna] / a[coluna][coluna]
            a[linha][coluna] = 0.0

            for j in range(coluna + 1, n):
                a[linha][j] -= fator * a[coluna][j]

            b[linha] -= fator * b[coluna]

    solucao = [0.0 for _ in range(n)]

    # Substituicao regressiva.
    for linha in range(n - 1, -1, -1):
        soma = 0.0
        for coluna in range(linha + 1, n):
            soma += a[linha][coluna] * solucao[coluna]

        solucao[linha] = (b[linha] - soma) / a[linha][linha]

    return solucao
