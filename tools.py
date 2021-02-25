import wx
import cv2 as cv

__all__ = ["get_imagesize", "loadimage_cv", "saveimage_cv", "toWxBitmap"]

from numba import np


def get_imagesize(img):
    return (0, 0) if img is None else img.shape[1::-1]


def loadimage_cv(name):
    try:
        img = cv.cvtColor(cv.imread(name), cv.COLOR_BGR2RGB)
    except Exception:
        return None
    return img


def saveimage_cv(name, img):
    try:
        cv.imwrite(name, img)
        return True
    except Exception:
        return False


def toWxBitmap(img):
    h, w = img.shape[:2]
    try:
        image = wx.Bitmap.FromBuffer(w, h, img)
    except Exception:
        image = wx.BitmapFromBuffer(w, h, img)
    return image
