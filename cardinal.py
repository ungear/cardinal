import os.path
import getpass
import json
import aes

PASSWORD_BASE_FILENAME = 'data'
PASSWORD_BASE_PATH = os.path.join(os.getcwd(), PASSWORD_BASE_FILENAME)

def main():
    print('Cardinal Password Manager')
    if os.path.isfile(PASSWORD_BASE_PATH):
        password = getpass.getpass("Password: ")
        decoding_result = decode_password_base(password)
        if decoding_result == 0:
            print("Wrong password")
        elif isinstance(decoding_result, list):
            start_data_grid(decoding_result)
    else:
        print('base not found')
        # create password base then work with it
        # print ("I/O error({0}): {1}".format(err.errno, err.strerror))

def decode_password_base(master_password):
    """
    Tries to decode the password base using passed master password
    Returns 0 if decoding failed, otherwise returns decoded data
    """
    with open(PASSWORD_BASE_PATH, 'rb+') as data_file:
        encoded_data_bytes = data_file.read()
        encoded_data_str = encoded_data_bytes.decode()
        decoded_data_str = aes.decode(master_password, encoded_data_str)
        try:
            data = json.loads(decoded_data_str)
            return data
        except json.decoder.JSONDecodeError:
            return 0

def start_data_grid(data_list):
    """Represents data to the user and deals with changes"""
    row_template = "| {0: <20} | {1: <20} | {2: <20} |"
    header = row_template.format("Title", "Login", "Password")
    rows = [header]
    for entry in data_list:
        row = row_template.format(entry['title'], entry['login'], '***')
        rows.append(row)

    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
