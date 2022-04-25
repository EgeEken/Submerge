from PIL import Image
import PIL
import time
import math
import numpy as np

def save(img, name):
    img.save(name + ".png", "PNG")

def open(imgname):
    return Image.open(imgname)

def load(image):
    return image.load()

cscale = [(0, 0, 255),(0, 48, 255),(0, 96, 255),(0, 144, 255),(0, 192, 255),(0, 240, 255),(0, 255, 191),(0, 255, 95),(0, 255, 0),(48, 255, 0),(96, 255, 0),(144, 255, 0),(192, 255, 0),(239, 255, 0),(255, 224, 0),(255, 176, 0),(255, 128, 0),(255, 80, 0),(255, 32, 0),(255, 15, 15),(255, 63, 63),(255, 111, 111),(255, 159, 159),(255, 207, 207),(255, 255, 255)]

def distance(c1,c2):
    r1,g1,b1 = c1
    r2,g2,b2 = c2
    return math.sqrt(((r2-r1)**2+(g2-g1)**2+(b2-b1)**2))

def scale2height(x):                  #for any (above sea level) given map: plug (0 - 25) and (bottomHeight - topHeight) in 
    a=0.000023                            #https://stats.blue/Stats_Suite/polynomial_regression_calculator.html  with 4th degree 
    b=-0.002135                           #and a sufficient number of digits, then copy the coefficients here and run the script
    c=0.112806
    d=1.081289
    e=-1.176363
    return (a*x**4+b*x**3+c*x**2+d*x+e)
    
def scale2color(x):
    if x>=0 and x<=8:        #red
        red=0
    elif x>8 and x<=13.33:
        red=48*(x-8)
    elif x>13.33 and x<=24:
        red=255
    if x>=0 and x<=5.33:         #green
        green=48*x
    elif x>5.33 and x<=13.33:
        green=255
    elif x>13.33 and x<=18.66:
        green=224-48*(x-14)
    elif x>18.66 and x<=24:
        green=15+48*(x-19)
    if x>=0 and x<=5.33:         #blue
        blue=255
    elif x>5.33 and x<=8:
        blue=192-96*(x-6)
    elif x>8 and x<=18.33:
        blue=0
    elif x>18.33 and x<=24:
        blue=15+48*(x-19)
    return (red,green,blue)
        
def color2scale(c):
    r,g,b = c
    if r==0 and b==255:
        return g/48
    if r==0 and g==255:
        return (192-b)/96+6
    if g==255 and b==0:
        return r/48+8
    if r==255 and b==0:
        return (224-g)/48+14
    if g==b and r==255:
        return (g-15)/48+19

def mins(c):            #2 smallest values of the distances
    ds= {distance(c,cscalei):cscalei for cscalei in cscale}
    a=cscale.index(ds[min(ds)])
    del ds[min(ds)]
    return (a,cscale.index(ds[min(ds)]))           #gives back the indexes in the cscale of the two closest colours

def closestX(c, precision):                    #gives back the closest value in the continuous scale
    ind1, ind2 = mins(c)
    if ind2<=ind1:
        ind2, ind1 = ind1, ind2
    if ind2-ind1 > 2:
        if ind1 == 0:
            ind2 = ind1 + 1
        else:
            ind1 -= 1
            ind2 = ind1 + 2
    closestdistance = 1000
    for i in range(precision + 1):
        calc = ind1 + i*(ind2-ind1)/precision
        d = distance(c,scale2color(calc))
        if d < closestdistance:
            closestdistance = d
            closestcolor = calc
    return closestcolor

def color2height(c,precision):
    return scale2height(closestX(c,precision))

def topographyfind(img, rise, precision):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    res = set()
    for x in range(width):
        for y in range(height):
            if img_colorpixels[x,y] == (0,0,255):
                res.add((x,y))
            elif color2height(img_colorpixels[x,y], precision) <= rise:
                res.add((x,y))
    return res

def topographysubmerge(img, rise,precision):
    img_name = img.filename[:len(img.filename)-4]
    img_color = img.convert('RGB')
    img_pixels = load(img_color)
    for pixel in topographyfind(img, rise, precision):
        x,y = pixel
        img_pixels[x,y] = (0,0,255)
    save(img_color, (img_name + '_' + str(rise)))

def matrix_create(img, precision):
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    width = img.size[0]
    height = img.size[1]
    res = np.zeros((height,width))
    for x in range(width):
        for y in range(height):
            res[y,x] = color2height(img_colorpixels[x,y], precision)
    return res

def matrixtopofind(matrix_img, rise):
    res = set()
    width = len(matrix_img[0])
    height = len(matrix_img)
    for x in range(width):
        for y in range(height):
            if matrix_img[y,x] <= rise:
                res.add((x,y))
    return res

def matrixtoposubmerge(img, matrix_img, rise, count):
    submerge = matrixtopofind(matrix_img, rise)
    img_name = img.filename
    img_colors = img.convert('RGB')
    img_colorpixels = load(img_colors)
    for pixel in submerge:
        x,y = pixel
        img_colorpixels[x,y] = (50,71,128)
    save(img_colors, (img_name + '_' + str(count)))

def LQHQmatrixsubmergemain():
    LQimg = open(input('LQ File name: '))
    HQimg = open(input('HQ File name: '))
    precision = int(input('Precision: '))
    print('Creating matrix...')
    startmatrix = time.time()
    matrix_img = matrix_create(LQimg, precision)
    endmatrix = time.time()
    print('Created matrix in ' + str(round(endmatrix-startmatrix,4)) + ' seconds.')
    cont = True
    while cont:
        riseinc = float(input('Increments of __ meters: '))
        riseupto = float(input('Rise up to __ meters: '))
        print('Processing images...')
        count = 0
        startall = time.time()
        for i in range(int(riseupto/riseinc) + 1):
            start = time.time()
            matrixtoposubmerge(HQimg, matrix_img, round(i*riseinc,5), count)
            end = time.time()
            count += 1
            print('Saved image submerged ' + str(round(i*riseinc,5)) + ' meters in ' + str(round(end - start, 4)) + 'seconds.')
        endall = time.time()
        if endall-startall > 60:
            print('Saved ' + str(int(riseupto/riseinc) + 1) + ' images in ' + str(round((endall-startall)/60, 4)) + ' minutes and ' + str(round((endall-startall)%60,4)) + ' seconds.')
        else:
            print('Saved ' + str(int(riseupto/riseinc) + 1) + ' images in ' + str(round(endall-startall,4)) + ' seconds.')
        contcheck = input('Continue?  :  ')
        if contcheck in "stopnodoneexitdont":
            cont = False

LQHQmatrixsubmergemain()
    
a = input()
