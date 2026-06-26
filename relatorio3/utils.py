"""Funções auxiliares para criação de saídas do projeto."""

import csv
from pathlib import Path


def criar_pastas():
    """Cria as pastas de saída usadas pelo projeto."""
    for pasta in ("resultados", "graficos", "explicacoes", "relatorio"):
        Path(pasta).mkdir(exist_ok=True)


def salvar_csv(tabela, caminho):
    """Salva uma tabela em CSV usando codificação UTF-8."""
    if not tabela:
        return

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(tabela[0].keys()))
        escritor.writeheader()
        escritor.writerows(tabela)


def salvar_markdown(texto, caminho):
    """Salva um texto Markdown usando codificação UTF-8."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)


def arredondar(valor, casas=6):
    """Arredonda números para tabelas sem esconder valores não numéricos."""
    if isinstance(valor, (int, float)):
        return round(valor, casas)
    return valor


def erro_absoluto(exato, aproximado):
    """Calcula o erro absoluto."""
    return abs(exato - aproximado)


def erro_relativo(exato, aproximado):
    """Calcula o erro relativo, evitando divisão por zero."""
    if exato == 0:
        return ""
    return abs(exato - aproximado) / abs(exato)
