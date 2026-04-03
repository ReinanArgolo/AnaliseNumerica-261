# Questao 3.8 - Implementacao e Relato

## Objetivo
Implementar a Questao 3.8 seguindo o mesmo padrao das questoes anteriores, aplicando metodos de busca de raizes para comparar as taxas de juros dos planos de financiamento.

Arquivo implementado:
- relatorio1/src/scripts_questoes/questao_3_8.py

## Enunciado modelado
Dados:
- Preco a vista: R$ 162,00
- Entrada: R$ 22,00
- Valor financiado: VF = 162 - 22 = 140

Planos:
- Plano A: P = 9, PM = 26,50
- Plano B: P = 12, PM = 21,50

Equacao fornecida:
- (1 - (1+J)^(-P)) / J = VF / PM

Substituicoes:
- x = 1 + J
- k = VF / PM

Forma para zero de funcao:
- f(x) = k*x^(P+1) - (k+1)*x^P + 1 = 0

Com isso:
- Plano A: k_A = 140/26.5 = 5.2830188679, P_A = 9
- Plano B: k_B = 140/21.5 = 6.5116279070, P_B = 12

## Funcoes implementadas
No script foram definidas:
- f1: funcao do Plano A
- f2: funcao do Plano B
- g1 e g2: iteracoes de ponto fixo por relaxacao

Mapeamento explicito (mesmo padrao da questao 3.6):
- _mapping = { 'f1': ['g1'], 'f2': ['g2'] }

## Motor de execucao
Foi mantido o padrao das questoes anteriores:
- inicializar_ambiente(nome_script)
- leitura de arquivo em dados/entradas/questao_3_8.txt
- execucao dos metodos:
  - Bisseccao
  - Posicao Falsa
  - Newton-Raphson
  - Secante
  - Ponto Fixo (via mapping)
- geracao de:
  - CSV de historico por metodo
  - CSV consolidado final com colunas Metodo, Raiz, Juros, Iteracoes, Erro

Conversao de taxa:
- J = x - 1

## Intervalo contendo raiz positiva != 1
Durante a modelagem, os intervalos com troca de sinal para a raiz positiva diferente de 1 foram identificados como:
- Plano A: aproximadamente [1.1220, 1.1225]
- Plano B: aproximadamente [1.1090, 1.1095]

Para robustez de execucao no template de entrada, foram sugeridos intervalos mais amplos:
- f1_a = 1.10, f1_b = 1.20
- f2_a = 1.08, f2_b = 1.15

## Como executar
1. Rodar o script:
   c:/home/reinan/AnaliseNum/.venv/Scripts/python.exe relatorio1/src/scripts_questoes/questao_3_8.py

2. Se o arquivo de entrada nao existir, ele sera criado automaticamente em:
   relatorio1/dados/entradas/questao_3_8.txt

3. Preencher/ajustar parametros e rodar novamente.

4. Resultados esperados em:
   relatorio1/dados/saida/questao_3_8/

## Criterio de comparacao entre planos
O melhor plano para o consumidor e aquele com menor J (taxa mensal), apos obter a raiz x e aplicar J = x - 1.

## Observacoes tecnicas
- A estrutura foi mantida coerente com os scripts anteriores (3.3 e 3.6).
- Foi adotado mapeamento explicito de funcoes de iteracao por funcao principal.
- O script ja exporta a taxa de juros em valor decimal e imprime tambem em percentual no console.

## Registro de mudancas (para relatorio)
1. Criacao do novo script da questao:
   - relatorio1/src/scripts_questoes/questao_3_8.py
2. Criacao automatica de arquivo de entrada parametrico:
   - relatorio1/dados/entradas/questao_3_8.txt
3. Inclusao de mapeamento explicito entre funcoes principais e iteracoes de ponto fixo:
   - _mapping = { 'f1': ['g1'], 'f2': ['g2'] }
4. Inclusao da coluna Juros no CSV consolidado (J = x - 1).
5. Inclusao de resumo de comparacao entre planos no console com base em raizes nao triviais (x != 1).
6. Ajuste dos intervalos de entrada para reduzir convergencia na raiz trivial x = 1.

## Registro de erros encontrados e correcoes
1. Erro operacional no terminal (comandos Python executados em contexto interativo incorreto):
   - Sintoma: SyntaxError e interpretacao quebrada do comando em PowerShell.
   - Correcao: encerramento do interpretador interativo e execucao dos comandos com a venv configurada.
2. Erro de caminho relativo durante execucao:
   - Sintoma: arquivo do script nao encontrado quando o terminal estava em relatorio1/docs.
   - Correcao: execucao a partir da raiz do workspace (C:/home/reinan/AnaliseNum).
3. Comportamento numerico observado na Secante:
   - Sintoma: convergencia para a raiz trivial x = 1 em alguns cenarios.
   - Correcao: refinamento dos intervalos padrao e registro de comparacao focando na raiz positiva nao trivial (x != 1), conforme pedido do enunciado.

## Ambiente de execucao validado
- Python da venv:
  - c:/home/reinan/AnaliseNum/.venv/Scripts/python.exe
- Execucao valida do script:
  - c:/home/reinan/AnaliseNum/.venv/Scripts/python.exe relatorio1/src/scripts_questoes/questao_3_8.py
