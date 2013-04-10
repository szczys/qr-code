
def fillQrCode(qrVersion,tabooDict,messageString):
    #use column index based on mod 2 for ever other row
    #start on bottom row
    #use direction indicator for up or down

    size = getGridSize(qrVersion)
    dataIndex = 0
    symbolDict = {}
    y = size-1
    direction = -1 #-1 for up, 1 for down

    #give me a descending list of every other column index:
    decCols = range(size-2,-1,-2)
    #fix that list to account for the vertial timing in column 6:
    decCols[-1] -= 1
    decCols[-2] -= 1
    decCols[-3] -= 1
    
    for x in decCols:
        while(size>y>-1):
            if ((x+1,y) not in tabooDict.keys()):
                symbolDict[(x+1,y)] = int(messageString[dataIndex])
                dataIndex += 1
                if (dataIndex >= len(messageString)):
                    return symbolDict
                
            if ((x,y) not in tabooDict.keys()):
                symbolDict[(x,y)] = int(messageString[dataIndex])
                dataIndex += 1
                if (dataIndex >= len(messageString)):
                    return symbolDict

            y += direction

        direction *= -1 #multiply direction by -1 to flip between 1 and -1
        y += direction
