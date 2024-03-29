#This is the 1-M test from ISO/IEC 18004:2000(E) page 84


#FIXME:    DEPRECATED: This file won't work since the code was formatted into classes.
#FIXME:                    It remains here for reference only but should be removed.


message = 'HELLO WORLD'
qrVersion = 1
errorLevel = 'M'

#get new object based on our test message
info = SymbolInfo(message,qrVersion,1)

exit()

#Start by converting data to a string of binary
dataString = makeNumericMessage(message,qrVersion)

#Pad that string to make it an even number of 8-bit words
dataString = padBinMessage(dataString)

#Pad the set of 8-bit words to fill the QR code's data word area
dataString = padCodeWords(dataString,qrVersion,errorLevel)

#Translate the binary words into ints
messageWords = []
for i in range(len(dataString)/8):
    messageWords.append(int(dataString[(i*8):(i*8)+8],2))

#Generate gode words from that list of ints
ecCodes = generateCodewords(10,messageWords)

#Convert codewords to binary and append to the dataString
for i in ecCodes:
    dataString += intToBinString(i,8)

#build a version 1 tabooList
tabooDict = {}
tabooDict.update(getFinderDict(qrVersion))
tabooDict.update(getAlignmentDict(qrVersion,tabooDict))
tabooDict.update(getSeparatorDict(qrVersion))
tabooDict.update(getTimingDict(qrVersion,tabooDict))
tabooDict.update(getFormatDict(qrVersion))
tabooDict.update(getVersionDict(qrVersion))

#Place the datastring in the version 1 code matrix
messageDict = fillQrCode(qrVersion,tabooDict,dataString)

#Generate a grid and fill it
grid = fillListFromDict(getEmptyGrid(qrVersion),messageDict)

#Add all of the tabooDict bits
grid = fillListFromDict(grid,tabooDict)

'''TODO: Add format data'''
grid = fillListFromDict(grid,getFormatDict(1,getFormatting('M',3)))

#mask data
grid = applyMask(grid,tabooDict,3)

'''TODO: autodiscriminate'''

'''TODO: add verion data'''

#make the tag
genQrImage(grid)
