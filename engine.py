import wx
import cv2 as cv


def get_imagesize(img):
    return (0, 0) if img is None else (img.shape[1], img.shape[0])


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


def detect_cv(srcimg):
    img = srcimg[:]
    result = {
        "Square": [],
        "Rectangle": [],
        "Trapezoid": [],
        "Triangle": [],
        "Circle": []
    }
    img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_grey, (11, 11), 0)
    _, thr = cv.threshold(img_blur, 244, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thr, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
        cv.drawContours(img, [approx], 0, (0, 0, 0), 3)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            result.get("Triangle").append((x, y))
        elif len(approx) == 4:
            x1, y1, w, h = cv.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                result.get("Square").append((x, y))
            elif 1.2 <= aspect_ratio <= 2:
                result.get("Rectangle").append((x, y))
            else:
                result.get("Trapezoid").append((x, y))
        elif len(approx) <= 17:
            result.get("Circle").append((x, y))
        else:
            pass
    return result, img
