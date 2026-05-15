"""Derivadas numericas de primeira e segunda ordem."""

from __future__ import annotations

from pathlib import Path

try:
    from metodos.funcoes import criar_funcao
    from metodos.io_utils import salvar_csv
except ModuleNotFoundError:
    from funcoes import criar_funcao
    from io_utils import salvar_csv


def derivada_primeira_central(funcao, x: float, h: float) -> float:
    """Aproxima f'(x) usando diferenca central."""
    return (funcao(x + h) - funcao(x - h)) / (2 * h)


def derivada_primeira_progressiva(funcao, x: float, h: float) -> float:
    """Aproxima f'(x) usando diferenca progressiva."""
    return (funcao(x + h) - funcao(x)) / h


def derivada_primeira_regressiva(funcao, x: float, h: float) -> float:
    """Aproxima f'(x) usando diferenca regressiva."""
    return (funcao(x) - funcao(x - h)) / h


def derivada_segunda_central(funcao, x: float, h: float) -> float:
    """Aproxima f''(x) usando diferenca central."""
    return (funcao(x + h) - 2 * funcao(x) + funcao(x - h)) / (h * h)


def extrapolacao_richardson(valor_h: float, valor_h2: float, ordem: int) -> float:
    """Melhora uma aproximacao usando extrapolacao de Richardson."""
    fator = 2**ordem
    return valor_h2 + (valor_h2 - valor_h) / (fator - 1)


def executar_derivadas(
    arquivo_entrada: str | Path = "input/derivadas.txt",
    arquivo_saida: str | Path = "output/derivadas.csv",
) -> None:
    """Executa derivadas a partir de um arquivo chave=valor."""
    dados: dict[str, str] = {}
    with Path(arquivo_entrada).open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            chave, valor = linha.split("=", 1)
            dados[chave.strip().lower()] = valor.strip()

    funcao = criar_funcao(dados["funcao"])
    x = float(dados["x"])
    h = float(dados["h"])

    d1_h = derivada_primeira_central(funcao, x, h)
    d1_h2 = derivada_primeira_central(funcao, x, h / 2)
    d2_h = derivada_segunda_central(funcao, x, h)
    d2_h2 = derivada_segunda_central(funcao, x, h / 2)

    linhas = [
        ("primeira_progressiva", derivada_primeira_progressiva(funcao, x, h)),
        ("primeira_regressiva", derivada_primeira_regressiva(funcao, x, h)),
        ("primeira_central", d1_h),
        ("primeira_central_richardson", extrapolacao_richardson(d1_h, d1_h2, 2)),
        ("segunda_central", d2_h),
        ("segunda_central_richardson", extrapolacao_richardson(d2_h, d2_h2, 2)),
    ]

    salvar_csv(arquivo_saida, ("metodo", "valor"), linhas)


if __name__ == "__main__":
    executar_derivadas()
    print("Derivadas numericas salvas em output/derivadas.csv")
