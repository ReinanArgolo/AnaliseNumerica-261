"""Minimos quadrados continuo para polinomios de qualquer grau."""

from __future__ import annotations

import math
from pathlib import Path

try:
    from metodos.io_utils import salvar_csv
    from metodos.polinomios import avaliar_polinomio, formatar_polinomio
    from metodos.sistemas_lineares import resolver_sistema_gauss
except ModuleNotFoundError:
    from io_utils import salvar_csv
    from polinomios import avaliar_polinomio, formatar_polinomio
    from sistemas_lineares import resolver_sistema_gauss


def ler_parametros(caminho_arquivo: str | Path) -> dict[str, str]:
    """Le um arquivo simples no formato chave=valor."""
    caminho = Path(caminho_arquivo)
    dados: dict[str, str] = {}

    with caminho.open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue

            if "=" not in linha:
                raise ValueError(f"Linha invalida em {caminho}: {linha}")

            chave, valor = linha.split("=", 1)
            dados[chave.strip().lower()] = valor.strip()

    return dados


def criar_funcao(expressao: str):
    """Cria uma funcao a partir de uma expressao em x.

    Exemplo de expressao: sin(x) + x**2
    """
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


def integrar_simpson(funcao, a: float, b: float, subintervalos: int = 1000) -> float:
    """Aproxima uma integral definida usando a regra composta de Simpson."""
    if subintervalos <= 0:
        raise ValueError("A quantidade de subintervalos deve ser positiva.")

    if subintervalos % 2 != 0:
        subintervalos += 1

    h = (b - a) / subintervalos
    soma = funcao(a) + funcao(b)

    for i in range(1, subintervalos):
        x = a + i * h

        if i % 2 == 0:
            soma += 2 * funcao(x)
        else:
            soma += 4 * funcao(x)

    return soma * h / 3


def ajustar_polinomio_mmq_continuo(
    funcao,
    a: float,
    b: float,
    grau: int,
    subintervalos: int = 1000,
) -> list[float]:
    """Ajusta um polinomio a uma funcao continua em [a,b]."""
    if grau < 0:
        raise ValueError("O grau do polinomio deve ser maior ou igual a zero.")

    tamanho = grau + 1
    matriz = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    vetor = [0.0 for _ in range(tamanho)]

    # Nas equacoes normais continuas aparecem integrais em vez de somatorios.
    for k in range(tamanho):
        for j in range(tamanho):
            potencia = j + k
            matriz[k][j] = (b ** (potencia + 1) - a ** (potencia + 1)) / (
                potencia + 1
            )

        vetor[k] = integrar_simpson(
            lambda x, k=k: funcao(x) * (x**k),
            a,
            b,
            subintervalos,
        )

    return resolver_sistema_gauss(matriz, vetor)


def salvar_resultado_continuo(
    caminho_saida: str | Path,
    funcao,
    a: float,
    b: float,
    coeficientes: list[float],
    pontos_tabela: int = 20,
) -> None:
    """Salva uma tabela comparando f(x) com o polinomio aproximador."""
    linhas: list[tuple[object, ...]] = []

    if pontos_tabela < 2:
        pontos_tabela = 2

    passo = (b - a) / (pontos_tabela - 1)

    for i in range(pontos_tabela):
        x = a + i * passo
        y_real = funcao(x)
        y_estimado = avaliar_polinomio(coeficientes, x)
        erro = y_real - y_estimado
        linhas.append((x, y_real, y_estimado, erro))

    linhas.append(())
    linhas.append(("Polinomio", formatar_polinomio(coeficientes)))

    for grau, coeficiente in enumerate(coeficientes):
        linhas.append((f"c{grau}", coeficiente))

    salvar_csv(caminho_saida, ("x", "f(x)", "p(x)", "erro"), linhas)


def executar_mmq_continuo(
    arquivo_entrada: str | Path = "input/mmq_continuo.txt",
    arquivo_saida: str | Path = "output/mmq_continuo.csv",
) -> list[float]:
    """Executa leitura, ajuste continuo e escrita dos resultados."""
    parametros = ler_parametros(arquivo_entrada)

    funcao = criar_funcao(parametros["funcao"])
    a = float(parametros["a"])
    b = float(parametros["b"])
    grau = int(parametros["grau"])
    subintervalos = int(parametros.get("subintervalos", "1000"))

    coeficientes = ajustar_polinomio_mmq_continuo(funcao, a, b, grau, subintervalos)
    salvar_resultado_continuo(arquivo_saida, funcao, a, b, coeficientes)

    return coeficientes


if __name__ == "__main__":
    coeficientes_ajustados = executar_mmq_continuo()

    print("MMQ continuo concluido.")
    print(f"P(x) = {formatar_polinomio(coeficientes_ajustados)}")
    print("Resultados salvos em output/mmq_continuo.csv")
