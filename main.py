from Parser import *
from gifConventor import workWithGif

def lab1():
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # lab1()
    gifFilePath = "gif/JoJo's Bizarre Adventure All Openings 1-13 1080p_1.gif"
    workWithGif(gifFilePath)
