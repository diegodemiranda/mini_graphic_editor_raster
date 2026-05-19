"""
src/tools/tools.py  ·  CAMADA MODEL (constantes compartilhadas)
================================================================
Define o enum de ferramentas, a paleta de cores e os tamanhos de pincel.
Importado por Model, View e Controller sem criar acoplamento entre eles.
"""

from enum import Enum, auto


class ToolType(Enum):
    """Ferramentas de desenho do Mini Paint (Requisito 2)."""

    PENCIL = auto()  # Lápis
    ERASER = auto()  # Borracha
    LINE = auto()  # Linha reta (Bresenham)
    RECT_HOLLOW = auto()  # Retângulo vazado
    RECT_FILLED = auto()  # Retângulo preenchido
    CIRCLE_HOLLOW = auto()  # Círculo vazado (ponto médio)
    CIRCLE_FILLED = auto()  # Círculo preenchido
    FLOOD_FILL = auto()  # Balde de tinta (BFS)


# Nome legível para cada ferramenta (exibido na sidebar e no título)
TOOL_LABELS: dict = {
    ToolType.PENCIL: "LAPIS",
    ToolType.ERASER: "BORRACHA",
    ToolType.LINE: "LINHA",
    ToolType.RECT_HOLLOW: "RETANGULO",
    ToolType.RECT_FILLED: "RET CHEIO",
    ToolType.CIRCLE_HOLLOW: "CIRCULO",
    ToolType.CIRCLE_FILLED: "CIR CHEIO",
    ToolType.FLOOD_FILL: "BALDE",
}

# Atalhos de teclado (GLFW KEY_*) para cada ferramenta
# Mapeados em app.py usando glfw.KEY_P, glfw.KEY_E, etc.
TOOL_SHORTCUTS: dict = {
    ToolType.PENCIL: "P",
    ToolType.ERASER: "E",
    ToolType.LINE: "L",
    ToolType.RECT_HOLLOW: "R",
    ToolType.RECT_FILLED: "SHIFT+R",
    ToolType.CIRCLE_HOLLOW: "C",
    ToolType.CIRCLE_FILLED: "SHIFT+C",
    ToolType.FLOOD_FILL: "F",
}

# Espessuras disponíveis: nome → pixels (Requisito 4)
BRUSH_SIZES: dict = {
    "FINO": 1,
    "MEDIO": 5,
    "GROSSO": 11,
}

# Paleta de 8 cores pré-definidas (nome, RGB) — Requisito 3
PALETTE: list = [
    ("PRETO", (0, 0, 0)),
    ("BRANCO", (255, 255, 255)),
    ("VERMELHO", (255, 0, 0)),
    ("VERDE", (0, 200, 0)),
    ("AZUL", (0, 0, 255)),
    ("AMARELO", (255, 255, 0)),
    ("CIANO", (0, 255, 255)),
    ("MAGENTA", (255, 0, 255)),
]
