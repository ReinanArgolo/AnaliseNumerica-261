from . import utils

def bisseccao(funcao, a, b, tol=1e-6, max_iter=100):
    historico = [] 
    
    for i in range(max_iter):
        c = (a + b)/2
        fc = funcao(c)
        denominador = a + b

        if denominador != 0:
            er = abs((a - b) / denominador)
        else:
            er = abs(b - a) 
        
        historico.append({
            'iter': i, 
            'a': a, 
            'b': b, 
            'c': c, 
            'f(c)': fc,
            'erro': er
        })
        
        if fc == 0 or er < tol:
            return c, i, historico
            
        if utils.teorema_bolzano(funcao, a, c):
            b = c
        else:
            a = c
            
    return c, max_iter, historico


def posicaoFalsa(funcao, a, b, tol=1e-6, max_iter=100):
    historico = [] 
    
    for i in range(max_iter):
        c_an = historico[-1]['c'] if historico else a  
        c = b - (funcao(b) * (a - b)) / (funcao(a) - funcao(b))
        fc = funcao(c)

        er = abs(c - c_an) / c if c != 0 else 0
       
        historico.append({
            'iter': i, 
            'a': a, 
            'b': b, 
            'c': c, 
            'f(c)': fc,
            'erro': er
        })
        
        if fc == 0 or er < tol:
            return c, i, historico
            
        if utils.teorema_bolzano(funcao, a, c):
            b = c
        else:
            a = c
            
    return c, max_iter, historico


def ponto_fixo(g, x0, tol=1e-6, max_iter=100):
    historico = [] 
    
    for i in range(max_iter):
        x_an = historico[-1]['x'] if historico else x0  
        x = g(x_an)
        gx = g(x)
        
        er = abs(x - x_an) / x if x != 0 else 0
        
        historico.append({
            'iter': i, 
            'x': x, 
            'g(x)': gx,
            'erro': er
        })
        
        if gx == 0 or er < tol:
            return x, i, historico
            
    return x, max_iter, historico

def newton_raphson(funcao, x0, tol=1e-6, max_iter=100):
    historico = []
    
    for i in range(1, max_iter + 1):
        fx0 = funcao(x0)
        dx0 = utils.derivada_aproximada(funcao, x0)

        # Se a derivada for zero, o método estaciona, então interrompemos.
        if dx0 == 0:
            print("Derivada nula no método de Newton-Raphson. Interrompendo.")
            break

        xk = x0 - (fx0 / dx0)

        # Calculando o erro relativo (seguindo o padrão de 'bisseccao')
        err = abs(xk - x0) / abs(xk) if xk != 0 else abs(xk - x0)

        historico.append({
            'iter': i,
            'x': xk,
            'f(x)': fx0,
            'f\'(x)': dx0,
            'erro': err
        })


        if fx0 == 0 or err < tol:
            return xk, i, historico
            
        # O passo crucial omitido: atualizar x0 para a próxima iteração
        x0 = xk
    
    return xk, max_iter, historico

def secante(funcao, x0, x1, tol=1e-6, max_iter=100):
    historico = []
    
    for i in range(1, max_iter + 1):
        fx0 = funcao(x0)
        fx1 = funcao(x1)
        
        # Evitar divisão por zero se a função for flat entre f(x0) e f(x1)
        if fx1 - fx0 == 0:
            print("Divisão por zero no método da Secante. Interrompendo.")
            break
            
        # Fórmula da secante: x_{k+1} = x_k - f(x_k) * (x_k - x_{k-1}) / (f(x_k) - f(x_{k-1}))
        xk = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        
        err = abs(xk - x1) / abs(xk) if xk != 0 else abs(xk - x1)
        
        historico.append({
            'iter': i,
            'x': xk,
            'f(x)': funcao(xk),
            'erro': err
        })
        
        if funcao(xk) == 0 or err < tol:
            return xk, i, historico
            
        # Atualiza os valores para a próxima iteração
        x0 = x1
        x1 = xk
        
    return xk, max_iter, historico

