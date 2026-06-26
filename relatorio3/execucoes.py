"""Rotinas de execução dos exercícios numéricos."""

import math
from pathlib import Path

from exercicios.pvc.haste_calor import obter_problema_haste
from exercicios.pvi.exercicio_12_3 import obter_exercicio_12_3
from exercicios.pvi.exercicio_12_10 import obter_exercicio_12_10
from exercicios.seiahr.modelo import obter_modelo_seiahr
from exercicios.sistemas.exercicio_12_16 import obter_exercicio_12_16
from graficos import (
    salvar_grafico_comparativo_seiahr,
    salvar_grafico_pvc,
    salvar_grafico_pvi,
    salvar_grafico_variavel_seiahr,
    salvar_graficos_detalhados_seiahr,
    salvar_graficos_lotka,
)
from metodos.pvc import diferencas_finitas_calor, shooting_calor
from metodos.pvi import METODOS_PVI
from metodos.sistemas import METODOS_SISTEMAS, rk4_sistema
from utils import arredondar, erro_absoluto, erro_relativo, salvar_csv, salvar_markdown


def numero_passos(t0, tf, h):
    """Calcula a quantidade de passos do intervalo."""
    return int(round((tf - t0) / h))


def executar_pvi_escalar(problema, h, prefixo):
    """Executa todos os métodos escalares para um problema de PVI."""
    n = numero_passos(problema["t0"], problema["tf"], h)
    resultados = {}
    for nome, metodo in METODOS_PVI.items():
        resultados[nome] = metodo(problema["f"], problema["t0"], problema["y0"], h, n)

    tempos = resultados["Euler"][0]
    tabela = []
    for indice, t in enumerate(tempos):
        linha = {"t": arredondar(t)}
        exato = problema["solucao_exata"](t)
        linha["Solução Exata"] = arredondar(exato)
        for nome in METODOS_PVI:
            aproximado = resultados[nome][1][indice]
            linha[nome] = arredondar(aproximado)
            linha[f"Erro Absoluto {nome}"] = arredondar(erro_absoluto(exato, aproximado))
            linha[f"Erro Relativo {nome}"] = arredondar(erro_relativo(exato, aproximado))
        tabela.append(linha)

    caminho_csv = Path("resultados") / f"{prefixo}.csv"
    caminho_png = Path("graficos") / f"{prefixo}.png"
    salvar_csv(tabela, caminho_csv)
    salvar_grafico_pvi(
        tabela,
        list(METODOS_PVI.keys()),
        caminho_png,
        f"{problema['nome']} - comparação dos métodos",
        problema["variavel"],
    )

    final = tabela[-1]
    resumo = [f"# {problema['nome']}", ""]
    resumo.append(f"Passo usado: h = {h}.")
    resumo.append(f"Valor exato final: {final['Solução Exata']}.")
    for nome in METODOS_PVI:
        resumo.append(
            f"- {nome}: valor final {final[nome]}, erro absoluto {final[f'Erro Absoluto {nome}']}."
        )
    resumo.append("")
    resumo.append("O erro diminui quando o passo é reduzido, pois as aproximações acompanham melhor a inclinação local da solução.")
    salvar_markdown("\n".join(resumo), Path("explicacoes") / f"{prefixo}.md")

    return tabela, caminho_csv, caminho_png


def executar_exercicio_12_3():
    """Executa o Exercício 12.3 para vários passos."""
    problema = obter_exercicio_12_3()
    tabelas = {}
    for h in problema["passos"]:
        prefixo = f"exercicio_12_3_h_{str(h).replace('.', '_')}"
        tabelas[h] = executar_pvi_escalar(problema, h, prefixo)
    return tabelas


def executar_exercicio_12_10():
    """Executa o Exercício 12.10."""
    problema = obter_exercicio_12_10()
    return executar_pvi_escalar(problema, problema["h"], "exercicio_12_10")


def executar_exercicio_12_16():
    """Executa o sistema hospedeiro-parasita."""
    problema = obter_exercicio_12_16()
    resultados = {}
    for nome, metodo in METODOS_SISTEMAS.items():
        resultados[nome] = metodo(
            problema["sistema"],
            problema["t0"],
            problema["estado_inicial"],
            problema["tf"],
            problema["h"],
            problema["parametros"],
        )

    tempos = resultados["RK4"][0]
    selecionados = [0.0, 0.5, 1.0, 1.5, 2.0]
    tabela = []
    for tempo_alvo in selecionados:
        indice = int(round((tempo_alvo - problema["t0"]) / problema["h"]))
        linha = {"t": tempo_alvo}
        for nome in METODOS_SISTEMAS:
            estado = resultados[nome][1][indice]
            linha[f"H {nome}"] = arredondar(estado[0])
            linha[f"P {nome}"] = arredondar(estado[1])
        tabela.append(linha)

    salvar_csv(tabela, Path("resultados") / "exercicio_12_16_valores_selecionados.csv")
    salvar_graficos_lotka(tempos, resultados["RK4"][1], "exercicio_12_16")

    final = resultados["RK4"][1][-1]
    texto = f"""# Exercício 12.16

O sistema de Lotka-Volterra foi resolvido com Euler, Heun, Ponto Médio e RK4.
No resultado RK4 final, os hospedeiros chegaram a {final[0]:.6f} e os parasitas chegaram a {final[1]:.6f}.

O modelo mostra uma relação acoplada: a população de hospedeiros favorece o crescimento dos parasitas, enquanto os parasitas reduzem a taxa de crescimento dos hospedeiros.
"""
    salvar_markdown(texto, Path("explicacoes") / "exercicio_12_16.md")
    return tabela


def montar_tabela_pvc(pontos, analitica, aproximada, coluna):
    """Monta tabela de comparação para PVC."""
    tabela = []
    for x, valor in zip(pontos, aproximada):
        exato = analitica(x)
        tabela.append(
            {
                "x": arredondar(x),
                "Solução Analítica": arredondar(exato),
                coluna: arredondar(valor),
                "Erro Absoluto": arredondar(erro_absoluto(exato, valor)),
            }
        )
    return tabela


def media_erros(tabela):
    """Calcula erro máximo e médio de uma tabela."""
    erros = [linha["Erro Absoluto"] for linha in tabela]
    return max(erros), sum(erros) / len(erros)


def executar_pvc():
    """Executa Shooting e Diferenças Finitas para a haste."""
    problema = obter_problema_haste()
    pontos_shooting, temperaturas_shooting, chute = shooting_calor(problema, problema["n_internos"])
    pontos_df, temperaturas_df = diferencas_finitas_calor(problema, problema["n_internos"])

    tabela_shooting = montar_tabela_pvc(
        pontos_shooting,
        problema["solucao_analitica"],
        temperaturas_shooting,
        "Shooting",
    )
    tabela_df = montar_tabela_pvc(
        pontos_df,
        problema["solucao_analitica"],
        temperaturas_df,
        "Diferenças Finitas",
    )
    salvar_csv(tabela_shooting, Path("resultados") / "pvc_shooting.csv")
    salvar_csv(tabela_df, Path("resultados") / "pvc_diferencas_finitas.csv")
    salvar_grafico_pvc(
        pontos_shooting,
        problema["solucao_analitica"],
        temperaturas_shooting,
        pontos_df,
        temperaturas_df,
    )

    erro_max_shooting, erro_med_shooting = media_erros(tabela_shooting)
    erro_max_df, erro_med_df = media_erros(tabela_df)
    melhor = "Shooting" if erro_med_shooting < erro_med_df else "Diferenças Finitas"
    texto = f"""# Problema de valor de contorno

O Método Shooting usou dois chutes iniciais para T'(0), integrou o sistema equivalente com RK4 e corrigiu o chute por interpolação linear. O chute corrigido foi {chute:.6f}.

Erro máximo do Shooting: {erro_max_shooting:.6f}.
Erro médio do Shooting: {erro_med_shooting:.6f}.
Erro máximo das Diferenças Finitas: {erro_max_df:.6f}.
Erro médio das Diferenças Finitas: {erro_med_df:.6f}.

Com 10 pontos internos, o método com menor erro médio foi: {melhor}.
"""
    salvar_markdown(texto, Path("explicacoes") / "pvc.md")
    return tabela_shooting, tabela_df, melhor


def executar_seiahr():
    """Executa o caso epidêmico SEIAHR normalizado e avalia a forma original."""
    modelo = obter_modelo_seiahr(normalizado=True)
    resultados = {}
    for nome, metodo in METODOS_SISTEMAS.items():
        resultados[nome] = metodo(
            modelo["sistema"],
            modelo["t0"],
            modelo["estado_inicial"],
            modelo["tf"],
            modelo["h"],
            modelo["parametros"],
        )

    tempos, estados_rk4 = resultados["RK4"]
    dias = list(range(0, 51, 5))
    tabela = []
    for dia in dias:
        indice = int(round(dia / modelo["h"]))
        estado = estados_rk4[indice]
        linha = {"Dia": dia}
        for nome_variavel, valor in zip(modelo["variaveis"], estado):
            linha[nome_variavel] = arredondar(valor)
        tabela.append(linha)
    salvar_csv(tabela, Path("resultados") / "seiahr_normalizado_rk4.csv")

    for indice, nome_variavel in enumerate(modelo["variaveis"]):
        salvar_grafico_variavel_seiahr(tempos, estados_rk4, indice, nome_variavel)
    salvar_graficos_detalhados_seiahr(tempos, resultados)
    salvar_grafico_comparativo_seiahr(tempos, estados_rk4, modelo["variaveis"])

    comparacao = []
    for nome, (_, estados) in resultados.items():
        final = estados[-1]
        comparacao.append(
            {
                "Método": nome,
                "S final": arredondar(final[0]),
                "I final": arredondar(final[2]),
                "H final": arredondar(final[4]),
                "R final": arredondar(final[5]),
                "D final": arredondar(final[6]),
            }
        )
    salvar_csv(comparacao, Path("resultados") / "seiahr_comparacao_metodos.csv")

    r0 = modelo["parametros"]["beta"] * (1 - modelo["parametros"]["chi"]) / modelo["parametros"]["delta"]
    infectados = [estado[2] for estado in estados_rk4]
    hospitalizados = [estado[4] for estado in estados_rk4]
    pico_i = max(infectados)
    dia_pico_i = tempos[infectados.index(pico_i)]
    pico_h = max(hospitalizados)
    dia_pico_h = tempos[hospitalizados.index(pico_h)]

    modelo_original = obter_modelo_seiahr(normalizado=False)
    status_original = "A simulação original foi iniciada, mas o termo lambda = beta(I+A) torna o sistema numericamente instável para população absoluta."
    try:
        tempos_original, estados_original = rk4_sistema(
            modelo_original["sistema"],
            modelo_original["t0"],
            modelo_original["estado_inicial"],
            modelo_original["tf"],
            modelo_original["h"],
            modelo_original["parametros"],
        )
        for estado in estados_original:
            if any((not math.isfinite(valor)) or abs(valor) > 10**12 for valor in estado):
                raise OverflowError("crescimento numérico excessivo")
        status_original = "A forma original executou sem estouro numérico, mas seus valores devem ser interpretados com cautela."
        salvar_csv(
            [
                {"Dia": arredondar(t), **{var: arredondar(valor) for var, valor in zip(modelo_original["variaveis"], estado)}}
                for t, estado in zip(tempos_original, estados_original)
            ],
            Path("resultados") / "seiahr_original_rk4.csv",
        )
    except (OverflowError, ValueError):
        salvar_csv(
            [{"Status": status_original}],
            Path("resultados") / "seiahr_original_rk4.csv",
        )

    texto = f"""# Caso epidêmico hipotético — modelo SEIAHR

O modelo foi resolvido principalmente na forma normalizada, usando lambda = beta(I+A)/N. Essa forma é mais adequada quando S, E, I, A, H e R representam número absoluto de pessoas.

O número básico de reprodução calculado foi R0 = {r0:.6f}.

No RK4 normalizado, o pico de infectados sintomáticos foi {pico_i:.6f} no dia {dia_pico_i:.1f}. O pico de hospitalizados foi {pico_h:.6f} no dia {dia_pico_h:.1f}. As mortes acumuladas ao final de 50 dias foram {estados_rk4[-1][6]:.6f}.

{status_original}

Entre os métodos testados, RK4 é o mais indicado para a discussão final porque usa quatro avaliações por passo e tende a ser mais estável e preciso que Euler, Heun e Ponto Médio neste sistema acoplado.
"""
    salvar_markdown(texto, Path("explicacoes") / "seiahr.md")
    return tabela, comparacao
