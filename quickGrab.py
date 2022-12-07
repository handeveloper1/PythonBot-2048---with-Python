import ImageGrab
import os
import time


#ekranın solu için ayarlı çözünürlük 1080
x_pad = 222
y_pad = 351

def screenGrab():
    box = (x_pad, y_pad, 722, 851)
    im = ImageGrab.grab(box)
    return im

def main():
    screenGrab()

if __name__ == '__main__':
    main()
