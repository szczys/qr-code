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



# polynomial for ten codewords:
# (even indices are A, odd are X)
# polynomial = [0,10,251,9,67,8,46,7,61,6,118,5,70,4,64,3,94,2,32,1,45,0]

testMessage = [32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236, 17, 236, 17]



def fillQrCode(qrVersion, tabooDict, messageString):
    # use column index based on mod 2 for ever other row
    # start on bottom row
    # use direction indicator for up or down

    size = getGridSize(qrVersion)
    dataIndex = 0
    symbolDict = {}
    y = size - 1
    direction = -1  # -1 for up, 1 for down

    # give me a descending list of every other column index:
    decCols = range(size - 2, -1, -2)
    # fix that list to account for the vertial timing in column 6:
    decCols[-1] -= 1
    decCols[-2] -= 1
    decCols[-3] -= 1

    for x in decCols:
        while(size > y > -1):
            if ((x + 1, y) not in tabooDict.keys()):
                symbolDict[(x + 1, y)] = int(messageString[dataIndex])
                dataIndex += 1
                if (dataIndex >= len(messageString)):
                    return symbolDict

            if ((x, y) not in tabooDict.keys()):
                symbolDict[(x, y)] = int(messageString[dataIndex])
                dataIndex += 1
                if (dataIndex >= len(messageString)):
                    return symbolDict

            y += direction

        direction *= -1  # multiply direction by -1 to flip between 1 and -1
        y += direction

def getGridSize(qrVersion):
    size = (4 * qrVersion) + 17
    return size

def getFinderDict(qrVersion):
    finderDict = {}

    # create list of upper left pixels for each finder pattern
    finderOffset = getGridSize(qrVersion) - 7
    startPixels = (
        (0, 0),
        (finderOffset, 0),
        (0, finderOffset)
        )

    # add finder pixels at each of three locations
    for coord in startPixels:
        for x in range(7):
            for y in range(7):
                # most pixels are black:
                thisPixel = 1

                # certain pixels are white:
                if (((y == 1) or (y == 5)) and (0 < x < 6)):
                    thisPixel = 0
                elif (((x == 1) or (x == 5)) and (1 < y < 5)):
                    thisPixel = 0

                finderDict[coord[0] + x, coord[1] + y] = thisPixel
    return finderDict

def getAlignmentDict(qrVersion, tabooDict):
    alignmentLocs = (
        (),  # There is no version 0
        (),  # Version 1 has no alignment symbol
        (6, 18),
        (6, 22),
        (6, 26),
        (6, 30),
        (6, 34),
        (6, 22, 38),
        (6, 24, 42),
        (6, 26, 46),
        (6, 28, 50),
        (6, 30, 54),
        (6, 32, 58),
        (6, 34, 62),
        (6, 26, 46, 66),
        (6, 26, 48, 70),
        (6, 26, 50, 74),
        (6, 30, 54, 78),
        (6, 30, 56, 82),
        (6, 30, 58, 86),
        (6, 34, 62, 90),
        (6, 28, 50, 72, 94),
        (6, 26, 50, 74, 98),
        (6, 30, 54, 78, 102),
        (6, 28, 54, 80, 106),
        (6, 32, 58, 84, 110),
        (6, 30, 58, 86, 114),
        (6, 34, 62, 90, 118),
        (6, 26, 50, 74, 98, 122),
        (6, 30, 54, 78, 102, 126),
        (6, 26, 52, 78, 104, 130),
        (6, 30, 56, 82, 108, 134),
        (6, 34, 60, 86, 112, 138),
        (6, 30, 58, 86, 114, 142),
        (6, 34, 62, 90, 118, 146),
        (6, 30, 54, 78, 102, 126, 150),
        (6, 24, 50, 76, 102, 128, 154),
        (6, 28, 54, 80, 106, 132, 158),
        (6, 32, 58, 84, 110, 136, 162),
        (6, 26, 54, 82, 110, 138, 166),
        (6, 30, 58, 86, 114, 142, 170)
    )
    alignmentDict = {}
    for centerX in alignmentLocs[qrVersion]:
        for centerY in alignmentLocs [qrVersion]:
            patternOutOfBounds = False
            curPattern = {}
            for x in range(centerX - 2, centerX + 3):
                for y in range(centerY - 2, centerY + 3):
                    '''
                    #most pixels are black:
                    thisPixel = 1
                    #but some pixels are white:
                    if ((centerX-2<x<centerX+2) and (centerY-2<y<centerY+2)):
                        #don't change the center pixel:
                        if ((x!=centerX) and (y!=centerY)):
                            thisPixel = 0
                    '''
                    # start with white pixels:
                    thisPixel = 0
                    # change outer ring to black pixels:
                    if ((x == centerX - 2) or (x == centerX + 2) or (y == centerY - 2) or (y == centerY + 2)):
                        thisPixel = 1
                    # change center pixel to black:
                    elif ((x == centerX) and (y == centerY)):
                        thisPixel = 1

                    curPattern[x, y] = thisPixel

                    # make sure not to add this pattern if it overlaps other features:
                    if ((x, y) in tabooDict.keys()):
                        patternOutOfBounds = True

            if not patternOutOfBounds:
                alignmentDict.update(curPattern)

    return alignmentDict

def getSeparatorDict(qrVersion):
    separatorDict = {}
    size = getGridSize(qrVersion)
    # add horizontal postions to the list:
    for x in range(0, 8):
        separatorDict[x, 7] = 0
        separatorDict[x + (size - 8), 7] = 0
        separatorDict[x, size - 8] = 0

    # add verital positions to the list:
    for y in range(0, 7):
        separatorDict[7, y] = 0
        separatorDict[size - 8, y] = 0
        separatorDict[7, size - 7 + y] = 0

    return separatorDict

def getTimingDict(qrVersion, tabooDict):
    timingDict = {}
    size = getGridSize(qrVersion)
    for i in range(8, size - 8):
        if (i % 2): pixel = 0
        else: pixel = 1
        if ((6, i) not in tabooDict.keys()):
            timingDict[6, i] = pixel
        if ((i, 6) not in tabooDict.keys()):
            timingDict[i, 6] = pixel
    return timingDict

def getFormatDict(qrVersion, formattingString=None):
    # Takes a binary string as an optional formatting argument

    '''
    8,0 through 8,5
    8,7 through 8,8
    7,8
    5,8 throuhg 0,8


    size-1,8 through size-8,8
    8,size-8 is dark
    8,size-7 through 8,size-1
    '''
    size = getGridSize(qrVersion)
    primary = ((0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (7, 8), (8, 8), (8, 7), (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0))
    secondary = ((8, size - 1), (8, size - 2), (8, size - 3), (8, size - 4), (8, size - 5), (8, size - 6), (8, size - 7), (size - 8, 8), (size - 7, 8), (size - 6, 8), (size - 5, 8), (size - 4, 8), (size - 3, 8), (size - 2, 8), (size - 1, 8))


    # fill list with zeros if None was passed as an argument
    if (formattingString == None):
        formattingString = '0' * 15
    elif (len(formattingString) != 15):
        raise Exception("Binary string argument is wrong length (not 15 characters)")
    # populate the format dictionary
    formatDict = {}

    for i in range(15):
        formatDict[primary[i]] = int(formattingString[i])
        formatDict[secondary[i]] = int(formattingString[i])

    # add the always dark pixel:
    formatDict[(8, size - 8)] = 1

    return formatDict

def getVersionDict(qrVersion, versionString=None):
    versionDict = {}

    # only version 7 and up have version blocks
    if (qrVersion < 7):
        return versionDict

    '''
    3x6 area starting at 0,size-11
    6x3 area starting at size-11,0
    '''
    size = getGridSize(qrVersion)
    upper = (0, size - 11)
    lower = (size - 11, 0)

    if (versionString == None):
        versionString = '0' * 18
    if (len(versionString) != 18):
        raise Exception("Version string argument is wrong length (not 18 characters)")

    for i in range(18):
        # offest for upper right version block
        x1offset = i / 3
        y1offset = i % 3
        # offset for lower left version block
        x2offset = i % 3
        y2offset = i / 3

        # add value to both locations:
        versionDict[upper[0] + x1offset, upper[1] + y1offset] = int(versionString[i])
        versionDict[lower[0] + x2offset, lower[1] + y2offset] = int(versionString[i])
    return versionDict

def getEmptyGrid(qrVersion):
    size = getGridSize(qrVersion)
    grid = [[0] * size for _ in range(size)]
    
    return grid

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


