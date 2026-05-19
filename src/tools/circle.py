"""
src/tools/circle.py  ·  CAMADA MODEL (algoritmo)
=================================================
Círculo Vazado e Preenchido.

VAZADO — Algoritmo do Ponto Médio (Bresenham para Círculos)
------------------------------------------------------------
Rasteriza o contorno explorando a simetria de 8 oitantes.
Começa em (x=0, y=radius) e avança enquanto x < y.

Parâmetro de decisão inicial:   d = 1 - radius
    Se d < 0:  próximo pixel → (x+1,  y  );  d += 2x + 3
    Se d ≥ 0:  próximo pixel → (x+1, y-1 );  d += 2(x-y) + 5

Para cada (x,y) calculado, os 8 pontos simétricos são pintados.
Todo o algoritmo usa aritmética inteira pura.

PREENCHIDO — Scan-line com verificação Pitagórica inteira
---------------------------------------------------------
Para cada linha dy ∈ [-radius, radius], encontra o maior dx inteiro
tal que dx² + dy² ≤ radius² (sem sqrt) e preenche a linha horizontal.
"""

from src.canvas.canvas import Canvas
import numpy as np

# ── Auxiliares ────────────────────────────────────────────────────────────────


def _plot8(
    canvas: Canvas, cx: int, cy: int, x: int, y: int, color: tuple, thickness: int
) -> None:
    """Pinta os 8 pontos simétricos com pincel quadrado de `thickness`."""
    r = thickness // 2
    for px, py in [
        (cx + x, cy + y),
        (cx - x, cy + y),
        (cx + x, cy - y),
        (cx - x, cy - y),
        (cx + y, cy + x),
        (cx - y, cy + x),
        (cx + y, cy - x),
        (cx - y, cy - x),
    ]:
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                canvas.put_pixel(px + dx, py + dy, color)


def _hline_numpy(canvas: Canvas, x0: int, x1: int, y: int, color: tuple) -> None:
    """Linha horizontal via escrita vetorizada NumPy. O(x1-x0)."""
    if not (0 <= y < canvas.height):
        return
    x0 = max(x0, 0)
    x1 = min(x1, canvas.width - 1)
    if x0 <= x1:
        canvas.pixels[y, x0 : x1 + 1] = color


# ── API pública ────────────────────────────────────────────────────────────────


def draw_circle_hollow(
    canvas: Canvas, cx: int, cy: int, radius: int, color: tuple, thickness: int = 1
) -> None:
    """
    Contorno do círculo via Algoritmo do Ponto Médio.
    Complexidade: O(radius).
    """
    if radius <= 0:
        canvas.put_pixel(cx, cy, color)
        return

    x, y = 0, radius
    d = 1 - radius  # parâmetro de decisão inicial

    _plot8(canvas, cx, cy, x, y, color, thickness)

    while x < y:
        if d < 0:
            # Ponto médio dentro do círculo → mantém y
            d += 2 * x + 3
        else:
            # Ponto médio fora do círculo → decrementa y
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        _plot8(canvas, cx, cy, x, y, color, thickness)

    canvas.dirty = True


def draw_circle_filled(
    canvas: Canvas, cx: int, cy: int, radius: int, color: tuple
) -> None:
    """
    Preenchimento circular via scan-line + verificação Pitagórica inteira.

    Para cada dy ∈ [-radius, radius]:
        Encontra dx máximo tal que dx² + dy² ≤ radius²  (sem sqrt)
        Preenche a linha [cx-dx, cx+dx] na altura cy+dy.

    Complexidade: O(radius²).
    """
    if radius <= 0:
        canvas.put_pixel(cx, cy, color)
        return

    r2 = radius * radius
    for dy in range(-radius, radius + 1):
        y = cy + dy
        # Busca decrescente: parte do máximo possível
        dx = radius
        while dx >= 0 and dx * dx + dy * dy > r2:
            dx -= 1
        _hline_numpy(canvas, cx - dx, cx + dx, y, color)

    canvas.dirty = True
