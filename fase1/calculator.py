"""
Módulo de cálculo de área e insumos agrícolas (Fase 1).

Este módulo define funções utilitárias para estimar a área de plantio e a
quantidade de insumos necessários por cultura.  Os valores utilizados são
derivados das definições apresentadas na Fase 1 do projeto FarmTech
Solutions e podem ser ajustados conforme a necessidade.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Insumo:
    """Estrutura que representa as quantidades de insumos por metro quadrado."""
    mudas: float  # número de mudas por m²
    calcario: float  # kg por m²
    fertilizante: float  # kg por m²
    palhada: float  # kg por m²


# Valores de referência de insumos por m² para cada cultura.
INSUMOS: Dict[str, Insumo] = {
    # Para café: 1 muda a cada 2,8 m² → 0,357 mudas por m²
    "cafe": Insumo(
        mudas=1 / 2.8,
        calcario=0.3,
        fertilizante=0.15,
        palhada=5.0,
    ),
    # Para soja: densidade média de 30 plantas/m²,
    # com insumos aproximados conforme tabela original.
    "soja": Insumo(
        mudas=30.0,
        calcario=0.15,  # média entre 100 e 200 g → 0,15 kg
        fertilizante=0.005,  # média de nutrientes por m²
        palhada=0.0,
    ),
}


def calcular_area(length: float, width: float) -> float:
    """Calcula a área de um retângulo em metros quadrados.

    Args:
        length: comprimento da área em metros.
        width: largura da área em metros.

    Returns:
        Área em metros quadrados.
    """
    return length * width


def calcular_insumos(cultura: str, area: float) -> Dict[str, float]:
    """Calcula a quantidade de insumos necessários para uma cultura.

    Args:
        cultura: nome da cultura ('cafe' ou 'soja').
        area: área de plantio em metros quadrados.

    Returns:
        Dicionário com as quantidades de cada insumo.

    Raises:
        ValueError: se a cultura não estiver cadastrada.
    """
    cultura = cultura.lower()
    if cultura not in INSUMOS:
        raise ValueError(f"Cultura desconhecida: {cultura}")
    ins = INSUMOS[cultura]
    return {
        "mudas": ins.mudas * area,
        "calcario_kg": ins.calcario * area,
        "fertilizante_kg": ins.fertilizante * area,
        "palhada_kg": ins.palhada * area,
    }


if __name__ == "__main__":
    # Exemplo de uso simples
    comprimento = 100.0  # metros
    largura = 50.0  # metros
    area_total = calcular_area(comprimento, largura)
    print(f"Área: {area_total:.2f} m²")
    for cultura in INSUMOS.keys():
        insumos = calcular_insumos(cultura, area_total)
        print(f"\nCultura: {cultura.title()}")
        for nome, quantidade in insumos.items():
            print(f"  {nome}: {quantidade:.2f}")