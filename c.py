import aes
import json

# write testdata to file
PASSWORD = '1234567890abcdef'
sourceData = {'id': 1, 'name':'ivan'}

stringifiedData = json.dumps(sourceData)
encodedStrData = aes.encode(PASSWORD, stringifiedData)
encodedBytes = encodedStrData.encode()
print([x for x in encodedStrData])
#print(encodedBytes)


with open('data.txt', 'wb') as file:
    file.write(encodedBytes)


with open('data.txt', 'rb') as file:
    rawBytes = file.read()
    rawEncodedStr = rawBytes.decode()
    decodedStrData = aes.decode(PASSWORD, rawEncodedStr)
    print(decodedStrData)
    data = json.loads(decodedStrData)
    print(data)

