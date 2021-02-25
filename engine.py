import cv2 as cv

__all__ = ["detect_cv"]


def detect_cv(srcimg):
    img = srcimg.copy()
    result = {
        "Square": [],
        "Rectangle": [],
        "Trapezoid": [],
        "Triangle": [],
        "Circle": [],
        "Ellipse": []
    }
    img_grey = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_blur = cv.GaussianBlur(img_grey, (11, 11), 0)
    _, thr = cv.threshold(img_blur, 244, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thr, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv.contourArea(contour)
        peri = cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, 0.01 * peri, True)
        cv.drawContours(img, [approx], 0, (0, 0, 0), 3)
        x = round(approx.ravel()[0])
        y = round(approx.ravel()[1] - 5)
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
        elif len(approx) <= 17 and peri > 0:
            # PI*R^2 / (2*PI*R)^2 = 1/4*PI = 0.079577
            t = area / (peri * peri)
            if 0.07 <= t <= 0.087:
                result.get("Circle").append((x, y))
            else:
                result.get("Ellipse").append((x, y))
        else:
            pass
    return result, img
