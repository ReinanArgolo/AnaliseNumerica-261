---
description: "Use when creating, editing, or evaluating numerical methods in Python, LaTeX reports, or data visualization pipelines. Covers architectural decisions, modularity rules, and the automated integration flow between Python scripts and LaTeX documents."
applyTo: "**/*.{py,tex}"
---

# Diretrizes do Projeto de Análise Numérica

- **Métodos Numéricos 'From Scratch'**: Implemente ou ajuste métodos numéricos (busca de raízes, sistemas lineares, etc.) utilizando a linguagem base do Python. Não utilize dicionários ou solucionadores *black-box* (como os de `scipy`, ou rotinas prontas de resolução empacotadas), pois o objetivo acadêmico exige a codificação dos métodos subjacentes.
- **Módulos vs Runners**: Apele estritamente à separação de responsabilidades:
  - Funções logico-matemáticas e puras devem ficar exclusivamente sob `src/metodos/`.
  - Scripts de execução (*runners*) e resolução de problemas ficam isolados sob `src/scripts_questoes/`.
- **Pipeline de Dados (I/O)**: Parametrizações locais (tolerância, iterações máximas) e arrays devem ser mantidos como arquivos estáticos (ASCII/CSV) em `dados/entradas/`. O histórico em iterações de cada teste/método deve sempre ser exportado num formato colunar como `.csv` na pasta `dados/saida/<questao>/`.
- **Integração Python $\rightarrow$ LaTeX**: Abandone transcrições manuais. O documento `.tex` em `docs/` deve consumir dinamicamente as tabelas em `dados/saida/<questao>/`.
- **Visualização e Gráficos**: Todo gráfico de convergência e representação visual de funções deve ser implementado com bibliotecas como `matplotlib` e exportado como um arquivo vetorial `.pdf` dentro de `docs/img/`, assegurando alta fidelidade exigida para o relatório acadêmico final.
