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
        
        logging.debug("%s:%s:inMessage: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.inMessage)
        logging.debug("%s:%s:charSet: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.charSet)
        logging.debug("%s:%s:qrVersion: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.qrVersion)
        logging.debug("%s:%s:errLevel: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.errLevel)
        logging.debug("%s:%s:dataCodewords: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.dataCodewords)
        logging.debug("%s:%s:dataBits: %s", self.__class__.__name__, sys._getframe().f_code.co_name, self.dataBits)

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
    pass
