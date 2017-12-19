import aes
import json

# write testdata to file
PASSWORD = 'asd'
sourceData = [
    {'title': 'entry1', 'login': 'somelogin', 'password':'qwerty'},
    {'title': 'entry2', 'login': 'Rudolf66', 'password':'letmein'},
]

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

