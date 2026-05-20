"""
src/tools/flood_fill.py  ·  CAMADA MODEL (algoritmo)
=====================================================
Balde de Tinta — Flood Fill BFS iterativo.

Algoritmo
---------
Implementação iterativa com `collections.deque` (FIFO).
NÃO usa recursão (evitaria RecursionError em áreas grandes).
NÃO usa nenhuma função de flood fill de biblioteca.

Passos:
    1. Lê target_color = pixel clicado.
    2. Se target == fill_color: retorna (sem efeito — evita loop infinito).
    3. Enfileira (x, y) e pinta-o ANTES de enfileirar.
    4. Loop: retira da fila → examina vizinhos (4 ou 8):
         Se vizinho tem target_color → pinta e enfileira.

Pintar antes de enfileirar garante que o mesmo pixel nunca seja
inserido duas vezes → O(N) tempo e O(N) espaço, onde N = pixels
conectados com target_color.

Acesso direto ao NumPy array (canvas.pixels) para máximo desempenho
em Python puro — sem chamar get_pixel/put_pixel em loop.
"""

from collections import deque
from src.canvas.canvas import Canvas

# ── Vizinhanças ────────────────────────────────────────────────────────────────
_N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
_N8 = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1))


def _bfs_fill(canvas: Canvas,
              x: int, y: int,
              fill_color: tuple,
              neighbors: tuple) -> None:
    """Núcleo genérico BFS — parametrizado pela vizinhança."""
    if not canvas.in_bounds(x, y):
        return

    pix = canvas.pixels
    w, h = canvas.width, canvas.height

    # Cor-alvo (a ser substituída)
    tp = pix[y, x]
    tr, tg, tb = int(tp[0]), int(tp[1]), int(tp[2])
    fr, fg, fb = int(fill_color[0]), int(fill_color[1]), int(fill_color[2])

    # Nada a fazer se a cor já é a desejada
    if (tr, tg, tb) == (fr, fg, fb):
        return

    q = deque()
    q.append((x, y))
    pix[y, x] = (fr, fg, fb)        # pinta antes de enfileirar

    while q:
        cx, cy = q.popleft()
        for ddx, ddy in neighbors:
            nx, ny = cx + ddx, cy + ddy
            if 0 <= nx < w and 0 <= ny < h:
                p = pix[ny, nx]
                # Compara canal a canal (mais rápido que np.array_equal)
                if int(p[0]) == tr and int(p[1]) == tg and int(p[2]) == tb:
                    pix[ny, nx] = (fr, fg, fb)
                    q.append((nx, ny))

    canvas.dirty = True


# ── API pública ────────────────────────────────────────────────────────────────

def flood_fill_4(canvas: Canvas, x: int, y: int,
                 fill_color: tuple) -> None:
    """
    Flood fill 4-conectado (cima, baixo, esquerda, direita).
    Comportamento padrão do balde — não atravessa diagonais.
    """
    _bfs_fill(canvas, x, y, fill_color, _N4)


def flood_fill_8(canvas: Canvas, x: int, y: int,
                 fill_color: tuple) -> None:
    """
    Flood fill 8-conectado (inclui diagonais).
    Mais agressivo — preenche regiões separadas apenas por cantos.
    """
    _bfs_fill(canvas, x, y, fill_color, _N8)

