"""Testes baseados nos exercicios indicados do livro de Neide Franco.

O script gera CSVs detalhados e figuras usadas no relatorio. Os algoritmos
numericos continuam nos modulos da pasta metodos; aqui ficam apenas os dados dos
exercicios e a organizacao das saidas.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from metodos.integracao_numerica import simpson_13_composto
from metodos.interpolacao_lagrange import coeficientes_lagrange
from metodos.interpolacao_newton import (
    avaliar_newton,
    coeficientes_newton_em_potencias,
    diferencas_divididas,
)
from metodos.io_utils import Ponto, ler_pontos_txt, salvar_csv
from metodos.mmq_discreto_polinomial import ajustar_polinomio_mmq
from metodos.polinomios import avaliar_polinomio, formatar_polinomio


PASTA_ENTRADA = Path("input/exercicios")
PASTA_SAIDA = Path("output/exercicios")
PASTA_FIGURAS = Path("output/figuras")


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


def salvar_figura(nome: str) -> None:
    """Salva a figura atual no diretorio padronizado."""
    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_FIGURAS / nome
    plt.tight_layout()
    plt.savefig(caminho, dpi=160)
    plt.close()


def regressao_potencia(pontos: list[Ponto]) -> tuple[float, float]:
    """Ajusta y = a*x^b usando a forma linear ln(y)=ln(a)+b ln(x)."""
    pontos_log = [(math.log(x), math.log(y)) for x, y in pontos]
    c0, c1 = ajustar_polinomio_mmq(pontos_log, 1)
    return math.exp(c0), c1


def escolher_pontos_proximos(pontos: list[Ponto], x: float, grau: int) -> list[Ponto]:
    """Escolhe grau+1 pontos mais proximos de x."""
    escolhidos = sorted(pontos, key=lambda p: abs(p[0] - x))[: grau + 1]
    return sorted(escolhidos)


def erro_quadratico(pontos: list[Ponto], coeficientes: list[float]) -> float:
    """Calcula soma dos quadrados dos residuos."""
    return sum((y - avaliar_polinomio(coeficientes, x)) ** 2 for x, y in pontos)


def coeficiente_determinacao(pontos: list[Ponto], coeficientes: list[float]) -> float:
    """Calcula R2 para um ajuste polinomial."""
    media = sum(y for _, y in pontos) / len(pontos)
    sq_total = sum((y - media) ** 2 for _, y in pontos)
    sq_res = erro_quadratico(pontos, coeficientes)
    return 1 - sq_res / sq_total if sq_total != 0 else 1.0


def sistema_normal(pontos: list[Ponto], grau: int) -> tuple[list[list[float]], list[float]]:
    """Monta a matriz e o vetor das equacoes normais do MMQ polinomial."""
    tamanho = grau + 1
    matriz = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    vetor = [0.0 for _ in range(tamanho)]

    for k in range(tamanho):
        for j in range(tamanho):
            matriz[k][j] = sum(x ** (j + k) for x, _ in pontos)
        vetor[k] = sum(y * (x**k) for x, y in pontos)

    return matriz, vetor


def tabela_diferencas_divididas(pontos: list[Ponto]) -> list[list[float | str]]:
    """Gera a tabela triangular de diferencas divididas para salvar em CSV."""
    n = len(pontos)
    tabela = [["" for _ in range(n + 1)] for _ in range(n)]

    for i, (x, y) in enumerate(pontos):
        tabela[i][0] = x
        tabela[i][1] = y

    for ordem in range(2, n + 1):
        for i in range(n - ordem + 1):
            numerador = tabela[i + 1][ordem - 1] - tabela[i][ordem - 1]
            denominador = pontos[i + ordem - 1][0] - pontos[i][0]
            tabela[i][ordem] = numerador / denominador

    return tabela


def integrar_com_historico(funcao, a: float, b: float, tolerancia: float):
    """Integra por Simpson 1/3 composto guardando o historico de refinamento."""
    n = 4
    anterior = simpson_13_composto(funcao, a, b, n)
    historico = [(n, anterior, "")]

    while True:
        n *= 2
        atual = simpson_13_composto(funcao, a, b, n)
        erro = abs(atual - anterior) / max(1.0, abs(atual))
        historico.append((n, atual, erro))

        if erro < tolerancia:
            return atual, n, erro, historico

        anterior = atual


def exercicio_8_1() -> None:
    """Regressao linear dos acidentes e quadratica da taxa por veiculos."""
    tabela = ler_tabela("ex8_1_acidentes.txt")
    pontos_acidentes = [(ano - 1980, acidentes) for ano, acidentes, _ in tabela]
    pontos_taxa = [(ano - 1980, taxa) for ano, _, taxa in tabela]

    reta = ajustar_polinomio_mmq(pontos_acidentes, 1)
    parabola = ajustar_polinomio_mmq(pontos_taxa, 2)
    x_2000 = 20

    linhas_resumo = [
        (
            "regressao_linear_acidentes",
            formatar_polinomio(reta),
            avaliar_polinomio(reta, x_2000),
            erro_quadratico(pontos_acidentes, reta),
            coeficiente_determinacao(pontos_acidentes, reta),
        ),
        (
            "regressao_quadratica_taxa",
            formatar_polinomio(parabola),
            avaliar_polinomio(parabola, x_2000),
            erro_quadratico(pontos_taxa, parabola),
            coeficiente_determinacao(pontos_taxa, parabola),
        ),
    ]
    salvar_csv(
        PASTA_SAIDA / "ex8_1.csv",
        ("item", "polinomio", "previsao_2000", "soma_quadrados_residuos", "R2"),
        linhas_resumo,
    )

    linhas_acidentes = []
    linhas_taxa = []
    for ano, acidentes, taxa in tabela:
        x = ano - 1980
        y_acidentes = avaliar_polinomio(reta, x)
        y_taxa = avaliar_polinomio(parabola, x)
        linhas_acidentes.append((ano, x, acidentes, y_acidentes, acidentes - y_acidentes))
        linhas_taxa.append((ano, x, taxa, y_taxa, taxa - y_taxa))

    salvar_csv(
        PASTA_SAIDA / "ex8_1_acidentes_linear_detalhado.csv",
        ("ano", "x", "acidentes", "ajustado", "residuo"),
        linhas_acidentes,
    )
    salvar_csv(
        PASTA_SAIDA / "ex8_1_taxa_quadratica_detalhado.csv",
        ("ano", "x", "taxa", "ajustado", "residuo"),
        linhas_taxa,
    )

    xs = [i for i in range(0, 21)]
    anos = [1980 + x for x in xs]
    plt.figure(figsize=(7, 4))
    plt.scatter([ano for ano, _, _ in tabela], [a for _, a, _ in tabela], label="dados")
    plt.plot(anos, [avaliar_polinomio(reta, x) for x in xs], label="reta ajustada")
    plt.scatter([2000], [avaliar_polinomio(reta, x_2000)], marker="x", s=80, label="previsao 2000")
    plt.xlabel("Ano")
    plt.ylabel("Acidentes (milhares)")
    plt.title("Exercicio 8.1 - Regressao linear dos acidentes")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex8_1_acidentes_linear.png")

    plt.figure(figsize=(7, 4))
    plt.scatter([ano for ano, _, _ in tabela], [t for _, _, t in tabela], label="dados")
    plt.plot(anos, [avaliar_polinomio(parabola, x) for x in xs], label="parabola ajustada")
    plt.scatter([2000], [avaliar_polinomio(parabola, x_2000)], marker="x", s=80, label="previsao 2000")
    plt.xlabel("Ano")
    plt.ylabel("Acidentes por 10000 veiculos")
    plt.title("Exercicio 8.1 - Regressao quadratica da taxa")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex8_1_taxa_quadratica.png")


def exercicio_8_5() -> None:
    """Ajuste quadratico do coeficiente de placa de orificio."""
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex8_5_orificio.txt")
    coef = ajustar_polinomio_mmq(pontos, 2)
    matriz, vetor = sistema_normal(pontos, 2)

    linhas = [("polinomio", formatar_polinomio(coef), "", "")]
    for x, y in pontos:
        ajustado = avaliar_polinomio(coef, x)
        residuo = y - ajustado
        linhas.append((x, y, ajustado, residuo))

    salvar_csv(PASTA_SAIDA / "ex8_5.csv", ("x", "C_tabela", "C_ajustado", "residuo"), linhas)
    salvar_csv(
        PASTA_SAIDA / "ex8_5_sistema_normal.csv",
        ("linha", "m0", "m1", "m2", "b"),
        [(i + 1, *matriz[i], vetor[i]) for i in range(3)],
    )

    xs = [0.1 + i * 0.009 for i in range(101)]
    plt.figure(figsize=(7, 4))
    plt.scatter([x for x, _ in pontos], [y for _, y in pontos], label="dados")
    plt.plot(xs, [avaliar_polinomio(coef, x) for x in xs], label="polinomio grau 2")
    plt.xlabel("A/A1")
    plt.ylabel("C")
    plt.title("Exercicio 8.5 - Ajuste do coeficiente C")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex8_5_orificio.png")


def exercicio_8_11() -> None:
    """Modelo de potencia para PNB em dolares correntes e constantes."""
    tabela = ler_tabela("ex8_11_pnb.txt")
    corrente = [(ano - 1979, pnb_corrente) for ano, pnb_corrente, _ in tabela]
    constante = [(ano - 1979, pnb_constante) for ano, _, pnb_constante in tabela]
    a_corr, b_corr = regressao_potencia(corrente)
    a_const, b_const = regressao_potencia(constante)

    x_2000 = 2000 - 1979
    pnb_corr_2000 = a_corr * (x_2000**b_corr)
    pnb_const_2000 = a_const * (x_2000**b_const)
    inflacao_relativa = pnb_corr_2000 / pnb_const_2000

    salvar_csv(
        PASTA_SAIDA / "ex8_11.csv",
        ("serie", "a", "b", "previsao_2000"),
        [
            ("corrente", a_corr, b_corr, pnb_corr_2000),
            ("constante", a_const, b_const, pnb_const_2000),
            ("razao_corrente_constante", "", "", inflacao_relativa),
        ],
    )

    linhas = []
    for ano, pnb_corrente, pnb_constante in tabela:
        x = ano - 1979
        ajuste_corr = a_corr * (x**b_corr)
        ajuste_const = a_const * (x**b_const)
        linhas.append(("corrente", ano, x, pnb_corrente, ajuste_corr, pnb_corrente - ajuste_corr))
        linhas.append(("constante", ano, x, pnb_constante, ajuste_const, pnb_constante - ajuste_const))
    salvar_csv(
        PASTA_SAIDA / "ex8_11_detalhado.csv",
        ("serie", "ano", "x", "observado", "ajustado", "residuo"),
        linhas,
    )

    anos = [ano for ano, _, _ in tabela] + [2000]
    xs = [ano - 1979 for ano in anos]
    plt.figure(figsize=(7, 4))
    plt.scatter([ano for ano, _, _ in tabela], [v for _, v, _ in tabela], label="corrente observado")
    plt.scatter([ano for ano, _, _ in tabela], [v for _, _, v in tabela], label="constante observado")
    plt.plot(anos, [a_corr * (x**b_corr) for x in xs], label="corrente ajustado")
    plt.plot(anos, [a_const * (x**b_const) for x in xs], label="constante ajustado")
    plt.scatter([2000, 2000], [pnb_corr_2000, pnb_const_2000], marker="x", s=80, label="previsao 2000")
    plt.xlabel("Ano")
    plt.ylabel("PNB (milhoes)")
    plt.title("Exercicio 8.11 - Modelo de potencia para PNB")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex8_11_pnb_corrente_constante.png")


def exercicio_10_2() -> None:
    """Interpolacao da trajetoria de um projetil."""
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_2_projetil.txt")
    coef = coeficientes_lagrange(pontos)
    a = coef[1]
    b = coef[2]
    g = 9.86
    angulo = math.atan(a)
    velocidade = math.sqrt(-g * (1 + a * a) / (2 * b))
    altitude_5m = avaliar_polinomio(coef, 5)

    salvar_csv(
        PASTA_SAIDA / "ex10_2.csv",
        ("item", "valor"),
        [
            ("polinomio", formatar_polinomio(coef)),
            ("angulo_rad", angulo),
            ("angulo_graus", math.degrees(angulo)),
            ("velocidade_inicial", velocidade),
            ("altitude_em_5m", altitude_5m),
        ],
    )
    salvar_csv(
        PASTA_SAIDA / "ex10_2_pontos_trajetoria.csv",
        ("x", "y_observado", "p(x)", "residuo"),
        [(x, y, avaliar_polinomio(coef, x), y - avaliar_polinomio(coef, x)) for x, y in pontos],
    )

    xs = [i * 0.2 for i in range(101)]
    ys = [avaliar_polinomio(coef, x) for x in xs]
    plt.figure(figsize=(7, 4))
    plt.scatter([x for x, _ in pontos], [y for _, y in pontos], label="pontos dados")
    plt.plot(xs, ys, label="trajetoria interpolada")
    plt.scatter([5], [altitude_5m], marker="x", s=80, label="P(5)")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Exercicio 10.2 - Trajetoria do projetil")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex10_2_trajetoria_projetil.png")


def exercicio_10_6() -> None:
    """Interpolacao da resistencia de um fio por graus 2 e 3."""
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_6_resistencia.txt")
    consultas = [1730.0, 3200.0]
    linhas_resultado = []
    linhas_pontos = []
    linhas_difs = []

    for x in consultas:
        for grau in [2, 3]:
            usados = escolher_pontos_proximos(pontos, x, grau)
            coef = coeficientes_newton_em_potencias(usados)
            valor = avaliar_polinomio(coef, x)
            linhas_resultado.append((x, grau, formatar_polinomio(coef), valor))

            for xp, yp in usados:
                linhas_pontos.append((x, grau, xp, yp))

            tabela = tabela_diferencas_divididas(usados)
            for indice, linha in enumerate(tabela):
                linhas_difs.append((x, grau, indice, *linha))

    salvar_csv(
        PASTA_SAIDA / "ex10_6.csv",
        ("comprimento", "grau", "polinomio", "resistencia"),
        linhas_resultado,
    )
    salvar_csv(
        PASTA_SAIDA / "ex10_6_pontos_usados.csv",
        ("consulta", "grau", "x", "resistencia"),
        linhas_pontos,
    )
    salvar_csv(
        PASTA_SAIDA / "ex10_6_diferencas_divididas.csv",
        ("consulta", "grau", "linha", "x", "ordem0", "ordem1", "ordem2", "ordem3"),
        linhas_difs,
    )

    xs = [500 + i * 35 for i in range(101)]
    plt.figure(figsize=(7, 4))
    plt.scatter([x for x, _ in pontos], [y for _, y in pontos], label="dados")
    for consulta in consultas:
        usados = escolher_pontos_proximos(pontos, consulta, 3)
        coef = coeficientes_newton_em_potencias(usados)
        faixa = [x for x in xs if min(p[0] for p in usados) <= x <= max(p[0] for p in usados)]
        plt.plot(faixa, [avaliar_polinomio(coef, x) for x in faixa], label=f"grau 3 perto de {consulta:g}")
        plt.scatter([consulta], [avaliar_polinomio(coef, consulta)], marker="x", s=80)
    plt.xlabel("Comprimento (m)")
    plt.ylabel("Resistencia (Ohms)")
    plt.title("Exercicio 10.6 - Interpolacao da resistencia")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex10_6_resistencia_interpolacao.png")


def exercicio_10_9() -> None:
    """Interpolacao direta e inversa para circuito com varistor."""
    pontos = ler_pontos_txt(PASTA_ENTRADA / "ex10_9_varistor.txt")
    difs = diferencas_divididas(pontos)
    corrente_23 = avaliar_newton(pontos, difs, 2.3)
    e1 = 10 * corrente_23
    e_total = e1 + 2.3

    pontos_inversos = [(i, e2) for e2, i in pontos]
    usados = escolher_pontos_proximos(pontos_inversos, 1.0, 2)
    coef_inv = coeficientes_lagrange(usados)
    e2_inv = avaliar_polinomio(coef_inv, 1.0)

    salvar_csv(
        PASTA_SAIDA / "ex10_9.csv",
        ("item", "valor"),
        [
            ("item_a_corrente_E2_2_3", corrente_23),
            ("item_a_E1", e1),
            ("item_a_E_total", e_total),
            ("item_b_E2_quando_E1_10", e2_inv),
        ],
    )
    salvar_csv(
        PASTA_SAIDA / "ex10_9_pontos_inversa.csv",
        ("I", "E2"),
        usados,
    )

    xs = [i * 0.045 for i in range(101)]
    plt.figure(figsize=(7, 4))
    plt.scatter([x for x, _ in pontos], [y for _, y in pontos], label="dados E2 x I")
    plt.plot(xs, [avaliar_newton(pontos, difs, x) for x in xs], label="interpolacao direta")
    plt.scatter([2.3], [corrente_23], marker="x", s=80, label="E2=2.3")
    plt.xlabel("E2 (V)")
    plt.ylabel("I (A)")
    plt.title("Exercicio 10.9 - Varistor")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex10_9_varistor.png")


def exercicio_11_1() -> None:
    """Eficiencia luminosa de corpo negro."""
    dados = ler_parametros("ex11_1_corpo_negro.txt")
    l1 = float(dados["lambda1"])
    l2 = float(dados["lambda2"])
    tol = float(dados["tolerancia"])
    linhas = []
    historico_linhas = []

    for grupo in ["temperaturas_i", "temperaturas_ii"]:
        temperaturas = [float(t) for t in dados[grupo].split(",")]
        for temperatura in temperaturas:
            def integrando(x, temperatura=temperatura):
                return 1 / (x**5 * (math.exp(1.432 / (temperatura * x)) - 1))

            integral, n, erro, historico = integrar_com_historico(integrando, l1, l2, tol)
            eficiencia = 64.77 * integral / (temperatura**4)
            linhas.append((grupo, temperatura, integral, eficiencia, n, erro))
            for n_hist, valor_hist, erro_hist in historico:
                historico_linhas.append((grupo, temperatura, n_hist, valor_hist, erro_hist))

    salvar_csv(
        PASTA_SAIDA / "ex11_1.csv",
        ("grupo", "temperatura", "integral", "eficiencia", "subintervalos", "erro_relativo"),
        linhas,
    )
    salvar_csv(
        PASTA_SAIDA / "ex11_1_refinamento.csv",
        ("grupo", "temperatura", "subintervalos", "integral", "erro_relativo"),
        historico_linhas,
    )

    for grupo, marcador in [("temperaturas_i", "o"), ("temperaturas_ii", "s")]:
        dados_grupo = [(temp, efic) for g, temp, _, efic, _, _ in linhas if g == grupo]
        plt.plot([t for t, _ in dados_grupo], [e for _, e in dados_grupo], marker=marcador, label=grupo)
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Eficiencia luminosa (%)")
    plt.title("Exercicio 11.1 - Eficiencia luminosa")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex11_1_eficiencia_luminosa.png")


def exercicio_11_6() -> None:
    """Radiacao emitida por radiador perfeito."""
    dados = ler_parametros("ex11_6_radiador.txt")
    l1 = float(dados["lambda1"])
    l2 = float(dados["lambda2"])
    tol = float(dados["tolerancia"])
    h = 6.6256e-27
    c = 2.99793e10
    k = 1.38054e-16
    linhas = []
    historico_linhas = []

    for temperatura in [float(t) for t in dados["temperaturas"].split(",")]:
        def integrando(x, temperatura=temperatura):
            expoente = h * c / (k * x * temperatura)
            return 2 * math.pi * h * c * c / (x**5 * (math.exp(expoente) - 1))

        q, n, erro, historico = integrar_com_historico(integrando, l1, l2, tol)
        linhas.append((temperatura, q, n, erro))
        for n_hist, valor_hist, erro_hist in historico:
            historico_linhas.append((temperatura, n_hist, valor_hist, erro_hist))

    salvar_csv(PASTA_SAIDA / "ex11_6.csv", ("temperatura", "Q", "subintervalos", "erro_relativo"), linhas)
    salvar_csv(
        PASTA_SAIDA / "ex11_6_refinamento.csv",
        ("temperatura", "subintervalos", "Q", "erro_relativo"),
        historico_linhas,
    )

    plt.figure(figsize=(7, 4))
    plt.bar([str(int(temp)) for temp, _, _, _ in linhas], [q for _, q, _, _ in linhas])
    plt.xlabel("Temperatura (K)")
    plt.ylabel("Q")
    plt.yscale("log")
    plt.title("Exercicio 11.6 - Radiacao emitida")
    plt.grid(True, axis="y", alpha=0.3)
    salvar_figura("ex11_6_radiacao.png")


def exercicio_11_11() -> None:
    """Probabilidade acumulada para peso dos pacotes de acucar."""
    dados = ler_parametros("ex11_11_spc.txt")
    media = float(dados["media"])
    desvio = float(dados["desvio"])
    x0 = float(dados["x0"])
    tol = float(dados["tolerancia"])

    def normal(x):
        z = (x - media) / desvio
        return math.exp(-0.5 * z * z) / (desvio * math.sqrt(2 * math.pi))

    area, n, erro, historico = integrar_com_historico(normal, media, x0, tol)
    probabilidade = 0.5 + area
    acima_5kg = 1 - probabilidade

    salvar_csv(
        PASTA_SAIDA / "ex11_11.csv",
        ("item", "valor"),
        [
            ("F(5)", probabilidade),
            ("probabilidade_menos_ou_igual_5kg", probabilidade),
            ("probabilidade_acima_de_5kg", acima_5kg),
            ("pacotes_menos_ou_igual_5kg_em_100", 100 * probabilidade),
            ("subintervalos", n),
            ("erro_relativo", erro),
        ],
    )
    salvar_csv(
        PASTA_SAIDA / "ex11_11_refinamento.csv",
        ("subintervalos", "integral_media_ate_5", "erro_relativo"),
        historico,
    )

    xs = [media - 4 * desvio + i * (8 * desvio / 300) for i in range(301)]
    ys = [normal(x) for x in xs]
    plt.figure(figsize=(7, 4))
    plt.plot(xs, ys, label="densidade normal")
    xs_area = [x for x in xs if x <= x0]
    plt.fill_between(xs_area, [normal(x) for x in xs_area], alpha=0.25, label="F(5)")
    plt.axvline(x0, color="black", linestyle="--", linewidth=1, label="5 kg")
    plt.xlabel("Peso (kg)")
    plt.ylabel("f(x)")
    plt.title("Exercicio 11.11 - Distribuicao normal dos pesos")
    plt.grid(True, alpha=0.3)
    plt.legend()
    salvar_figura("ex11_11_normal.png")


def main() -> None:
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
    PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)
    exercicio_8_1()
    exercicio_8_5()
    exercicio_8_11()
    exercicio_10_2()
    exercicio_10_6()
    exercicio_10_9()
    exercicio_11_1()
    exercicio_11_6()
    exercicio_11_11()
    print("Testes do livro executados. Resultados em output/exercicios e output/figuras.")


if __name__ == "__main__":
    main()
