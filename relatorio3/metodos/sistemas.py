"""Métodos numéricos para sistemas de EDOs sem NumPy."""


def somar(vetor_a, vetor_b):
    """Soma dois vetores representados por listas."""
    return [a + b for a, b in zip(vetor_a, vetor_b)]


def multiplicar_escalar(escalar, vetor):
    """Multiplica uma lista por um escalar."""
    return [escalar * valor for valor in vetor]


def combinar(estado, h, derivada):
    """Calcula estado + h * derivada."""
    return somar(estado, multiplicar_escalar(h, derivada))


def euler_sistema(f, t0, y0, tf, h, parametros=None):
    """Resolve um sistema por Euler explícito."""
    parametros = parametros or {}
    tempos = [float(t0)]
    estados = [list(y0)]
    t_atual = float(t0)
    estado_atual = list(y0)
    n = int(round((tf - t0) / h))

    for _ in range(n):
        derivada = f(t_atual, estado_atual, parametros)
        estado_atual = combinar(estado_atual, h, derivada)
        t_atual = t_atual + h
        tempos.append(t_atual)
        estados.append(list(estado_atual))

    return tempos, estados


def heun_sistema(f, t0, y0, tf, h, parametros=None):
    """Resolve um sistema pelo Método de Heun."""
    parametros = parametros or {}
    tempos = [float(t0)]
    estados = [list(y0)]
    t_atual = float(t0)
    estado_atual = list(y0)
    n = int(round((tf - t0) / h))

    for _ in range(n):
        k1 = f(t_atual, estado_atual, parametros)
        predito = combinar(estado_atual, h, k1)
        k2 = f(t_atual + h, predito, parametros)
        media = multiplicar_escalar(0.5, somar(k1, k2))
        estado_atual = combinar(estado_atual, h, media)
        t_atual = t_atual + h
        tempos.append(t_atual)
        estados.append(list(estado_atual))

    return tempos, estados


def ponto_medio_sistema(f, t0, y0, tf, h, parametros=None):
    """Resolve um sistema pelo Método do Ponto Médio."""
    parametros = parametros or {}
    tempos = [float(t0)]
    estados = [list(y0)]
    t_atual = float(t0)
    estado_atual = list(y0)
    n = int(round((tf - t0) / h))

    for _ in range(n):
        k1 = f(t_atual, estado_atual, parametros)
        meio = combinar(estado_atual, h / 2, k1)
        k2 = f(t_atual + h / 2, meio, parametros)
        estado_atual = combinar(estado_atual, h, k2)
        t_atual = t_atual + h
        tempos.append(t_atual)
        estados.append(list(estado_atual))

    return tempos, estados


def rk4_sistema(f, t0, y0, tf, h, parametros=None):
    """Resolve um sistema pelo método de Runge-Kutta de quarta ordem."""
    parametros = parametros or {}
    tempos = [float(t0)]
    estados = [list(y0)]
    t_atual = float(t0)
    estado_atual = list(y0)
    n = int(round((tf - t0) / h))

    for _ in range(n):
        k1 = f(t_atual, estado_atual, parametros)
        k2 = f(t_atual + h / 2, combinar(estado_atual, h / 2, k1), parametros)
        k3 = f(t_atual + h / 2, combinar(estado_atual, h / 2, k2), parametros)
        k4 = f(t_atual + h, combinar(estado_atual, h, k3), parametros)
        soma = []
        for valores in zip(k1, k2, k3, k4):
            soma.append((valores[0] + 2 * valores[1] + 2 * valores[2] + valores[3]) / 6)
        estado_atual = combinar(estado_atual, h, soma)
        t_atual = t_atual + h
        tempos.append(t_atual)
        estados.append(list(estado_atual))

    return tempos, estados


METODOS_SISTEMAS = {
    "Euler": euler_sistema,
    "Heun": heun_sistema,
    "Ponto Médio": ponto_medio_sistema,
    "RK4": rk4_sistema,
}
