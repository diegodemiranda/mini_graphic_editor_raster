"""
main.py  ·  Ponto de entrada do Mini Paint
==========================================
Responsabilidade ÚNICA: inicializar o GLFW, criar a janela OpenGL e
instanciar o Controller (App).  Nenhuma lógica de aplicação aqui.

Por que separar main.py de app.py?
-----------------------------------
Em MVC, o "ponto de entrada" não é o Controller — é um bootstrapper
neutro que monta as peças.  Isso permite, por exemplo, testar o
Controller (App) em isolamento passando uma janela mock, ou trocar o
backend de janelamento sem tocar na lógica de negócio.

Configuração da janela OpenGL
------------------------------
• Versão: OpenGL 2.1 
• Tamanho fixo: (SIDEBAR_W + CANVAS_WIDTH) × CANVAS_HEIGHT = 950 × 600.
• VSync habilitado (swap_interval=1) para evitar tearing e limitar CPU.
"""

import sys
import glfw
from OpenGL.GL import glEnable, GL_POINT_SMOOTH, GL_LINE_SMOOTH

from src.canvas.canvas import CANVAS_WIDTH, CANVAS_HEIGHT
from src.renderer.renderer import SIDEBAR_W
from src.app.app import App

WIN_W = SIDEBAR_W + CANVAS_WIDTH   # 150 + 800 = 950
WIN_H = CANVAS_HEIGHT              # 600


def init_glfw() -> object:
    """
    Inicializa o GLFW e cria a janela OpenGL.

    Retorna
    -------
    window : GLFWwindow — handle da janela criada.

    Encerra o processo com código 1 se a inicialização falhar.
    """
    if not glfw.init():
        print("[ERRO] Falha ao inicializar o GLFW.", file=sys.stderr)
        sys.exit(1)

    # ── Hints de contexto OpenGL ──────────────────────────────────────────────
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)   # canvas de tamanho fixo

    window = glfw.create_window(WIN_W, WIN_H, "Mini Paint", None, None)
    if not window:
        print("[ERRO] Falha ao criar janela GLFW.", file=sys.stderr)
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)
    glfw.swap_interval(1)    # VSync: limita ao refresh rate do monitor

    # Suavização de pontos e linhas (melhora a aparência da fonte bitmap)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)

    return window


def main() -> None:
    """Bootstrapper: monta a janela e entrega o controle ao Controller."""
    print("Mini Paint — iniciando...")
    print(f"  Janela  : {WIN_W} × {WIN_H} px")
    print(f"  Canvas  : {CANVAS_WIDTH} × {CANVAS_HEIGHT} px")
    print(f"  Sidebar : {SIDEBAR_W} px")
    print()
    print("  Atalhos de teclado:")
    print("    P        → Lápis          E → Borracha")
    print("    L        → Linha          F → Balde de tinta")
    print("    R        → Retângulo      Shift+R → Retângulo preenchido")
    print("    C        → Círculo        Shift+C → Círculo preenchido")
    print("    1/2/3    → Espessura (Fino / Médio / Grosso)")
    print("    KP 0-7   → Selecionar cor pelo teclado numérico")
    print("    N/Delete → Novo (limpar canvas)")
    print("    Esc      → Sair")
    print()

    window = init_glfw()
    app    = App(window)   # Controller — registra callbacks e monta Model/View
    app.run()              # loop principal até a janela ser fechada


if __name__ == "__main__":
    main()