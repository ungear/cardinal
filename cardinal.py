import aes
import getpass
import json
import os.path

def main():
    print('Cardinal Password Manager')
    if(os.path.isfile('data.txt')):
        # password = getpass.getpass("Password: ")
        decodingResult = decodePasswordBase('1234567890abcdef')
        if(decodingResult == 0):
            print("Wrong password")
        elif(isinstance(decodingResult, dict)):
            print(decodingResult)
    else:
        print('base not found')
        # create password base then work with it
        # print ("I/O error({0}): {1}".format(err.errno, err.strerror))    

def decodePasswordBase(masterPassword):
    with open('data.txt', 'rb+') as dataFile:
        encodedDataBytes = dataFile.read()
        encodedDataStr = encodedDataBytes.decode()
        decodedDataStr = aes.decode(masterPassword, encodedDataStr)
        try:
            passwdData = json.loads(decodedDataStr)
            return passwdData
        except json.decoder.JSONDecodeError as err:
            return 0
            

if __name__ == "__main__":
    main()


'''
exampleInputBytes = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
exampleCypherKeyBytes = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]

exampleText = ''
exampleCypherKey = ''
for charCode in exampleInputBytes:
    exampleText += chr(charCode)

for charCode in exampleCypherKeyBytes:
    exampleCypherKey += chr(charCode)
print(exampleText, ' * ', exampleCypherKey)
t = aes.encode(exampleCypherKey, exampleText)

print(t)

inputBytes = [0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30, 0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a] 
exampleCypherKeyBytes = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f]

exampleText = "".join([chr(x) for x in inputBytes])
exampleCypherKey = "".join([chr(x) for x in exampleCypherKeyBytes])
r = aes.decode(exampleCypherKey, exampleText)

aes.printState(r)

# result = []
# for rowIndex in range(len(y)):
#     for colIndex in range(len(y[rowIndex])):
#         result.append(hex(y[rowIndex][colIndex]))

# inputText = 'abcdef0123456789-*-*-*-*-*-*-*-*'
inputText = 'abcdef012345678acascacas das ascaasas a as as '
passwd = '1234567890abcdef'

test = True
for x in range(1000):
    encodedText = aes.encode(passwd, inputText)
    decodedText = aes.decode(passwd, encodedText)
    result = decodedText == inputText
    test = test and result
# print(encodedText)
print(test)
'''
