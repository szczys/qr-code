

#calling len(bin(x)) will always return 2 more than the actual
#number of bits because it includes '0b' in the count

def getFormatting(errAndMaskString):
    bchCalc = int(errAndMaskString,2)<<10 #add ten zeros to begin calculation
    polynomial = 0b10100110111

    while (len(bin(bchCalc))-2 >= 11):
        bchLen = len(bin(bchCalc))-2

        padding = bchLen-(len(bin(polynomial))-2)
        bchCalc = bchCalc ^ (polynomial<<padding)

    #Combine formatting bits with error correcting bits
    fbin = (int(errAndMaskString,2)<<10) | bchCalc
    #Apply the string mask
    fbin = fbin ^ 0b101010000010010
    formatList = [0]*15

    formatString = intToBinString(fbin,15)

    return formatString
