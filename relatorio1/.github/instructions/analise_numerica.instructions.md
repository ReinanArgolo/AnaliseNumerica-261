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

## Regras Específicas para Sistemas Lineares

- **Escopo destas Regras**: As regras desta seção se aplicam somente aos artefatos de sistemas lineares (implementações, scripts de questões, saídas e texto técnico correspondente).
- **Capítulos do Relatório**: Ao trabalhar em `docs/relatorio1.tex` e seções relacionadas, manter a estrutura macro com dois blocos de conteúdo: soluções de equações não lineares e solução de sistemas lineares. No bloco de sistemas lineares, incluir fundamentação teórica, implementação e análise de resultados.
- **Métodos Obrigatórios (Implementação Manual)**: Implementar explicitamente os métodos de condicionamento e solução de sistemas lineares, incluindo Eliminação de Gauss (com e sem pivotamento parcial), Fatoração LU, Jacobi-Richardson e Gauss-Seidel, sem chamar solucionadores prontos.
- **Restrições de Biblioteca**: Permitir `numpy` e `pandas` apenas para entrada/saída e organização de dados fora do núcleo matemático. Proibir uso de rotinas prontas de resolução numérica, por exemplo: `numpy.linalg.solve`, `numpy.linalg.inv`, `numpy.linalg.det`, `numpy.linalg.cond`, `scipy.linalg`, `scipy.sparse.linalg` e equivalentes.
- **Padrão de Código (Espelhando `src/metodos/zeros_de_funcao.py`)**: Em novos métodos, usar assinatura simples com parâmetros de controle (`tol`, `max_iter` quando aplicável), retornar solução + metadados de iteração e manter histórico por iteração como lista de dicionários. A exportação para CSV deve ocorrer no script runner da questão.
- **Entrada e Saída por Questão**: Cada questão de sistemas lineares deve possuir arquivo de entrada em `dados/entradas/`, script dedicado em `src/scripts_questoes/` e saídas em `dados/saida/<questao>/`, incluindo histórico iterativo em `.csv` e resumo final por questão.
- **Validação e Casos Patológicos**: Sempre detectar e registrar falhas numéricas esperadas (pivô nulo/quase nulo, matriz singular, não convergência, violação de critério de convergência, sensibilidade a condicionamento).
- **Documentação dos Problemas Inerentes**: Toda limitação observada durante os testes deve ser descrita no relatório técnico com evidência (tabela/histórico/erro), não apenas mencionada de forma textual.
