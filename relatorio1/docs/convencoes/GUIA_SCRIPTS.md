# Guia: Como Modelar e Testar Funções de Análise Numérica

Este guia serve como referência rápida para você criar novos scripts para resolver as listas de questões e gerar os arquivos `.csv` que irão direto para o seu relatório em LaTeX.

---

## 1. Como modelar a sua Função ($f(x)$)
Em Python, se a função for simples, usamos `lambda` (funções anônimas). Se for complexa (com condicionais ou módulos), usamos o clássico `def`.

*   Sempre importe o módulo `math` nativo se precisar de exponenciais, seno, cosseno, ou constantes matemáticas ($\pi$, $e$).
*   Para o **Método do Ponto Fixo**, lembre-se que você precisará isolar o $x$ no papel e criar uma função de iteração $g(x)$.

**Exemplo de Função Típica:**
Vamos modelar uma equação algébrica clássica: $f(x) = x^3 - 9x + 3$.
Sabemos que há uma raiz no intervalo $[0, 1]$, pois $f(0) = 3$ e $f(1) = -5$ (há troca de sinal).

*   **A função normal $f(x)$**: `f = lambda x: x**3 - 9*x + 3`
*   **A função de iteração $g(x)$**: Se isolarmos o $9x$, temos $9x = x^3 + 3$, logo $g(x) = \frac{x^3 + 3}{9}$. 
    Em Python: `g = lambda x: (x**3 + 3) / 9`

---

## 2. Capturando o nome do script (Exportação Dinâmica)
Para gerar os saídas dinamicamente com o formato `<nome_do_.py>.csv` sem reescrever o código toda hora, use as bibliotecas `os` e `sys` do Python para capturar o nome do arquivo em execução:

```python
import os
nome_script = os.path.splitext(os.path.basename(__file__))[0]
```

Se o seu arquivo se chamar `questao_4_lista_1.py`, essa variável valerá exatamente `"questao_4_lista_1"`, e o CSV resultante será `questao_4_lista_1.csv`.

---

## 3. Entradas, Saídas e o Template Base

Para rodar uma nova questão, você usará o arquivo `src/scripts_questoes/modelo_questao.py` como base (basta dar Ctrl+C e renomear). A regra das instruções pede que você parametrize os métodos utilizando arquivos de texto `.txt`.

O código deste modelo já **cria o arquivo `.txt` automaticamente por você** na primeira vez que for executado!  Eis como isso vai funcionar:

### Como funciona as Entradas (`dados/entradas/questao_N.txt`)
O arquivo gerado será de texto plano contendo chave e valor. Edite-o com as diretrizes do livro/professor:
```text
# Preencha os parametros para o script e o rode novamente.
a:0.0
b:1.0
x0:0.5
tol:1e-4
max_iter:100
```
* **`a` e `b`:** Limites do intervalo exigidos no método da Bissecção, Posição Falsa e Secante.
* **`x0`:** O chute inicial requisitado para Newton-Raphson e Ponto Fixo.
* **`tol` e `max_iter`:** Margem de tolerância e limite de segurança para o `while` não estourar a memória.

### Template do Script em Python (`src/scripts_questoes/modelo_questao.py`)
No seu script, a **ÚNICA** parte que precisará ser alterada é a **"SEÇÃO 1"**. Defina nela a equação alvo e, se necessário, o $g(x)$. O restante do código cuidará da leitura do TXT, executará os 5 métodos e enviará tudinho pro CSV sem dor de cabeça!

```python
import math
import sys
import os

# Adiciona o diretório 'src' ao path principal se não estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import zeros_de_funcao, utils

# ==============================================================================
# SEÇÃO 1: MODELAGEM MATEMÁTICA (O Único Local Que Você Precisa Editar)
# ==============================================================================
def modelar_funcoes():
    """Defina as funções alvo para seu problema matemático aqui."""
    
    # Exemplo: f(x) = x^3 - 9x + 3
    # Função principal (usada em Bissecção, Posição Falsa, Newton e Secante)
    f = lambda x: x**3 - 9*x + 3
    
    # Exemplo: isolando o x, temos x = (x^3 + 3) / 9
    # Função de iteração g(x) isolando o "x" (Necessária APENAS no Ponto Fixo)
    g = lambda x: (x**3 + 3) / 9
    
    return f, g

# ==============================================================================
# SEÇÃO 2: MOTOR DOS TESTES (NÃO PRECISA MEXER, SÓ COPIAR)
# ==============================================================================
def inicializar_ambiente(nome_script):
    # (... Essa função cria os arquivos .txt automaticamente caso não existam e os carrega)
    # [... código intencionalmente omitido no guia. Apenas copie do modelo_questao.py]

def rodar_algoritmos():
    # (... Essa função aciona os 5 métodos, e escreve 6 planilhas .CSV completas organizadas)
    # [... código intencionalmente omitido no guia. Apenas copie do modelo_questao.py]

if __name__ == '__main__':
    rodar_algoritmos()
```
    utils.salvar_csv(caminho_comparativo, resultados)
    
    # Históricos com passo a passo (Tire ou coloque de métodos específicos conforme precisar mostrar no LATEX)
    utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_bisseccao.csv"), hist_bis)
    utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_newton.csv"), hist_nw)

    print(f"Dados consolidados salvos com sucesso em: {caminho_comparativo}")

if __name__ == '__main__':
    resolver_questao()
```

---

## 🚀 Resumo do Fluxo de Trabalho (Para novas Listas)
Sempre que o professor passar uma lista de exercícios:
1. Copie o `Template Base` acima e cole em um novo arquivo (ex: `src/scripts_questoes/questao_X.py`).
2. Atualize localmente o *Lambda* da função $f(x)$ e a candidata a $g(x)$.
3. Altere o escopo do intervalo (valores de `a`, `b`) e `x0` indicados na questão do livro.
4. Execute o terminal: `python src/scripts_questoes/questao_X.py`.
5. Vá na pasta `dados/saidas/` e colha o arquivo final em formato numérico `.csv`!