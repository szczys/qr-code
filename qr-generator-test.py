ver2_qr = [
    [1,1,1,1,1,1,1,0,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,1,0,1,0,1,0,0,1,1,1,0,1,1,1,0,0,1,1,1],
    [0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,1,0],
    [0,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,0,1,1,1,1,1],
    [0,0,0,1,1,0,0,0,1,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,1],
    [0,0,0,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1,0,1,1,0,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,0,0,0],
    [1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,0,0,0,1,0,0,0,1,1,1],
    [1,0,1,1,0,1,0,0,0,0,0,1,1,0,1,0,1,1,1,0,0,0,0,0,0],
    [1,0,0,0,1,1,1,0,1,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,1,1,1],
    [1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,1,0,1,0,0,1,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,1],
    [1,0,1,1,1,0,1,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0],
    [1,0,1,1,1,0,1,0,1,1,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,0,1,0,0,1,0,1,1,0,0,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,0,1,0,0,1,1,1,1,1,1]
    ]

def genQrImage(qrData):
    import Image, ImageDraw

    out = '/home/mike/Desktop/qr_gen_test.png'
    size = 2
    bgcolor = 0xFFFFFF
    fgcolor = 0x000000
    quiet_zone_modules = 4 #required quiet zone pixels around code

    offset = quiet_zone_modules*size

    image = Image.new("RGB", (size*(len(qrData)+(quiet_zone_modules*2)),size*(len(qrData)+(quiet_zone_modules*2))), bgcolor)
    draw = ImageDraw.Draw(image)

    for y in range(len(qrData)):
        for x in range(len(qrData)):
            if qrData[y][x]:
                #draw foreground pixel
                x1 = (x*size)+offset
                y1 = (y*size)+offset
                x2 = (x*size)+offset+size-1
                y2 = (y*size)+offset+size-1
                #print x1,y1,x2,y2
                draw.rectangle((x1,y1,x2,y2),fgcolor)
            '''
            else:
                #draw background pixel
                #draw.rectangle((x*size,y*size,(x*size)+size,(y*size)+size),bgcolor)
                draw.rectangle(((x+quiet_zone_modules)*size,(y+quiet_zone_modules)*size,((x+quiet_zone_modules)*size)+size,((y+quiet_zone_modules)*size)+size),bgcolor)
            '''

    del draw
    image.save(out, 'PNG')
            
        

    