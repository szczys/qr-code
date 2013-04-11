message = 'HELLO WORLD'
qrVersion = 1
errorLevel = 'Q'

#Start by converting data to a string of binary
dataString = makeAlphaNumMessage(message,qrVersion)
print "preliminary dataString:",dataString

#Pad that string to make it an even number of 8-bit words
dataString = padMessageString(dataString)

#Pad the set of 8-bit words to fill the QR code's data word area
dataString = padCodeWords(dataString,qrVersion,errorLevel)
print 'padCodeWords: ',dataString

#Translate the binary words into ints
messageWords = []
for i in range(len(dataString)/8):
    messageWords.append(int(dataString[(i*8):(i*8)+8],2))

#Generate gode words from that list of ints
'''FIXME: Number of error correcting codewords should be calculated:'''
ecCodes = generateCodewords(13,messageWords)

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
grid = fillListFromDict(grid,getFormatDict(qrVersion,getFormatting(errorLevel,0)))

#mask data
grid = applyMask(grid,tabooDict,0)

'''TODO: autodiscriminate'''

'''TODO: add verion data'''

#make the tag
genQrImage(grid)
