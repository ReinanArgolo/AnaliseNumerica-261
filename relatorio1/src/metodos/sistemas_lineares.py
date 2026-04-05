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


def _substituicao_regressiva(U, y, tol=1e-12):
	"""Resolve Ux = y para U triangular superior."""
	n = len(U)
	x = [0.0 for _ in range(n)]

	for i in range(n - 1, -1, -1):
		soma = 0.0
		for j in range(i + 1, n):
			soma += U[i][j] * x[j]

		if abs(U[i][i]) < tol:
			raise ValueError(f"Sistema singular ou quase singular na linha {i}.")

		x[i] = (y[i] - soma) / U[i][i]

	return x


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

	x = _substituicao_regressiva(U, y, tol=tol_pivo)
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
