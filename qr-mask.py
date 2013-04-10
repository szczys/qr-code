def applyMask(qrList,tabooDict,maskVersion):
    maskedList = list(qrList)
    for x in range(len(maskedList[0])):
        for y in range(len(maskedList)):
            if ((x,y) not in tabooDict.keys()):
                maskedList[y][x] = calcMask(maskVersion,x,y,maskedList[y][x])
    return maskedList

def calcMask(mask,x,y,value):
    if (mask == 0):
        if ((x+y)%2): return value
        else: return (value^1)
    elif (mask == 1):
        if (y%2): return value
        else: return (value^1)
    elif (mask == 2):
        if (x%3): return value
        else: return (value^1)
    elif (mask == 3):
        if ((x+y)%3): return value
        else: return (value^1)
    elif (mask == 4):
        if (((y/2)+(x/3))%2): return value
        else: return (value^1)
    elif (mask == 5):
        if (((x*y)%2)+((x*y)%3)): return value
        else: return (value^1)
    elif (mask == 6):
        if ((((x*y)%2)+((x*y)%3))%2): return value
        else: return (value^1)
    elif (mask == 7):
        if ((((x*y)%3)+((x+y)%2))%2): return value
        else: return (value^1)
    else:
        raise Exception("Mask type value is invalide (needs to between 0 and 7)")
    
