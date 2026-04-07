# Comparação entre Métodos Diretos e Iterativos na Resolução de Sistemas Lineares

## Objetivo

Este documento reúne um contexto sintético para comparar os resultados obtidos com métodos **diretos** e **iterativos** na resolução de sistemas lineares do relatório. A ideia é servir como base para a redação das seções comparativas em LaTeX, destacando não apenas o desempenho numérico, mas também as características estruturais de cada família de métodos.

## Visão geral

### Métodos diretos

Os métodos diretos, como **Eliminação de Gauss**, **Fatoração LU** e **Gauss-Jordan**, buscam a solução em um número finito de passos algébricos. Em geral:

- produzem solução exata até o erro de máquina;
- são mais sensíveis ao custo $O(n^3)$;
- funcionam bem para sistemas pequenos e médios;
- costumam exigir mais operações quando a matriz é densa ou quando a estrutura do sistema precisa ser reaproveitada em várias resoluções.

### Métodos iterativos

Os métodos iterativos, como **Gauss-Jacobi** e **Gauss-Seidel**, constroem aproximações sucessivas até satisfazer um critério de parada. Em geral:

- produzem solução aproximada;
- dependem de tolerância, chute inicial e critério de convergência;
- tendem a ser mais vantajosos em matrizes esparsas e grandes;
- podem falhar ou divergir se a matriz não tiver propriedades favoráveis, como dominância diagonal ou condições equivalentes.

## Resultados observados no relatório

### Questão 5.2 — comparação direta vs. iterativa

Os resultados consolidados mostram a seguinte tendência:

| Método | Iterações / passos | Solução obtida |
|---|---:|---|
| Eliminação de Gauss | 7 | $(2, 1, 1)$ |
| Fatoração LU | 13 | $(2, 1, 1)$ |
| Gauss-Jordan | 10 | $(2, 1, 1)$ |
| Gauss-Jacobi | 8 | $(1.9747, 0.9783, 0.9824)$ |
| Gauss-Seidel | 6 | $(1.9949, 0.9970, 0.9982)$ |

#### Leitura dos resultados

- Os **métodos diretos** chegaram à solução exata do sistema, compatível com o vetor $(2, 1, 1)$.
- Entre eles, a **Eliminação de Gauss** apareceu como a mais econômica em número de passos principais.
- **Gauss-Jordan** resolveu o sistema corretamente, mas com custo maior por realizar a redução completa da matriz.
- A **Fatoração LU** também chegou ao vetor exato, porém é conceitualmente mais vantajosa quando se deseja reutilizar a mesma matriz $A$ para vários vetores $b$.
- Entre os métodos iterativos, **Gauss-Seidel** convergiu mais rapidamente que **Gauss-Jacobi** e aproximou melhor a solução final.

### Questão 5.1 — Laplace / malha 6×6

- **Gauss-Jacobi** convergiu em **17 iterações** para erro relativo inferior a $10^{-4}$.
- **Gauss-Seidel** convergiu em **10 iterações** para o mesmo nível de precisão.

#### Interpretação

Nesse caso, o método de Seidel foi mais eficiente porque usa as atualizações assim que elas ficam disponíveis, acelerando a propagação da correção pelo sistema.

### Questão 5.5 — malha térmica 9×9

- **Gauss-Jacobi** precisou de **32 iterações**.
- **Gauss-Seidel** precisou de **18 iterações**.

#### Interpretação

O ganho de Seidel ficou ainda mais evidente em um sistema maior e mais esparso. Isso reforça a ideia de que, quando as condições de convergência são satisfeitas, o uso de valores atualizados em tempo real reduz o número total de ciclos necessários.

## Síntese comparativa

### Desempenho numérico

- **Diretos:** entregam a solução com maior exatidão formal e independem de um critério de parada iterativo.
- **Iterativos:** fornecem aproximações controladas por tolerância; em problemas bem condicionados, podem alcançar erro muito pequeno com custo computacional menor.

### Custo computacional

- **Diretos:** têm custo dominante associado à eliminação/fatoração; são adequados quando o sistema é resolvido uma única vez.
- **Iterativos:** têm custo por iteração menor e podem ser mais econômicos em problemas grandes e esparsos.

### Dependência estrutural

- **Diretos:** são menos dependentes de um chute inicial, mas podem sofrer com pivôs pequenos e instabilidade sem estratégias auxiliares.
- **Iterativos:** dependem fortemente de dominância diagonal, raio espectral favorável e boa escolha de tolerância.

### Reutilização

- **LU:** é especialmente vantajosa quando há vários vetores $b$ para a mesma matriz $A$.
- **Jacobi e Seidel:** são mais úteis quando o sistema é grande, esparso e a convergência está assegurada.

## Conclusão prática para o relatório

A comparação dos resultados indica que:

1. **Os métodos diretos** são preferíveis quando se deseja a solução exata e o sistema não é muito grande.
2. **Os métodos iterativos** se destacam quando a matriz é grande, esparsa e bem comportada numericamente.
3. **Gauss-Seidel** normalmente supera **Gauss-Jacobi** em velocidade de convergência.
4. **Gauss**, **LU** e **Gauss-Jordan** chegam ao mesmo vetor solução, mas com estratégias algébricas e custos diferentes.
5. A escolha do método deve considerar não apenas a resposta final, mas também o tamanho da matriz, a esparsidade, a precisão requerida e a possibilidade de reaproveitamento da fatoração.

## Frases úteis para a redação

- "Os métodos diretos atingiram a solução exata até o erro de máquina, enquanto os métodos iterativos forneceram aproximações controladas por tolerância."
- "Gauss-Seidel apresentou convergência mais rápida que Gauss-Jacobi, reduzindo o número de iterações necessárias para atingir o mesmo patamar de erro."
- "A Fatoração LU mostrou-se especialmente adequada quando a matriz dos coeficientes pode ser reutilizada em diferentes vetores de termos independentes."
- "Em sistemas esparsos e de maior ordem, os métodos iterativos tendem a apresentar melhor relação entre custo e precisão."

## Observação de uso

Este texto pode ser reutilizado como base para escrever:

- comparações entre capítulos de métodos diretos e iterativos;
- conclusões sobre custo computacional;
- discussão sobre precisão, convergência e estabilidade numérica;
- justificativas para a escolha de um método em cada tipo de problema.
