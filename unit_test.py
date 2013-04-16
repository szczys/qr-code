from qrSymbolCapacity import BinaryMessage, SymbolInfo, ErrorCodewords, \
    SymbolDict, SymbolGenerator
import unittest

class TestQr(unittest.TestCase):
    
    def testNumeric(self):
        '''
        symInf = SymbolInfo('01234567',1,1)
        binary_message = BinaryMessage(symInf)
        expectedString = '00010000001000000000110001010110011000011000000011101100000100011110110000010001111011000001000111101100000100011110110000010001'
        self.assertEqual(binary_message.binMessage, expectedString, "Binary version doesn't match text message input")

        
        error_correction = ErrorCodewords(symInf,binary_message)
        expectedMessageList = [16, 32, 12, 86, 97, 128, 236, 17, 236, 17, 236, 17, 236, 17, 236, 17]
        self.assertEqual(error_correction.messageWords,expectedMessageList,"Messageword list is wrong")
        expectedCodeList = [165, 36, 212, 193, 237, 54, 199, 135, 44, 85]
        self.assertEqual(error_correction.codewords,expectedCodeList,"Codeword list is wrong")
        expectedBinCodeString = '10100101001001001101010011000001111011010011011011000111100001110010110001010101'
        self.assertEqual(error_correction.binCodewords,expectedBinCodeString,"BinCodeString wrong")
        
        symbol_dict = SymbolDict(symInf,binary_message.binMessage,error_correction.binCodewords)
        
        symbol_generator = SymbolGenerator(symInf, binary_message, error_correction, symbol_dict)
        '''
        
        
        symInf = SymbolInfo('Hello World!')
        #symInf = SymbolInfo("Hello World! This is working great!")
        binary_message = BinaryMessage(symInf)      
        error_codewords = ErrorCodewords(symInf,binary_message)
        # expectedInt = 13
        # self.assertEqual(error_codewords.codewordCount, expectedInt)
        symbol_dict = SymbolDict(symInf, binary_message.binMessage, error_codewords.binCodewords)
        SymbolGenerator(symInf, binary_message, error_codewords, symbol_dict)
        