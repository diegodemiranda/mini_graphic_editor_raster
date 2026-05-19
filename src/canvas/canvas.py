"""
src/canvas/canvas.py  ·  CAMADA MODEL
======================================
Framebuffer principal do Mini Paint.

Estrutura de dados
------------------
NumPy array de forma (height, width, 3) dtype=uint8.
    pixels[y, x, 0]  →  canal R
    pixels[y, x, 1]  →  canal G
    pixels[y, x, 2]  →  canal B

O array é contíguo em memória (C-order) e pode ser passado diretamente
ao OpenGL via glTexSubImage2D — sem conversão adicional.

Flag `dirty`
------------
Marcada como True sempre que algum pixel é alterado.
O Renderer a consulta para saber se deve re-enviar os dados à GPU,
evitando uploads desnecessários por frame.
"""

import numpy as np

# ── Dimensões padrão do canvas (Requisito 1) ──────────────────────────────────
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


class Canvas:
    """
    Framebuffer 2-D representado como array NumPy (H, W, 3) uint8.

    Único ponto de acesso a pixels: put_pixel / get_pixel.
    Todo algoritmo de desenho usa exclusivamente essas primitivas.
    """

    def __init__(
        self,
        width: int = CANVAS_WIDTH,
        height: int = CANVAS_HEIGHT,
        bg_color: tuple = (255, 255, 255),
    ) -> None:
        self.width = width
        self.height = height
        self.bg_color = bg_color
        # Framebuffer inicializado com a cor de fundo
        self.pixels: np.ndarray = np.full((height, width, 3), bg_color, dtype=np.uint8)
        self.dirty: bool = True  # força upload inicial à GPU

    # ── Primitivas de pixel ────────────────────────────────────────────────────

    def put_pixel(self, x: int, y: int, color: tuple) -> None:
        """
        Escreve a cor RGB em (x, y).  O(1).
        Ignora silenciosamente coordenadas fora dos limites.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y, x, 0] = color[0]
            self.pixels[y, x, 1] = color[1]
            self.pixels[y, x, 2] = color[2]
            self.dirty = True

    def get_pixel(self, x: int, y: int) -> tuple:
        """
        Lê a cor RGB de (x, y).  O(1).
        Retorna bg_color para coordenadas fora dos limites.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            p = self.pixels[y, x]
            return (int(p[0]), int(p[1]), int(p[2]))
        return self.bg_color

    def in_bounds(self, x: int, y: int) -> bool:
        """Verifica se (x, y) está dentro da área de desenho."""
        return 0 <= x < self.width and 0 <= y < self.height

    # ── Operações de estado ────────────────────────────────────────────────────

    def clear(self) -> None:
        """Preenche todo o canvas com bg_color (botão Novo — Requisito 5)."""
        self.pixels[:] = self.bg_color
        self.dirty = True

    def save_snapshot(self) -> np.ndarray:
        """
        Retorna cópia profunda do framebuffer atual.
        Usado pelo mecanismo de preview de formas no Controller:
            pressiona → salva snapshot
            arrasta   → restaura snapshot + redesenha forma temporária
            solta     → aplica forma definitiva
        """
        return self.pixels.copy()

    def restore_snapshot(self, snapshot: np.ndarray) -> None:
        """Restaura o framebuffer a partir de um snapshot salvo."""
        self.pixels[:] = snapshot
        self.dirty = True
