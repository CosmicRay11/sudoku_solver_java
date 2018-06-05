'''
Created on 15 Apr 2018

@author: George
'''

from grid_generation import FindLines, LocateSquares
from PIL import Image, ImageFilter
#import numpy as np

def rotate_with_colour(image, angle, colour):
    convertedImage = image.convert("RGBA")
    rotatedImage = convertedImage.rotate(angle, expand = True)
    
    fff = Image.new('RGBA', rotatedImage.size, colour)

    out = Image.composite(rotatedImage, fff, rotatedImage)

    rotatedImage = out.convert(rotatedImage.mode)
    return rotatedImage

def resize_image(image, width):
    size = image.size
    widthRatio = size[0]/width
    height = round(size[1] / widthRatio)
    image = image.resize((width,height), Image.ANTIALIAS)
    return image
    

if __name__ == "__main__":
    print()
    url = "C:\\Users\\George\\Documents\\Computing\\Python files\\sudoku solver stuff\\target3a.jpg"
    im = Image.open( url )
    im = resize_image(im, 500)
    original = im.copy()
    im.show()
    finder = FindLines(im.copy(), 100)
    finder.get_lines()
    angle = finder.find_angle()
    
    rotatedImage = rotate_with_colour(im.copy(), angle, (255,255,255,255))
    rotatedImage.show()

    locator = LocateSquares(rotatedImage)
    minorAngle, coords = locator.get_corners()
    print(minorAngle, coords)
    doubleRotatedImage = rotatedImage.rotate(minorAngle, center = (0,0))
    sudokuGrid = rotatedImage.crop(coords)
    sudokuGrid.show()
    

    