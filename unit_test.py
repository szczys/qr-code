from qrSymbolCapacity import BinaryMessage, SymbolInfo
import unittest

class TestQr(unittest.TestCase):
    
    def testNumeric(self):
        symInf = SymbolInfo('01234567',1,1)
        binary_message = BinaryMessage(symInf)
        expectedString = '00010000001000000000110001010110011000011000000011101100000100011110110000010001111011000001000111101100000100011110110000010001'
        self.assertEqual(binary_message.binMessage, expectedString, "Binary version doesn't match text message input")

        symInf = SymbolInfo('HELLO WORLD')
        binary_message = BinaryMessage(symInf)
        expectedString = '00100000010110110000101101111000110100010111001011011100010011010100001101000000111011000001000111101100'
        self.assertEqual(binary_message.binMessage, expectedString, "Message mismatch")
        
