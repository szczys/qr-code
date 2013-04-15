import Image
import ImageDraw
import logging
import string
import sys

logging.basicConfig(level=logging.DEBUG)

class SymbolInfo:
    # ISO/IEC 18004:2000(E) page 28
    # capacityTableKey:
    #    -Version
    #        -Error Correction Level
    #            -Capitol letter corresponding to error correction level
    #            -Number of data codewords
    #            -Number of data bits
    #            -Numeric data capacity
    #            -Alpha-Numeric data capacity
    #            -8-bit byte data capacity
    #            -Kanji data capacity
    capacityTable = (
        (),
        (('L', 19, 152, 41, 25, 17, 10), ('M', 16, 128, 34, 20, 14, 8), ('Q', 13, 104, 27, 16, 11, 7), ('H', 9, 72, 17, 10, 7, 4)),
        (('L', 34, 272, 77, 47, 32, 20), ('M', 28, 224, 63, 38, 26, 16), ('Q', 22, 176, 48, 29, 20, 12), ('H', 16, 128, 34, 20, 14, 8)),
        (('L', 55, 440, 127, 77, 53, 32), ('M', 44, 352, 101, 61, 42, 26), ('Q', 34, 272, 77, 47, 32, 20), ('H', 26, 208, 58, 35, 24, 15)),
        (('L', 80, 640, 187, 114, 78, 48), ('M', 64, 512, 149, 90, 62, 38), ('Q', 48, 384, 111, 67, 46, 28), ('H', 36, 288, 82, 50, 34, 21)),
        (('L', 108, 864, 255, 154, 106, 65), ('M', 86, 688, 202, 122, 84, 52), ('Q', 62, 496, 144, 87, 60, 37), ('H', 46, 368, 106, 64, 44, 27)),
        (('L', 136, 1088, 322, 195, 134, 82), ('M', 108, 864, 255, 154, 106, 65), ('Q', 76, 608, 178, 108, 74, 45), ('H', 60, 480, 139, 84, 58, 36)),
        (('L', 156, 1248, 370, 224, 154, 95), ('M', 124, 992, 293, 178, 122, 75), ('Q', 88, 704, 207, 125, 86, 53), ('H', 66, 528, 154, 93, 64, 39)),
        (('L', 194, 1552, 461, 279, 192, 118), ('M', 154, 1232, 365, 221, 152, 93), ('Q', 110, 880, 259, 157, 108, 66), ('H', 86, 688, 202, 122, 84, 52)),
        (('L', 232, 1856, 552, 335, 230, 141), ('M', 182, 1456, 432, 262, 180, 111), ('Q', 132, 1056, 312, 189, 130, 80), ('H', 100, 800, 235, 143, 98, 60)),
        (('L', 274, 2192, 652, 395, 271, 167), ('M', 216, 1728, 513, 311, 213, 131), ('Q', 154, 1232, 364, 221, 151, 93), ('H', 122, 976, 288, 174, 119, 74)),
        (('L', 324, 2592, 772, 468, 321, 198), ('M', 254, 2032, 604, 366, 251, 155), ('Q', 180, 1440, 427, 259, 177, 109), ('H', 140, 1120, 331, 200, 137, 85)),
        (('L', 370, 2960, 883, 535, 367, 226), ('M', 290, 2320, 691, 419, 287, 177), ('Q', 206, 1648, 489, 296, 203, 125), ('H', 158, 1264, 374, 227, 155, 96)),
        (('L', 428, 3424, 1022, 619, 425, 262), ('M', 334, 2672, 796, 483, 331, 204), ('Q', 244, 1952, 580, 352, 241, 149), ('H', 180, 1440, 427, 259, 177, 109)),
        (('L', 461, 3688, 1101, 667, 458, 282), ('M', 365, 2920, 871, 528, 362, 223), ('Q', 261, 2088, 621, 376, 258, 159), ('H', 197, 1576, 468, 283, 194, 120)),
        (('L', 523, 4184, 1250, 758, 520, 320), ('M', 415, 3320, 991, 600, 412, 254), ('Q', 295, 2360, 703, 426, 292, 180), ('H', 223, 1784, 530, 321, 220, 136)),
        (('L', 589, 4712, 1408, 854, 586, 361), ('M', 453, 3624, 1082, 656, 450, 277), ('Q', 325, 2600, 775, 470, 322, 198), ('H', 253, 2024, 602, 365, 250, 154)),
        (('L', 647, 5176, 1548, 938, 644, 397), ('M', 507, 4056, 1212, 734, 504, 310), ('Q', 367, 2936, 876, 531, 364, 224), ('H', 283, 2264, 674, 408, 280, 173)),
        (('L', 721, 5768, 1725, 1046, 718, 442), ('M', 563, 4504, 1346, 816, 560, 345), ('Q', 397, 3176, 948, 574, 394, 243), ('H', 313, 2504, 746, 452, 310, 191)),
        (('L', 795, 6360, 1903, 1153, 792, 488), ('M', 627, 5016, 1500, 909, 624, 384), ('Q', 445, 3560, 1063, 644, 442, 272), ('H', 341, 2728, 813, 493, 338, 208)),
        (('L', 861, 6888, 2061, 1249, 858, 528), ('M', 669, 5352, 1600, 970, 666, 410), ('Q', 485, 3880, 1159, 702, 482, 297), ('H', 385, 3080, 919, 557, 382, 235)),
        (('L', 932, 7456, 2232, 1352, 929, 572), ('M', 714, 5712, 1708, 1035, 711, 438), ('Q', 512, 4096, 1224, 742, 509, 314), ('H', 406, 3248, 969, 587, 403, 248)),
        (('L', 1006, 8048, 2409, 1460, 1003, 618), ('M', 782, 6256, 1872, 1134, 779, 480), ('Q', 568, 4544, 1358, 823, 565, 348), ('H', 442, 3536, 1056, 640, 439, 270)),
        (('L', 1094, 8752, 2620, 1588, 1091, 672), ('M', 860, 6880, 2059, 1248, 857, 528), ('Q', 614, 4912, 1468, 890, 611, 376), ('H', 464, 3712, 1108, 672, 461, 284)),
        (('L', 1174, 9392, 2812, 1704, 1171, 721), ('M', 914, 7312, 2188, 1326, 911, 561), ('Q', 664, 5312, 1588, 963, 661, 407), ('H', 514, 4112, 1228, 744, 511, 315)),
        (('L', 1276, 10208, 3057, 1853, 1273, 784), ('M', 1000, 8000, 2395, 1451, 997, 614), ('Q', 718, 5744, 1718, 1041, 715, 440), ('H', 538, 4304, 1286, 779, 535, 330)),
        (('L', 1370, 10960, 3283, 1990, 1367, 842), ('M', 1062, 8496, 2544, 1542, 1059, 652), ('Q', 754, 6032, 1804, 1094, 751, 462), ('H', 596, 4768, 1425, 864, 593, 365)),
        (('L', 1468, 11744, 3517, 2132, 1465, 902), ('M', 1128, 9024, 2701, 1637, 1125, 692), ('Q', 808, 6464, 1933, 1172, 805, 496), ('H', 628, 5024, 1501, 910, 625, 385)),
        (('L', 1531, 12248, 3669, 2223, 1528, 940), ('M', 1193, 9544, 2857, 1732, 1190, 732), ('Q', 871, 6968, 2085, 1263, 868, 534), ('H', 661, 5288, 1581, 958, 658, 405)),
        (('L', 1631, 13048, 3909, 2369, 1628, 1002), ('M', 1267, 10136, 3035, 1839, 1264, 778), ('Q', 911, 7288, 2181, 1322, 908, 559), ('H', 701, 5608, 1677, 1016, 698, 430)),
        (('L', 1735, 13880, 4158, 2520, 1732, 1066), ('M', 1373, 10984, 3289, 1994, 1370, 843), ('Q', 985, 7880, 2358, 1429, 982, 604), ('H', 745, 5960, 1782, 1080, 742, 457)),
        (('L', 1843, 14744, 4417, 2677, 1840, 1132), ('M', 1455, 11640, 3486, 2113, 1452, 894), ('Q', 1033, 8264, 2473, 1499, 1030, 634), ('H', 793, 6344, 1897, 1150, 790, 486)),
        (('L', 1955, 15640, 4686, 2840, 1952, 1201), ('M', 1541, 12328, 3693, 2238, 1538, 947), ('Q', 1115, 8920, 2670, 1618, 1112, 684), ('H', 845, 6760, 2022, 1226, 842, 518)),
        (('L', 2071, 16568, 4965, 3009, 2068, 1273), ('M', 1631, 13048, 3909, 2369, 1628, 1002), ('Q', 1171, 9368, 2805, 1700, 1168, 719), ('H', 901, 7208, 2157, 1307, 898, 553)),
        (('L', 2191, 17528, 5253, 3183, 2188, 1347), ('M', 1725, 13800, 4134, 2506, 1722, 1060), ('Q', 1231, 9848, 2949, 1787, 1228, 756), ('H', 961, 7688, 2301, 1394, 958, 590)),
        (('L', 2306, 18448, 5529, 3351, 2303, 1417), ('M', 1812, 14496, 4343, 2632, 1809, 1113), ('Q', 1286, 10288, 3081, 1867, 1283, 790), ('H', 986, 7888, 2361, 1431, 983, 605)),
        (('L', 2434, 19472, 5836, 3537, 2431, 1496), ('M', 1914, 15, 312, 4588, 2780, 1911, 1176), ('Q', 1354, 10832, 3244, 1966, 1351, 832), ('H', 1054, 8432, 2524, 1530, 1051, 647)),
        (('L', 2566, 20528, 6153, 3729, 2563, 1577), ('M', 1992, 15, 936, 4775, 2894, 1989, 1224), ('Q', 1426, 11408, 3417, 2071, 1423, 876), ('H', 1096, 8768, 2625, 1591, 1093, 673)),
        (('L', 2702, 21616, 6479, 3927, 2699, 1661), ('M', 2102, 16816, 5039, 3054, 2099, 1292), ('Q', 1502, 12016, 3599, 2181, 1499, 923), ('H', 1142, 9136, 2735, 1658, 1139, 701)),
        (('L', 2812, 22496, 6743, 4087, 2809, 1729), ('M', 2216, 17728, 5313, 3220, 2213, 1362), ('Q', 1582, 12656, 3791, 2298, 1579, 972), ('H', 1222, 9, 776, 2927, 1774, 1219, 750)),
        (('L', 2956, 23648, 7089, 4296, 2953, 1817), ('M', 2334, 18672, 5596, 3391, 2331, 1435), ('Q', 1666, 13328, 3993, 2420, 1663, 1024), ('H', 1276, 10208, 3057, 1852, 1273, 784))
        )
      
    def __init__(self, inMessage, qrVersion=None, errLevel=None):      
        self.inMessage = inMessage
        self.qrVersion = qrVersion
        self.errLevel = errLevel
        self.charSet = self.whichCharSet()
        
        # TODO: this will automatically choose the smallest tag with the most error
        # correction. should this be parametric instead?
        if ((self.qrVersion == None) and (self.errLevel == None)):
            possibleSizes = self.getSizes(self.charSet, len(self.inMessage))
            winner = len(possibleSizes) - 1
            for i in range(len(possibleSizes) - 2, -1, -1):
                if possibleSizes[i] < possibleSizes[winner]:
                    winner = i
            self.qrVersion = possibleSizes[winner]
            self.errLevel = winner
                  
        if ((self.errLevel == None) and (self.qrVersion != None)):
            # This should catch when qrLevel is specified but errLevel is not
            self.qrVersion = qrVersion
            # dig through the table to find highest errLevel that will work
            self.errLevel = errLevel
            for i in range(4):
                if (len(self.inMessage) <= self.capacityTable[self.qrVersion][i][self.charSet + 2]):
                    self.errLevel = i
            
            if (self.errLevel == None):
                raise ValueError("Specified QR Version can't fit this message using any error correction level") 
        
        if (self.qrVersion == None):
            # This should catch when errLevel is specified but qrVersion is not
            self.errLevel = errLevel
            self.qrVersion = self.getSizes(self.charSet, len(self.inMessage))[self.errLevel]
            
        # Sanity check the qrVersion and errLevel to ensure that they will work
        if (self.capacityTable[self.qrVersion][self.errLevel][self.charSet + 2] < len(self.inMessage)):
            raise ValueError("QR Version and Error Correction levels selected don't contain enough room for this message")
        
        # Version and error correction level work, fill in the rest of the variables
        self.dataCodewords = self.capacityTable[self.qrVersion][self.errLevel][1]
        self.dataBits = self.capacityTable[self.qrVersion][self.errLevel][2]
        self.gridSize = (4 * self.qrVersion) + 17
        
        logging.debug("%s:%s:inMessage: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.inMessage)
        logging.debug("%s:%s:charSet: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.charSet)
        logging.debug("%s:%s:qrVersion: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.qrVersion)
        logging.debug("%s:%s:errLevel: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.errLevel)
        logging.debug("%s:%s:dataCodewords: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.dataCodewords)
        logging.debug("%s:%s:dataBits: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.dataBits)
        logging.debug("%s:%s:gridSize: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.gridSize)

    def getSizes(self, charSet, charCount):
        results = []
        symbolSize = 1
        while (symbolSize <= 40):
            for errorLevel in range(4):
                if (len(results) < errorLevel + 1):
                    if (charCount <= self.capacityTable[symbolSize][errorLevel][charSet + 2]):
                        results.append(symbolSize)
            symbolSize += 1
            
        return results
        
    def whichCharSet(self):
        # find out which charSet should be used
        charSetScoreboard = [
            0,  # ECI - Not Implemented yet
            1,  # Numeric
            1,  # Alphanumeric
            1,  # 8-bit Byte
            0,  # Kanji - Not Implemented yet
            0,  # Structured Append - Not Implemented yet
            0  # FNC1 - Not Implemented yet
            ]
    
        charSetListing = (
            (),  # ECI - Not Implemented yet
            (string.digits),  # Numeric
            (string.digits + string.uppercase + ' $%*+-./:'),  # Alphanumeric
            (string.punctuation.replace('\\', '') + string.digits + string.lowercase + string.uppercase + ' '
             # '\xef\xbd\xa1', '\xef\xbd\xa2', '\xef\xbd\xa3', '\xef\xbd\xa4', '\xef\xbd\xa5', '\xef\xbd\xa6', '\xef\xbd\xa7', '\xef\xbd\xa8', '\xef\xbd\xa9', '\xef\xbd\xaa', '\xef\xbd\xab', '\xef\xbd\xac', '\xef\xbd\xad', '\xef\xbd\xae', '\xef\xbd\xaf', '\xef\xbd\xb0', '\xef\xbd\xb1', '\xef\xbd\xb2', '\xef\xbd\xb3', '\xef\xbd\xb4', '\xef\xbd\xb5', '\xef\xbd\xb6', '\xef\xbd\xb7', '\xef\xbd\xb8', '\xef\xbd\xb9', '\xef\xbd\xba', '\xef\xbd\xbb', '\xef\xbd\xbc', '\xef\xbd\xbd', '\xef\xbd\xbe', '\xef\xbd\xbf', '\xef\xbe\x80', '\xef\xbe\x81', '\xef\xbe\x82', '\xef\xbe\x83', '\xef\xbe\x84', '\xef\xbe\x85', '\xef\xbe\x86', '\xef\xbe\x87', '\xef\xbe\x88', '\xef\xbe\x89', '\xef\xbe\x8a', '\xef\xbe\x8b', '\xef\xbe\x8c', '\xef\xbe\x8d', '\xef\xbe\x8e', '\xef\xbe\x8f', '\xef\xbe\x90', '\xef\xbe\x91', '\xef\xbe\x92', '\xef\xbe\x93', '\xef\xbe\x94', '\xef\xbe\x95', '\xef\xbe\x96', '\xef\xbe\x97', '\xef\xbe\x98', '\xef\xbe\x99', '\xef\xbe\x9a', '\xef\xbe\x9b', '\xef\xbe\x9c', '\xef\xbe\x9d', '\xef\xbe\x9e', '\xef\xbe\x9f'
             ),  # 8-bit Byte
            (),  # Kanji - Not Implemented yet
            (),  # Structured Append - Not Implemented yet
            ()  # FNC1 - Not Implemented yet
            )
    
        for char in self.inMessage:
            for i in range(len(charSetListing)):
                if (char not in charSetListing[i]):
                    charSetScoreboard[i] = 0
    
        for i in range(len(charSetScoreboard)):
            if (charSetScoreboard[i] != 0):
                return i
        
        raise ValueError("Message contains invalid characters")
        return

class BinaryMessage:
    def __init__(self, symInf):
        # symInf must be a SymbolInfo object
        self.infoSource = symInf
               
        if (self.infoSource.charSet == 1):  # Numeric
            self.binMessage = self.makeNumericMessage()
        if (self.infoSource.charSet == 2):  # Alphanumeric
            self.binMessage = self.makeAlphaNumMessage()
        if (self.infoSource.charSet == 3):  # 8-bit
            logging.error("Not Implemented")
            exit(1)
        if (self.infoSource.charSet == 4):  # Kanji
            logging.error("Not Implemented")
            exit(1)
        
        self.padBinMessage()
        self.padDataWords()
       
                

            

    def makeNumericMessage(self):
        # hardcode Numeric message mode indicator
        messageString = '0001'
    
        # append character count:
        length = len(self.infoSource.inMessage)
        binLength = self.intToBinString(length, self.getCountLength())
        messageString += binLength
    
        i = 0
        while(i < length):
            if (i + 2 < length):
                curSet = int(self.infoSource.inMessage[i] + self.infoSource.inMessage[i + 1] + self.infoSource.inMessage[i + 2])
                messageString += self.intToBinString(curSet, 10)
                i += 3
            else:
                if (i + 1 < length):
                    curSet = int(self.infoSource.inMessage[i] + self.infoSource.inMessage[i + 1])
                    messageString += self.intToBinString(curSet, 7)
                    i += 2
                else:
                    curSet = int(self.infoSource.inMessage[i])
                    messageString += self.intToBinString(curSet, 4)
                    i += 1
    
        return messageString
    
    def make8bitMessage(self):
        # hardcode 8-bit byte encoding:
        messageString = '0100'
        # append character count:
        messageString += self.intToBinString(len(self.infoSource.inMessage), self.getCountLength())
    
        for char in self.infoSource.inMessage:
            messageString += self.intToBinString(ord(char), 8)
    
        return messageString

    def makeAlphaNumMessage(self):
        alphaNumSet = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*', '+', '-', '.', '/', ':')
    
        messageString = '0010'
        messageString += self.intToBinString(len(self.infoSource.inMessage), self.getCountLength())
            
        # check to make sure it's alpha-numeric only:
        for char in self.infoSource.inMessage:
            # check to make sure it's alpha-numeric only:
            if not (char in alphaNumSet):
                raise ValueError(char)
    
        for index in range(len(self.infoSource.inMessage)):
            # only operate on the even indices:
            if (index % 2 == 0):
                # if this is the last number simply append it
                if (index == len(self.infoSource.inMessage) - 1):
                    curCode = alphaNumSet.index(self.infoSource.inMessage[index])
                    binCode = '0' * (6 - len(bin(curCode)[2:])) + bin(curCode)[2:]
                    messageString += binCode
                else:
                    curCode = alphaNumSet.index(self.infoSource.inMessage[index])
                    nextCode = alphaNumSet.index(self.infoSource.inMessage[index + 1])
                    calcCode = (45 * curCode) + nextCode
                    binCode = '0' * (11 - len(bin(calcCode)[2:])) + bin(calcCode)[2:]
                    messageString += binCode
        return messageString
    
    def intToBinString(self, num, digitLength):
        # converts an integer to an eight bit binary number returned as a string
        # the ord() function can be used to convert a char to its int value
        return '0' * (digitLength - len(bin(num)[2:])) + bin(num)[2:]
    
    def getCountLength(self):
        charCountBitLength = (
                              (10, 9, 8, 8),
                              (12, 11, 16, 10),
                              (14, 13, 16, 12)
                              )
        if (0 < self.infoSource.qrVersion < 10):
            return  charCountBitLength[0][self.infoSource.charSet - 1]
        elif(10 <= self.infoSource.qrVersion <= 27):
            return  charCountBitLength[1][self.infoSource.charSet - 1]
        elif(28 <= self.infoSource.qrVersion <= 40):
            return  charCountBitLength[2][self.infoSource.charSet - 1]
        else:
            raise ValueError("Bit length of message count cannot be calculated for some reason.")
        
    def padBinMessage(self):
        remainingBits = self.infoSource.dataBits - len(self.binMessage)
        if (remainingBits < 0):
            raise ValueError("Somehow our binary message is longer than the limit")
        elif (remainingBits > 0):
            if (remainingBits <= 4):
                self.binMessage += '0' * remainingBits
            else:
                # add the terminator
                self.binMessage += '0000'
                self.binMessage += '0' * (8 - (len(self.binMessage) % 8))
        logging.debug("%s:%s:binMessage: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.binMessage)
                
    def padDataWords(self):
        # padding codewords (alternating): 11101100 and 00010001
        for i in range(self.infoSource.dataCodewords - (len(self.binMessage) / 8)):
            if (i % 2):
                self.binMessage += '00010001'
            else: self.binMessage += '11101100'
        logging.debug("%s:%s:binMessage: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.binMessage)

class ErrorCodewords():
    # Most of what you find in this class class was designed around error correction examples from thonky.com
    # http://www.thonky.com/qr-code-tutorial/error-correction-coding/#step-6-understand-multiplication-with-logs-and-antilogs
    
    antiLogTable = (
    # table courtesy of thonky.com
    # http://bit.ly/YWcXLk
        0, 0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52, 141, 239, 129, 28, 193, 105,
        248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106,
        39, 249, 185, 201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 152, 37, 179, 16, 145,
        34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126,
        110, 107, 58, 40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 172, 115, 243, 167, 87,
        7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17,
        68, 146, 217, 35, 32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 190, 97, 242, 86,
        211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236,
        127, 12, 111, 246, 108, 161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 95, 176, 156,
        169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213, 233, 230, 231, 173, 232, 116, 214, 244, 234, 168,
        80, 88, 175
        )
    
    logTable = (
    # table courtesy of thonky.com
    # http://bit.ly/YWcXLk
        1, 2, 4, 8, 16, 32, 64, 128, 29, 58, 116, 232, 205, 135, 19, 38, 76, 152, 45, 90, 180, 117, 234, 201, 143,
        3, 6, 12, 24, 48, 96, 192, 157, 39, 78, 156, 37, 74, 148, 53, 106, 212, 181, 119, 238, 193, 159, 35, 70,
        140, 5, 10, 20, 40, 80, 160, 93, 186, 105, 210, 185, 111, 222, 161, 95, 190, 97, 194, 153, 47, 94, 188,
        101, 202, 137, 15, 30, 60, 120, 240, 253, 231, 211, 187, 107, 214, 177, 127, 254, 225, 223, 163, 91, 182,
        113, 226, 217, 175, 67, 134, 17, 34, 68, 136, 13, 26, 52, 104, 208, 189, 103, 206, 129, 31, 62, 124, 248,
        237, 199, 147, 59, 118, 236, 197, 151, 51, 102, 204, 133, 23, 46, 92, 184, 109, 218, 169, 79, 158, 33, 66,
        132, 21, 42, 84, 168, 77, 154, 41, 82, 164, 85, 170, 73, 146, 57, 114, 228, 213, 183, 115, 230, 209, 191,
        99, 198, 145, 63, 126, 252, 229, 215, 179, 123, 246, 241, 255, 227, 219, 171, 75, 150, 49, 98, 196, 149,
        55, 110, 220, 165, 87, 174, 65, 130, 25, 50, 100, 200, 141, 7, 14, 28, 56, 112, 224, 221, 167, 83, 166,
        81, 162, 89, 178, 121, 242, 249, 239, 195, 155, 43, 86, 172, 69, 138, 9, 18, 36, 72, 144, 61, 122, 244,
        245, 247, 243, 251, 235, 203, 139, 11, 22, 44, 88, 176, 125, 250, 233, 207, 131, 27, 54, 108, 216, 173,
        71, 142, 1)
    
    polyDict = {
    # table from ISO/IEC 18004:2000(E)
    # pages 67-73
    #
    # (even indices are A, odd are X)
        7: [0, 7, 87, 6, 229, 5, 146, 4, 149, 3, 238, 2, 102, 1, 21, 0],
        10: [0, 10, 251, 9, 67, 8, 46, 7, 61, 6, 118, 5, 70, 4, 64, 3, 94, 2, 32, 1, 45, 0],
        13: [0, 13, 74, 12, 152, 11, 176, 10, 100, 9, 86, 8, 100, 7, 106, 6, 104, 5, 130, 4, 218, 3, 206, 2, 140, 1, 78, 0],
        15: [0, 15, 8, 14, 183, 13, 61, 12, 91, 11, 202, 10, 37, 9, 51, 8, 58, 7, 58, 6, 237, 5, 140, 4, 124, 3, 5, 2, 99, 1, 105, 0],
        16: [0, 16, 120, 15, 104, 14, 107, 13, 109, 12, 102, 11, 161, 10, 76, 9, 3, 8, 91, 7, 191, 6, 147, 5, 169, 4, 182, 3, 194, 2, 225, 1, 120, 0],
        17: [0, 17, 43, 16, 139, 15, 206, 14, 78, 13, 43, 12, 239, 11, 123, 10, 206, 9, 214, 8, 147, 7, 24, 6, 99, 5, 150, 4, 39, 3, 243, 2, 163, 1, 136, 0],
        18: [0, 18, 215, 17, 234, 16, 158, 15, 94, 14, 184, 13, 97, 12, 118, 11, 170, 10, 79, 9, 187, 8, 152, 7, 148, 6, 252, 5, 179, 4, 5, 3, 98, 2, 96, 1, 153, 0],
        20: [0, 20, 17, 19, 60, 18, 79, 17, 50, 16, 61, 15, 163, 14, 26, 13, 187, 12, 202, 11, 180, 10, 221, 9, 225, 8, 83, 7, 239, 6, 156, 5, 164, 4, 212, 3, 212, 2, 188, 1, 190, 0],
        22: [0, 22, 210, 21, 171, 20, 247, 19, 242, 18, 93, 17, 230, 16, 14, 15, 109, 14, 221, 13, 53, 12, 200, 11, 74, 10, 8, 9, 172, 8, 98, 7, 80, 6, 219, 5, 134, 4, 160, 3, 105, 2, 165, 1, 231, 0],
        24: [0, 24, 229, 23, 121, 22, 135, 21, 48, 20, 211, 19, 117, 18, 251, 17, 126, 16, 159, 15, 180, 14, 169, 13, 152, 12, 192, 11, 226, 10, 228, 9, 218, 8, 111, 7, 0, 6, 117, 5, 232, 4, 87, 3, 96, 2, 227, 1, 21, 0],
        26: [0, 26, 173, 25, 125, 24, 158, 23, 2, 22, 103, 21, 182, 20, 118, 19, 17, 18, 145, 17, 201, 16, 111, 15, 28, 14, 165, 13, 53, 12, 161, 11, 21, 10, 245, 9, 142, 8, 13, 7, 102, 6, 48, 5, 227, 4, 153, 3, 145, 2, 218, 1, 70, 0],
        28: [0, 28, 168, 27, 223, 26, 200, 25, 104, 24, 224, 23, 234, 22, 108, 21, 180, 20, 110, 19, 190, 18, 195, 17, 147, 16, 205, 15, 27, 14, 232, 13, 201, 12, 21, 11, 43, 10, 245, 9, 87, 8, 42, 7, 195, 6, 212, 5, 119, 4, 242, 3, 37, 2, 9, 1, 123, 0],
        30: [0, 30, 41, 29, 173, 28, 145, 27, 152, 26, 216, 25, 31, 24, 179, 23, 182, 22, 50, 21, 48, 20, 110, 19, 86, 18, 239, 17, 96, 16, 222, 15, 125, 14, 42, 13, 173, 12, 226, 11, 193, 10, 224, 9, 130, 8, 156, 7, 37, 6, 251, 5, 216, 4, 238, 3, 40, 2, 192, 1, 180, 0],
        32: [0, 32, 10, 31, 6, 30, 106, 29, 190, 28, 249, 27, 167, 26, 4, 25, 67, 24, 209, 23, 138, 22, 138, 21, 32, 20, 242, 19, 123, 18, 89, 17, 27, 16, 120, 15, 185, 14, 80, 13, 156, 12, 38, 11, 69, 10, 171, 9, 60, 8, 28, 7, 222, 6, 80, 5, 52, 4, 254, 3, 185, 2, 220, 1, 241, 0],
        34: [0, 34, 111, 33, 77, 32, 146, 31, 94, 30, 26, 29, 21, 28, 108, 27, 19, 26, 105, 25, 94, 24, 113, 23, 193, 22, 86, 21, 140, 20, 163, 19, 125, 18, 58, 17, 158, 16, 229, 15, 239, 14, 218, 13, 103, 12, 56, 11, 70, 10, 114, 9, 61, 8, 183, 7, 129, 6, 167, 5, 13, 4, 98, 3, 62, 2, 129, 1, 51, 0],
        36: [0, 36, 200, 35, 183, 34, 98, 33, 16, 32, 172, 31, 31, 30, 246, 29, 234, 28, 60, 27, 152, 26, 115, 25, 0, 24, 167, 23, 152, 22, 113, 21, 248, 20, 238, 19, 107, 18, 18, 17, 63, 16, 218, 15, 37, 14, 87, 13, 210, 12, 105, 11, 177, 10, 120, 9, 74, 8, 121, 7, 196, 6, 117, 5, 251, 4, 113, 3, 233, 2, 30, 1, 120, 0],
        40: [0, 40, 59, 39, 116, 38, 79, 37, 161, 36, 252, 35, 98, 34, 128, 33, 205, 32, 128, 31, 161, 30, 247, 29, 57, 28, 163, 27, 56, 26, 235, 25, 106, 24, 53, 23, 26, 22, 187, 21, 174, 20, 226, 19, 104, 18, 170, 17, 7, 16, 175, 15, 35, 14, 181, 13, 114, 12, 88, 11, 41, 10, 47, 9, 163, 8, 125, 7, 134, 6, 72, 5, 20, 4, 232, 3, 53, 2, 35, 1, 15, 0],
        42: [0, 42, 250, 41, 103, 40, 221, 39, 230, 38, 25, 37, 18, 36, 137, 35, 231, 34, 0, 33, 3, 32, 58, 31, 242, 30, 221, 29, 191, 28, 110, 27, 84, 26, 230, 25, 8, 24, 188, 23, 106, 22, 96, 21, 147, 20, 15, 19, 131, 18, 139, 17, 34, 16, 101, 15, 223, 14, 39, 13, 101, 12, 213, 11, 199, 10, 237, 9, 254, 8, 201, 7, 123, 6, 171, 5, 162, 4, 194, 3, 117, 2, 50, 1, 96, 0],
        44: [0, 44, 190, 43, 7, 42, 61, 41, 121, 40, 71, 39, 246, 38, 69, 37, 55, 36, 168, 35, 188, 34, 89, 33, 243, 32, 191, 31, 25, 30, 72, 29, 123, 28, 9, 27, 145, 26, 14, 25, 247, 24, 0, 23, 238, 22, 44, 21, 78, 20, 143, 19, 62, 18, 224, 17, 126, 16, 118, 15, 114, 14, 68, 13, 163, 12, 52, 11, 194, 10, 217, 9, 147, 8, 204, 7, 169, 6, 37, 5, 130, 4, 113, 3, 102, 2, 73, 1, 181, 0],
        46: [0, 46, 112, 45, 94, 44, 88, 43, 112, 42, 253, 41, 224, 40, 202, 39, 115, 38, 187, 37, 99, 36, 89, 35, 5, 34, 54, 33, 113, 32, 129, 31, 44, 30, 58, 29, 16, 28, 135, 27, 216, 26, 169, 25, 211, 24, 36, 23, 0, 22, 4, 21, 96, 20, 60, 19, 241, 18, 73, 17, 104, 16, 234, 15, 8, 14, 249, 13, 245, 12, 119, 11, 174, 10, 52, 9, 25, 8, 157, 7, 224, 6, 43, 5, 202, 4, 223, 3, 19, 2, 82, 1, 15, 0],
        48: [0, 48, 228, 47, 25, 46, 196, 45, 130, 44, 211, 43, 146, 42, 60, 41, 24, 40, 251, 39, 90, 38, 39, 37, 102, 36, 240, 35, 61, 34, 178, 33, 63, 32, 46, 31, 123, 30, 115, 29, 18, 28, 221, 27, 111, 26, 135, 25, 160, 24, 182, 23, 205, 22, 107, 21, 206, 20, 95, 19, 150, 18, 120, 17, 184, 16, 91, 15, 21, 14, 247, 13, 156, 12, 140, 11, 238, 10, 191, 9, 11, 8, 94, 7, 227, 6, 84, 5, 50, 4, 163, 3, 39, 2, 34, 1, 108, 0],
        50: [0, 50, 232, 49, 125, 48, 157, 47, 161, 46, 164, 45, 9, 44, 118, 43, 46, 42, 209, 41, 99, 40, 203, 39, 193, 38, 35, 37, 3, 36, 209, 35, 111, 34, 195, 33, 242, 32, 203, 31, 225, 30, 46, 29, 13, 28, 32, 27, 160, 26, 126, 25, 209, 24, 130, 23, 160, 22, 242, 21, 215, 20, 242, 19, 75, 18, 77, 17, 42, 16, 189, 15, 32, 14, 113, 13, 65, 12, 124, 11, 69, 10, 228, 9, 114, 8, 235, 7, 175, 6, 124, 5, 170, 4, 215, 3, 232, 2, 133, 1, 205, 0],
        52: [0, 52, 116, 51, 50, 50, 86, 49, 186, 48, 50, 47, 220, 46, 251, 45, 89, 44, 192, 43, 46, 42, 86, 41, 127, 40, 124, 39, 19, 38, 184, 37, 233, 36, 151, 35, 215, 34, 22, 33, 14, 32, 59, 31, 145, 30, 37, 29, 242, 28, 203, 27, 134, 26, 254, 25, 89, 24, 190, 23, 94, 22, 59, 21, 65, 20, 124, 19, 113, 18, 100, 17, 233, 16, 235, 15, 121, 14, 22, 13, 76, 12, 86, 11, 97, 10, 39, 9, 242, 8, 200, 7, 220, 6, 101, 5, 33, 4, 239, 3, 254, 2, 116, 1, 51, 0],
        54: [0, 54, 183, 53, 26, 52, 201, 51, 87, 50, 210, 49, 221, 48, 113, 47, 21, 46, 46, 45, 65, 44, 45, 43, 50, 42, 238, 41, 184, 40, 249, 39, 225, 38, 102, 37, 58, 36, 209, 35, 218, 34, 109, 33, 165, 32, 26, 31, 95, 30, 184, 29, 192, 28, 52, 27, 245, 26, 35, 25, 254, 24, 238, 23, 175, 22, 172, 21, 79, 20, 123, 19, 25, 18, 122, 17, 43, 16, 120, 15, 108, 14, 215, 13, 80, 12, 128, 11, 201, 10, 235, 9, 8, 8, 153, 7, 59, 6, 101, 5, 31, 4, 198, 3, 76, 2, 31, 1, 156, 0],
        56: [0, 56, 106, 55, 120, 54, 107, 53, 157, 52, 164, 51, 216, 50, 112, 49, 116, 48, 2, 47, 91, 46, 248, 45, 163, 44, 36, 43, 201, 42, 202, 41, 229, 40, 6, 39, 144, 38, 254, 37, 155, 36, 135, 35, 208, 34, 170, 33, 209, 32, 12, 31, 139, 30, 127, 29, 142, 28, 182, 27, 249, 26, 177, 25, 174, 24, 190, 23, 28, 22, 10, 21, 85, 20, 239, 19, 184, 18, 101, 17, 124, 16, 152, 15, 206, 14, 96, 13, 23, 12, 163, 11, 61, 10, 27, 9, 196, 8, 247, 7, 151, 6, 154, 5, 202, 4, 207, 3, 20, 2, 61, 1, 10, 0],
        58: [0, 58, 82, 57, 116, 56, 26, 55, 247, 54, 66, 53, 27, 52, 62, 51, 107, 50, 252, 49, 182, 48, 200, 47, 185, 46, 235, 45, 55, 44, 251, 43, 242, 42, 210, 41, 144, 40, 154, 39, 237, 38, 176, 37, 141, 36, 192, 35, 248, 34, 152, 33, 249, 32, 206, 31, 85, 30, 253, 29, 142, 28, 65, 27, 165, 26, 125, 25, 23, 24, 24, 23, 30, 22, 122, 21, 240, 20, 214, 19, 6, 18, 129, 17, 218, 16, 29, 15, 145, 14, 127, 13, 134, 12, 206, 11, 245, 10, 117, 9, 29, 8, 41, 7, 63, 6, 159, 5, 142, 4, 233, 3, 125, 2, 148, 1, 123, 0],
        60: [0, 60, 107, 59, 140, 58, 26, 57, 12, 56, 9, 55, 141, 54, 243, 53, 197, 52, 226, 51, 197, 50, 219, 49, 45, 48, 211, 47, 101, 46, 219, 45, 120, 44, 28, 43, 181, 42, 127, 41, 6, 40, 100, 39, 247, 38, 2, 37, 205, 36, 198, 35, 57, 34, 115, 33, 219, 32, 101, 31, 109, 30, 160, 29, 82, 28, 37, 27, 38, 26, 238, 25, 49, 24, 160, 23, 209, 22, 121, 21, 86, 20, 11, 19, 124, 18, 30, 17, 181, 16, 84, 15, 25, 14, 194, 13, 87, 12, 65, 11, 102, 10, 190, 9, 220, 8, 70, 7, 27, 6, 209, 5, 16, 4, 89, 3, 7, 2, 33, 1, 240, 0],
        62: [0, 62, 65, 61, 202, 60, 113, 59, 98, 58, 71, 57, 223, 56, 248, 55, 118, 54, 214, 53, 94, 52, 0, 51, 122, 50, 37, 49, 23, 48, 2, 47, 228, 46, 58, 45, 121, 44, 7, 43, 105, 42, 135, 41, 78, 40, 243, 39, 118, 38, 70, 37, 76, 36, 223, 35, 89, 34, 72, 33, 50, 32, 70, 31, 111, 30, 194, 29, 17, 28, 212, 27, 126, 26, 181, 25, 35, 24, 221, 23, 117, 22, 235, 21, 11, 20, 229, 19, 149, 18, 147, 17, 123, 16, 213, 15, 40, 14, 115, 13, 6, 12, 200, 11, 100, 10, 26, 9, 246, 8, 182, 7, 218, 6, 127, 5, 215, 4, 36, 3, 186, 2, 110, 1, 106, 0],
        64: [0, 64, 45, 63, 51, 62, 175, 61, 9, 60, 7, 59, 158, 58, 159, 57, 49, 56, 68, 55, 119, 54, 92, 53, 123, 52, 177, 51, 204, 50, 187, 49, 254, 48, 200, 47, 78, 46, 141, 45, 149, 44, 119, 43, 26, 42, 127, 41, 53, 40, 160, 39, 93, 38, 199, 37, 212, 36, 29, 35, 24, 34, 145, 33, 156, 32, 208, 31, 150, 30, 218, 29, 209, 28, 4, 27, 216, 26, 91, 25, 47, 24, 184, 23, 146, 22, 47, 21, 140, 20, 195, 19, 195, 18, 125, 17, 242, 16, 238, 15, 63, 14, 99, 13, 108, 12, 140, 11, 230, 10, 242, 9, 31, 8, 204, 7, 11, 6, 178, 5, 243, 4, 217, 3, 156, 2, 213, 1, 231, 0],
        66: [0, 66, 5, 65, 118, 64, 222, 63, 180, 62, 136, 61, 136, 60, 162, 59, 51, 58, 46, 57, 117, 56, 13, 55, 215, 54, 81, 53, 17, 52, 139, 51, 247, 50, 197, 49, 171, 48, 95, 47, 173, 46, 65, 45, 137, 44, 178, 43, 68, 42, 111, 41, 95, 40, 101, 39, 41, 38, 72, 37, 214, 36, 169, 35, 197, 34, 95, 33, 7, 32, 44, 31, 154, 30, 77, 29, 111, 28, 236, 27, 40, 26, 121, 25, 143, 24, 63, 23, 87, 22, 80, 21, 253, 20, 240, 19, 126, 18, 217, 17, 77, 16, 34, 15, 232, 14, 106, 13, 50, 12, 168, 11, 82, 10, 76, 9, 146, 8, 67, 7, 106, 6, 171, 5, 25, 4, 132, 3, 93, 2, 45, 1, 105, 0],
        68: [0, 68, 247, 67, 159, 66, 223, 65, 33, 64, 224, 63, 93, 62, 77, 61, 70, 60, 90, 59, 160, 58, 32, 57, 254, 56, 43, 55, 150, 54, 84, 53, 101, 52, 190, 51, 205, 50, 133, 49, 52, 48, 60, 47, 202, 46, 165, 45, 220, 44, 203, 43, 151, 42, 93, 41, 84, 40, 15, 39, 84, 38, 253, 37, 173, 36, 160, 35, 89, 34, 227, 33, 52, 32, 199, 31, 97, 30, 95, 29, 231, 28, 52, 27, 177, 26, 41, 25, 125, 24, 137, 23, 241, 22, 166, 21, 225, 20, 118, 19, 2, 18, 54, 17, 32, 16, 82, 15, 215, 14, 175, 13, 198, 12, 43, 11, 238, 10, 235, 9, 27, 8, 101, 7, 184, 6, 127, 5, 3, 4, 5, 3, 8, 2, 163, 1, 238, 0]
        }
    
    def __init__(self, symInf, binMess):
        self.infoSource = symInf
        self.binMessageSource = binMess
        self.messageWords = self.binStringToIntList(self.binMessageSource.binMessage)
        # FIXME: I hard coded the number of error correction words needed
        self.codewordCount = 10
        
        self.codewords = self.generateCodewords()
        self.binCodewords = self.intListToBinString(self.codewords)
        
    def generateCodewords(self):
        messageLen = len(self.messageWords)
        # set the message up for the operation by making firstTerm list
        firstTerm = []
        for word in self.messageWords:
            firstTerm.append(word)
            firstTerm.append(messageLen - 1)
            messageLen = messageLen - 1
    
        # multiply the firstTerm by the number of codewords needed
        for index in range(len(firstTerm)):
            if (index % 2):
                firstTerm[index] = firstTerm[index] + self.codewordCount
    
        # set up a counter for the correct number of divisions:
        divCount = len(self.messageWords)
    
        # loop:
        while divCount:
    
            # set up the polynomial to match the x powers of the message
            poly = list(self.polyDict[self.codewordCount])
            powerTest = firstTerm[1] - poly[1]
            if powerTest:
                for index in range(len(poly)):
                    if (index % 2):
                        poly[index] = poly[index] + powerTest    
    
            # perform division and XOR process to produce the codewords
            multicand = self.antiLogTable[firstTerm[0]]

            for index in range(len(poly)):
                if (index % 2 == 0):
                    power = multicand + poly[index]
                    if (power > 255):
                        power = power % 255
                    poly[index] = self.logTable[power]
    
            # time to XOR the result with the firstTerm
            for index in range(len(firstTerm)):
                if (index % 2 == 0):
                    if (index + 1 > len(poly)):
                        poly.append(firstTerm[index])
                        poly.append(firstTerm[index + 1])
                    else:
                        poly[index] = poly[index] ^ firstTerm[index]
    
            # get rid of any leading zeros from the list
            while (poly[0] == 0):
                poly.pop(0)
                poly.pop(0)
    
            # poly now becomes the first term and we start over by building a new poly
            firstTerm = list(poly)
    
    
            # decrement our function count
            divCount = divCount - 1
    
        codeWords = []
        for item in range(len(firstTerm)):
            if (item % 2 == 0):
                codeWords.append(firstTerm[item])
        logging.debug("%s:%s:codeWords: %s", self.__class__.__name__, sys._getframe().f_code.co_name, codeWords)
        return codeWords
    
    def binStringToIntList(self, inString):
        intList = []
        for i in range(len(inString) / 8):
            intList.append(int(inString[(i * 8):(i * 8) + 8], 2))
        logging.debug("%s:%s:intList: %s", self.__class__.__name__, sys._getframe().f_code.co_name, intList)
        return intList
    
    def intListToBinString(self, inList):
        binString = ''
        for i in inList:
            binString += self.binMessageSource.intToBinString(i, 8)
        return binString

class SymbolDict():
    def __init__(self, symInf, messageString, codewordString):
        # FIXME: messageString and codewordString may have to be passed differently to accommodate interleaved blocks
        self.infoSource = symInf
        
        self.taboo_dict = {}
        self.finder_dict = self.getFinderDict()
        self.taboo_dict.update(self.finder_dict)
        self.separator_dict = self.getSeparatorDict()
        self.taboo_dict.update(self.separator_dict)
        self.alignment_dict = self.getAlignmentDict()
        self.taboo_dict.update(self.alignment_dict)
        self.timing_dict = self.getTimingDict()
        self.taboo_dict.update(self.timing_dict)
        self.format_dict = self.getFormatDict()
        self.taboo_dict.update(self.format_dict)
        self.version_dict = self.getVersionDict()
        self.taboo_dict.update(self.version_dict)
        
        self.message_dict = self.getMessageDict(messageString + codewordString)
                
    def getFinderDict(self):
        finderDict = {}
    
        # create list of upper left pixels for each finder pattern
        finderOffset = self.infoSource.gridSize - 7
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
    
    def getSeparatorDict(self):
        separatorDict = {}
        size = self.infoSource.gridSize
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

    def getAlignmentDict(self):
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
        for centerX in alignmentLocs[self.infoSource.qrVersion]:
            for centerY in alignmentLocs [self.infoSource.qrVersion]:
                patternOutOfBounds = False
                curPattern = {}
                for x in range(centerX - 2, centerX + 3):
                    for y in range(centerY - 2, centerY + 3):
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
                        if ((x, y) in self.tabooDict.keys()):
                            patternOutOfBounds = True
    
                if not patternOutOfBounds:
                    alignmentDict.update(curPattern)
    
        return alignmentDict
    
    def getTimingDict(self):
        timingDict = {}
        for i in range(8, self.infoSource.gridSize - 8):
            if (i % 2): pixel = 0
            else: pixel = 1
            if ((6, i) not in self.taboo_dict.keys()):
                timingDict[6, i] = pixel
            if ((i, 6) not in self.taboo_dict.keys()):
                timingDict[i, 6] = pixel
        return timingDict
    
    def getFormatDict(self, formattingString=None):
        # Takes a binary string as an optional formatting argument
        # because formatting won't be known until symbol is built and best mask is chosen
    
        '''
        8,0 through 8,5
        8,7 through 8,8
        7,8
        5,8 throuhg 0,8
    
    
        size-1,8 through size-8,8
        8,size-8 is dark
        8,size-7 through 8,size-1
        '''
        size = self.infoSource.gridSize
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
    
    def getVersionDict(self, versionString=None):
        versionDict = {}
    
        # only version 7 and up have version blocks
        if (self.infoSource.qrVersion < 7):
            return versionDict
    
        '''
        3x6 area starting at 0,size-11
        6x3 area starting at size-11,0
        '''
        size = self.infoSource.gridSize
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

    def getMessageDict(self, messageString):
        # use column index based on mod 2 for ever other row
        # start on bottom row
        # use direction indicator for up or down
    
        size = self.infoSource.gridSize
        dataIndex = 0
        symbolDict = {}
        y = size - 1
        direction = -1  # -1 for up, 1 for down
    
        # give me a descending list of every other column index:
        decCols = range(size - 2, -1, -2)
        # fix that list to account for the vertical timing in column 6:
        decCols[-1] -= 1
        decCols[-2] -= 1
        decCols[-3] -= 1
    
        for x in decCols:
            while(size > y > -1):
                if ((x + 1, y) not in self.taboo_dict.keys()):
                    symbolDict[(x + 1, y)] = int(messageString[dataIndex])
                    dataIndex += 1
                    if (dataIndex >= len(messageString)):
                        return symbolDict
    
                if ((x, y) not in self.taboo_dict.keys()):
                    symbolDict[(x, y)] = int(messageString[dataIndex])
                    dataIndex += 1
                    if (dataIndex >= len(messageString)):
                        return symbolDict
    
                y += direction
    
            direction *= -1  # multiply direction by -1 to flip between 1 and -1
            y += direction

    def getFormatting(self, maskType):
        #NOTE: I've always considered error levels to come in this order:
        #        L,M,Q,H. But their binary representaiton is:
        #        'L':'01', 'M':'00', 'Q':'11', 'H':'10'
        #    I will account for that here:
        errorLevelKey = ('01','00','11','10')
        errAndMaskString = errorLevelKey[self.infoSource.errLevel] + self.intToBinString(maskType, 3)
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
    
        formatString = self.intToBinString(fbin, 15)
    
        return formatString

    def intToBinString(self, num, digitLength):
        # converts an integer to an eight bit binary number returned as a string
        # the ord() function can be used to convert a char to its int value
        return '0' * (digitLength - len(bin(num)[2:])) + bin(num)[2:]
    
class SymbolGenerator():
    def __init__(self, symInf, binMess, errCw, symDict):
        self.infoSource = symInf
        self.binMessageSource = binMess
        self.errorCodewordSource = errCw
        self.symbolDictSource = symDict
        
        # generate a list of 0 representing the QR symbol
        self.qr_grid = self.getEmptyGrid()
        # fill the newly generated code
        self.qr_grid = self.fillListFromDict(self.qr_grid, self.symbolDictSource.taboo_dict)
        self.qr_grid = self.fillListFromDict(self.qr_grid, self.symbolDictSource.message_dict)
        
        masked = MaskSymbol(self.symbolDictSource.taboo_dict,self.qr_grid)
        self.masked_qr_grid = masked.masked_grid
        
        #Get format information (this should be fun to figure out)
        format_dict = self.symbolDictSource.getFormatDict(self.symbolDictSource.getFormatting(masked.best_mask))
        self.masked_qr_grid = self.fillListFromDict(self.masked_qr_grid, format_dict)
        
        self.genQrImage(self.masked_qr_grid)
   
    def getEmptyGrid(self):
        size = self.infoSource.gridSize
        grid = [[0] * size for _ in range(size)]
        return grid
        
    def fillListFromDict(self, theList, theDict):
        for key in theDict.keys():
            theList[key[1]][key[0]] = theDict[key]
        return theList
    
    def genQrImage(self, qrData):
    
        #FIXME: These settings probably shouldn't be hardcoded
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
    
    
class MaskSymbol():
    def __init__(self, tabooDict, theList):
        self.taboo_dict = tabooDict
        self.data_list = theList
        
        #FIXME: This class should test out ever mask and find the best one. Right now it's just hardcoded here
        self.best_mask = 0
    
        self.masked_grid = self.applyMask(self.data_list, self.taboo_dict, self.best_mask)
        
    def applyMask(self, qrList, tabooDict, maskVersion):
        maskedList = list(qrList)
        for x in range(len(maskedList[0])):
            for y in range(len(maskedList)):
                if ((x, y) not in tabooDict.keys()):
                    maskedList[y][x] = self.calcMask(maskVersion, x, y, maskedList[y][x])
        return maskedList
    
    def calcMask(self, mask, x, y, value):
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
