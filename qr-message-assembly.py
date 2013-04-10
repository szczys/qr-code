def makeNumericMessage(inMessage,qrVersion):
    #hardcode Numeric message mode indicator
    messageString = '0001'

    #append character count:
    '''FIXME: the bit length should be calculated, not hardcoded'''
    length = len(inMessage)
    binLength = intToBinString(length,10)
    messageString += binLength

    i = 0
    while(i<length):
        if (i+2 < length):
            curSet = int(inMessage[i] + inMessage[i+1] + inMessage[i+2])
            messageString += intToBinString(curSet,10)
            i += 3
        else:
            if (i+1 <length):
                curSet = int(inMessage[i] + inMessage[i+1])
                messageString += intToBinString(curSet,7)
                i += 2
            else:
                curSet = int(inMessage[i])
                messageString += intToBinString(curSet,4)
                i += 1

    #add terminator (0000):
    '''FIXME: "This may be omitted if the data bit stream
            completely fills the capacity of the
            symbol, or abbreviated if the remaining
            capacity of the symbol is less than 4 bits."
    '''
    messageString += '0000'
    return messageString
    

def make8bitMessage(inMessage):
    #hardcode 8-bit byte encoding:
    messageString = '0100'
    #append character count:
    '''FIXME: the bit length of this character count should be calculated'''
    messageString += intToBinString(len(inMessage),8)
    
    for char in inMessage:
        messageString += intToBinString(ord(char),8)
    
    return messageString

def intToBinString(num,digitLength):
    #converts an integer to an eight bit binary number returned as a string
    #the ord() function can be used to convert a char to its int value
    return '0'*(digitLength-len(bin(num)[2:])) + bin(num)[2:]

def makeAlphaNumMessage(inMessage):
    alphaNumSet = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','$','%','*','+','-','.','/',':')

    messageString = '0010'

    '''FIXME: number of bits used in length should depend on version and error correction level'''
    binCount = bin(len(inMessage))
    paddedCount = '0'*(9-len(binCount[2:])) + binCount[2:]
    messageString += paddedCount
                       
    #check to make sure it's alpha-numeric only:
    for char in inMessage:
        #check to make sure it's alpha-numeric only:
        if not (char in alphaNumSet):
            raise ValueError(char)
        
    for index in range(len(inMessage)):
        #only operate on the even indices:
        if (index % 2 == 0):
            #if this is the last number simply append it
            if (index == len(inMessage)-1):
                curCode = alphaNumSet.index(inMessage[index])
                print curCode
                binCode= '0'*(6-len(bin(curCode)[2:])) + bin(curCode)[2:]
                print binCode
                messageString += binCode
            else:
                curCode = alphaNumSet.index(inMessage[index])
                print curCode
                nextCode = alphaNumSet.index(inMessage[index+1])
                print nextCode
                calcCode = (45*curCode)+nextCode
                binCode = '0'*(11-len(bin(calcCode)[2:])) + bin(calcCode)[2:]
                print binCode
                messageString += binCode
    return messageString

def padMessageString(messageString):
    #adds zeros to right side of string to create all 8-bit words
    messageString += '0'*(8-(len(messageString)%8))
    return messageString

def padCodeWords(messageString,qrVersion,errorLevel):
    codeWordLength = {
        'L':(0,19,34,55,80,108,136,156,194),
        'M':(0,16,28,44,64,86,108,124,154),
        'Q':(0,13,22,34,48,62,76,88,110),
        'H':(0,9,16,26,36,46,60,66,86)
        }
    wordLimit = codeWordLength[errorLevel][qrVersion]
    if (len(messageString)/8 > wordLimit):
        raise Exception("Message codewords too long for this Version/Error Correction level")

    paddedCodewords = messageString
    #padding codewords (alternating): 11101100 and 00010001
    for i in range(wordLimit-(len(messageString)/8)):
        if (i%2):
            paddedCodewords += '00010001'
        else: paddedCodewords += '11101100'

    return paddedCodewords
