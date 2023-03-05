import numpy as np
from Parser import Parser
from PIL import Image

from Point import Point


def calculateNormal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    nx = (y1 - y0) * (z1 - z2) - (z1 - z0) * (y1 - y2)
    ny = (x1 - x0) * (z1 - z2) - (z1 - z0) * (x1 - x2)
    nz = (x1 - x0) * (y1 - y2) - (y1 - y0) * (x1 - x2)
    return nx, ny, nz


def scalarProduct(x0, y0, z0, x1, y1, z1):
    res = (x0 * x1 + y0 * y1 + z0 * z1) / (np.sqrt(x0 * x0 + y0 * y0 + z0 * z0) * np.sqrt(x1 * x1 + y1 * y1 + z1 * z1))
    return res


def calculateBaricentricCoord(x, y, x0, y0, x1, y1, x2, y2):
    lambda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
    lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
    lambda2 = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / ((x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))

    assert lambda0 + lambda1 + lambda2 == 1.0

    return lambda0, lambda1, lambda2


class ImageCreator:
    def __init__(self, width=100, height=100, channels=3, img=None):
        self.width = width
        self.height = height
        self.channels = channels
        self.zBuffer = np.zeros((self.height, self.width), dtype=float)
        self.zBuffer[:, :] = 30000
        if img is None:
            self.img = np.zeros((self.height, self.width, self.channels), dtype=float)
        else:
            self.img = img

    def setPixel(self, x, y, color):
        self.img[x, y] = color

    def save(self, path):
        im = Image.fromarray(self.img, 'RGB')
        im.save(path)

    def drawLineV1(self, point1, point2, color = (255, 255, 255), delta=0.1):
        for t in np.arange(0, 1, delta):
            x = int(point1.x * (1.0 - t) + point2.x * t)
            y = int(point1.y * (1.0 - t) + point2.y * t)
            self.setPixel(x, y, color)

    def drawLineV2(self, point1, point2, color=(255, 255, 255)):
        for x in range(int(point1.x), int(point2.x), 1):
            t = (x - point1.x) / (float)(point2.x - point1.x)
            y = int(point1.y * (1.0 - t) + point2.y * t)
            self.setPixel(int(x), int(y), color)

    def drawLineV3(self, point1, point2, color=(255, 255, 255)):
        steep = False
        if np.abs(point1.x - point2.x) < np.abs(point1.y - point2.y):
            point1.x, point1.y = point1.y, point1.x
            point2.x, point2.y = point2.y, point2.x
            steep = True
        if point1.x > point2.x:
            point1.x, point2.x = point2.x, point1.x
            point1.y, point2.y = point2.y, point1.y

        for x in range(int(point1.x), int(point2.x), 1):
            t = (x - point1.x) / (float)(point2.x - point1.x)
            y = int(point1.y * (1.0 - t) + point2.y * t)
            if steep:
                self.setPixel(int(y), int(x), color)
            else:
                self.setPixel(int(x), int(y), color)

    def drawLineV4(self, point1, point2, color=(255, 255, 255)):
        # Алгоритм Брезенхема
        steep = False
        if np.abs(point1.x - point2.x) < np.abs(point1.y - point2.y):
            point1.x, point1.y = point1.y, point1.x
            point2.x, point2.y = point2.y, point2.x
            steep = True
        if point1.x > point2.x:
            point1.x, point2.x = point2.x, point1.x
            point1.y, point2.y = point2.y, point1.y
        dx = point2.x - point1.x
        dy = point2.y - point1.y
        derr = abs(dy / float(dx)) if dx != 0 else 0
        err = 0
        y = int(point1.y)
        for x in range(int(point1.x), int(point2.x), 1):
            if steep:
                self.setPixel(int(y), int(x), color)
            else:
                self.setPixel(int(x), int(y), color)
            err += derr
            if err > 0.5:
                y += 1 if point2.y > point1.y else -1
                err -= 1

    def drawTriangle(self, p1, p2, p3, color=(255, 255, 255)):
        xmin = min(p1.x, p2.x, p3.x) if min(p1.x, p2.x, p3.x) < 0 else 0
        xmax = max(p1.x, p2.x, p3.x) if max(p1.x, p2.x, p3.x) < self.width else self.width
        ymin = min(p1.y, p2.y, p3.y) if min(p1.y, p2.y, p3.y) < 0 else 0
        ymax = max(p1.y, p2.y, p3.y) if max(p1.y, p2.y, p3.y) < self.height else self.height
        for xIndex in range(round(xmin), round(xmax)):
            for yIndex in range(round(ymin), round(ymax)):
                bar1, bar2, bar3 = calculateBaricentricCoord(xIndex, yIndex, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)
                if bar1 > 0 and bar2 > 0 and bar3 > 0:
                    self.img[xIndex, yIndex] = color

    def drawTriangle_v2(self, p1, p2, p3, zBuffer,
                        color = (255, 255, 255)):
        xmin = min(p1.x, p2.x, p3.x) if min(p1.x, p2.x, p3.x) < 0 else 0
        xmax = max(p1.x, p2.x, p3.x) if max(p1.x, p2.x, p3.x) < self.width else self.width
        ymin = min(p1.y, p2.y, p3.y) if min(p1.y, p2.y, p3.y) < 0 else 0
        ymax = max(p1.y, p2.y, p3.y) if max(p1.y, p2.y, p3.y) < self.height else self.height
        if xmax < (-self.width):
            xmax = -self.width
        if ymax < (-self.height):
            ymax = -self.height
        if xmin < (-self.width):
            xmin = -self.width
        if ymin < (-self.height):
            ymin = -self.height
        for xIndex in range(int(xmin), int(xmax)):
            for yIndex in range(int(ymin), int(ymax)):
                if xIndex > 0:
                    break
                if yIndex > 0:
                    break

                bar1, bar2, bar3 = calculateBaricentricCoord(xIndex, yIndex, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)
                if bar1 > 0 and bar2 > 0 and bar3 > 0:
                    sourceZ = bar1 * p1.z + bar2 * p2.z + bar3 * p3.z
                    if sourceZ < zBuffer[xIndex, yIndex]:
                        self.setPixel(xIndex, yIndex, color)
                        zBuffer[xIndex, yIndex] = sourceZ

    def drawTriangle_v3(self, p1, p2, p3, zBuffer,
                        l1, l2, l3):
        xmin = min(p1.x, p2.x, p3.x) if min(p1.x, p2.x, p3.x) < 0 else 0
        xmax = max(p1.x, p2.x, p3.x) if max(p1.x, p2.x, p3.x) < self.width else self.width
        ymin = min(p1.y, p2.y, p3.y) if min(p1.y, p2.y, p3.y) < 0 else 0
        ymax = max(p1.y, p2.y, p3.y) if max(p1.y, p2.y, p3.y) < self.height else self.height
        if xmax < (-self.width):
            xmax = -self.width
        if ymax < (-self.height):
            ymax = -self.height
        if xmin < (-self.width):
            xmin = -self.width
        if ymin < (-self.height):
            ymin = -self.height
        for xIndex in range(int(xmin), int(xmax)):
            for yIndex in range(int(ymin), int(ymax)):
                if xIndex > 0:
                    break
                if yIndex > 0:
                    break

                bar1, bar2, bar3 = calculateBaricentricCoord(xIndex, yIndex, p1.x, p1.y, p2.x, p2.y, p3.x, p3.y)
                colorSub = l1 * bar1 + l2 * bar2 + l3 * bar3
                if colorSub <= 0:
                    if bar1 >= 0 and bar2 >= 0 and bar3 >= 0:
                        sourceZ = bar1 * p1.z + bar2 * p2.z + bar3 * p3.z
                        if sourceZ < zBuffer[xIndex, yIndex]:
                            self.setPixel(xIndex, yIndex, (int(-colorSub * 255), 0, 0))
                            zBuffer[xIndex, yIndex] = sourceZ


class Obj3D:
    def __init__(self, path):
        self.vertexList = None
        self.vertexListVN = None
        self.polyVertexIndexesList = None
        self.polyNormalIndexesList = None
        self.img = ImageCreator()
        self.readModel(path)

    def readModel(self, path):
        self.vertexList, self.vertexListVN = Parser.getVertexes(path)
        self.polyNormalIndexesList, self.polyNormalIndexesList = Parser.getPolygons(path)

    def drawEdgesV1(self, displX=0, displY=0, scaleX=1, scaleY=1):
        for vertexIndexes in self.polyVertexIndexesList:
            self.img.drawLineV4(Point(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displX, 
                                      scaleY * self.vertexList[vertexIndexes[0] - 1].y - displY),
                                Point(scaleX * self.vertexList[vertexIndexes[1] - 1].x - displX,
                                      scaleY * self.vertexList[vertexIndexes[1] - 1].y - displY))
            self.img.drawLineV4(Point(scaleX * self.vertexList[vertexIndexes[1] - 1].x - displX,
                                      scaleY * self.vertexList[vertexIndexes[1] - 1].y - displY),
                                Point(scaleX * self.vertexList[vertexIndexes[2] - 1].x - displX,
                                      scaleY * self.vertexList[vertexIndexes[2] - 1].y, (255, 255, 255)))
            self.img.drawLineV4(Point(scaleX * self.vertexList[vertexIndexes[2] - 1].x - displX,
                                      scaleY * self.vertexList[vertexIndexes[2] - 1].y - displY),
                                Point(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displX,
                                      scaleY * self.vertexList[vertexIndexes[0] - 1].y - displY))

    def drawEdgesV2(self, displX=0, displY=0, scaleX=1, scaleY=1):
        i = 1
        for vertexIndexes in self.polyVertexIndexesList:
            self.img.drawTriangle(Point(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displX,
                                        scaleY * self.vertexList[vertexIndexes[0] - 1].y - displY),
                                  Point(scaleX * self.vertexList[vertexIndexes[1] - 1].x - displX,
                                        scaleY * self.vertexList[vertexIndexes[1] - 1].y - displY),
                                  Point(scaleX * self.vertexList[vertexIndexes[2] - 1].x - displX,
                                        scaleY * self.vertexList[vertexIndexes[2] - 1].y - displY),
                                  (i % 255, (i + 50) % 255, (i + 100) % 255))
            i = i + 20

    def drawEdgesV3(self, displX=0, displY=0, scaleX=1, scaleY=1):
        i = 1
        for vertexIndexes in self.polyVertexIndexesList:
            nx, ny, nz = calculateNormal(self.vertexList[vertexIndexes[0] - 1].x,
                                         self.vertexList[vertexIndexes[0] - 1].y,
                                         self.vertexList[vertexIndexes[0] - 1].z,
                                         self.vertexList[vertexIndexes[1] - 1].x,
                                         self.vertexList[vertexIndexes[1] - 1].y,
                                         self.vertexList[vertexIndexes[1] - 1].z,
                                         self.vertexList[vertexIndexes[2] - 1].x,
                                         self.vertexList[vertexIndexes[2] - 1].y,
                                         self.vertexList[vertexIndexes[2] - 1].z)
            cosine = scalarProduct(nx, ny, nz, 0, 0, 1)
            if cosine < 0:
                self.img.drawTriangle_v2(Point(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displX,
                                               scaleY * self.vertexList[vertexIndexes[0] - 1].y - displY,
                                               self.vertexList[vertexIndexes[0] - 1].z),
                                         Point(scaleX * self.vertexList[vertexIndexes[1] - 1].x - displX,
                                               scaleY * self.vertexList[vertexIndexes[1] - 1].y - displY,
                                               self.vertexList[vertexIndexes[1] - 1].z),
                                         Point(scaleX * self.vertexList[vertexIndexes[2] - 1].x - displX,
                                               scaleY * self.vertexList[vertexIndexes[2] - 1].y - displY,
                                               self.vertexList[vertexIndexes[2] - 1].z),
                                         self.img.zBuffer, (-255 * cosine, 0, 0))
