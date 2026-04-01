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
