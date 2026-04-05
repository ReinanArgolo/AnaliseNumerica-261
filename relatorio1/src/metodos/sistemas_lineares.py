def _copiar_sistema(A, b):
	"""Cria copias numericas do sistema para evitar mutacao externa."""
	matriz = [[float(valor) for valor in linha] for linha in A]
	vetor = [float(valor) for valor in b]
	return matriz, vetor


def _validar_sistema(A, b):
	if not A or not b:
		raise ValueError("A matriz A e o vetor b nao podem ser vazios.")

	n = len(A)
	if len(b) != n:
		raise ValueError("Dimensoes invalidas: len(b) deve ser igual ao numero de linhas de A.")

	for linha in A:
		if len(linha) != n:
			raise ValueError("A matriz A deve ser quadrada (n x n).")


def _substituicao_regressiva(U, y, tol=1e-12, iteracao_inicial=0):
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


def eliminacao_gauss(A, b, pivotamento_parcial=True, tol_pivo=1e-12):
	"""
	Resolve Ax = b por eliminacao de Gauss.

	Retorno:
	- x: vetor solucao
	- etapas: numero de etapas principais de eliminacao
	- historico: lista de dicionarios com operacoes realizadas
	"""
	_validar_sistema(A, b)
	U, y = _copiar_sistema(A, b)
	n = len(U)
	historico = []
	iteracao = 0

	for k in range(n - 1):
		if pivotamento_parcial:
			linha_pivo = max(range(k, n), key=lambda i: abs(U[i][k]))
			if linha_pivo != k:
				U[k], U[linha_pivo] = U[linha_pivo], U[k]
				y[k], y[linha_pivo] = y[linha_pivo], y[k]
				historico.append({
					"iter": iteracao,
					"fase": "pivotamento",
					"k": k,
					"linha_pivo": linha_pivo,
					"linha_alvo": k,
					"pivo": U[k][k],
					"multiplicador": None,
					"acao": "troca_linhas"
				})
				iteracao += 1

		pivo = U[k][k]
		if abs(pivo) < tol_pivo:
			raise ValueError(f"Pivo nulo/quase nulo na etapa k={k}.")

		for i in range(k + 1, n):
			multiplicador = U[i][k] / pivo

			for j in range(k, n):
				U[i][j] = U[i][j] - multiplicador * U[k][j]
			y[i] = y[i] - multiplicador * y[k]

			historico.append({
				"iter": iteracao,
				"fase": "eliminacao",
				"k": k,
				"linha_pivo": k,
				"linha_alvo": i,
				"pivo": pivo,
				"multiplicador": multiplicador,
				"acao": "anular_elemento"
			})
			iteracao += 1

	x, hist_retr = _substituicao_regressiva(U, y, tol=tol_pivo, iteracao_inicial=iteracao)
	historico.extend(hist_retr)
	iteracao += len(hist_retr)
	
	historico.append({
		"iter": iteracao,
		"fase": "retrosubstituicao",
		"k": n - 1,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "solucao_obtida"
	})

	return x, n - 1, historico

def _decomposicao_LU(A, tol_pivo=1e-12, iteracao_inicial=0):
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



def fatoracao_LU(A, b, tol_pivo=1e-12):
	"""
	Resolve Ax = b por fatoracao LU.
	
	Etapas:
	1. Decompõe A = LU (eliminacao de Gauss sem pivotamento)
	2. Resolve Ly = b (substituicao progressiva)
	3. Resolve Ux = y (substituicao regressiva)

	Retorno:
	- x: vetor solucao
	- etapas: numero de etapas principais (n-1 para decomposicao + n para substituicoes)
	- historico: lista de dicionarios com todas operacoes realizadas
	"""
	_validar_sistema(A, b)
	
	historico = []
	iteracao = 0
	
	historico.append({
		"iter": iteracao,
		"fase": "fatoracao_LU",
		"k": None,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "inicio_fatoracao"
	})
	iteracao += 1
	
	# Etapa 1: Decomposicao LU
	L, U, hist_fatoracao = _decomposicao_LU(A, tol_pivo=tol_pivo, iteracao_inicial=iteracao)
	historico.extend(hist_fatoracao)
	iteracao += len(hist_fatoracao)
	
	historico.append({
		"iter": iteracao,
		"fase": "substituicao_progressiva",
		"k": None,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "inicio_substituicao_progressiva"
	})
	iteracao += 1
	
	# Etapa 2: Substituicao progressiva (Ly = b)
	y, hist_progressiva = substituicao_progressiva(L, b, tol=tol_pivo, iteracao_inicial=iteracao)
	historico.extend(hist_progressiva)
	iteracao += len(hist_progressiva)
	
	historico.append({
		"iter": iteracao,
		"fase": "substituicao_regressiva",
		"k": None,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "inicio_substituicao_regressiva"
	})
	iteracao += 1
	
	# Etapa 3: Substituicao regressiva (Ux = y)
	x, hist_regressiva = _substituicao_regressiva(U, y, tol=tol_pivo, iteracao_inicial=iteracao)
	historico.extend(hist_regressiva)
	iteracao += len(hist_regressiva)
	
	# Adicionar evento final
	historico.append({
		"iter": iteracao,
		"fase": "solucao",
		"k": None,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "solucao_obtida"
	})
	
	n = len(A)
	etapas = (n - 1) + n + n  # decomposicao + substituicoes
	
	return x, etapas, historico


def gauss_seidel(A, b, tol=1e-5, max_iter=100, x0=None):
	"""
	Resolve o sistema Ax = b pelo metodo iterativo de Gauss-Seidel.
	
	Retorno:
	- x: vetor solucao aproximado
	- iteracoes: numero de iteracoes realizadas
	- historico: lista de dicionarios com detalhes de cada iteracao
	"""
	_validar_sistema(A, b)
	
	n = len(A)
	if x0 is None:
		x0 = [0.0 for _ in range(n)]
	
	x = list(x0)
	historico = []
	
	for iteracao in range(1, max_iter + 1):
		x_ant = list(x)
		
		for i in range(n):
			soma = 0.0
			for j in range(n):
				if j != i:
					soma += A[i][j] * x[j]
					
			if abs(A[i][i]) == 0.0:
				raise ValueError(f"Pivot nulo encontrado na linha {i}. O metodo de Gauss-Seidel nao pode prosseguir.")
				
			x[i] = (b[i] - soma) / A[i][i]
			
		# Critério de parada: erro relativo com norma infinito
		max_diff = max(abs(x[i] - x_ant[i]) for i in range(n))
		max_x = max(abs(v) for v in x)
		erro = max_diff / max_x if max_x != 0 else max_diff
		
		historico.append({
			"iter": iteracao,
			"x": list(x),
			"erro": erro
		})
		
		if erro < tol:
			return x, iteracao, historico
			
	raise ValueError(f"Metodo de Gauss-Seidel nao convergiu apos {max_iter} iteracoes (erro = {erro}).")


def gauss_jordan(A, b, pivotamento_parcial=True, tol_pivo=1e-12):
	"""
	Resolve Ax = b pelo metodo de Gauss-Jordan.
	
	Retorno:
	- x: vetor solucao
	- etapas: numero de etapas principais
	- historico: lista de dicionarios com operacoes realizadas
	"""
	_validar_sistema(A, b)
	U, y = _copiar_sistema(A, b)
	n = len(U)
	historico = []
	iteracao = 0

	for k in range(n):
		if pivotamento_parcial:
			linha_pivo = max(range(k, n), key=lambda i: abs(U[i][k]))
			if linha_pivo != k:
				U[k], U[linha_pivo] = U[linha_pivo], U[k]
				y[k], y[linha_pivo] = y[linha_pivo], y[k]
				historico.append({
					"iter": iteracao,
					"fase": "pivotamento",
					"k": k,
					"linha_pivo": linha_pivo,
					"linha_alvo": k,
					"pivo": U[k][k],
					"multiplicador": None,
					"acao": "troca_linhas"
				})
				iteracao += 1

		pivo = U[k][k]
		if abs(pivo) < tol_pivo:
			raise ValueError(f"Pivo nulo/quase nulo na etapa k={k}.")

		# Normaliza a linha do pivô
		pivo_inverso = 1.0 / pivo
		for j in range(k, n):
			U[k][j] *= pivo_inverso
		y[k] *= pivo_inverso
		
		historico.append({
			"iter": iteracao,
			"fase": "normalizacao",
			"k": k,
			"linha_pivo": k,
			"linha_alvo": k,
			"pivo": pivo,
			"multiplicador": pivo_inverso,
			"acao": "normalizar_linha"
		})
		iteracao += 1

		# Zera os elementos da coluna k nas outras linhas
		for i in range(n):
			if i != k:
				multiplicador = U[i][k]
				
				for j in range(k, n):
					U[i][j] -= multiplicador * U[k][j]
				y[i] -= multiplicador * y[k]

				historico.append({
					"iter": iteracao,
					"fase": "eliminacao",
					"k": k,
					"linha_pivo": k,
					"linha_alvo": i,
					"pivo": 1.0,
					"multiplicador": multiplicador,
					"acao": "anular_elemento"
				})
				iteracao += 1
				
	historico.append({
		"iter": iteracao,
		"fase": "solucao",
		"k": None,
		"linha_pivo": None,
		"linha_alvo": None,
		"pivo": None,
		"multiplicador": None,
		"acao": "solucao_obtida"
	})

	return y, n, historico


def inversa_matriz(A, tol_pivo=1e-12):
	"""
	Calcula a matriz inversa de A utilizando o metodo de Gauss-Jordan.
	
	Retorno:
	- inversa: matriz inversa de A
	"""
	n = len(A)
	# Criar matriz aumentada [A | I]
	AI = []
	for i in range(n):
		if len(A[i]) != n:
			raise ValueError("A matriz A deve ser quadrada (n x n).")
		linha = [float(val) for val in A[i]] + [1.0 if i == j else 0.0 for j in range(n)]
		AI.append(linha)
		
	for k in range(n):
		# Pivotamento parcial
		linha_pivo = max(range(k, n), key=lambda i: abs(AI[i][k]))
		if linha_pivo != k:
			AI[k], AI[linha_pivo] = AI[linha_pivo], AI[k]
			
		pivo = AI[k][k]
		if abs(pivo) < tol_pivo:
			raise ValueError(f"Matriz singular, nao e possivel calcular a inversa (pivo nulo/quase nulo em k={k}).")
			
		# Normaliza a linha do pivô
		pivo_inverso = 1.0 / pivo
		for j in range(k, 2 * n):
			AI[k][j] *= pivo_inverso
			
		# Zera os elementos da coluna k nas outras linhas
		for i in range(n):
			if i != k:
				multiplicador = AI[i][k]
				for j in range(k, 2 * n):
					AI[i][j] -= multiplicador * AI[k][j]
					
	# Extrair a matriz inversa da direita da matriz aumentada
	inversa = []
	for i in range(n):
		inversa.append(AI[i][n:])
		
	return inversa


def norma_infinito_matriz(A):
	"""
	Calcula a norma infinito de uma matriz A (maxima soma absoluta das linhas).
	"""
	if not A:
		return 0.0
	
	max_soma = 0.0
	for linha in A:
		soma = sum(abs(valor) for valor in linha)
		if soma > max_soma:
			max_soma = soma
	return max_soma


def condicionamento(A):
	"""
	Calcula o numero de condicionamento da matriz A usando a norma infinito.
	cond(A) = ||A||_inf * ||A^-1||_inf
	
	Retorno:
	- numero de condicionamento (float)
	"""
	norma_A = norma_infinito_matriz(A)
	
	if norma_A == 0.0:
		raise ValueError("A matriz A é identicamente nula.")
		
	inv_A = inversa_matriz(A)
	norma_inv_A = norma_infinito_matriz(inv_A)
	
	return norma_A * norma_inv_A


