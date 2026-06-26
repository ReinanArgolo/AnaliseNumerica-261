"""Modelo SEIAHR com mortes acumuladas."""


def sistema_seiahr(t, estado, parametros):
    """Calcula as derivadas do modelo SEIAHR."""
    s, e, i, a, h, r, d = estado
    chi = parametros["chi"]
    alpha = parametros["alpha"]
    p = parametros["p"]
    delta = parametros["delta"]
    phi = parametros["phi"]
    mu = parametros["mu"]
    beta = parametros["beta"]
    rho = parametros["rho"]
    normalizado = parametros["normalizado"]

    if normalizado:
        populacao = s + e + i + a + h + r
        if populacao <= 0:
            lambd = 0.0
        else:
            lambd = beta * (i + a) / populacao
    else:
        lambd = beta * (i + a)

    d_s = -lambd * ((1 - chi) * s)
    d_e = lambd * ((1 - chi) * s) - alpha * e
    d_i = (1 - p) * alpha * e - delta * i
    d_a = p * alpha * e - delta * a
    d_h = phi * delta * i - (rho + mu) * h
    d_r = (1 - phi) * delta * i + rho * h + delta * a
    d_d = mu * h

    return [d_s, d_e, d_i, d_a, d_h, d_r, d_d]


def obter_modelo_seiahr(normalizado=True):
    """Retorna os dados e parâmetros do modelo SEIAHR."""
    parametros = {
        "chi": 0.6,
        "alpha": 0.33,
        "p": 0.75,
        "delta": 0.1,
        "phi": 0.01,
        "mu": 0.03,
        "beta": 0.5,
        "rho": 0.1,
        "normalizado": normalizado,
    }
    return {
        "nome": "Modelo SEIAHR",
        "t0": 0.0,
        "tf": 50.0,
        "h": 1.0,
        "estado_inicial": [400000.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        "variaveis": ["S", "E", "I", "A", "H", "R", "D"],
        "parametros": parametros,
        "sistema": sistema_seiahr,
    }
