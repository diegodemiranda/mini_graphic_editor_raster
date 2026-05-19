Trabalho 1 - Mini Paint: Implementação de um Editor Grafico Raster com
Fundamentos de Computação Gráfica"
Objetivos de aprendizado
• Compreender e manipular uma matriz de pixels (framebuffer);
• Implementar algoritmos de rasterização de primitivas (linhas,
círculos, retângulos, polígonos);
• Aplicar transformações geométricas simples (translado, rotação,
escala) em objetos desenhados;
• Implementar preenchimento de regiões (flood fill ou boundary fill);
• Gerenciar interação do usuário (mouse/teclado) para desenho em
tempo real;
• Entender o conceito de cores (RGB) e operações de blend.
Requisitos funcionais mínimos (versão básica)
O software deve permitir ao usuário:
1. Área de desenho (canvas) de tamanho fixo (ex.: 800x600 pixels).
2. Ferramentas essenciais:
• Lápis (pincel de 1 pixel).
• Borracha (pinta com a cor de fundo).
• Linha reta (algoritmo de Bresenham ou DDA).
• Retângulo vazado e preenchido.
• Círculo vazado e preenchido.
• Balde de tinta (flood fill 4 ou 8 conectado).
1. Paleta de cores com pelo menos 8 cores pré-definidas (preto, branco,
vermelho, verde, azul, amarelo, ciano, magenta).
2. Seleção de espessura do pincel/ferramentas (3 opções: fino, médio,
grosso).
3. Botão "Novo" (limpar canvas com cor de fundo).
4. Botão "Salvar" (exportar para um formato simples, como BMP, PPM
ou PNG via biblioteca).
Requisitos técnicos (núcleo da avaliação) Sem uso de bibliotecas
gráficas de alto nível
• para desenho primitivo (ex.: não pode usar drawLine pronta). Você
pode usar SDL2, SFML, OpenGL com g|DrawPixels, ou até uma
biblioteca simples como graphics.h (Turbo C++) apenas para criar
a janela e acesso ao framebuffer.
O aluno deve implementar:
• put_pixel (x, y, cor)
• get_pixel (x, y)
• Algoritmo de linha (Bresenham).
• Algoritmo de círculo (Bresenham ou ponto médio).
• Flood fill recursivo ou com pilha/queue (não usar função pronta).
• Tratamento de eventos do mouse (clique, arrasto, soltar).
• Estrutura de dados para o canvas: matriz 2D de inteiros (cores
indexadas) ou struct RGB.
Critérios de avaliação
Critério
Funcionalidades obrigatórias completas
Correta implementação dos algoritmos de rasterização
(sem trapaça com funções prontas)
Interface usável e responsiva (feedback visual, mouse)
Organização do código (modul., comentários, clareza)
Peso
40%
25%
15%
20%
