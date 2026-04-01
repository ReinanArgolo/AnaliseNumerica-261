import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminhos dos arquivos
csv_path = '../../dados/saida/questao_3_3/questao_3_3_hist_f1_bisseccao.csv'
img_dir = '../../docs/img'
img_path = os.path.join(img_dir, 'bisseccao_convergencia.png')

# Garantir que o diretório de imagens exista
os.makedirs(img_dir, exist_ok=True)

# Ler os dados
df = pd.read_csv(csv_path)

# Configurar o estilo do gráfico
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'sans-serif']

fig, ax1 = plt.subplots(figsize=(10, 6))

color1 = '#1f77b4'
color2 = '#d62728'

# Eixo Y primário (Erro Relativo)
ax1.set_xlabel('Iterações', fontsize=12, fontweight='bold')
ax1.set_ylabel('Erro Estimado ($E_r$)', color=color1, fontsize=12, fontweight='bold')
ax1.plot(df['iter'], df['erro'], marker='o', color=color1, linestyle='-', linewidth=2, markersize=6, label='Erro Estimado')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_yscale('log') # Usar escala logarítmica para o erro
ax1.grid(True, which="both", ls="--", alpha=0.5)

# Eixo Y secundário (Valor de f(c))
ax2 = ax1.twinx()  
ax2.set_ylabel('Valor de $f(c)$', color=color2, fontsize=12, fontweight='bold')  
# Calculando valor absoluto para o plot logarítmico se for o caso, ou linear para f(c)
ax2.plot(df['iter'], df['f(c)'].abs(), marker='s', color=color2, linestyle='--', linewidth=2, markersize=6, label='$|f(c)|$')
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_yscale('log')

# Título e legendas
plt.title('Análise de Convergência - Método da Bissecção', fontsize=14, fontweight='bold', pad=15)

# Adicionar legendas conjuntas
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right', frameon=True, framealpha=0.9, shadow=True)

# Ajuste fino das margens
fig.tight_layout()  

# Salvar gráfico
plt.savefig(img_path, dpi=300, bbox_inches='tight')
print(f'Gráfico salvo em {img_path}')
