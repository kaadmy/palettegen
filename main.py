#! /usr/bin/python3

# Palette generator

from palettegenerator import *

pg = PaletteGenerator(16, 16)

pg.addRange((0, 0, 0), (255, 255, 255), 16, PG_POW, 1.7)

pg.addRange((20, 10, 0), (160, 120, 70), 16, PG_POW, 2.0)
pg.addRange((20, 40, 50), (230, 240, 250), 16, PG_POW, 3.0)

pg.addRange((250, 150, 40), (110, 200, 250), 10)

pg.write("final_palette.png")
pg.writeLightmap("final_lightmap.png", 32)
