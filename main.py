from imageCreator import *
from gifConventor import workWithGif


def lab1():
    W = 128
    H = 128
    arr = np.zeros((H, W), dtype=np.uint8)
    image = Image.fromarray(arr, 'L')
    image.show()
    arr2 = np.copy(arr)
    arr2 += 255
    image2 = Image.fromarray(arr2, 'L')
    image2.show()
    arr3 = np.zeros((H, W, 3), dtype=np.uint8)
    arr3[:, :, :] = (255, 0, 0)
    image3 = Image.fromarray(arr3, 'RGB')
    image3.show()
    arr4 = np.zeros((H, W, 3), dtype=np.uint8)
    for i in range(H):
        for j in range(W):
            for k in range(3):
                arr4[i, j, k] = (i + j + k) % 256
    image4 = Image.fromarray(arr4, 'RGB')
    image4.show()
    img = MyImage()
    img.width = 1000
    img.height = 1000
    img.initImgArray()
    img.draw_star(img.draw_line_v1)
    img.saveImage("result/1.jpg")
    img.draw_star(img.draw_line_v2)
    img.saveImage("result/2.jpg")
    img.draw_star(img.draw_line_v3)
    img.saveImage("result/3.jpg")
    img.draw_star(img.draw_line_v4)
    img.saveImage("result/4.jpg")
    img.draw_line_v4(125, 0, 125, 225, (255, 255, 255))
    obj = OBJ3DModel()
    obj.img.width = 1600
    obj.img.height = 1600
    obj.img.initImgArray()
    obj.draw_edges_v1("objects/deer.obj", 650, 0, 1, -1)
    obj.img.saveImage("objects/deer.jpg")
    obj.img.imshow()


def lab2():
    obj = OBJ3DModel()
    obj.img.width = 1600
    obj.img.height = 1600
    obj.img.initImgArray()
    print('First')
    obj.draw_edges_v1("objects/deer.obj", 650, 0, 1, -1)
    obj.img.saveImage('result/deerV1.png')
    print('Second')
    obj.draw_edges_v2("objects/deer.obj", 650, 0, 1, -1)
    obj.img.saveImage('result/deerV2.png')
    print('Third')
    obj.img.initZBuffer()
    obj.draw_edges_v3("objects/deer.obj", 650, 0, 1, -1)
    obj.img.saveImage('result/deerV3.png')


def lab3():
    # drawTriangle(300, 500, 20, 30, 150, 700)
    obj = OBJ3DModel()
    obj.img.width = 1600
    obj.img.height = 1600
    obj.img.initImgArray()
    obj.img.initZBuffer()
    obj.draw_projective_edges("objects/rabbit.obj", 800, 800, 400, -400)
    obj.img.saveImage("result/rabbit_lighted_colored_foved.jpg")
    obj.img.imshow()


def lab4():
    obj = OBJ3DModel()
    obj.img.width = 1600
    obj.img.height = 1600
    obj.img.initImgArray()
    obj.img.initZBuffer()
    obj.draw_guro_edges("objects/rabbit.obj")
    obj.img.saveImage("result/rabbit_guro.jpg")
    obj.img.imshow()


def misc():
    gifFilePath = "gif/JoJo's Bizarre Adventure All Openings 1-13 1080p_1.gif"
    workWithGif(gifFilePath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Lab 1')
    lab1()
    print('Lab 2')
    lab2()
    print('Lab 3')
    lab3()
    print('Lab 4')
    lab4()
    # misc()
