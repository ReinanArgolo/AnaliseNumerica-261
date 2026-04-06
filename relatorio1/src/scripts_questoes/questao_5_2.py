import sys
import os

# Adiciona o diretório 'src' ao path principal se não estiver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from metodos import sistemas_lineares, utils

def modelar_sistema():
    A = [
        [ 20.0, -10.0,  -4.0],
        [-10.0,  25.0,  -5.0],
        [ -4.0,  -5.0,  20.0]
    ]
    b = [26.0, 0.0, 7.0]
    return A, b



def rodar_algoritmos():
    nome_script = os.path.splitext(os.path.basename(__file__))[0]
    parametros, saidas_dir = utils.configurar_ambiente(nome_script, ["# Parametros\n", "tol:1e-2\n", "max_iter:100\n"])
    
    A, b = modelar_sistema()
    tol = parametros.get('tol', 1e-2)
    max_iter = int(parametros.get('max_iter', 100))

    resultados = []
    print(f"\n=== RODANDO EXPERIMENTOS - SCRIPT [{nome_script}.py] ===")
    
    metodos = {
        "Eliminacao de Gauss": lambda: sistemas_lineares.eliminacao_gauss(A, b),
        "Fatoracao LU": lambda: sistemas_lineares.fatoracao_LU(A, b),
        "Gauss-Jordan": lambda: sistemas_lineares.gauss_jordan(A, b),
        "Gauss-Jacobi": lambda: sistemas_lineares.gauss_jacobi(A, b, tol=tol, max_iter=max_iter),
        "Gauss-Seidel": lambda: sistemas_lineares.gauss_seidel(A, b, tol=tol, max_iter=max_iter)
    }

    for nome_metodo, chamada in metodos.items():
        try:
            res = chamada()
            
            if nome_metodo in ["Eliminacao de Gauss", "Fatoracao LU", "Gauss-Jordan"]:
                raiz, _, historico = res
                iteracoes = len(historico) if historico else 0
            else:
                raiz, iteracoes, historico = res
            
            # Consolida log numérico granular
            nome_arquivo_seguro = nome_metodo.lower().replace(" ", "").replace("-", "_").replace("ç", "c").replace("ã", "a")
            utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}_hist_{nome_arquivo_seguro}.csv"), historico)

            # Format output map
            d = {"Metodo": nome_metodo, "Iteracoes": iteracoes}
            for idx, val in enumerate(raiz):
                d[f"i{idx+1}"] = val
                
            resultados.append(d)
        except Exception as e:
            print(f"Erro em {nome_metodo}: {e}")

    utils.salvar_csv(os.path.join(saidas_dir, f"{nome_script}.csv"), resultados)

    print("\n= RESULTADOS FINAIS:")
    for res in resultados:
        print(f" -> {res['Metodo']:<25} | Iteracoes = {res['Iteracoes']}")
        for k, v in res.items():
            if k.startswith("i") and len(k) <= 2:
                print(f"      {k} = {v}")

if __name__ == '__main__':
    rodar_algoritmos()
