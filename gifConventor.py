from PIL import Image, ImageFont
import os, sys



def main():
    gifFilePath = "gif/JoJo's Bizarre Adventure All Openings 1-13 1080p_1.gif"
    workWithGif(gifFilePath)


def extractFrames(gif):
    # Вытаскиваем кадры из gif файла
    frames = []
    try:
        while True:
            gif.seek(gif.tell()+1)
            frame = Image.new('RGBA', gif.size)
            frame.paste(gif, (0, 0), gif.convert('RGBA'))

            frames.append(frame)
    except EOFError:
        pass
    return frames


def convertImageToAscii(image):
    # Преобразовываем изображение в ASCII изображение
    font = ImageFont.load_default()  # Загружаем стандартный монохромный битмап фонт
    (chrx, chry) = font.getsize(chr(32))
    # Рассчитываем весы для ASCII символов
    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chry):
            for x in range(chrx):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chrx * chry))

    output = ""
    (imgx, imgy) = image.size
    image = image.convert("L")  # Преобразовываем в grayscale изображение
    pixels = image.load()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255
            # Находим ближайший по весу символ
            wf = -1.0
            k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i];
                    k = i
            output += chr(k + 32)
        output += "\n"
    return output


def playVideoInConsole(frames):
    clear_console = 'clear' if os.name == 'posix' else 'cls'
    for frame in frames:
        newFrame = convertImageToAscii(frame)
        os.system(clear_console)
        sys.stdout.write(newFrame)
        sys.stdout.flush()


def workWithGif(filePath):
    gif = Image.open(filePath)
    frames = extractFrames(gif)
    playVideoInConsole(frames)


if __name__ in '__main__':
    main()

