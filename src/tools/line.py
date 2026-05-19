"""
src/tools/line.py  ·  CAMADA MODEL (algoritmo)
===============================================
Linha reta — Algoritmo de Bresenham (1965).

Teoria
------
Determina quais pixels de uma grade discreta melhor aproximam um
segmento contínuo usando exclusivamente aritmética inteira.

Formulação incremental utilizada:
    err = dx + dy           (dy já é negativo: dy = -|dy_real|)
    Loop:
        e2 = 2 * err
        Se e2 >= dy  →  avança em x:  err += dy;  x += sx
        Se e2 <= dx  →  avança em y:  err += dx;  y += sy

Espessura
---------
Para thickness > 1, cada pixel rasterizado é expandido para um
quadrado de lado `thickness` centrado nele.  Produz linhas espessas
com extremidades quadradas (comportamento padrão de editores de imagem).
"""

from src.canvas.canvas import Canvas


def _thick_pixel(canvas: Canvas, x: int, y: int, color: tuple, t: int) -> None:
    """Expande um pixel para quadrado de lado t centrado em (x, y)."""
    r = t // 2
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            canvas.put_pixel(x + dx, y + dy, color)


def draw_line(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, color: tuple, thickness: int = 1
) -> None:
    """
    Rasteriza o segmento de (x0,y0) a (x1,y1) via Bresenham.

    Funciona em qualquer octante sem casos especiais:
    sx/sy definem a direção e o erro acumulado gerencia ambos os eixos.

    Parâmetros
    ----------
    thickness : espessura em pixels — 1 = um pixel, >1 = pixel quadrado.
    """
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        _thick_pixel(canvas, x0, y0, color, thickness)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
