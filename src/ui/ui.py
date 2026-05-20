"""
src/ui/ui.py  ·  CAMADA VIEW
==============================
Renderização da sidebar (painel lateral esquerdo) via OpenGL imediato.

Layout (largura = SIDEBAR_W = 240 px, altura = janela inteira)
--------------------------------------------------------------
  y   0 –  20 : título "MINI PAINT"
  y  25 – 205 : 8 botões de ferramenta  (22 px cada)
  y 210 – 240 : separador + rótulo "TAMANHO"
  y 245 – 305 : 3 botões de espessura   (20 px cada)
  y 310 – 340 : separador + rótulo "CORES"
  y 345 – 430 : grade 2×4 de swatches   (34×34 px)
  y 440 – 480 : retângulo de cor ativa + rótulo

Todo desenho usa primitivas OpenGL imediatas (GL_QUADS, GL_LINES,
GL_POINTS para texto via font.py).

Regiões clicáveis
-----------------
A UI não tem widgets — a detecção de clique é feita no Controller
(app.py) comparando as coordenadas do mouse com os retângulos aqui
definidos.  A função `hit_test(x, y)` retorna o que foi clicado.
"""

from OpenGL.GL import (
    glBegin,
    glEnd,
    glVertex2f,
    glColor3f,
    GL_QUADS,
    GL_LINE_LOOP,
    GL_LINES,
)
from src.tools.tools import ToolType, TOOL_LABELS, BRUSH_SIZES, PALETTE
from src.ui.font import draw_text, text_width, text_height

# ── Constantes de layout ──────────────────────────────────────────────────────
SIDEBAR_W = 240
PAD = 8  # margem interna
BTN_H = 22  # altura dos botões de ferramenta
SIZE_H = 20  # altura dos botões de espessura
SWATCH = 34  # tamanho dos swatches de cor (px)

# Paleta ordenada (mesmo de tools.py) — usada para indexação dos swatches
_PALETTE = PALETTE  # lista de (nome, (R,G,B))
_TOOLS = list(ToolType)


# ── Helpers de desenho primitivo ─────────────────────────────────────────────


def _filled_rect(
    x: float, y: float, w: float, h: float, r: float, g: float, b: float
) -> None:
    """Quad preenchido. Coordenadas em pixels (y=0 no topo)."""
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def _border_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    r: float,
    g: float,
    b: float,
    lw: float = 1.0,
) -> None:
    """Contorno de retângulo."""
    from OpenGL.GL import glLineWidth

    glLineWidth(lw)
    glColor3f(r, g, b)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()
    glLineWidth(1.0)


def _hline(y: float, r: float, g: float, b: float) -> None:
    """Linha horizontal separadora na sidebar."""
    glColor3f(r, g, b)
    glBegin(GL_LINES)
    glVertex2f(PAD, y)
    glVertex2f(SIDEBAR_W - PAD, y)
    glEnd()


# ── Cálculo de posições ───────────────────────────────────────────────────────


def _tool_rect(index: int):
    """Retorna (x, y, w, h) do botão da ferramenta `index`."""
    x = PAD
    y = 26 + index * (BTN_H + 2)
    w = SIDEBAR_W - 2 * PAD
    return x, y, w, BTN_H


def _size_rect(index: int):
    """Retorna (x, y, w, h) do botão de espessura `index`."""
    x = PAD
    y = 250 + index * (SIZE_H + 4)
    w = SIDEBAR_W - 2 * PAD
    return x, y, w, SIZE_H


def _swatch_rect(index: int):
    """Retorna (x, y, w, h) do swatch de cor `index` (grade 2 colunas)."""
    col = index % 2
    row = index // 2
    x = PAD + col * (SWATCH + 4)
    y = 360 + row * (SWATCH + 4)
    return x, y, SWATCH, SWATCH


def active_color_rect():
    """Retângulo do indicador de cor ativa."""
    return PAD, 540, SIDEBAR_W - 2 * PAD, 30


# ── Renderização da sidebar ───────────────────────────────────────────────────


def draw_sidebar(active_tool: ToolType, active_size: int, active_color: tuple) -> None:
    """
    Renderiza toda a sidebar para o frame atual.

    Parâmetros
    ----------
    active_tool  : ferramenta selecionada no Controller
    active_size  : espessura ativa em pixels
    active_color : cor ativa (R, G, B) 0–255
    """
    # ── Fundo ──
    _filled_rect(0, 0, SIDEBAR_W, 9999, 0.18, 0.18, 0.20)

    # ── Título ──
    draw_text("MINI PAINT", PAD, 6, color=(0.9, 0.7, 0.2), scale=2)

    _hline(26, 0.35, 0.35, 0.35)

    # ── Botões de ferramenta ──
    size_names = list(BRUSH_SIZES.keys())

    for i, tool in enumerate(_TOOLS):
        x, y, w, h = _tool_rect(i)
        is_active = tool == active_tool

        # Fundo do botão
        if is_active:
            _filled_rect(x, y, w, h, 0.18, 0.42, 0.75)
        else:
            _filled_rect(x, y, w, h, 0.25, 0.25, 0.27)

        # Borda sutil
        _border_rect(x, y, w, h, 0.35, 0.35, 0.38)

        # Rótulo (texto bitmap)
        label = TOOL_LABELS[tool]
        tx = x + 4
        ty = y + (h - text_height(scale=2)) // 2
        txt_color = (1.0, 1.0, 1.0) if is_active else (0.75, 0.75, 0.75)
        draw_text(label, tx, ty, color=txt_color, scale=2)

    # ── Seção Tamanho ──
    _hline(222, 0.35, 0.35, 0.35)
    draw_text("TAMANHO", PAD, 228, color=(0.6, 0.6, 0.6), scale=2)

    for i, (name, px) in enumerate(BRUSH_SIZES.items()):
        x, y, w, h = _size_rect(i)
        is_active = px == active_size

        _filled_rect(
            x,
            y,
            w,
            h,
            0.18,
            0.42,
            0.75 if is_active else 0.0,
        )
        if not is_active:
            _filled_rect(x, y, w, h, 0.25, 0.25, 0.27)

        _border_rect(x, y, w, h, 0.35, 0.35, 0.38)

        label = f"{name} ({px}px)"
        ty = y + (h - text_height(scale=2)) // 2
        txt_color = (1.0, 1.0, 1.0) if is_active else (0.70, 0.70, 0.70)
        draw_text(label, x + 4, ty, color=txt_color, scale=2)

    # ── Seção Cores ──
    _hline(330, 0.35, 0.35, 0.35)
    draw_text("CORES", PAD, 337, color=(0.6, 0.6, 0.6), scale=2)

    for i, (name, rgb) in enumerate(_PALETTE):
        x, y, w, h = _swatch_rect(i)
        r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
        _filled_rect(x, y, w, h, r, g, b)

        # Borda branca se for a cor ativa
        if rgb == active_color:
            _border_rect(x - 1, y - 1, w + 2, h + 2, 1.0, 1.0, 1.0, 2.0)
        else:
            _border_rect(x, y, w, h, 0.4, 0.4, 0.4)

    # ── Cor ativa ──
    _hline(530, 0.35, 0.35, 0.35)
    draw_text("COR ATIVA", PAD, 516, color=(0.6, 0.6, 0.6), scale=2)

    ax, ay, aw, ah = active_color_rect()
    r, g, b = active_color[0] / 255, active_color[1] / 255, active_color[2] / 255
    _filled_rect(ax, ay, aw, ah, r, g, b)
    _border_rect(ax, ay, aw, ah, 0.5, 0.5, 0.5)


# ── Hit-test: o que foi clicado na sidebar ───────────────────────────────────


def hit_test(mx: float, my: float):
    """
    Retorna o elemento da sidebar clicado por um clique em (mx, my).

    Retornos possíveis
    ------------------
    ('tool',  ToolType)   — botão de ferramenta
    ('size',  int)        — botão de espessura (valor em pixels)
    ('color', tuple)      — swatch de cor (R, G, B)
    None                  — nenhum elemento atingido
    """
    if mx < 0 or mx >= SIDEBAR_W:
        return None

    # Ferramentas
    for i, tool in enumerate(_TOOLS):
        x, y, w, h = _tool_rect(i)
        if x <= mx < x + w and y <= my < y + h:
            return ("tool", tool)

    # Espessuras
    for i, (name, px) in enumerate(BRUSH_SIZES.items()):
        x, y, w, h = _size_rect(i)
        if x <= mx < x + w and y <= my < y + h:
            return ("size", px)

    # Swatches de cor
    for i, (name, rgb) in enumerate(_PALETTE):
        x, y, w, h = _swatch_rect(i)
        if x <= mx < x + w and y <= my < y + h:
            return ("color", rgb)

    return None
