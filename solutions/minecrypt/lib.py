from PIL import Image

def prepare_image(image):
    im = Image.open(image)
    im = im.convert(mode='RGB')
    width, height = im.size

    for x in range(width):
        for y in range(height):
            pixel = im.getpixel((x,y))            
            if 255 not in pixel:
                colorize(pixel, im, (x,y), (0,0,0))

    for x in range(width//4):
        for y in range(height//4):
            for i in range(4):
                for j in range(4):
                        coords = x+i*width//4,y+j*height//4
                        pixel = im.getpixel(coords)
                        if 255 in pixel:
                            colorize(pixel, im, coords, (200,10,4) if i%2 == j%2 else (12,110,3))

    for x in range(width//2):
        for y in range(height//2):
            abc = (im.getpixel((2*x,2*y)), im.getpixel((2*x+1,2*y)), im.getpixel((2*x,2*y+1)), im.getpixel((2*x+1,2*y+1)))
            if abc[0] != abc[1]:
                im.putpixel((2*x,2*y), im.getpixel((2*x+1,2*y)))
            if abc[2] != abc[3]:
                im.putpixel((2*x,2*y+1), im.getpixel((2*x+1,2*y+1)))
    im.save(image)

def colorize(pixel, im, coords, color):
    im.putpixel(coords, color)


def read_as_rgb_2x2_blocks(image):
    pixels = []
    
    im = Image.open(image)
    im = im.convert(mode='RGB')
    width, height = im.size

    for x in range(width//2):
        for y in range(height//2):
            pixels.append((
                im.getpixel((2*x  ,2*y  )), 
                im.getpixel((2*x+1,2*y  )), 
                im.getpixel((2*x  ,2*y+1)), 
                im.getpixel((2*x+1,2*y+1))
                ))
    return pixels

def cipher_block(block):
    a, b, c, d = block
    a = a[0] + 20*a[1] + 100*a[2]
    b = 201*b[0] + 11*b[1] + 2*b[2]
    c = 1000*c[2] + c[0]
    d = d[0] + 172*d[1] - d[2]
    res = hex(sum((a,b,c,d)))[2:]
    res = '{}{}'.format('0'*(5-len(res)),res)
    res = tuple(map(''.join,zip(res,res[::-1])))
    res = ''.join(res[0:3]) + res[4] + res[3]
    hexdigits = '0123456789abcdef'
    if res[1] in hexdigits[:-1]:
        res = res[0] + (hexdigits[hexdigits.index(res[1]) + 1]) + res[2:]
    if res[5] in hexdigits[1:]:
        res = res[:5] + (hexdigits[hexdigits.index(res[5]) - 1]) + res[6:]
    return res[::-1]

def reverse_second_part(block):
    return block[:len(block)//2] + block[len(block)//2:]