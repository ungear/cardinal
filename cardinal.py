import aes
import getpass
import json
import os.path

def main():
    print('Cardinal Password Manager')
    if(os.path.isfile('data.txt')):
        password = getpass.getpass("Password: ")
        decodingResult = decodePasswordBase(password)
        if(decodingResult == 0):
            print("Wrong password")
        elif(isinstance(decodingResult, list)):
            print(decodingResult)
    else:
        print('base not found')
        # create password base then work with it
        # print ("I/O error({0}): {1}".format(err.errno, err.strerror))    

# Tries to decode the password base usind passed master password.
# Returns 0 if decoding failed, otherwise returns decoded data
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