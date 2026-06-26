"""Métodos de passo único para Problemas de Valor Inicial escalares."""


def euler(f, t0, y0, h, n):
    """Resolve y' = f(t, y) pelo Método de Euler explícito."""
    tempos = [float(t0)]
    valores = [float(y0)]
    t_atual = float(t0)
    y_atual = float(y0)

    for _ in range(n):
        y_atual = y_atual + h * f(t_atual, y_atual)
        t_atual = t_atual + h
        tempos.append(t_atual)
        valores.append(y_atual)

    return tempos, valores


def heun(f, t0, y0, h, n):
    """Resolve y' = f(t, y) pelo Método de Heun."""
    tempos = [float(t0)]
    valores = [float(y0)]
    t_atual = float(t0)
    y_atual = float(y0)

    for _ in range(n):
        k1 = f(t_atual, y_atual)
        y_predito = y_atual + h * k1
        k2 = f(t_atual + h, y_predito)
        y_atual = y_atual + (h / 2) * (k1 + k2)
        t_atual = t_atual + h
        tempos.append(t_atual)
        valores.append(y_atual)

    return tempos, valores


def ponto_medio(f, t0, y0, h, n):
    """Resolve y' = f(t, y) pelo Método do Ponto Médio."""
    tempos = [float(t0)]
    valores = [float(y0)]
    t_atual = float(t0)
    y_atual = float(y0)

    for _ in range(n):
        k1 = f(t_atual, y_atual)
        k2 = f(t_atual + h / 2, y_atual + (h / 2) * k1)
        y_atual = y_atual + h * k2
        t_atual = t_atual + h
        tempos.append(t_atual)
        valores.append(y_atual)

    return tempos, valores


def rk4(f, t0, y0, h, n):
    """Resolve y' = f(t, y) pelo método de Runge-Kutta de quarta ordem."""
    tempos = [float(t0)]
    valores = [float(y0)]
    t_atual = float(t0)
    y_atual = float(y0)

    for _ in range(n):
        k1 = f(t_atual, y_atual)
        k2 = f(t_atual + h / 2, y_atual + (h / 2) * k1)
        k3 = f(t_atual + h / 2, y_atual + (h / 2) * k2)
        k4 = f(t_atual + h, y_atual + h * k3)
        y_atual = y_atual + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        t_atual = t_atual + h
        tempos.append(t_atual)
        valores.append(y_atual)

    return tempos, valores


METODOS_PVI = {
    "Euler": euler,
    "Heun": heun,
    "Ponto Médio": ponto_medio,
    "RK4": rk4,
}
