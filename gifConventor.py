import time

from PIL import Image, ImageFont
import vlc
import os, sys

folderWorkPath = 'gif/'
gifToPlay = '.gif'
musicToPlay = '.mp3'


def extractFrames(gif):
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
    font = ImageFont.load_default()  # load default bitmap monospaced font
    (chrx, chry) = font.getsize(chr(32))
    # calculate weights of ASCII chars
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
    # NEAREST/BILINEAR/BICUBIC/ANTIALIAS
    #image = image.resize((imgx, imgy), Image.BICUBIC)
    image = image.convert("L")  # convert to grayscale
    pixels = image.load()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255
            # find closest weight match
            wf = -1.0;
            k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i];
                    k = i
            output += chr(k + 32)
        output += "\n"
    return output


def playVideoInConsole(frames, musicFilePath):
    clear_console = 'clear' if os.name == 'posix' else 'cls'
    p = vlc.MediaPlayer(musicFilePath)
    p.play()
    for frame in frames:
        newFrame = convertImageToAscii(frame)
        os.system(clear_console)
        sys.stdout.write(newFrame)
        sys.stdout.flush()
        #time.sleep(0.1)


def workWithGif(filePath, musicFilePath):
    gif = Image.open(filePath)
    frames = extractFrames(gif)
    playVideoInConsole(frames, musicFilePath)

