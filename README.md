# 🎨 Mini Paint — Editor Gráfico Raster
 
Projeto acadêmico de Computação Gráfica: editor gráfico raster com algoritmos
de rasterização implementados manualmente.
 
---
 
## Estrutura do Projeto
 
```
mini_paint/
├── main.py                    # Ponto de entrada
├── requirements.txt
├── README.md
└── src/
    ├── canvas/
    │   └── canvas.py          # Framebuffer: put_pixel / get_pixel
    ├── tools/
    │   ├── tools.py           # Enum de ferramentas
    │   ├── pencil.py          # Lápis  — pincel circular + Bresenham suavizado
    │   ├── eraser.py          # Borracha — pincel quadrado com cor de fundo
    │   ├── line.py            # Linha reta — algoritmo de Bresenham
    │   ├── rectangle.py       # Retângulo vazado e preenchido
    │   ├── circle.py          # Círculo — algoritmo do ponto médio (Bresenham)
    │   └── flood_fill.py      # Balde de tinta — BFS 4/8 conectado
    ├── renderer/
    │   └── renderer.py        # Renderização OpenGL
    ├── app/
    │   └── app.py             # Loop principal, estado, eventos
    ├── ui/                    # (TODO — Requisito 3/4/5)
    │   └── ui.py
    ├── io/                    # (TODO — Requisito 5: salvar/carregar)
    │   └── io_handler.py
    └── transforms/            # (TODO — Objetivo: transformações geométricas)
        └── transforms.py
```
 
---
 
## Dependências
 
```bash
pip install -r requirements.txt
```
 
---
 
## Como Executar
 
```bash
python main.py
```
 
---
 
## Controles:
 
| Tecla         | Ação                          |
|---------------|-------------------------------|
| `P`           | Lápis                         |
| `E`           | Borracha                      |
| `L`           | Linha reta                    |
| `R`           | Retângulo vazado               |
| `Shift+R`     | Retângulo preenchido           |
| `C`           | Círculo vazado                 |
| `Shift+C`     | Círculo preenchido             |
| `F`           | Balde de tinta (flood fill)    |
| `1`           | Espessura: fina (1 px)        |
| `2`           | Espessura: média (5 px)       |
| `3`           | Espessura: grossa (11 px)     |
| `KP 0–7`      | Selecionar cor (teclado num.) |
| `Delete`      | Limpar canvas                 |
 
---
