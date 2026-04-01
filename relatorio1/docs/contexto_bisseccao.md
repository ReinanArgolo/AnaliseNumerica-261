# Contexto da Implementação: Método da Bissecção

Este documento resume as estratégias, funcionamentos e dificuldades referentes à implementação do Método da Bissecção, para servir de apoio na escrita do relatório.

## 1. Estratégia de Implementação (Código e Matemática)
- **Modularização:** O método foi desenvolvido "do zero" no arquivo `src/metodos/zeros_de_funcao.py`, sem o uso de bibliotecas de resolução prontas.
- **Cálculo da Raiz:** O ponto médio é calculado iterativamente por `c = (a + b)/2`. A escolha do subintervalo na próxima iteração é delegada à função auxiliar `utils.teorema_bolzano(funcao, a, c)`.
- **Cálculo do Erro:** 
  - A métrica adotada por padrão parece ser um erro relativo baseado nos limites do intervalo: `abs((a - b) / (a + b))`.
  - Existe um tratamento de exceção (fallback): caso a soma $a + b$ seja zero (o que causaria divisão por zero), o algoritmo passa a calcular o erro de forma absoluta `abs(b - a)`.
- **Critérios de Parada:** Interrompe se $f(c) == 0$, erro calculado `< tolerância` ou número máximo de iterações atingido.
- **Registro:** Todas as variáveis importantes de cada iteração (`iter, a, b, c, f(c), erro`) são salvas numa lista `historico` retornada ao fim da função, separando totalmente a matemática da estrutura de salvamento em arquivo.

## 2. Estrutura de Arquivos de Entrada e Saída
- **Entradas:** Ficam na pasta `dados/entradas/` (ex.: dados das questões em formato `.txt`), onde são lidos os parâmetros do problema (função, intervalo, precisão).
- **Saídas:** Os históricos retornados pela função iterativa são gravados em planilhas CSV na pasta `dados/saidas/` (ex.: `questao_3_3_hist_f1_bisseccao.csv`), garantindo fácil rastreabilidade e facilitando a geração posterior de gráficos e integração com LaTeX.

## 3. Dificuldades Enfrentadas (Anotações do Código)
- **Divisão por Zero no Erro Relativo:** Um dos problemas que exigiu atenção explícita na implementação está nas linhas 11-14: quando os limites do intervalo inicial são opostos ($a = -b$, ou ao longo das iterações a soma deles zera), a métrica de erro causaria um `ZeroDivisionError`. A solução foi contornar usando o erro absoluto `|b - a|` para esses casos.
- **Isolamento de Responsabilidades:** O método matemático foi construído estritamente para calcular a raiz (pura lógica), e os dados precisaram ser trafegados em formato de lista (dicionários) para fora do método numérico. Isso permitiu centralizar a escrita de arquivos (os `.csv`) num nível diferente do código, o que pode dar mais trabalho mas melhora o design.
