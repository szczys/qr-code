def make8bitMessage(inMessage):
    #hardcode 8-bit byte encoding:
    messageString = '0100'
    #append character count:
    messageString += intToBinString(len(inMessage))
    
    for char in inMessage:
        messageString += intToBinString(ord(char))
    
    return messageString

def intToBinString(num):
    #converts an integer to an eight bit binary number returned as a string
    #the ord() function can be used to convert a char to its int value
    return '0'*(8-len(bin(num)[2:])) + bin(num)[2:]

def makeAlphaNumMessage(inMessage):
    alphaNumSet = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',' ','$','%','*','+','-','.','/',':')

    messageString = '0010'

    #FIXME: number of bits used in length should depend on version and error correction level
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
