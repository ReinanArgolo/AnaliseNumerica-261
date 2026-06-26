"""Definição do Exercício 12.3."""


def obter_exercicio_12_3():
    """Retorna os dados do problema da velocidade com resistência do ar."""
    return {
        "nome": "Exercício 12.3",
        "variavel": "v",
        "t0": 0.0,
        "tf": 50.0,
        "y0": 0.0,
        "passos": [5.0, 2.5, 1.0],
        "f": lambda t, v: (2000 - 2 * v) / (200 - t),
        "solucao_exata": lambda t: 10 * t - (t * t) / 40,
        "descricao": "Velocidade de um corpo sujeito à resistência do ar igual a duas vezes a velocidade.",
    }
