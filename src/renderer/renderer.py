"""
src/renderer/renderer.py  ·  CAMADA VIEW
=========================================
Responsável por exibir o framebuffer do Canvas na janela OpenGL.

Pipeline
--------
1. O array NumPy (H, W, 3) do Canvas é carregado como textura GL_RGB
   via glTexImage2D (upload inicial) ou glTexSubImage2D (atualização).
2. A textura é desenhada como um quad 2D na área do canvas.
3. A projeção ortográfica mapeia coordenadas de janela (pixels, y=0 em
   cima) diretamente para NDC, sem necessidade de conversão manual.

Uso do OpenGL
-------------
Apenas para:
  • Criar e atualizar a textura do framebuffer (glTexImage2D)
  • Desenhar o quad textured (imediato — GL_QUADS)
  • Configurar a projeção (glOrtho)
  • Preparar o estado de renderização (glEnable, glClear, etc.)
Nenhuma chamada de "desenho primitivo" de biblioteca — todo pixel
que aparece no canvas veio de put_pixel nos algoritmos do Model.
"""

import ctypes
import numpy as np

from OpenGL.GL import (
    glGenTextures,
    glBindTexture,
    glTexParameteri,
    glTexImage2D,
    glTexSubImage2D,
    glEnable,
    glDisable,
    GL_TEXTURE_2D,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_MAG_FILTER,
    GL_NEAREST,
    GL_RGB,
    GL_UNSIGNED_BYTE,
    glBegin,
    glEnd,
    glTexCoord2f,
    glVertex2f,
    GL_QUADS,
    glClear,
    glClearColor,
    GL_COLOR_BUFFER_BIT,
    glMatrixMode,
    glLoadIdentity,
    glOrtho,
    GL_PROJECTION,
    GL_MODELVIEW,
    glViewport,
    glColor3f,
)

from src.canvas.canvas import Canvas

# ── Largura da sidebar (área não-canvas à esquerda) ───────────────────────────
SIDEBAR_W = 240


class Renderer:
    """
    Gerencia a textura OpenGL do framebuffer e a renderização do canvas.

    Atributos
    ----------
    win_w, win_h : int  — dimensões totais da janela (sidebar + canvas)
    texture_id   : int  — ID da textura OpenGL
    """

    def __init__(self, win_w: int, win_h: int) -> None:
        self.win_w = win_w
        self.win_h = win_h
        self._tex_initialized = False
        self.texture_id = self._create_texture()

    # ── Setup de projeção ─────────────────────────────────────────────────────

    def setup_projection(self) -> None:
        """
        Configura projeção ortográfica em coordenadas de janela (pixels).
        y=0 no topo, y=win_h na base — compatível com as coordenadas GLFW.
        Chamado uma vez na inicialização e sempre que a janela for redimensionada.
        """
        glViewport(0, 0, self.win_w, self.win_h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # left, right, bottom, top, near, far
        glOrtho(0, self.win_w, self.win_h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    # ── Textura do canvas ─────────────────────────────────────────────────────

    def _create_texture(self) -> int:
        """Gera e configura a textura OpenGL (filtragem NEAREST = pixels nítidos)."""
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return tex

    def upload_canvas(self, canvas: Canvas) -> None:
        """
        Envia o framebuffer NumPy à GPU.

        • Primeira chamada: glTexImage2D (aloca memória na GPU).
        • Chamadas seguintes: glTexSubImage2D (só atualiza o conteúdo).
        • Só executa se canvas.dirty == True (evita uploads desnecessários).

        O array (H, W, 3) uint8 é passado diretamente — sem cópia adicional —
        pois o NumPy C-order produz exatamente o layout GL_RGB row-major.
        """
        if not canvas.dirty:
            return

        # NumPy usa y=0 no topo; OpenGL usa y=0 na base.
        # Invertemos o eixo Y do array antes do upload para que a imagem
        # apareça corretamente orientada na textura.
        data = np.ascontiguousarray(canvas.pixels[::-1])

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        if not self._tex_initialized:
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                canvas.width,
                canvas.height,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                data,
            )
            self._tex_initialized = True
        else:
            glTexSubImage2D(
                GL_TEXTURE_2D,
                0,
                0,
                0,
                canvas.width,
                canvas.height,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                data,
            )

        canvas.dirty = False

    # ── Renderização do quad do canvas ────────────────────────────────────────

    def draw_canvas_quad(self, canvas: Canvas) -> None:
        """
        Desenha o quad 2D texturizado que exibe o canvas.
        Posicionado à direita da sidebar: x ∈ [SIDEBAR_W, win_w], y ∈ [0, win_h].
        """
        x0 = float(SIDEBAR_W)
        x1 = float(self.win_w)
        y0 = 0.0
        y1 = float(self.win_h)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glColor3f(1.0, 1.0, 1.0)  # sem tinte

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x0, y0)  # topo-esquerdo
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x1, y0)  # topo-direito
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x1, y1)  # base-direito
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x0, y1)  # base-esquerdo
        glEnd()

        glDisable(GL_TEXTURE_2D)

    # ── Frame ─────────────────────────────────────────────────────────────────

    def begin_frame(self) -> None:
        glClearColor(0.17, 0.17, 0.17, 1.0)  # fundo da sidebar (cinza escuro)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

    def end_frame(self, window) -> None:
        import glfw

        glfw.swap_buffers(window)
