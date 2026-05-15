# Analise Numerica - Relatorio 2

Projeto para implementacao de metodos numericos sem bibliotecas prontas para os
algoritmos principais. As entradas e saidas devem ser salvas em UTF-8.

## Estrutura

- `metodos/`: implementacoes dos metodos numericos.
- `input/`: arquivos TXT ou CSV de entrada.
- `output/`: resultados gerados pelos metodos.
- `docs/`: relatorio em LaTeX.
- `docs/secoes/`: secoes independentes do relatorio.

## Execucao do metodo atual

```powershell
python .\metodos\regressao_linear_mmq.py
```

## Minimos quadrados polinomial discreto

Entrada: `input/mmq_discreto.txt`, com um par `x y` por linha.

```powershell
python .\metodos\mmq_discreto_polinomial.py
```

O grau fica na variavel `grau_escolhido`, no final do arquivo. Para testar outro
grau, basta trocar esse valor.

## Minimos quadrados polinomial continuo

Entrada: `input/mmq_continuo.txt`, no formato:

```txt
funcao=sin(x)
a=0
b=3.141592653589793
grau=2
subintervalos=1000
```

Depois execute:

```powershell
python .\metodos\mmq_continuo_polinomial.py
```

## Outros metodos implementados

```powershell
python .\metodos\interpolacao_lagrange.py
python .\metodos\interpolacao_newton.py
python .\metodos\derivadas_numericas.py
python .\metodos\integracao_numerica.py
```

## Testes com exercicios do livro

As entradas dos exercicios ficam em `input/exercicios/` e os resultados em
`output/exercicios/`.

```powershell
python .\testes_livro_neide.py
```

## Compilacao do relatorio completo

Entre na pasta do relatorio:

```powershell
cd docs
```

Depois compile o arquivo principal:

```powershell
pdflatex -output-directory=out main.tex
```

## Compilacao de uma secao isolada

As secoes usam o pacote `subfiles`, entao podem ser compiladas separadamente.

```powershell
pdflatex -output-directory=out secoes\regressao_linear_mmq.tex
```

## Padrao para novos metodos

1. Criar um arquivo em `metodos/` com funcoes pequenas e nomes descritivos.
2. Usar funcoes auxiliares de `metodos/io_utils.py` para entrada e saida UTF-8.
3. Salvar resultados em `output/`.
4. Criar uma secao correspondente em `docs/secoes/`.
5. Incluir a secao no arquivo `docs/main.tex` com `\subfile{...}`.
