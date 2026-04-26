import matplotlib.pyplot as plt
from metodos.regressao_linear_mmq import ler_dados_txt, calcular_regressao_mmq

def gerar_grafico(caminho_entrada, caminho_imagem):
    dados = ler_dados_txt(caminho_entrada)
    if not dados: return

    a, b = calcular_regressao_mmq(dados)
    x_vals = [p[0] for p in dados]
    y_vals = [p[1] for p in dados]
    y_preditos = [a * x + b for x in x_vals]

    plt.figure(figsize=(12, 7))
    
    # Desenhar as linhas de erro (resíduos) antes dos pontos para ficarem atrás
    for i in range(len(x_vals)):
        plt.plot([x_vals[i], x_vals[i]], [y_vals[i], y_preditos[i]], 
                 color='gray', linestyle='--', linewidth=1, alpha=0.6)
    
    # Legenda especial para a primeira linha de erro
    plt.plot([], [], color='gray', linestyle='--', label='Resíduos (Erros)')

    plt.scatter(x_vals, y_vals, color='red', label='Dados Experimentais', zorder=5)
    plt.plot(x_vals, y_preditos, color='blue', label=f'Reta Ajustada: y = {a:.4f}x + {b:.4f}', linewidth=2)
    
    plt.title('Regressão Linear: Visualização dos Mínimos Quadrados (Minimização dos Erros)')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    
    plt.savefig(caminho_imagem)
    print(f"Gráfico atualizado com linhas de erro em: {caminho_imagem}")

if __name__ == "__main__":
    gerar_grafico('input/dados_teste.txt', 'output/grafico_regressao.png')
