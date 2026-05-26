# 🎨 Mini Paint — Editor Gráfico Raster
 
Projeto acadêmico de Computação Gráfica: editor gráfico raster com algoritmos
manuais de rasterização e interface OpenGL.
 
---
 
## Status do Projeto
 
O editor já implementa as ferramentas básicas de desenho, o framebuffer em
`src/canvas/canvas.py`, o renderizador OpenGL em `src/renderer/renderer.py`,
o controlador em `src/app/app.py`, a interface da sidebar em `src/ui/ui.py`
e salvamento/carregamento de arquivos `.mpr` em `src/io/io_handler.py`.
 
---
 
## Estrutura do Projeto
 
```
mini_graphic_editor_raster/
├── main.py                    # Ponto de entrada
├── requirements.txt
├── README.md
└── src/
    ├── canvas/
    │   └── canvas.py          # Framebuffer: put_pixel / get_pixel
    ├── tools/
    │   ├── tools.py           # Enum de ferramentas e valores de UI
    │   ├── pencil.py          # Lápis — pincel circular + Bresenham suavizado
    │   ├── eraser.py          # Borracha — pincel quadrado com cor de fundo
    │   ├── line.py            # Linha reta — algoritmo de Bresenham
    │   ├── rectangle.py       # Retângulo vazado e preenchido
    │   ├── circle.py          # Círculo — algoritmo do ponto médio
    │   └── flood_fill.py      # Balde de tinta — BFS 4 conectado
    ├── renderer/
    │   └── renderer.py        # Renderização do canvas via OpenGL
    ├── app/
    │   └── app.py             # Loop principal, estado e eventos
    ├── ui/
    │   ├── ui.py              # Sidebar e elementos de UI
    │   └── font.py            # Fonte bitmap utilizada no UI
    ├── io/                    # Salvar e carregar arquivos .mpr
        └── io_handler.py
    
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
 
## Controles
 
| Tecla              | Ação                                |
|--------------------|--------------------------------------|
| `P`                | Lápis                               |
| `E`                | Borracha                            |
| `L`                | Linha reta                          |
| `R`                | Retângulo vazado                    |
| `Shift+R`          | Retângulo preenchido                |
| `C`                | Círculo vazado                      |
| `Shift+C`          | Círculo preenchido                  |
| `F`                | Balde de tinta                      |
| `1`                | Espessura fina (1 px)               |
| `2`                | Espessura média (5 px)              |
| `3`                | Espessura grossa (11 px)            |
| `← / ↑ / → / ↓`    | Selecionar cor anterior/próxima      |
| `N` / `Delete`     | Limpar canvas                       |
| `S`                | Salvar canvas em `desenho.mpr`      |
| `O`                | Carregar canvas de `desenho.mpr`    |
| `Esc`              | Sair                                |
 
---

## Formato `.mpr`

O projeto usa um formato binário próprio para salvar imagens raster. O arquivo
começa com um cabeçalho simples contendo identificador, largura, altura e número
de canais RGB. Depois do cabeçalho, vêm os bytes dos pixels em ordem linha por
linha.
