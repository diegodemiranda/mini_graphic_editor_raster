"""
src/tools/rectangle.py  ·  CAMADA MODEL (algoritmo)
====================================================
Retângulo Vazado e Preenchido.

Vazado
------
Quatro segmentos de reta via draw_line (Bresenham). Suporta espessura.

Preenchido
----------
Scan-line fill: varre cada linha y ∈ [y0, y1] e escreve os pixels
de x0 a x1 diretamente no array NumPy (sem chamar put_pixel em loop,
para aproveitar a escrita vetorizada).

A escrita ainda é O((x1-x0)*(y1-y0)) pixels, mas o overhead Python
por pixel é eliminado pelo NumPy.
"""

from src.canvas.canvas import Canvas
from src.tools.line import draw_line
import numpy as np


def _normalize(x0: int, y0: int, x1: int, y1: int):
    """Garante que (x0,y0) é o canto superior-esquerdo."""
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    return x0, y0, x1, y1


def draw_rect_hollow(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, color: tuple, thickness: int = 1
) -> None:
    """4 lados rasterizados com Bresenham."""
    x0, y0, x1, y1 = _normalize(x0, y0, x1, y1)
    draw_line(canvas, x0, y0, x1, y0, color, thickness)  # topo
    draw_line(canvas, x1, y0, x1, y1, color, thickness)  # direita
    draw_line(canvas, x0, y1, x1, y1, color, thickness)  # base
    draw_line(canvas, x0, y0, x0, y1, color, thickness)  # esquerda


def draw_rect_filled(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, color: tuple
) -> None:
    """
    Scan-line fill via escrita vetorizada NumPy.
    Equivalente a iterar put_pixel(x, y, color) para todo (x,y) na área,
    mas sem o overhead de loop Python por pixel.
    """
    x0, y0, x1, y1 = _normalize(x0, y0, x1, y1)
    # Clamping ao canvas
    x0 = max(x0, 0)
    y0 = max(y0, 0)
    x1 = min(x1, canvas.width - 1)
    y1 = min(y1, canvas.height - 1)
    if x0 > x1 or y0 > y1:
        return
    canvas.pixels[y0 : y1 + 1, x0 : x1 + 1] = color
    canvas.dirty = True
