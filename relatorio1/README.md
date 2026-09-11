# Relatório 1 — Zeros de funções e sistemas lineares

Implementações dos primeiros conteúdos da disciplina de Análise Numérica.

## Conteúdo

- bissecção, posição falsa, ponto fixo, Newton–Raphson e secante;
- eliminação de Gauss, Gauss–Jordan e fatoração LU;
- métodos iterativos de Jacobi e Gauss–Seidel;
- análise de erro, convergência e condicionamento.

## Estrutura

- `src/metodos/`: implementações reutilizáveis;
- `src/scripts_questoes/`: execução das questões;
- `dados/entradas/`: parâmetros dos experimentos;
- `dados/saida/`: tabelas geradas;
- `docs/`: fontes LaTeX e PDF do relatório.

## Execução

A partir desta pasta, execute a questão desejada:

```bash
python src/scripts_questoes/questao_3_3.py
```

Substitua `questao_3_3.py` pelo script correspondente. Os parâmetros são lidos
de `dados/entradas/` e os CSVs são gravados em `dados/saida/`.

## Relatório

O [PDF compilado](docs/out/relatorio1.pdf) está disponível para leitura. Para
recompilar:

```bash
cd docs
pdflatex -output-directory=out relatorio1.tex
```
