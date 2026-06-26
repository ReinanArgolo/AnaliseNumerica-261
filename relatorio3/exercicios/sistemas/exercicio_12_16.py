"""Definição do Exercício 12.16: modelo hospedeiro-parasita."""


def sistema_lotka_volterra(t, estado, parametros):
    """Calcula as derivadas do sistema hospedeiro-parasita."""
    hospedeiros, parasitas = estado
    g1 = parametros["g1"]
    d1 = parametros["d1"]
    g2 = parametros["g2"]
    d2 = parametros["d2"]

    d_h = g1 * hospedeiros - d1 * parasitas * hospedeiros
    d_p = -d2 * parasitas + g2 * parasitas * hospedeiros

    return [d_h, d_p]


def obter_exercicio_12_16():
    """Retorna os dados do problema de Lotka-Volterra."""
    return {
        "nome": "Exercício 12.16",
        "t0": 0.0,
        "tf": 2.0,
        "h": 0.01,
        "estado_inicial": [20.0, 5.0],
        "variaveis": ["H", "P"],
        "parametros": {
            "g1": 1.0,
            "d1": 0.1,
            "g2": 0.02,
            "d2": 0.5,
        },
        "sistema": sistema_lotka_volterra,
    }
