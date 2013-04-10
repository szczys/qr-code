#This is the 1-M test from ISO/IEC 18004:2000(E) page 84


message = '01234567'
qrVersion = 1
errorLevel = 'M'
dataString = makeNumericMessage(message,qrVersion)
dataString = padMessageString(dataString)
dataString = padCodeWords(dataString,qrVersion,errorLevel)
