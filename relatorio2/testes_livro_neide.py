"""Testes baseados nos exercicios indicados do livro de Neide Franco."""

from __future__ import annotations

import math
from pathlib import Path

from metodos.integracao_numerica import integrar_ate_convergir, simpson_13_composto
from metodos.interpolacao_lagrange import coeficientes_lagrange
from metodos.interpolacao_newton import (
    coeficientes_newton_em_potencias,
    diferencas_divididas,
    avaliar_newton,
)
from metodos.io_utils import Ponto, ler_pontos_txt, salvar_csv
from metodos.mmq_discreto_polinomial import ajustar_polinomio_mmq
from metodos.polinomios import avaliar_polinomio, formatar_polinomio


PASTA_ENTRADA = Path("input/exercicios")
PASTA_SAIDA = Path("output/exercicios")


def ler_tabela(caminho: str) -> list[list[float]]:
    """Le uma tabela numerica ignorando comentarios."""
    linhas: list[list[float]] = []

    with (PASTA_ENTRADA / caminho).open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            linhas.append([float(valor) for valor in linha.split()])

    return linhas


def ler_parametros(caminho: str) -> dict[str, str]:
    """Le arquivo simples no formato chave=valor."""
    dados: dict[str, str] = {}

    with (PASTA_ENTRADA / caminho).open("r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            chave, valor = linha.split("=", 1)
            dados[chave.strip().lower()] = valor.strip()

    return dados


def regressao_potencia(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta y = a*x^b usando logaritmos."""
    pontos_log = [(math.log(x), math.log(y)) for x, y in pontos]
    c0, c1 = ajustar_polinomio_mmq(pontos_log, 1)
    return math.exp(c0), c1


def escolher_pontos_proximos(pontos: list[Ponto], x: float, grau: int) -> list[Ponto]:
    """Escolhe grau+1 pontos mais proximos de x."""
    escolhidos = sorted(pontos, key=lambda p: abs(p[0] - x))[: grau + 1]
    return sorted(escolhidos)


def exercicio_8_1() -> None:
    tabela = ler_tabela("ex8_1_acidentes.txt")
    pontos_acidentes = [(ano - 1980, acidentes) for ano, acidentes, _ in tabela]
    pontos_taxa = [(ano - 1980, taxa) for ano, _, taxa in tabela]

    reta = ajustar_polinomio_mmq(pontos_acidentes, 1)
    parabola = ajustar_polinomio_mmq(pontos_taxa, 2)
    x_2000 = 20

    linhas = [
        ("regressao_linear_acidentes", formatar_polinomio(reta), avaliar_polinomio(reta, x_2000)),
        ("regressao_quadratica_taxa", formatar_polinomio(parabola), avaliar_polinomio(parabola, x_2000)),
    ]
    salvar_csv(PASTA_SAIDA / "ex8_1.csv", ("item", "polinomio", "previsao_2000"), linhas)


def exercicio_8_5() -> None:
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex8_5_orificio.txt")
    coef = ajustar_polinomio_mmq(pontos, 2)
    linhas = [("polinomio", formatar_polinomio(coef), "")]

    for x, y in pontos:
        linhas.append((x, y, avaliar_polinomio(coef, x)))

    salvar_csv(PASTA_SAIDA / "ex8_5.csv", ("x", "C_tabela", "C_ajustado"), linhas)


def exercicio_8_11() -> None:
    tabela = ler_tabela("ex8_11_pnb.txt")

    # Usa-se ano - 1979 para evitar x = 0 no modelo de potencia.
    corrente = [(ano - 1979, pnb_corrente) for ano, pnb_corrente, _ in tabela]
    constante = [(ano - 1979, pnb_constante) for ano, _, pnb_constante in tabela]
    a_corr, b_corr = regressao_potencia(corrente)
    a_const, b_const = regressao_potencia(constante)

    x_2000 = 2000 - 1979
    pnb_corr_2000 = a_corr * (x_2000**b_corr)
    pnb_const_2000 = a_const * (x_2000**b_const)
    inflacao_relativa = pnb_corr_2000 / pnb_const_2000

    linhas = [
        ("corrente", a_corr, b_corr, pnb_corr_2000),
        ("constante", a_const, b_const, pnb_const_2000),
        ("razao_corrente_constante", "", "", inflacao_relativa),
    ]
    salvar_csv(PASTA_SAIDA / "ex8_11.csv", ("serie", "a", "b", "previsao_2000"), linhas)


def exercicio_10_2() -> None:
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_2_projetil.txt")
    coef = coeficientes_lagrange(pontos)
    a = coef[1]
    b = coef[2]
    g = 9.86
    angulo = math.atan(a)
    velocidade = math.sqrt(-g * (1 + a * a) / (2 * b))
    altitude_5m = avaliar_polinomio(coef, 5)

    linhas = [
        ("polinomio", formatar_polinomio(coef)),
        ("angulo_rad", angulo),
        ("angulo_graus", math.degrees(angulo)),
        ("velocidade_inicial", velocidade),
        ("altitude_em_5m", altitude_5m),
    ]
    salvar_csv(PASTA_SAIDA / "ex10_2.csv", ("item", "valor"), linhas)


def exercicio_10_6() -> None:
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_6_resistencia.txt")
    consultas = [1730.0, 3200.0]
    linhas = []

    for x in consultas:
        for grau in [2, 3]:
            usados = escolher_pontos_proximos(pontos, x, grau)
            coef = coeficientes_newton_em_potencias(usados)
            linhas.append((x, grau, formatar_polinomio(coef), avaliar_polinomio(coef, x)))

    salvar_csv(PASTA_SAIDA / "ex10_6.csv", ("comprimento", "grau", "polinomio", "resistencia"), linhas)


def exercicio_10_9() -> None:
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_9_varistor.txt")
    difs = diferencas_divididas(pontos)
    corrente_23 = avaliar_newton(pontos, difs, 2.3)
    e1 = 10 * corrente_23
    e_total = e1 + 2.3

    # Interpolacao inversa: agora a variavel independente e I.
    pontos_inversos = [(i, e2) for e2, i in pontos]
    usados = escolher_pontos_proximos(pontos_inversos, 1.0, 2)
    coef_inv = coeficientes_lagrange(usados)
    e2_inv = avaliar_polinomio(coef_inv, 1.0)

    linhas = [
        ("item_a_corrente_E2_2_3", corrente_23),
        ("item_a_E1", e1),
        ("item_a_E_total", e_total),
        ("item_b_E2_quando_E1_10", e2_inv),
    ]
    salvar_csv(PASTA_SAIDA / "ex10_9.csv", ("item", "valor"), linhas)


def exercicio_11_1() -> None:
    dados = ler_parametros("ex11_1_corpo_negro.txt")
    l1 = float(dados["lambda1"])
    l2 = float(dados["lambda2"])
    tol = float(dados["tolerancia"])
    linhas = []

    for grupo in ["temperaturas_i", "temperaturas_ii"]:
        temperaturas = [float(t) for t in dados[grupo].split(",")]
        for temperatura in temperaturas:
            def integrando(x, temperatura=temperatura):
                return 1 / (x**5 * (math.exp(1.432 / (temperatura * x)) - 1))

            integral = integrar_ate_convergir(integrando, l1, l2, tol)
            eficiencia = 64.77 * integral / (temperatura**4)
            linhas.append((grupo, temperatura, integral, eficiencia))

    salvar_csv(PASTA_SAIDA / "ex11_1.csv", ("grupo", "temperatura", "integral", "eficiencia"), linhas)


def exercicio_11_6() -> None:
    dados = ler_parametros("ex11_6_radiador.txt")
    l1 = float(dados["lambda1"])
    l2 = float(dados["lambda2"])
    tol = float(dados["tolerancia"])
    h = 6.6256e-27
    c = 2.99793e10
    k = 1.38054e-16
    linhas = []

    for temperatura in [float(t) for t in dados["temperaturas"].split(",")]:
        def integrando(x, temperatura=temperatura):
            expoente = h * c / (k * x * temperatura)
            return 2 * math.pi * h * c * c / (x**5 * (math.exp(expoente) - 1))

        q = integrar_ate_convergir(integrando, l1, l2, tol)
        linhas.append((temperatura, q))

    salvar_csv(PASTA_SAIDA / "ex11_6.csv", ("temperatura", "Q"), linhas)


def exercicio_11_11() -> None:
    dados = ler_parametros("ex11_11_spc.txt")
    media = float(dados["media"])
    desvio = float(dados["desvio"])
    x0 = float(dados["x0"])
    tol = float(dados["tolerancia"])

    def normal(x):
        z = (x - media) / desvio
        return math.exp(-0.5 * z * z) / (desvio * math.sqrt(2 * math.pi))

    area = integrar_ate_convergir(normal, media, x0, tol)
    probabilidade = 0.5 + area
    acima_5kg = 1 - probabilidade

    linhas = [
        ("F(5)", probabilidade),
        ("probabilidade_menos_ou_igual_5kg", probabilidade),
        ("probabilidade_acima_de_5kg", acima_5kg),
        ("pacotes_menos_ou_igual_5kg_em_100", 100 * probabilidade),
    ]
    salvar_csv(PASTA_SAIDA / "ex11_11.csv", ("item", "valor"), linhas)


def main() -> None:
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    exercicio_8_1()
    exercicio_8_5()
    exercicio_8_11()
    exercicio_10_2()
    exercicio_10_6()
    exercicio_10_9()
    exercicio_11_1()
    exercicio_11_6()
    exercicio_11_11()
    print("Testes do livro executados. Resultados em output/exercicios.")


if __name__ == "__main__":
    main()
