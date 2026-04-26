import os
import csv

def teorema_bolzano(funcao, a, b):
    
    return funcao(a) * funcao(b) < 0

def derivada_aproximada(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h

def salvar_csv(caminho, dados, fieldnames=None):
    """Função auxiliar para salvar uma lista de dicionários em CSV."""
    if not dados:
        return
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)

def copiar_sistema(A, b):
	"""Cria copias numericas do sistema para evitar mutacao externa."""
	matriz = [[float(valor) for valor in linha] for linha in A]
	vetor = [float(valor) for valor in b]
	return matriz, vetor


def validar_sistema(A, b):
	if not A or not b:
		raise ValueError("A matriz A e o vetor b nao podem ser vazios.")

	n = len(A)
	if len(b) != n:
		raise ValueError("Dimensoes invalidas: len(b) deve ser igual ao numero de linhas de A.")

	for linha in A:
		if len(linha) != n:
			raise ValueError("A matriz A deve ser quadrada (n x n).")


def substituicao_regressiva(U, y, tol=1e-12, iteracao_inicial=0):
	"""
	Resolve Ux = y para U triangular superior.
	
	Retorno:
	- x: vetor solucao
	- historico: lista detalhada das operacoes realizadas
	"""
	n = len(U)
	x = [0.0 for _ in range(n)]
	historico = []
	iteracao = iteracao_inicial

	for i in range(n - 1, -1, -1):
		soma = 0.0
		for j in range(i + 1, n):
			soma += U[i][j] * x[j]

		if abs(U[i][i]) < tol:
			raise ValueError(f"Sistema singular ou quase singular na linha {i}.")

		x[i] = (y[i] - soma) / U[i][i]
		
		historico.append({
			"iter": iteracao,
			"fase": "substituicao_regressiva",
			"k": i,
			"linha_pivo": None,
			"linha_alvo": i,
			"pivo": U[i][i],
			"multiplicador": None,
			"acao": "calcular_x[i]"
		})
		iteracao += 1

	return x, historico


def decomposicao_LU(A, tol_pivo=1e-12, iteracao_inicial=0):
	"""
	Decompõe A em L e U usando eliminacao de Gauss sem pivotamento.
	
	Retorno:
	- L: matriz triangular inferior
	- U: matriz triangular superior
	- historico: lista detalhada das operacoes realizadas
	"""
	n = len(A)
	L = [[0.0 if i != j else 1.0 for j in range(n)] for i in range(n)]
	U = [[float(valor) for valor in linha] for linha in A]
	historico = []
	iteracao = iteracao_inicial

	for k in range(n - 1):
		pivo = U[k][k]
		if abs(pivo) < tol_pivo:
			raise ValueError(f"Pivo nulo/quase nulo na etapa k={k}.")

		for i in range(k + 1, n):
			multiplicador = U[i][k] / pivo
			L[i][k] = multiplicador

			historico.append({
				"iter": iteracao,
				"fase": "fatoracao_LU",
				"k": k,
				"linha_pivo": k,
				"linha_alvo": i,
				"pivo": pivo,
				"multiplicador": multiplicador,
				"acao": "armazenar_multiplicador_L_e_anular_U"
			})

			for j in range(k, n):
				U[i][j] = U[i][j] - multiplicador * U[k][j]
			
			iteracao += 1

	return L, U, historico

def substituicao_progressiva(L, b, tol=1e-12, iteracao_inicial=0):
	"""
	Resolve Ly = b para L triangular inferior.
	
	Retorno:
	- y: vetor solucao
	- historico: lista detalhada das operacoes realizadas
	"""
	n = len(L)
	y = [0.0 for _ in range(n)]
	historico = []
	iteracao = iteracao_inicial

	for i in range(n):
		soma = 0.0
		for j in range(i):
			soma += L[i][j] * y[j]

		if abs(L[i][i]) < tol:
			raise ValueError(f"Sistema singular ou quase singular na linha {i}.")

		y[i] = (b[i] - soma) / L[i][i]
		
		historico.append({
			"iter": iteracao,
			"fase": "substituicao_progressiva",
			"k": i,
			"linha_pivo": None,
			"linha_alvo": i,
			"pivo": L[i][i],
			"multiplicador": None,
			"acao": "calcular_y[i]"
		})
		iteracao += 1

	return y, historico





def configurar_ambiente(nome_script, linhas_padrao=None):
    """Garante a estrutura de pastas e ler arquivo txt.
    Substitui as funcoes `inicializar_ambiente` redundantes."""
    if linhas_padrao is None:
        linhas_padrao = ['tol:1e-4\n', 'max_iter:100\n']

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    entradas_dir = os.path.join(base_dir, 'dados', 'entradas')
    saidas_dir = os.path.join(base_dir, 'dados', 'saida', nome_script)

    os.makedirs(entradas_dir, exist_ok=True)
    os.makedirs(saidas_dir, exist_ok=True)

    arquivo_entrada = os.path.join(entradas_dir, f"{nome_script}.txt")

    if not os.path.exists(arquivo_entrada):
        print(f"[{nome_script}] Arquivo '{nome_script}.txt' ausente. Criando template...")
        with open(arquivo_entrada, 'w') as file:
            file.writelines(linhas_padrao)
        return None, saidas_dir

    parametros = {}
    with open(arquivo_entrada, 'r') as file:
        for linha in file:
            linha = linha.strip()
            if linha and not linha.startswith('#') and ':' in linha:
                chave, valor = linha.split(':')
                parametros[chave.strip()] = float(valor.strip())

    return parametros, saidas_dir
