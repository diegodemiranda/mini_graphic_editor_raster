"""
renderer.py
-----------
Responsável por transferir o framebuffer (NumPy array do Canvas) para a
janela pygame e apresentá-lo na tela.

Pipeline de renderização
------------------------
1. `pygame.surfarray.blit_array` copia o array NumPy diretamente para uma
   Surface pygame, sem iterar pixel a pixel em Python.
   - O array do Canvas tem forma (height, width, 3) → precisa ser
     transposto para (width, height, 3) porque o surfarray indexa por (x, y).
2. A Surface é blitada para a janela principal (screen).
3. `pygame.display.flip()` envia o frame para o monitor.

Uso de pygame
-------------
pygame é utilizado APENAS para:
    • Criar a janela (pygame.display.set_mode)
    • Tratar eventos (pygame.event — em app.py)
    • Exibir o framebuffer (surfarray.blit_array + flip)
Todo o desenho ocorre no NumPy array via put_pixel / algoritmos próprios.
"""

import numpy as np
import pygame

from src.canvas.canvas import Canvas


class Renderer:
    """
    Gerencia a janela pygame e a atualização do framebuffer na tela.

    Atributos
    ----------
    screen  : pygame.Surface — janela principal
    surface : pygame.Surface — buffer de trabalho (mesmo tamanho que o canvas)
    """

    def __init__(self, title: str, width: int, height: int) -> None:
        """
        Inicializa pygame e cria a janela.

        Parâmetros
        ----------
        title  : str — título inicial da janela
        width  : int — largura em pixels
        height : int — altura em pixels
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.surface = pygame.Surface((width, height))
        pygame.display.set_caption(title)

    # ── Atualização ────────────────────────────────────────────────────────────

    def update(self, canvas: Canvas) -> None:
        """
        Copia o framebuffer do Canvas para a janela e apresenta o frame.

        O array canvas.pixels tem forma (H, W, 3).
        surfarray.blit_array espera (W, H, 3) → transpõe eixos 0 e 1.
        """
        # Transpõe (height, width, 3) → (width, height, 3)
        surf_array = np.transpose(canvas.pixels, (1, 0, 2))
        pygame.surfarray.blit_array(self.surface, surf_array)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

    def set_title(self, title: str) -> None:
        """Atualiza o título da janela (usado para exibir ferramenta/tamanho)."""
        pygame.display.set_caption(title)

    def destroy(self) -> None:
        """Finaliza o pygame."""
        pygame.quit()
