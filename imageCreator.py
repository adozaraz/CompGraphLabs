import numpy as np
from Parser import Parser
from PIL import Image


def calculateNormal(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    nx = (y1 - y0) * (z1 - z2) - (z1 - z0) * (y1 - y2)
    ny = (x1 - x0) * (z1 - z2) - (z1 - z0) * (x1 - x2)
    nz = (x1 - x0) * (y1 - y2) - (y1 - y0) * (x1 - x2)
    return nx, ny, nz


def scalarProduct(x0, y0, z0, x1, y1, z1):
    return (x0 * x1 + y0 * y1 + z0 * z1) / (np.sqrt(x0 * x0 + y0 * y0 + z0 * z0) * np.sqrt(x1 * x1 + y1 * y1 + z1 * z1))


def projectiveTransformation(x, y, z, ax, ay, u0, v0, tz):
    u = (ax * x + u0 * (z + tz)) / z
    v = (ay * y + v0 * (z + tz)) / z
    return u, v


class OBJ3DModel:
    def __init__(self):
        self.vertexList = None
        self.vertexIndexList = None
        self.polyVertexIndexesList = None
        self.polyNormalIndexesList = None
        self.img = MyImage()

    def read_model(self, path):
        self.vertexList, self.vertexIndexList = Parser.parseAllVertex(path)
        self.polyVertexIndexesList, self.polyNormalIndexesList = Parser.parseAllPolygon(path)

    def rotate(self, alpha, beta, gamma, withNormal=0):
        alpha *= np.pi / 180
        beta *= np.pi / 180
        gamma *= np.pi / 180
        rotation = np.mat([[1.0, 0, 0], [0, np.cos(alpha), np.sin(alpha)], [0, -np.sin(alpha), np.cos(alpha)]]) \
            * np.mat([[np.cos(beta), 0, np.sin(beta)], [0, 1.0, 0], [-np.sin(beta), 0, np.cos(beta)]]) \
            * np.mat([[np.cos(gamma), np.sin(gamma), 0], [-np.sin(gamma), np.cos(gamma), 0], [0, 0, 1.0]])

        coordinatesFinish = np.zeros((len(self.vertexList), 3), np.float64)
        for i in range(len(self.vertexList)):
            coordinatesFinish[i, 0] = self.vertexList[i].x
            coordinatesFinish[i, 1] = self.vertexList[i].y
            coordinatesFinish[i, 2] = self.vertexList[i].z
        coordinatesFinish = coordinatesFinish.dot(rotation).getA()
        for i in range(len(self.vertexList)):
            self.vertexList[i].x = coordinatesFinish[i, 0]
            self.vertexList[i].y = coordinatesFinish[i, 1]
            self.vertexList[i].z = coordinatesFinish[i, 2]
        if withNormal:
            coordinatesFinish2 = np.zeros((len(self.vertexList), 3), np.float64)
            for i in range(len(self.vertexIndexList)):
                coordinatesFinish2[i, 0] = self.vertexIndexList[i].x
                coordinatesFinish2[i, 1] = self.vertexIndexList[i].y
                coordinatesFinish2[i, 2] = self.vertexIndexList[i].z
            coordinatesFinish2 = coordinatesFinish2.dot(rotation).getA()
            for i in range(len(self.vertexIndexList)):
                self.vertexIndexList[i].x = coordinatesFinish2[i, 0]
                self.vertexIndexList[i].y = coordinatesFinish2[i, 1]
                self.vertexIndexList[i].z = coordinatesFinish2[i, 2]

    def perspective(self, ax, ay, u0, v0, zsup):
        for i in range(len(self.vertexList)):
            self.vertexList[i].x = (self.vertexList[i].x * ax) / (self.vertexList[i].z + zsup) + u0
            self.vertexList[i].y = (self.vertexList[i].y * ay) / (self.vertexList[i].z + zsup) + v0

    def centralize(self):
        x_max = y_max = z_max = -20_000_000.0
        x_min = y_min = z_min = 20_000_000.0

        for i in range(len(self.vertexList)):
            x_max = max(self.vertexList[i].x, x_max)
            y_max = max(self.vertexList[i].y, y_max)
            z_max = max(self.vertexList[i].z, z_max)
            x_min = min(self.vertexList[i].x, x_min)
            y_min = min(self.vertexList[i].y, y_min)
            z_min = min(self.vertexList[i].z, z_min)

        x_min = x_max - (x_max - x_min) / 2
        y_min = y_max - (y_max - y_min) / 2
        z_min = z_max - (z_max - z_min) / 2

        for i in range(len(self.vertexList)):
            self.vertexList[i].x -= x_min
            self.vertexList[i].y -= y_min
            self.vertexList[i].z -= z_min

    def normalize(self):
        x = y = z = -20000000.0
        for i in range(len(self.vertexList)):
            x = max(abs(self.vertexList[i].x), x)
            y = max(abs(self.vertexList[i].y), y)
            z = max(abs(self.vertexList[i].z), z)
        for i in range(len(self.vertexList)):
            self.vertexList[i].x /= x
            self.vertexList[i].y /= y
            self.vertexList[i].z /= z

    def draw_edges_v1(self, path, displacementX=0, displacementY=0, scaleX=1, scaleY=1):
        self.read_model(path)
        for vertexIndexes in self.polyVertexIndexesList:
            self.img.draw_line_v4(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[0] - 1].y - displacementY,
                                  scaleX * self.vertexList[vertexIndexes[1] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[1] - 1].y - displacementY,
                                  (255, 255, 255))
            self.img.draw_line_v4(scaleX * self.vertexList[vertexIndexes[1] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[1] - 1].y - displacementY,
                                  scaleX * self.vertexList[vertexIndexes[2] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[2] - 1].y, (255, 255, 255))
            self.img.draw_line_v4(scaleX * self.vertexList[vertexIndexes[2] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[2] - 1].y - displacementY,
                                  scaleX * self.vertexList[vertexIndexes[0] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[0] - 1].y - displacementY,
                                  (255, 255, 255))

    def draw_edges_v2(self, path, displacementX=0, displacementY=0, scaleX=1, scaleY=1):
        self.read_model(path)
        i = 1
        for vertexIndexes in self.polyVertexIndexesList:
            self.img.drawTriangle(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[0] - 1].y - displacementY,
                                  scaleX * self.vertexList[vertexIndexes[1] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[1] - 1].y - displacementY,
                                  scaleX * self.vertexList[vertexIndexes[2] - 1].x - displacementX,
                                  scaleY * self.vertexList[vertexIndexes[2] - 1].y - displacementY,
                                  (i % 255, (i + 50) % 255, (i + 100) % 255))
            i = i + 20

    def draw_edges_v3(self, path, displacementX=0, displacementY=0, scaleX=1, scaleY=1):
        self.read_model(path)
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
                self.img.drawTriangle_v2(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[0] - 1].y - displacementY,
                                         self.vertexList[vertexIndexes[0] - 1].z,
                                         scaleX * self.vertexList[vertexIndexes[1] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[1] - 1].y - displacementY,
                                         self.vertexList[vertexIndexes[1] - 1].z,
                                         scaleX * self.vertexList[vertexIndexes[2] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[2] - 1].y - displacementY,
                                         self.vertexList[vertexIndexes[2] - 1].z,
                                         self.img.zBuffer, (-255 * cosine, 0, 0))

    def draw_projective_edges(self, path, displacementX=0, displacementY=0, scaleX=1, scaleY=1):
        self.read_model(path)
        self.centralize()
        self.normalize()
        self.rotate(0, 45, 0)
        self.perspective(-2000, 2000, 0, 0, 10)
        self.normalize()
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
            if cosine >= 0:
                self.img.drawTriangle_v2(scaleX * self.vertexList[vertexIndexes[0] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[0] - 1].y - displacementY,
                                         scaleX * self.vertexList[vertexIndexes[0] - 1].z,
                                         scaleX * self.vertexList[vertexIndexes[1] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[1] - 1].y - displacementY,
                                         scaleX * self.vertexList[vertexIndexes[1] - 1].z,
                                         scaleX * self.vertexList[vertexIndexes[2] - 1].x - displacementX,
                                         scaleY * self.vertexList[vertexIndexes[2] - 1].y - displacementY,
                                         scaleX * self.vertexList[vertexIndexes[2] - 1].z,
                                         self.img.zBuffer, (255 * cosine, 0, 0))

    def draw_guro_edges(self, path):
        self.read_model(path)
        self.centralize()
        self.normalize()
        self.rotate(0, 45, 0, withNormal=1)
        self.perspective(-2000, -2000, -800, -800, 10)
        for i in range(len(self.polyVertexIndexesList)):
            vertexIndexes = self.polyVertexIndexesList[i]
            normalIndexes = self.polyNormalIndexesList[i]
            nx1 = self.vertexIndexList[normalIndexes[0] - 1].x
            ny1 = self.vertexIndexList[normalIndexes[0] - 1].y
            nz1 = self.vertexIndexList[normalIndexes[0] - 1].z
            nx2 = self.vertexIndexList[normalIndexes[1] - 1].x
            ny2 = self.vertexIndexList[normalIndexes[1] - 1].y
            nz2 = self.vertexIndexList[normalIndexes[1] - 1].z
            nx3 = self.vertexIndexList[normalIndexes[2] - 1].x
            ny3 = self.vertexIndexList[normalIndexes[2] - 1].y
            nz3 = self.vertexIndexList[normalIndexes[2] - 1].z
            cosine1 = scalarProduct(nx1, ny1, nz1, 0, 0, 1)
            cosine2 = scalarProduct(nx2, ny2, nz2, 0, 0, 1)
            cosine3 = scalarProduct(nx3, ny3, nz3, 0, 0, 1)

            self.img.drawTriangle_v3(self.vertexList[vertexIndexes[0] - 1].x,
                                     self.vertexList[vertexIndexes[0] - 1].y,
                                     self.vertexList[vertexIndexes[0] - 1].z,
                                     self.vertexList[vertexIndexes[1] - 1].x,
                                     self.vertexList[vertexIndexes[1] - 1].y,
                                     self.vertexList[vertexIndexes[1] - 1].z,
                                     self.vertexList[vertexIndexes[2] - 1].x,
                                     self.vertexList[vertexIndexes[2] - 1].y,
                                     self.vertexList[vertexIndexes[2] - 1].z,
                                     self.img.zBuffer, cosine1, cosine2, cosine3)


class MyImage:
    def __init__(self):
        self.img_arr = None
        self.width = 0
        self.height = 0
        self.channels = 3
        self.delta_t = 0.01
        self.zBuffer = None

    # инициализация z буфера
    def initZBuffer(self, bufferSize=30000):
        self.zBuffer = np.zeros((self.height, self.width), dtype=float)
        self.zBuffer[:, :] = bufferSize

    def initImgArray(self):
        self.img_arr = np.zeros((self.height, self.width, self.channels), dtype=np.uint8)

    def set_pixel(self, x, y, color):
        self.img_arr[y, x, :] = color

    def imshow(self):
        Image.fromarray(self.img_arr, 'RGB').show()

    def saveImage(self, path):
        im = Image.fromarray(self.img_arr, 'RGB')
        im.save(path)

    # рисование линии, первый вариант алгоритма
    def draw_line_v1(self, x0, y0, x1, y1, color):
        for t in np.arange(0, 1, self.delta_t):
            x = int(x0 * (1.0 - t) + x1 * t)
            y = int(y0 * (1.0 - t) + y1 * t)
            self.set_pixel(x, y, color)

    # рисование линии, второй вариант алгоритма
    def draw_line_v2(self, x0, y0, x1, y1, color):
        for x in range(int(x0), int(x1), 1):
            t = (x - x0) / float(x1 - x0)
            y = int(y0 * (1.0 - t) + y1 * t)
            self.set_pixel(int(x), int(y), color)

    @staticmethod
    def checkInitialCoords(x0, y0, x1, y1):
        steep = False
        if np.abs(x0 - x1) < np.abs(y0 - y1):
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            steep = True
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        return x0, y0, x1, y1, steep

    # рисование линии, третий вариант алгоритма
    def draw_line_v3(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1, steep = self.checkInitialCoords(x0, y0, x1, y1)
        for x in range(int(x0), int(x1), 1):
            t = (x - x0) / float(x1 - x0)
            y = int(y0 * (1.0 - t) + y1 * t)
            if steep:
                self.set_pixel(int(y), int(x), color)
            else:
                self.set_pixel(int(x), int(y), color)

    # рисование линии, четвертый вариант алгоритма (алгоритм Брезенхема)
    def draw_line_v4(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1, steep = self.checkInitialCoords(x0, y0, x1, y1)
        dx = x1 - x0
        dy = y1 - y0
        derror = np.abs(dy / float(dx))
        error = 0
        y = y0
        for x in range(int(x0), int(x1), 1):
            if steep:
                self.set_pixel(int(y), int(x), color)
            else:
                self.set_pixel(int(x), int(y), color)
            error += derror
            if error > 0.5:
                y += 1 if y1 > y0 else -1
                error -= 1

    # в качестве параметра можно передать саму функцию отрисовки линии
    @staticmethod
    def draw_star(draw_line_variant):
        for i in range(13):
            alpha = 2 * np.pi * i / 13
            draw_line_variant(100, 100, 100 + 95 * np.cos(alpha), 100 + 95 * np.sin(alpha), (255, 255, 255))

    @staticmethod
    def getMinMaxCoords(x0, y0, x1, y1, x2, y2, width, height, checkMax=1):
        xmin = min(x0, x1, x2) if min(x0, x1, x2) < 0 else 0
        ymin = min(y0, y1, y2) if min(y0, y1, y2) < 0 else 0
        xmax = max(x0, x1, x2) if max(x0, x1, x2) < width else width
        ymax = max(y0, y1, y2) if max(y0, y1, y2) < height else height
        if checkMax:
            xmax = max(xmax, -width)
            ymax = max(ymax, -height)
            xmin = max(xmin, -width)
            ymin = max(ymin, -height)
        return xmin, ymin, xmax, ymax

    def drawTriangle(self, x0, y0, x1, y1, x2, y2, color):
        xmin, ymin, xmax, ymax = self.getMinMaxCoords(x0, y0, x1, y1, x2, y2, self.width, self.height, checkMax=0)
        for xIndex in range(round(xmin), round(xmax)):
            for yIndex in range(round(ymin), round(ymax)):
                bar1, bar2, bar3 = convertToBarycentric(xIndex, yIndex, x0, y0, x1, y1, x2, y2)
                if bar1 > 0 and bar2 > 0 and bar3 > 0:
                    self.set_pixel(xIndex, yIndex, color)
        pass

    def drawTriangle_v2(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, zBuffer,
                        color):
        xmin, ymin, xmax, ymax = self.getMinMaxCoords(x0, y0, x1, y1, x2, y2, self.width, self.height)
        for xIndex in range(int(xmin), int(xmax)):
            for yIndex in range(int(ymin), int(ymax)):
                if xIndex > 0:
                    break
                if yIndex > 0:
                    break

                bar1, bar2, bar3 = convertToBarycentric(xIndex, yIndex, x0, y0, x1, y1, x2, y2)
                if bar1 > 0 and bar2 > 0 and bar3 > 0:
                    sourceZ = bar1 * z0 + bar2 * z1 + bar3 * z2
                    if sourceZ < zBuffer[xIndex, yIndex]:
                        self.set_pixel(xIndex, yIndex, color)
                        zBuffer[xIndex, yIndex] = sourceZ
        pass

    def drawTriangle_v3(self, x0, y0, z0, x1, y1, z1, x2, y2, z2, zBuffer,
                        l1, l2, l3):
        xmin, ymin, xmax, ymax = self.getMinMaxCoords(x0, y0, x1, y1, x2, y2, self.width, self.height)
        for xIndex in range(int(xmin), int(xmax)):
            for yIndex in range(int(ymin), int(ymax)):
                if xIndex > 0:
                    break
                if yIndex > 0:
                    break

                bar1, bar2, bar3 = convertToBarycentric(xIndex, yIndex, x0, y0, x1, y1, x2, y2)
                colorSub = l1 * bar1 + l2 * bar2 + l3 * bar3
                if colorSub <= 0:
                    if bar1 >= 0 and bar2 >= 0 and bar3 >= 0:
                        sourceZ = bar1 * z0 + bar2 * z1 + bar3 * z2
                        if sourceZ < zBuffer[xIndex, yIndex]:
                            self.set_pixel(xIndex, yIndex, (int(-colorSub * 255), 0, 0))
                            zBuffer[xIndex, yIndex] = sourceZ
        pass


def convertToBarycentric(x, y, x0, y0, x1, y1, x2, y2):
    lambda0 = ((x1 - x2) * (y - y2) - (y1 - y2) * (x - x2)) / ((x1 - x2) * (y0 - y2) - (y1 - y2) * (x0 - x2))
    lambda1 = ((x2 - x0) * (y - y0) - (y2 - y0) * (x - x0)) / ((x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0))
    lambda2 = ((x0 - x1) * (y - y1) - (y0 - y1) * (x - x1)) / ((x0 - x1) * (y2 - y1) - (y0 - y1) * (x2 - x1))
    return lambda0, lambda1, lambda2
