import Image, ImageDraw

def getFormatting(errorLevel, maskType):
    errorLevelKey = {'L':'01', 'M':'00', 'Q':'11', 'H':'10'}
    errAndMaskString = errorLevelKey[errorLevel] + intToBinString(maskType, 3)
    bchCalc = int(errAndMaskString, 2) << 10  # add ten zeros to begin calculation
    polynomial = 0b10100110111

    while (len(bin(bchCalc)) - 2 >= 11):
        bchLen = len(bin(bchCalc)) - 2

        padding = bchLen - (len(bin(polynomial)) - 2)
        bchCalc = bchCalc ^ (polynomial << padding)

    # Combine formatting bits with error correcting bits
    fbin = (int(errAndMaskString, 2) << 10) | bchCalc
    # Apply the string mask
    fbin = fbin ^ 0b101010000010010

    formatString = intToBinString(fbin, 15)

    return formatString

















def fillListFromDict(theList, theDict):
    for key in theDict.keys():
        theList[key[1]][key[0]] = theDict[key]
    return theList

def applyMask(qrList, tabooDict, maskVersion):
    maskedList = list(qrList)
    for x in range(len(maskedList[0])):
        for y in range(len(maskedList)):
            if ((x, y) not in tabooDict.keys()):
                maskedList[y][x] = calcMask(maskVersion, x, y, maskedList[y][x])
    return maskedList

def calcMask(mask, x, y, value):
    if (mask == 0):
        if ((x + y) % 2): return value
        else: return (value ^ 1)
    elif (mask == 1):
        if (y % 2): return value
        else: return (value ^ 1)
    elif (mask == 2):
        if (x % 3): return value
        else: return (value ^ 1)
    elif (mask == 3):
        if ((x + y) % 3): return value
        else: return (value ^ 1)
    elif (mask == 4):
        if (((y / 2) + (x / 3)) % 2): return value
        else: return (value ^ 1)
    elif (mask == 5):
        if (((x * y) % 2) + ((x * y) % 3)): return value
        else: return (value ^ 1)
    elif (mask == 6):
        if ((((x * y) % 2) + ((x * y) % 3)) % 2): return value
        else: return (value ^ 1)
    elif (mask == 7):
        if ((((x * y) % 3) + ((x + y) % 2)) % 2): return value
        else: return (value ^ 1)
    else:
        raise Exception("Mask type value is invalide (needs to between 0 and 7)")

def genQrImage(qrData):

    out = '/home/mike/Desktop/qr_gen_test.png'
    size = 2
    bgcolor = 0xFFFFFF
    fgcolor = 0x000000
    quiet_zone_modules = 4  # required quiet zone pixels around code

    offset = quiet_zone_modules * size

    image = Image.new("RGB", (size * (len(qrData) + (quiet_zone_modules * 2)), size * (len(qrData) + (quiet_zone_modules * 2))), bgcolor)
    draw = ImageDraw.Draw(image)

    for y in range(len(qrData)):
        for x in range(len(qrData)):
            if qrData[y][x]:
                # draw foreground pixel
                x1 = (x * size) + offset
                y1 = (y * size) + offset
                x2 = (x * size) + offset + size - 1
                y2 = (y * size) + offset + size - 1
                # print x1,y1,x2,y2
                draw.rectangle((x1, y1, x2, y2), fgcolor)
            '''
            else:
                #draw background pixel
                #draw.rectangle((x*size,y*size,(x*size)+size,(y*size)+size),bgcolor)
                draw.rectangle(((x+quiet_zone_modules)*size,(y+quiet_zone_modules)*size,((x+quiet_zone_modules)*size)+size,((y+quiet_zone_modules)*size)+size),bgcolor)
            '''

    del draw
    image.save(out, 'PNG')


