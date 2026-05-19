"""
src/tools/eraser.py  ·  CAMADA MODEL (algoritmo)
=================================================
Ferramenta Borracha.

Comportamento
-------------
Pinta pixels com a cor de fundo (bg_color), simulando apagamento.
Usa pincel QUADRADO para diferenciação visual do lápis (circular).
Tamanho efetivo dobrado: eraser_size = size * 2 + 1 para maior ergonomia.

A interpolação Bresenham garante traço contínuo durante o arrasto,
exatamente como no lápis.
"""

from src.canvas.canvas import Canvas

# ── Pincel quadrado ────────────────────────────────────────────────────────────


def _square_brush(canvas: Canvas, cx: int, cy: int, color: tuple, size: int) -> None:
    """Pinta quadrado de lado `size` centrado em (cx, cy)."""
    r = size // 2
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            canvas.put_pixel(cx + dx, cy + dy, color)


# ── Interpolação Bresenham (reutilizada internamente) ─────────────────────────


def _bresenham_walk(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, color: tuple, size: int
) -> None:
    """Walk de Bresenham aplicando pincel quadrado em cada passo."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy

    while True:
        _square_brush(canvas, x0, y0, color, size)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


# ── API pública ────────────────────────────────────────────────────────────────


def draw_eraser_dot(canvas: Canvas, x: int, y: int, bg_color: tuple, size: int) -> None:
    _square_brush(canvas, x, y, bg_color, size * 2 + 1)


def draw_eraser_stroke(
    canvas: Canvas, x0: int, y0: int, x1: int, y1: int, bg_color: tuple, size: int
) -> None:
    _bresenham_walk(canvas, x0, y0, x1, y1, bg_color, size * 2 + 1)
