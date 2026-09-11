# Relatório 3 — Equações diferenciais ordinárias

Implementações de métodos numéricos para problemas de valor inicial (PVI),
sistemas de EDOs e problemas de valor de contorno (PVC).

## Conteúdo

- Euler, Heun, Ponto Médio e Runge–Kutta de quarta ordem;
- sistema hospedeiro–parasita de Lotka–Volterra;
- modelo epidemiológico SEIAHR;
- método de shooting e diferenças finitas para uma haste com transferência de calor;
- comparação com soluções analíticas, erros, tabelas e gráficos.

## Estrutura

- `metodos/`: algoritmos numéricos;
- `exercicios/`: definição dos problemas e parâmetros;
- `execucoes.py`: orquestração dos experimentos;
- `graficos.py`: geração das visualizações;
- `resultados/`: tabelas CSV;
- `graficos/`: imagens produzidas;
- `relatorio/`: fonte LaTeX e PDF final.

## Execução completa

Entre nesta pasta antes de executar, pois os caminhos de saída são relativos:

```bash
python main.py
```

O comando recria as saídas em `resultados/`, `graficos/` e `explicacoes/`.

## Relatório

O [PDF compilado](relatorio/out/relatorio_3_EDOs.pdf) está disponível para
leitura. Para recompilar:

```bash
cd relatorio
pdflatex -output-directory=out relatorio_3_EDOs.tex
```
