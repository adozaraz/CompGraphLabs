import numpy as np

from lab1 import *
from Point import Point
from math import pi, cos, sin

def task1(H, W):
    print('# Task 1')
    print('Creating Image Matrices')
    imgs = createImageMatrix(H, W)
    print('Generating Image Files')
    i = 0
    for img in imgs:
        saveImage(img, i)
        i += 1
    print('Finished')

def task2(H, W):
    print('\n\n# Task 2')
    imgs = [np.zeros((H, W, 3), dtype=np.uint8) for i in range(4)]
    print('Drawing Lines')
    for j in range(len(imgs)):
        print(f'Algorithm {j}')
        for i in range(13):
            startingPoint = Point(100, 100)
            alpha = 2 * pi * i / 13
            point = Point(int(100 + 95 * cos(alpha)), int(100 + 95 * sin(alpha)))
            print(f'Point {i}')
            print(f'({startingPoint.x}, {startingPoint.y}), ({point.x}, {point.y})')
            imgs[j] = drawLine(startingPoint, point, imgs[j], [255, 255, 255], j)

    print('Saving images')
    i = 0
    for img in imgs:
        saveImage(img, f'star{i}')
        i += 1


def task3():
    print('\n\n# Task 3')
    nodes = getNodesFromFile('objects/fox.obj')
    for i in nodes:
        print(i)


def task4(H, W, filePath='objects/rabbit.obj', color=None, fileName='rabbit', transformNumber=4000):
    if color is None:
        color = [255, 255, 255]
    nodes = getNodesFromFile(filePath)
    image = drawNodes(nodes, H, W, color, transformNumber)
    saveImage(image, f'{fileName}', rotate=True)





def task6(H, W, filePath='objects/rabbit.obj', fileName='RabbitPolygon', transformNumber=4000):
    nodes = getNodesFromFile(filePath, toPoint=True)
    polygons = getPolygons(filePath)
    image = drawPolygons(H, W, nodes, polygons, transformNumber)
    saveImage(image, fileName, rotate=True)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    H = 200
    W = 200
    filePath = 'objects/rabbit.obj'
    fox = 'objects/fox.obj'
    deer = 'objects/deer.obj'
    task1(H, W)
    task2(H, W)
    H = 1000
    W = 1000
    task3()
    task4(H, W, filePath=fox, fileName='Fox', transformNumber=5)
    # Олень - .34, Кролик - 4000, Лис - 5
    task6(H, W, deer, 'Deer', 0.34)
