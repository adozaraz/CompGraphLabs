import numpy as np

from lab1 import *
from Point import Point
from math import pi, cos, sin

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    H = 200
    W = 200
    print('# Task 1')
    print('Creating Image Matrices')
    imgs = createImageMatrix(H, W)
    print('Generating Image Files')
    i = 0
    for img in imgs:
        saveImage(img, i)
        i += 1
    print('Finished')
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
    for img in imgs:
        saveImage(img, i)
        i += 1




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
