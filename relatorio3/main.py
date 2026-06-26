"""Ponto de entrada para executar os exercícios de Métodos Numéricos."""

from execucoes import (
    executar_exercicio_12_3,
    executar_exercicio_12_10,
    executar_exercicio_12_16,
    executar_pvc,
    executar_seiahr,
)
from utils import criar_pastas


def executar_tudo():
    """Executa todos os exercícios e gera os arquivos de saída."""
    criar_pastas()
    executar_exercicio_12_3()
    executar_exercicio_12_10()
    executar_exercicio_12_16()
    executar_pvc()
    executar_seiahr()
    print("Execução concluída.")
    print("Resultados salvos em resultados/, graficos/ e explicacoes/.")


if __name__ == "__main__":
    executar_tudo()
