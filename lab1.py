import numpy as np
from PIL import Image
from Point import Point
from operator import methodcaller

# Задание 1


def createImageMatrix(H, W):
    blackImage = np.zeros((H, W), dtype=np.uint8)

    whiteImage = np.full((H, W), 255, dtype=np.uint8)

    RGBImage = np.full((H, W, 3), (255, 0, 0), dtype=np.uint8)

    gradientImage = np.zeros((H, W, 3), dtype=np.uint8)

    for i in range(H):
        for j in range(W):
            for chan in range(3):
                gradientImage[i, j, chan] = (i + j + chan) % 256

    return blackImage, whiteImage, RGBImage, gradientImage


def saveImage(imgMatrix, name, rotate=False):
    img = Image.fromarray(imgMatrix)
    if rotate:
        img = img.rotate(90)
    img.save(f'{name}.png')


# Задание 2


def drawLine(point1, point2, image, color, algorithmType):
    if algorithmType == 0:
        t = 0.
        while t < 1.:
            x = int(point1.x * (1.0 - t) + point2.x * t)
            y = int(point1.y * (1.0 - t) + point2.y * t)
            image[x, y] = color
            t += 0.01
    elif algorithmType == 1:
        x = point1.x
        while x <= point2.x:
            t = float((x - point1.x)/(point2.x - point1.x))
            y = int(point1.y*(1-t) + point2.y * t)
            image[x, y] = color
            x += 1
    elif algorithmType == 2 or algorithmType == 3:
        steep = False
        if abs(point1.x - point2.x) < abs(point1.y - point2.y):
            point1.x, point1.y = point1.y, point1.x
            point2.x, point2.y = point2.y, point2.x
            steep = True
        if point1.x > point2.x:
            point1.x, point2.x = point2.x, point1.x
            point1.y, point2.y = point2.y, point1.y
        if algorithmType == 2:
            x = point1.x
            while x <= point2.x:
                t = float((x - point1.x) / (point2.x - point1.x))
                y = int(point1.y * (1.0 - t) + point2.y * t)
                if steep:
                    image[y, x] = color
                else:
                    image[x, y] = color
                x += 1
        else:
            dx = int(point2.x - point1.x)
            dy = int(point2.y - point1.y)
            derr = abs(dy / float(dx)) if dx != 0 else 0
            err = 0
            y = int(point1.y)
            x = int(point1.x)
            while x <= point2.x:
                if steep:
                    image[y, x] = color
                else:
                    image[x, y] = color
                err += derr
                if err > .5:
                    y += 1 if point2.y > point1.y else -1
                    err -= 1.
                x += 1

    return image


# Задание 3

def getNodesFromFile(filePath, toPoint=False):
    nodes = []
    with open(filePath, 'r') as f:
        for i in f.readlines():
            if 'v ' in i:
                result = i.strip().split(' ')
                result.pop(0)
                result = list(map(float, result))
                if toPoint:
                    result = Point(result[0], result[1])
                nodes.append(result)
    return nodes


# Задание 4


def drawNodes(nodes, H, W, color, transformNumber):
    image = np.zeros([H, W, 3], dtype=np.uint8)
    for node in nodes:
        if isinstance(node, Point):
            x = int(transformNumber * node.x + 500)
            y = int(transformNumber * node.y + 500)
        else:
            x = int(transformNumber * node[0] + 500)
            y = int(transformNumber * node[1] + 500)
        image[x, y] = color
    return image


# Задание 5


def getPolygons(filePath):
    polygons = []
    with open(filePath, 'r') as f:
        for i in f.readlines():
            if 'f ' in i:
                result = i.strip().split(' ')
                result.pop(0)
                result = list(map(methodcaller('split', '/'), result))
                result = list(map(int, [result[0][0], result[1][0], result[2][0]]))
                polygons.append(result)
    return polygons

# Задание 6


def drawPolygons(H, W, nodes, polygons, transformNumber):
    image = drawNodes(nodes, H, W, [255, 255, 255], transformNumber)
    saveImage(image, 'Test', rotate=True)
    for i in polygons:
        point1 = Point(transformNumber * nodes[i[0] - 1].x + 500, transformNumber * nodes[i[0] - 1].y + 500)
        point2 = Point(transformNumber * nodes[i[1] - 1].x + 500, transformNumber * nodes[i[1] - 1].y + 500)
        image = drawLine(point1, point2, image, [255, 255, 255], 3)

    return image