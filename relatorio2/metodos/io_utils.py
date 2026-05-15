"""Funcoes auxiliares para entrada e saida de dados em UTF-8."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Sequence


Ponto = tuple[float, float]


def ler_pontos_txt(caminho_arquivo: str | Path) -> list[Ponto]:
    """Le pontos bidimensionais de um arquivo TXT em UTF-8.

    Cada linha valida deve conter pelo menos dois valores numericos separados
    por espaco, tabulacao, ponto e virgula ou virgula.
    """
    caminho = Path(caminho_arquivo)
    pontos: list[Ponto] = []

    with caminho.open("r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha_limpa = linha.strip()

            # Linhas vazias e comentarios sao ignorados para facilitar testes.
            if not linha_limpa or linha_limpa.startswith("#"):
                continue

            partes = linha_limpa.replace(";", " ").replace(",", " ").split()
            if len(partes) < 2:
                raise ValueError(
                    f"Linha {numero_linha} invalida em {caminho}: esperados x e y."
                )

            try:
                pontos.append((float(partes[0]), float(partes[1])))
            except ValueError as erro:
                raise ValueError(
                    f"Linha {numero_linha} invalida em {caminho}: valores numericos esperados."
                ) from erro

    return pontos


def salvar_csv(
    caminho_arquivo: str | Path,
    cabecalho: Sequence[str],
    linhas: Iterable[Sequence[object]],
) -> None:
    """Salva dados tabulares em CSV com codificacao UTF-8."""
    caminho = Path(caminho_arquivo)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)
