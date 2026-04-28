import csv
import math

def ler_dados_txt(caminho_arquivo):
    """
    Lê dados de um arquivo .txt no formato:
    x1 y1
    x2 y2
    ...
    """
    pontos = []
    try:
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                if linha.strip():
                    parts = linha.split()
                    if len(parts) >= 2:
                        x = float(parts[0])
                        y = float(parts[1])
                        pontos.append((x, y))
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
    return pontos

def calcular_regressao_mmq(pontos):
    """
    Calcula os coeficientes da regressão linear y = ax + b
    usando o método dos mínimos quadrados.
    """
    n = len(pontos)
    if n == 0:
        return None

    soma_x = soma_y = soma_xy = soma_x2 = 0
    for x, y in pontos:
        soma_x += x
        soma_y += y
        soma_xy += x * y
        soma_x2 += x**2

    # Cálculo do coeficiente angular (a)
    denominador = (n * soma_x2 - soma_x**2)
    if denominador == 0:
        raise ValueError("Denominador zero: os pontos x são todos iguais.")
        
    a = (n * soma_xy - soma_x * soma_y) / denominador
    
    # Cálculo do coeficiente linear (b)
    # b = (soma_y - a * soma_x) / n
    media_x = soma_x / n
    media_y = soma_y / n
    b = media_y - a * media_x

    return a, b


def calcular_coeficiente_correlacao(pontos, a, b):
    """
    Calcula o coeficiente de correlação (r) para os pontos e a linha de regressão dada por y = ax + b.
    
    utiloiza a fórmula de correlação de Pearson:
    r = (n * Σ(xy) - Σx * Σy) / sqrt((n * Σ(x^2) - (Σx)^2) * (n * Σ(y^2) - (Σy)^2))
    
    return:
    - r: Coeficiente de correlação, variando entre -1 e 1.
    """

    sum_prod_xy = sum(p[0] * p[1] for p in pontos)
    sum_x = sum(p[0] for p in pontos)
    sum_y = sum(p[1] for p in pontos)
    sum_x2 = sum(p[0]**2 for p in pontos)
    sum_y2 = sum(p[1]**2 for p in pontos)

    n_pontos = len(pontos)

    numerador = ((n_pontos) * sum_prod_xy) - (sum_x * sum_y)

    variacao_x = math.sqrt(n_pontos * sum_x2 - sum_x**2)
    variacao_y = math.sqrt(n_pontos * sum_y2 - sum_y**2)

    denominador = variacao_x * variacao_y

    if denominador == 0:
        return 0
    
    erro = numerador / denominador

    return math.sqrt(erro)


import math

def calcular_desvio_padrao_residuos(pontos, a, b):
    n = len(pontos)
    
    if n <= 2:
        return 0.0 

    soma_quadrados_residuos = sum((y - (a * x + b))**2 for x, y in pontos)
    variancia_residuos = soma_quadrados_residuos / (n - 2)
    
    return math.sqrt(variancia_residuos)
    

def salvar_resultados_csv(caminho_arquivo, pontos, a, b, r2=None, desvio_padrao_residuos=None):
    """
    Salva os pontos originais, os valores preditos e o erro em um CSV.
    """
    try:
        with open(caminho_arquivo, 'w', newline='') as f:
            escritor = csv.writer(f)
            escritor.writerow(['x', 'y_original', 'y_predito', 'residuo'])
            
            for x, y in pontos:
                y_predito = a * x + b
                residuo = y - y_predito
                escritor.writerow([x, y, y_predito, residuo])
            
            escritor.writerow([])
            escritor.writerow(['Coeficiente Angular (a)', a])
            escritor.writerow(['Coeficiente Linear (b)', b])
            escritor.writerow(['Coeficiente de Correlação (r)', r2])
            escritor.writerow(['Desvio Padrão dos Resíduos', desvio_padrao_residuos])
            
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

if __name__ == "__main__":
    # Exemplo de uso
    arquivo_entrada = 'input/dados_valid.txt'
    arquivo_saida = 'output/resultado_regressao.csv'
    
    # Criar um arquivo de exemplo se não existir
    import os
    if not os.path.exists('input'):
        os.makedirs('input')

    # cria arquivos de teste
    if not os.path.exists(arquivo_entrada):
        with open(arquivo_entrada, 'w') as f:
            f.write("1 1.2\n2 1.9\n3 3.2\n4 4.1\n5 5.0")
            
    dados = ler_dados_txt(arquivo_entrada)
    if dados:
        coef_a, coef_b = calcular_regressao_mmq(dados)
        coef_correlacao = calcular_coeficiente_correlacao(dados, coef_a, coef_b)
        desvio_padrao_residuos = calcular_desvio_padrao_residuos(dados, coef_a, coef_b)
        print(f"Coeficiente de Correlação (r): {coef_correlacao:.4f}")
        print(f"Desvio Padrão dos Resíduos: {desvio_padrao_residuos:.4f}") 

        if not os.path.exists('output'):
            os.makedirs('output')

        salvar_resultados_csv(arquivo_saida, dados, coef_a, coef_b, r2=coef_correlacao, desvio_padrao_residuos=desvio_padrao_residuos)
        print(f"Regressão concluída: y = {coef_a:.4f}x + {coef_b:.4f}")
        print(f"Resultados salvos em {arquivo_saida}")
