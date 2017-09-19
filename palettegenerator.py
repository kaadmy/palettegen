
#
# PaletteGenerator
#
# Handles creating and adding colors to an arbitrary palette, then writing it to an image file
#
# All color values are RGB tuples from 0-255
# The 0th palette index is not automatically added, but many programs may treat this as null
# Unset pixels will be fully opaque black
# Loading palettes requires a 24-bit RBG image
#

import math

from PIL import Image

PG_LINEAR = 0
PG_POW = 1

def lerp(a, b, ratio):
    return a + ((b - a) * ratio)

def plerp(a, b, ratio, v):
    ratio = pow(ratio, v)

    return a + ((b - a) * ratio)

def darknessDifference(idealColor, checkColor):
    diffTable = [
        abs(idealColor[0] - checkColor[0]),
        abs(idealColor[1] - checkColor[1]),
        abs(idealColor[2] - checkColor[2])
    ]

    return sum([x * x for x in diffTable])

class PaletteException(Exception):
    pass

class PaletteGenerator:

    def __init__(self, w, h):
        self.makeSize(w, h)

    def makeSize(self, w, h):
        self.w = w
        self.h = h

        self.length = w * h
        self.plength = 0

        self.palette = []

        print("Palette resized to %d colors at %dx%d" % (self.length, w, h))

    def addColor(self, color):
        self.palette.append(color)

        self.plength += 1

        if len(self.palette) > self.length:
            raise PaletteException("Palette size exceeded, please expand the palette size")

    def addRange(self, startColor, endColor, length, interpolation = 0, value = 1):
        if length < 2:
            raise PaletteException("Adding a color range smaller than 2 pixels, use addColor instead")

        for i in range(length):
            ratio = i / (length - 1)

            # -1 to ensure the first and last colors are exactly what is specified

            c = None

            # Handle multiple interpolation methods

            if interpolation == PG_POW:
                c = [int(plerp(startColor[x], endColor[x], ratio, value)) for x in range(3)]
            else:
                c = [int(lerp(startColor[x], endColor[x], ratio)) for x in range(3)]

            self.addColor(tuple(c))

    def load(self, path):
        image = Image.open(path, "r")

        self.makeSize(image.width, image.height)

        for y in range(image.height):
            for x in range(image.width):
                self.addColor(image.getpixel((x, y)))

        print("Loaded %d colors from %s" % (self.length, path))

    def write(self, path):
        image = Image.new("RGB", (self.w, self.h))

        for i in range(self.plength):
            print("Generating palette [%3d%%]\r" % (math.ceil((i / self.plength) * 100)), end = "")

            image.putpixel((i % self.w, int(i / self.w)), self.palette[i])

        image.save(path)

        print("\nWrote %d colors with %d unused colors to %s" %
              (self.plength, self.length - self.plength, path))

    def writeLightmap(self, path, shades):
        image = Image.new("RGB", (shades, self.length))

        for i in range(self.plength):
            print("Generating lightmap [%3d%%]\r" % (math.ceil((i / self.plength) * 100)), end = "")

            for shade in range(shades):
                idealColor = [int(x - (x * (shade / shades))) for x in self.palette[i]]

                bestColor = 0 # 0th palette index
                bestDiff = 100000 # Largest darkness difference

                for c in range(len(self.palette)):
                    diff = darknessDifference(idealColor, self.palette[c])

                    if diff < bestDiff:
                        bestDiff = diff
                        bestColor = c

                image.putpixel((shade, i), self.palette[bestColor])

        image.save(path)

        print("\nWrote %d lightmap colors with %d shades to %s" %
              (self.plength, shades, path))
