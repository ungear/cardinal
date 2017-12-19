import aes
import unittest

TEST_MESSAGE_BLOCK = [0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f, 0x70]
TEST_KEY_BYTES = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

class TestKeyExpansion(unittest.TestCase):
    def testKeyScheduleLastKey(self):
        keySchedule = aes.keyExpansion(TEST_KEY_BYTES)
        lastKey = keySchedule[len(keySchedule)-1]
        self.assertEqual(lastKey, 0xb6630ca6)

    def testKeyScheduleLength(self):
        keySchedule = aes.keyExpansion(TEST_KEY_BYTES)
        self.assertEqual(len(keySchedule), 44)

    def testKeyScheduleException(self):
        with self.assertRaises(ValueError):
            aes.keyExpansion(TEST_KEY_BYTES[:10:])

class TestCreateWord(unittest.TestCase):
    def testWord(self):
        self.assertEqual(aes.createWord(0xa1, 0x11, 0x3b, 0x59), 0xa1113b59)

class TestRotWord(unittest.TestCase):
    def testWord(self):
        self.assertEqual(aes.rotWord(0xa13c3b59), 0x3c3b59a1)

class TestSubWord(unittest.TestCase):
    def testWord(self):
        self.assertEqual(aes.subWord(0xa13c3b59), 0x32ebe2cb)

class TestCreateState(unittest.TestCase):
    def testState(self):
        state = aes.createState(TEST_MESSAGE_BLOCK)
        expectedState = [
            TEST_MESSAGE_BLOCK[0::4],
            TEST_MESSAGE_BLOCK[1::4],
            TEST_MESSAGE_BLOCK[2::4],
            TEST_MESSAGE_BLOCK[3::4],
        ]
        self.assertEqual(state, expectedState)

class TestSubBytes(unittest.TestCase):
    def testSubBytes(self):
        state = aes.createState(TEST_MESSAGE_BLOCK)
        expectedBytes = [0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51]
        expectedMutatedState = aes.createState(expectedBytes)
        aes.subBytes(state)
        self.assertEqual(state, expectedMutatedState)

class TestInvSubBytes(unittest.TestCase):
    def testSubBytes(self):
        state = aes.createState(TEST_MESSAGE_BLOCK)
        expectedBytes = [0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0]
        expectedMutatedState = aes.createState(expectedBytes)
        aes.invSubBytes(state)
        self.assertEqual(state, expectedMutatedState)

class TestShiftRows(unittest.TestCase):
    def testShiftRows(self):
        state = aes.createState(TEST_MESSAGE_BLOCK)     
        expectedBytes = [0x61, 0x66, 0x6b, 0x70, 0x65, 0x6a, 0x6f, 0x64, 0x69, 0x6e, 0x63, 0x68, 0x6d, 0x62, 0x67, 0x6c]
        expectedState = aes.createState(expectedBytes)
        aes.shiftRows(state)
        self.assertEqual(state, expectedState)

class TestInvShiftRows(unittest.TestCase):
    def testInvShiftRows(self):
        state = aes.createState(TEST_MESSAGE_BLOCK)
        expectedBytes = [0x61, 0x6e, 0x6b, 0x68, 0x65, 0x62, 0x6f, 0x6c, 0x69, 0x66, 0x63, 0x70, 0x6d, 0x6a, 0x67, 0x64]
        expectedState = aes.createState(expectedBytes)
        aes.invShiftRows(state)
        self.assertEqual(state, expectedState)

class TestMixColumns(unittest.TestCase):
    def testMixColumns(self):
        originalBytes = [0xd4, 0xbf, 0x5d, 0x30, 0xe0, 0xb4, 0x52, 0xae, 0xb8, 0x41, 0x11, 0xf1, 0x1e, 0x27, 0x98, 0xe5]
        expectedBytes = [0x04, 0x66, 0x81, 0xe5, 0xe0, 0xcb, 0x19, 0x9a, 0x48, 0xf8, 0xd3, 0x7a, 0x28, 0x06, 0x26, 0x4c]
        state = aes.createState(originalBytes)     
        expectedState = aes.createState(expectedBytes)
        aes.mixColumns(state)
        self.assertEqual(state, expectedState)

class TestInvMixColumns(unittest.TestCase):
    def testInvMixColumns(self):
        originalBytes = [0x04, 0x66, 0x81, 0xe5, 0xe0, 0xcb, 0x19, 0x9a, 0x48, 0xf8, 0xd3, 0x7a, 0x28, 0x06, 0x26, 0x4c]
        expectedBytes = [0xd4, 0xbf, 0x5d, 0x30, 0xe0, 0xb4, 0x52, 0xae, 0xb8, 0x41, 0x11, 0xf1, 0x1e, 0x27, 0x98, 0xe5]
        state = aes.createState(originalBytes)     
        expectedState = aes.createState(expectedBytes)
        aes.invMixColumns(state)
        self.assertEqual(state, expectedState)

class TestCipher(unittest.TestCase):
    def testCipher(self):
        inputBytes = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
        exampleCypherKeyBytes = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]
        expectedResultBytes = [0x39, 0x25, 0x84, 0x1d, 0x02, 0xdc, 0x09, 0xfb, 0xdc, 0x11, 0x85, 0x97, 0x19, 0x6a, 0x0b, 0x32]
        
        inputState = aes.createState(inputBytes)
        expectedState = aes.createState(expectedResultBytes)
        keySchedule = aes.keyExpansion(exampleCypherKeyBytes)

        result = aes.cipher(inputState, keySchedule)
        self.assertEqual(result, expectedState)

    def testCipher2(self):
        inputBytes = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
        exampleCypherKeyBytes = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
        expectedResultBytes = [0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30, 0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a]
        
        inputState = aes.createState(inputBytes)
        expectedState = aes.createState(expectedResultBytes)
        keySchedule = aes.keyExpansion(exampleCypherKeyBytes)

        result = aes.cipher(inputState, keySchedule)
        self.assertEqual(result, expectedState)

class TestInvCipher(unittest.TestCase):
    def testInvCipher(self):
        inputBytes = [0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30, 0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a]
        exampleCypherKeyBytes = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]
        expectedResultBytes = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff]
        
        inputState = aes.createState(inputBytes)
        expectedState = aes.createState(expectedResultBytes)
        keySchedule = aes.keyExpansion(exampleCypherKeyBytes)

        result = aes.invCipher(inputState, keySchedule)
        self.assertEqual(result, expectedState)

class TestTheWholeProcess(unittest.TestCase):
    def testEncriptDecript(self):
        plainText = 'idjpi23j023uc0j1-0i-soxl=kixq[wkz=21ks[qqwdqwd'
        password = 'dke8qpend'
        encodedText = aes.encode(password, plainText)
        decodedText = aes.decode(password, encodedText)

        self.assertEqual(decodedText, plainText)

class TestGetPasswordHash(unittest.TestCase):
    def testHashLength(self):
        password7 = '1234567'
        password20 = '0123456789abcdef0123'
        hash7 = aes.getPasswordHash(password7)
        hash20 = aes.getPasswordHash(password20)
        self.assertEqual(len(hash7), 16)
        self.assertEqual(len(hash20), 16)

if __name__ == '__main__':
    unittest.main()
