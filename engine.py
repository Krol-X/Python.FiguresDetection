from math import log

from PIL import Image


def fixrgb(rgb):
    return (
        min(255, max(0, rgb[0])),
        min(255, max(0, rgb[1])),
        min(255, max(0, rgb[2]))
    )


def apply_fun(src: Image.Image, fun, param: list) -> Image:
    result = src.copy()
    for j in range(result.height):
        for i in range(result.width):
            pix = src.getpixel((i, j))
            fun(pix, param)
            result.putpixel((i, j), pix)
    return result


def negative(pix, param):
    return 255 - pix[0], 255 - pix[1], 255 - pix[2]


def halftone(pix, param):
    x = 0.3 * pix[0] + 0.59 * pix[1] + 0.11 * pix[2]
    return x, x, x


def binary(pix, param):
    x = param[0]
    return param[1] if (pix[0]+pix[1]+pix[2])/3 <= x else param[2]


def linear_brightness(pix, param):
    x = param[0]
    result = (pix[0] + x, pix[1] + x, pix[2] + x)
    return fixrgb(result)


def nonlinear_brightness(pix, param):
    x = param[0]
    result = (
        pix[0] + log(1 + (265 - pix[0])) * x,
        pix[1] + log(1 + (265 - pix[1])) * x,
        pix[2] + log(1 + (265 - pix[2])) * x,
    )
    return fixrgb(result)


def get_brightness(src: Image.Image) -> float:
    pass


if __name__ == "__main__":
    img = Image.open("1.jpg")
    apply_fun(img, linear_brightness, [0])
