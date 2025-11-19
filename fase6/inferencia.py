"""
Placeholder para integração de modelos de visão computacional (Fase 6).

Este módulo deverá ser implementado de acordo com o notebook da Fase 6.
Por enquanto, ele contém funções de demonstração que recebem uma imagem e
retornam uma mensagem genérica.
"""
from pathlib import Path
from typing import Optional


def classificar_imagem(imagem: Path) -> str:
    """Classifica a imagem e retorna uma descrição.

    Args:
        imagem: caminho para o arquivo de imagem.

    Returns:
        Texto descritivo da classe detectada.
    """
    # TODO: substituir por modelo YOLOv5 ou CNN treinado.
    return f"Análise da imagem '{imagem.name}' não implementada."


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python inferencia.py <caminho_da_imagem>")
        sys.exit(1)
    resultado = classificar_imagem(Path(sys.argv[1]))
    print(resultado)