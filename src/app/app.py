"""
src/app/app.py  ·  CAMADA CONTROLLER (MVC)
==========================================
Controlador principal do Mini Paint.

Papel do Controller
-------------------
O Controller é o único elo entre Model e View:
  • Recebe eventos brutos do GLFW (mouse, teclado).
  • Mantém o estado da aplicação (ferramenta, cor, espessura, arrasto).
  • Traduz eventos em chamadas aos algoritmos do Model (canvas + tools).
  • Notifica o View (Renderer + UI) para redesenhar quando necessário.

Model   → src/canvas/canvas.py  +  src/tools/*.py
View    → src/renderer/renderer.py  +  src/ui/ui.py  +  src/ui/font.py
Controller → src/app/app.py  (este arquivo)

Estado mantido pelo Controller
------------------------------
current_tool  : ToolType    — ferramenta ativa
current_color : tuple       — cor de desenho (R,G,B)
brush_size    : int         — espessura em pixels
mouse_down    : bool        — botão esquerdo pressionado
start_pos     : (int,int)|None  — posição do clique inicial (formas)
prev_pos      : (int,int)|None  — posição anterior (lápis/borracha)
snapshot      : ndarray|None    — cópia do canvas para preview de formas

Mecanismo de preview
--------------------
Ferramentas de forma (linha, retângulo, círculo) precisam mostrar a
forma crescendo em tempo real durante o arrasto, sem deixar rastros:

    MOUSEBUTTONDOWN  → salva snapshot do canvas
    B1-MOTION        → restaura snapshot + desenha forma temporária
    MOUSEBUTTONUP    → restaura snapshot + aplica forma definitiva

Mapeamento de coordenadas
-------------------------
GLFW entrega coordenadas de janela (x, y) com (0,0) no canto superior
esquerdo.  O canvas começa em x = SIDEBAR_W.
    canvas_x = glfw_x - SIDEBAR_W
    canvas_y = glfw_y   (y=0 já é o topo, igual ao framebuffer NumPy)
"""

import math
import glfw

from src.canvas.canvas import Canvas, CANVAS_WIDTH, CANVAS_HEIGHT
from src.renderer.renderer import Renderer, SIDEBAR_W
from src.ui.ui import draw_sidebar, hit_test
from src.tools.tools import ToolType, PALETTE, BRUSH_SIZES
from src.tools.pencil import draw_pencil_dot, draw_pencil_stroke
from src.tools.eraser import draw_eraser_dot, draw_eraser_stroke
from src.tools.line import draw_line
from src.tools.rectangle import draw_rect_hollow, draw_rect_filled
from src.tools.circle import draw_circle_hollow, draw_circle_filled
from src.tools.flood_fill import flood_fill_4

# ── Constantes ────────────────────────────────────────────────────────────────
BG_COLOR = (255, 255, 255)
DEFAULT_COLOR = (0, 0, 0)
DEFAULT_SIZE = 1
WIN_W = SIDEBAR_W + CANVAS_WIDTH
WIN_H = CANVAS_HEIGHT


class App:
    """
    Controller MVC do Mini Paint.

    Instanciado pelo main.py após a criação da janela GLFW.
    Registra todos os callbacks e mantém o loop de renderização.
    """

    def __init__(self, window) -> None:
        self.window = window

        # ── Model ──────────────────────────────────────────────────────────────
        self.canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, BG_COLOR)

        # ── View ───────────────────────────────────────────────────────────────
        # O cursor do GLFW usa coordenadas de janela lógicas, mas o viewport
        # deve usar o tamanho do framebuffer em displays HiDPI.
        win_w, win_h = glfw.get_window_size(window)
        fb_w, fb_h = glfw.get_framebuffer_size(window)
        self.renderer = Renderer(win_w, win_h, fb_w, fb_h)
        self.renderer.setup_projection()

        # ── Estado do Controller ───────────────────────────────────────────────
        self.current_tool: ToolType = ToolType.PENCIL
        self.current_color: tuple = DEFAULT_COLOR
        self.brush_size: int = DEFAULT_SIZE
        self.mouse_down: bool = False
        self.start_pos = None  # (cx, cy) clique inicial
        self.prev_pos = None  # posição anterior
        self.snapshot = None  # cópia para preview

        # ── Registra callbacks GLFW ────────────────────────────────────────────
        glfw.set_mouse_button_callback(window, self._on_mouse_button)
        glfw.set_cursor_pos_callback(window, self._on_cursor_pos)
        glfw.set_key_callback(window, self._on_key)
        glfw.set_window_size_callback(window, self._on_window_resize)
        glfw.set_framebuffer_size_callback(window, self._on_framebuffer_resize)

    # ── Loop principal ─────────────────────────────────────────────────────────

    def run(self) -> None:
        """Loop de eventos e renderização. Encerra quando a janela fecha."""
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self._render()
        glfw.terminate()

    def _render(self) -> None:
        """Renderiza um frame: fundo → canvas → sidebar."""
        self.renderer.begin_frame()

        # Envia framebuffer à GPU se houve alteração (canvas.dirty)
        self.renderer.upload_canvas(self.canvas)
        # Desenha o quad texturizado na área do canvas
        self.renderer.draw_canvas_quad(self.canvas)

        # Desenha a sidebar (View pura — não altera o Model)
        draw_sidebar(self.current_tool, self.brush_size, self.current_color)

        self.renderer.end_frame(self.window)

    # ── Callbacks de mouse ─────────────────────────────────────────────────────

    def _on_mouse_button(self, window, button, action, mods) -> None:
        if button != glfw.MOUSE_BUTTON_LEFT:
            return

        mx, my = glfw.get_cursor_pos(window)
        mx, my = int(mx), int(my)

        if action == glfw.PRESS:
            # ── Clique na sidebar? ──
            if mx < SIDEBAR_W:
                result = hit_test(mx, my)
                if result:
                    kind, value = result
                    if kind == "tool":
                        self.current_tool = value
                    elif kind == "size":
                        self.brush_size = value
                    elif kind == "color":
                        self.current_color = value
                return  # não inicia traço no canvas

            # ── Clique no canvas ──
            cx, cy = self._to_canvas(mx, my)
            self.mouse_down = True
            self.start_pos = (cx, cy)
            self.prev_pos = (cx, cy)
            self._on_press(cx, cy)

        elif action == glfw.RELEASE:
            if not self.mouse_down:
                return
            cx, cy = self._to_canvas(mx, my)
            self._on_release(cx, cy)
            self.mouse_down = False
            self.snapshot = None

    def _on_cursor_pos(self, window, xpos, ypos) -> None:
        if not self.mouse_down:
            return
        cx, cy = self._to_canvas(int(xpos), int(ypos))
        self._on_drag(cx, cy)
        self.prev_pos = (cx, cy)

    # ── Lógica de arrasto ──────────────────────────────────────────────────────

    def _on_press(self, x: int, y: int) -> None:
        """Início do traço ou forma."""
        tool = self.current_tool

        if tool == ToolType.PENCIL:
            draw_pencil_dot(self.canvas, x, y, self.current_color, self.brush_size)

        elif tool == ToolType.ERASER:
            draw_eraser_dot(self.canvas, x, y, BG_COLOR, self.brush_size)

        elif tool == ToolType.FLOOD_FILL:
            flood_fill_4(self.canvas, x, y, self.current_color)
            self.mouse_down = False  # operação atômica — sem arrasto

        else:
            # Ferramentas de forma: salva snapshot para preview
            self.snapshot = self.canvas.save_snapshot()

    def _on_drag(self, x: int, y: int) -> None:
        """Atualização durante arrasto."""
        tool = self.current_tool
        px, py = self.prev_pos

        if tool == ToolType.PENCIL:
            draw_pencil_stroke(
                self.canvas,
                px,
                py,
                x,
                y,
                self.current_color,
                self.brush_size,
            )

        elif tool == ToolType.ERASER:
            draw_eraser_stroke(
                self.canvas,
                px,
                py,
                x,
                y,
                BG_COLOR,
                self.brush_size,
            )

        elif self.snapshot is not None:
            # Preview: restaura o snapshot e redesenha a forma temporária
            self._apply_shape(x, y)

    def _on_release(self, x: int, y: int) -> None:
        """Finalização: aplica a forma definitivamente."""
        if self.snapshot is not None:
            self._apply_shape(x, y)  # commit final no canvas

    def _apply_shape(self, x: int, y: int) -> None:
        """Restaura snapshot e redesenha a forma com as coordenadas atuais."""
        self.canvas.restore_snapshot(self.snapshot)
        sx, sy = self.start_pos
        tool = self.current_tool
        color = self.current_color
        thick = self.brush_size

        if tool == ToolType.LINE:
            draw_line(self.canvas, sx, sy, x, y, color, thick)

        elif tool == ToolType.RECT_HOLLOW:
            draw_rect_hollow(self.canvas, sx, sy, x, y, color, thick)

        elif tool == ToolType.RECT_FILLED:
            draw_rect_filled(self.canvas, sx, sy, x, y, color)

        elif tool == ToolType.CIRCLE_HOLLOW:
            r = int(math.hypot(x - sx, y - sy))
            draw_circle_hollow(self.canvas, sx, sy, r, color, thick)

        elif tool == ToolType.CIRCLE_FILLED:
            r = int(math.hypot(x - sx, y - sy))
            draw_circle_filled(self.canvas, sx, sy, r, color)

    # ── Callback de teclado ────────────────────────────────────────────────────

    def _on_key(self, window, key, scancode, action, mods) -> None:
        if action not in (glfw.PRESS, glfw.REPEAT):
            return

        shift = bool(mods & glfw.MOD_SHIFT)

        # Ferramentas
        if key == glfw.KEY_P:
            self.current_tool = ToolType.PENCIL
        elif key == glfw.KEY_E:
            self.current_tool = ToolType.ERASER
        elif key == glfw.KEY_L:
            self.current_tool = ToolType.LINE
        elif key == glfw.KEY_R:
            self.current_tool = ToolType.RECT_FILLED if shift else ToolType.RECT_HOLLOW
        elif key == glfw.KEY_C:
            self.current_tool = (
                ToolType.CIRCLE_FILLED if shift else ToolType.CIRCLE_HOLLOW
            )
        elif key == glfw.KEY_F:
            self.current_tool = ToolType.FLOOD_FILL

        # Espessura
        elif key == glfw.KEY_1:
            self.brush_size = 1
        elif key == glfw.KEY_2:
            self.brush_size = 5
        elif key == glfw.KEY_3:
            self.brush_size = 11

        # Cores via setas do teclado: Left/Up = anterior, Right/Down = próximo
        elif key in (glfw.KEY_LEFT, glfw.KEY_RIGHT, glfw.KEY_UP, glfw.KEY_DOWN):
            # Encontra índice atual na paleta (por cor). Se não achar, assume 0.
            try:
                cur_idx = next(i for i, p in enumerate(PALETTE) if p[1] == self.current_color)
            except StopIteration:
                cur_idx = 0

            if key in (glfw.KEY_RIGHT, glfw.KEY_DOWN):
                cur_idx = (cur_idx + 1) % len(PALETTE)
            else:
                cur_idx = (cur_idx - 1) % len(PALETTE)

            self.current_color = PALETTE[cur_idx][1]

        # Limpar canvas
        elif key == glfw.KEY_DELETE or key == glfw.KEY_N:
            self.canvas.clear()

        # Fechar
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)

    # ── Resize ────────────────────────────────────────────────────────────────

    def _on_window_resize(self, window, width, height) -> None:
        self.renderer.win_w = width
        self.renderer.win_h = height
        self.renderer.setup_projection()

    def _on_framebuffer_resize(self, window, width, height) -> None:
        self.renderer.fb_w = width
        self.renderer.fb_h = height
        self.renderer.setup_projection()

    # ── Utilitário ─────────────────────────────────────────────────────────────

    @staticmethod
    def _to_canvas(wx: int, wy: int) -> tuple:
        """
        Converte coordenadas de janela GLFW para coordenadas do canvas.
            canvas_x = glfw_x - SIDEBAR_W    (desconta a sidebar)
            canvas_y = glfw_y                (y=0 no topo em ambos)
        Valores podem ficar negativos ou maiores que o canvas — as
        funções put_pixel/get_pixel já tratam o boundary check.
        """
        return wx - SIDEBAR_W, wy
