"""
src/tools/pencil.py  ·  CAMADA MODEL (algoritmo)
=================================================
Ferramenta Lápis.

Primitiva
---------
Pincel circular de raio r = size // 2.
Para size == 1: pinta exatamente 1 pixel (lápis de 1 px — Requisito 2).
Fórmula: dx²+dy² ≤ r²  →  pinta o pixel (cx+dx, cy+dy).

Interpolação
------------
Durante o arrasto do mouse, a posição atual e a anterior podem estar
distantes vários pixels (movimentação rápida). O Algoritmo de Bresenham
é aplicado entre as duas posições para garantir traço contínuo.

Todo pixel é escrito via canvas.put_pixel — sem nenhuma função de
desenho de biblioteca.
"""

from src.canvas.canvas import Canvas

# ── Pincel circular ────────────────────────────────────────────────────────────


def _circular_brush(canvas: Canvas, cx: int, cy: int, color: tuple, size: int) -> None:
    """
    Pinta um disco de raio r=size//2 centrado em (cx, cy).
    Complexidade: O(size²).
    """
    r = size // 2
    if r == 0:
        canvas.put_pixel(cx, cy, color)
        return
    r2 = r * r
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r2:
                canvas.put_pixel(cx + dx, cy + dy, color)


# ── API pública ────────────────────────────────────────────────────────────────


def draw_pencil_dot(canvas: Canvas, x: int, y: int, color: tuple, size: int) -> None:
    """Pinta um único ponto. Chamado no MOUSEBUTTONDOWN."""
    _circular_brush(canvas, x, y, color, size)


def draw_pencil_stroke(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, color: tuple, size: int
) -> None:
    """
    Interpolação Bresenham de (x0,y0) a (x1,y1).

    Percorre todos os pixels da linha rasterizada e aplica o pincel
    circular em cada ponto, produzindo traço contínuo independentemente
    da velocidade de movimento do mouse.

    Algoritmo de Bresenham (inteiro, sem ponto flutuante):
        dx =  |x1-x0|,   dy = -|y1-y0|
        err = dx + dy
        A cada passo: e2 = 2*err
            Se e2 >= dy → avança em x
            Se e2 <= dx → avança em y
    """
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        _circular_brush(canvas, x0, y0, color, size)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
