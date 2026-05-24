"""
src/io/io_handler.py
====================

Funcoes para salvar e carregar o canvas em um formato binario proprio.

Formato do arquivo .mpr:
    MAGIC   4 bytes   identificador "MPR1"
    WIDTH   4 bytes   largura do canvas
    HEIGHT  4 bytes   altura do canvas
    CHANS   1 byte    quantidade de canais de cor, sempre 3 para RGB
    DATA    N bytes   pixels RGB em ordem linha por linha
"""

import struct

import numpy as np

MAGIC = b"MPR1"
CHANNELS = 3


def save_canvas(canvas, path: str) -> None:
    """
    Salva o framebuffer do canvas em um arquivo binario proprio.

    O canvas.pixels ja esta no formato ideal:
        altura x largura x 3 canais RGB
        dtype uint8, ou seja, cada canal ocupa 1 byte
    """
    with open(path, "wb") as file:
        file.write(MAGIC)

        header = struct.pack(
            "<IIB",
            canvas.width,
            canvas.height,
            CHANNELS,
        )
        file.write(header)

        file.write(canvas.pixels.tobytes())


def load_canvas(canvas, path: str) -> None:
    """
    Carrega um arquivo .mpr e substitui os pixels atuais do canvas.
    """
    with open(path, "rb") as file:
        magic = file.read(4)
        if magic != MAGIC:
            raise ValueError("Arquivo raster invalido")

        header = file.read(9)
        width, height, channels = struct.unpack("<IIB", header)

        if channels != CHANNELS:
            raise ValueError("Formato de cor nao suportado")

        expected_size = width * height * channels
        data = file.read(expected_size)

        if len(data) != expected_size:
            raise ValueError("Arquivo incompleto ou corrompido")

    pixels = np.frombuffer(data, dtype=np.uint8)
    pixels = pixels.reshape((height, width, channels))

    canvas.width = width
    canvas.height = height
    canvas.pixels = pixels.copy()
    canvas.dirty = True