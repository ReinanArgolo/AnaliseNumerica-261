"""Regras classicas de integracao numerica."""

from __future__ import annotations

from pathlib import Path

try:
    from metodos.funcoes import criar_funcao
    from metodos.io_utils import salvar_csv
except ModuleNotFoundError:
    from funcoes import criar_funcao
    from io_utils import salvar_csv


def trapezio_simples(funcao, a: float, b: float) -> float:
    """Regra do trapezio com um intervalo."""
    return (b - a) * (funcao(a) + funcao(b)) / 2


def trapezio_composto(funcao, a: float, b: float, n: int) -> float:
    """Regra do trapezio com n subintervalos."""
    h = (b - a) / n
    soma = (funcao(a) + funcao(b)) / 2

    for i in range(1, n):
        soma += funcao(a + i * h)

    return h * soma


def simpson_13_simples(funcao, a: float, b: float) -> float:
    """Regra 1/3 de Simpson simples."""
    meio = (a + b) / 2
    return (b - a) * (funcao(a) + 4 * funcao(meio) + funcao(b)) / 6


def simpson_13_composto(funcao, a: float, b: float, n: int) -> float:
    """Regra 1/3 de Simpson composta. n precisa ser par."""
    if n % 2 != 0:
        raise ValueError("Simpson 1/3 composto precisa de n par.")

    h = (b - a) / n
    soma = funcao(a) + funcao(b)

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            soma += 2 * funcao(x)
        else:
            soma += 4 * funcao(x)

    return h * soma / 3


def simpson_38_simples(funcao, a: float, b: float) -> float:
    """Regra 3/8 de Simpson simples."""
    h = (b - a) / 3
    return 3 * h * (
        funcao(a) + 3 * funcao(a + h) + 3 * funcao(a + 2 * h) + funcao(b)
    ) / 8


def simpson_38_composto(funcao, a: float, b: float, n: int) -> float:
    """Regra 3/8 de Simpson composta. n precisa ser multiplo de 3."""
    if n % 3 != 0:
        raise ValueError("Simpson 3/8 composto precisa de n multiplo de 3.")

    h = (b - a) / n
    soma = funcao(a) + funcao(b)

    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            soma += 2 * funcao(x)
        else:
            soma += 3 * funcao(x)

    return 3 * h * soma / 8


def extrapolacao_richardson(valor_h: float, valor_h2: float, ordem: int) -> float:
    """Extrapolacao de Richardson para uma regra de ordem conhecida."""
    return valor_h2 + (valor_h2 - valor_h) / (2**ordem - 1)


def quadratura_gauss(funcao, a: float, b: float, pontos: int = 3) -> float:
    """Quadratura de Gauss-Legendre com 2, 3 ou 4 pontos."""
    dados = {
        2: (
            [-0.5773502691896257, 0.5773502691896257],
            [1.0, 1.0],
        ),
        3: (
            [-0.7745966692414834, 0.0, 0.7745966692414834],
            [0.5555555555555556, 0.8888888888888888, 0.5555555555555556],
        ),
        4: (
            [
                -0.8611363115940526,
                -0.3399810435848563,
                0.3399810435848563,
                0.8611363115940526,
            ],
            [
                0.3478548451374538,
                0.6521451548625461,
                0.6521451548625461,
                0.3478548451374538,
            ],
        ),
    }

    if pontos not in dados:
        raise ValueError("Use 2, 3 ou 4 pontos na quadratura de Gauss.")

    raizes, pesos = dados[pontos]
    meio = (a + b) / 2
    metade = (b - a) / 2
    soma = 0.0

    for raiz, peso in zip(raizes, pesos):
        x = meio + metade * raiz
        soma += peso * funcao(x)

    return metade * soma


def integrar_ate_convergir(funcao, a: float, b: float, tolerancia: float) -> float:
    """Integra por Simpson 1/3 dobrando n ate a variacao relativa ser pequena."""
    n = 4
    anterior = simpson_13_composto(funcao, a, b, n)

    while True:
        n *= 2
        atual = simpson_13_composto(funcao, a, b, n)
        erro = abs(atual - anterior) / max(1.0, abs(atual))

        if erro < tolerancia:
            return atual

        anterior = atual


def executar_integracao(
    arquivo_entrada: str | Path = "input/integracao.txt",
    arquivo_saida: str | Path = "output/integracao.csv",
) -> None:
    """Executa as regras principais para uma funcao lida de TXT."""
    dados: dict[str, str] = {}
    with Path(arquivo_entrada).open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            chave, valor = linha.split("=", 1)
            dados[chave.strip().lower()] = valor.strip()

    funcao = criar_funcao(dados["funcao"])
    a = float(dados["a"])
    b = float(dados["b"])
    n = int(dados.get("n", "12"))

    linhas = [
        ("trapezio_simples", trapezio_simples(funcao, a, b)),
        ("trapezio_composto", trapezio_composto(funcao, a, b, n)),
        ("simpson_13_simples", simpson_13_simples(funcao, a, b)),
        ("simpson_13_composto", simpson_13_composto(funcao, a, b, n if n % 2 == 0 else n + 1)),
        ("simpson_38_simples", simpson_38_simples(funcao, a, b)),
        ("simpson_38_composto", simpson_38_composto(funcao, a, b, n if n % 3 == 0 else n + (3 - n % 3))),
        ("gauss_2_pontos", quadratura_gauss(funcao, a, b, 2)),
        ("gauss_3_pontos", quadratura_gauss(funcao, a, b, 3)),
        ("gauss_4_pontos", quadratura_gauss(funcao, a, b, 4)),
    ]

    salvar_csv(arquivo_saida, ("metodo", "valor"), linhas)


if __name__ == "__main__":
    executar_integracao()
    print("Integracao numerica salva em output/integracao.csv")
