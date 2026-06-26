"""Funções de geração de gráficos dos exercícios."""

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-relatorio3")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def salvar_grafico_pvi(tabela, metodos, caminho, titulo, eixo_y):
    """Gera gráfico comparativo para um PVI escalar."""
    tempos = [linha["t"] for linha in tabela]
    plt.figure(figsize=(9, 5))
    for metodo in metodos:
        plt.plot(tempos, [linha[metodo] for linha in tabela], marker="o", markersize=3, label=metodo)
    if "Solução Exata" in tabela[0]:
        plt.plot(tempos, [linha["Solução Exata"] for linha in tabela], linestyle="--", linewidth=2, label="Solução exata")
    plt.title(titulo)
    plt.xlabel("Tempo t")
    plt.ylabel(eixo_y)
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(caminho, dpi=150)
    plt.close()


def salvar_graficos_lotka(tempos, estados, prefixo):
    """Gera gráficos do sistema hospedeiro-parasita."""
    hospedeiros = [estado[0] for estado in estados]
    parasitas = [estado[1] for estado in estados]

    plt.figure(figsize=(9, 5))
    plt.plot(tempos, hospedeiros, label="Hospedeiros H(t)")
    plt.plot(tempos, parasitas, label="Parasitas P(t)")
    plt.title("Exercício 12.16 - evolução das populações")
    plt.xlabel("Tempo t")
    plt.ylabel("População")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / f"{prefixo}_evolucao.png", dpi=150)
    plt.close()

    plt.figure(figsize=(6, 5))
    plt.plot(hospedeiros, parasitas)
    plt.title("Exercício 12.16 - plano de fase")
    plt.xlabel("Hospedeiros H")
    plt.ylabel("Parasitas P")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.tight_layout()
    plt.savefig(Path("graficos") / f"{prefixo}_fase.png", dpi=150)
    plt.close()


def salvar_grafico_pvc(pontos, solucao_analitica, temperaturas_shooting, pontos_df, temperaturas_df):
    """Gera gráfico comparativo do problema de valor de contorno."""
    analitica = [solucao_analitica(x) for x in pontos]
    plt.figure(figsize=(9, 5))
    plt.plot(pontos, analitica, linestyle="--", label="Solução analítica")
    plt.plot(pontos, temperaturas_shooting, marker="o", label="Shooting")
    plt.plot(pontos_df, temperaturas_df, marker="s", label="Diferenças finitas")
    plt.title("PVC da haste - comparação dos métodos")
    plt.xlabel("Posição x")
    plt.ylabel("Temperatura T(x)")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "pvc_comparacao.png", dpi=150)
    plt.close()


def salvar_grafico_variavel_seiahr(tempos, estados, indice, nome):
    """Gera gráfico individual de uma variável SEIAHR."""
    valores = [estado[indice] for estado in estados]
    plt.figure(figsize=(8, 5))
    plt.plot(tempos, valores)
    plt.title(f"Modelo SEIAHR - {nome}(t)")
    plt.xlabel("Tempo em dias")
    plt.ylabel(nome)
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.tight_layout()
    plt.savefig(Path("graficos") / f"seiahr_{nome.lower()}.png", dpi=150)
    plt.close()


def salvar_graficos_detalhados_seiahr(tempos, resultados):
    """Gera gráficos adicionais para o modelo SEIAHR."""
    _, estados_rk4 = resultados["RK4"]

    plt.figure(figsize=(8, 5))
    plt.plot(tempos, [estado[2] for estado in estados_rk4], label="Infectados sintomáticos I(t)")
    plt.plot(tempos, [estado[3] for estado in estados_rk4], label="Assintomáticos A(t)")
    plt.title("Modelo SEIAHR - infectados sintomáticos e assintomáticos")
    plt.xlabel("Tempo em dias")
    plt.ylabel("Número de pessoas")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "seiahr_infectados_assintomaticos.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(tempos, [estado[5] for estado in estados_rk4], label="Recuperados R(t)")
    plt.plot(tempos, [estado[6] for estado in estados_rk4], label="Mortes acumuladas D(t)")
    plt.title("Modelo SEIAHR - recuperados e mortes acumuladas")
    plt.xlabel("Tempo em dias")
    plt.ylabel("Número de pessoas")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "seiahr_recuperados_mortes.png", dpi=150)
    plt.close()

    plt.figure(figsize=(9, 5))
    for nome_metodo, (_, estados) in resultados.items():
        plt.plot(tempos, [estado[2] for estado in estados], label=nome_metodo)
    plt.title("Modelo SEIAHR - comparação dos métodos para I(t)")
    plt.xlabel("Tempo em dias")
    plt.ylabel("Infectados sintomáticos")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "seiahr_comparacao_metodos_i.png", dpi=150)
    plt.close()

    plt.figure(figsize=(9, 5))
    for nome_metodo, (_, estados) in resultados.items():
        plt.plot(tempos, [estado[6] for estado in estados], label=nome_metodo)
    plt.title("Modelo SEIAHR - comparação dos métodos para D(t)")
    plt.xlabel("Tempo em dias")
    plt.ylabel("Mortes acumuladas")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "seiahr_comparacao_metodos_d.png", dpi=150)
    plt.close()


def salvar_grafico_comparativo_seiahr(tempos, estados, variaveis):
    """Gera gráfico conjunto das variáveis principais do SEIAHR."""
    plt.figure(figsize=(10, 6))
    for indice, nome_variavel in enumerate(variaveis):
        plt.plot(tempos, [estado[indice] for estado in estados], label=nome_variavel)
    plt.title("Modelo SEIAHR normalizado - variáveis principais")
    plt.xlabel("Tempo em dias")
    plt.ylabel("Número de pessoas")
    plt.grid(True, linestyle=":", linewidth=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig(Path("graficos") / "seiahr_comparativo.png", dpi=150)
    plt.close()
