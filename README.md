# Análise Numérica — UESC (2026.1)

Implementações didáticas de métodos numéricos desenvolvidas para a disciplina de
Análise Numérica do curso de Ciência da Computação da Universidade Estadual de
Santa Cruz (UESC).

O repositório reúne código em Python, entradas de exemplo, resultados numéricos,
gráficos e relatórios em LaTeX. Os algoritmos centrais foram implementados de
forma explícita, sem usar funções prontas para substituir os métodos estudados.

## Conteúdo

| Etapa | Tópicos principais | Código | Relatório |
| --- | --- | --- | --- |
| Relatório 1 | Zeros de funções e sistemas lineares | [`relatorio1/src`](relatorio1/src) | [`relatorio1/docs/out/relatorio1.pdf`](relatorio1/docs/out/relatorio1.pdf) |
| Relatório 2 | Regressão, mínimos quadrados, interpolação, derivação e integração | [`relatorio2/metodos`](relatorio2/metodos) | [`relatorio2/docs/out/main.pdf`](relatorio2/docs/out/main.pdf) |
| Relatório 3 | PVI, Euler, Heun, Ponto Médio, RK4, sistemas de EDOs e PVC | [`relatorio3`](relatorio3) | [`relatorio3/relatorio/out/relatorio_3_EDOs.pdf`](relatorio3/relatorio/out/relatorio_3_EDOs.pdf) |

## Métodos implementados

- zeros de funções: bissecção, posição falsa, ponto fixo, Newton–Raphson e secante;
- sistemas lineares: eliminação de Gauss, Gauss–Jordan, fatoração LU, Jacobi e Gauss–Seidel;
- aproximação de funções: regressão linear, mínimos quadrados e interpolação de Lagrange e Newton;
- derivação e integração numérica;
- equações diferenciais ordinárias: Euler, Heun, Ponto Médio e Runge–Kutta de quarta ordem;
- problemas de valor de contorno: método de shooting e diferenças finitas.

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
git clone https://github.com/ReinanArgolo/AnaliseNumerica-261.git
cd AnaliseNumerica-261
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Cada relatório é independente. Consulte suas instruções específicas:

- [Relatório 1](relatorio1/README.md)
- [Relatório 2](relatorio2/README.md)
- [Relatório 3](relatorio3/README.md)

## Estrutura do repositório

```text
.
├── relatorio1/   # raízes de equações e sistemas lineares
├── relatorio2/   # ajuste, interpolação, derivação e integração
├── relatorio3/   # equações diferenciais e problemas de contorno
├── Modelos/      # modelo acadêmico em LaTeX
└── enviar/       # pacote original de entrega do primeiro relatório
```

Em cada relatório, as entradas e os resultados permanecem junto da respectiva
implementação para facilitar a reprodução dos experimentos. Os PDFs compilados
permitem consultar os resultados sem configurar um ambiente LaTeX. As referências
bibliográficas utilizadas são identificadas nos próprios relatórios; materiais
de terceiros não são redistribuídos neste repositório.

## Compilação dos relatórios

É necessária uma distribuição LaTeX com `pdflatex`. Execute o comando dentro da
pasta que contém o arquivo `.tex` principal, por exemplo:

```bash
cd relatorio3/relatorio
mkdir -p out
pdflatex -output-directory=out relatorio_3_EDOs.tex
```

## Autor

[Reinan Lopes Argolo](https://github.com/ReinanArgolo) — Bacharelado em Ciência
da Computação, UESC.

> Projeto acadêmico. Os resultados e implementações devem ser interpretados no
> contexto da disciplina de Análise Numérica.
