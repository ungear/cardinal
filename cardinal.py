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
            start_data_grid(decoding_result, password)
    else:
        create_answer = input('Base not found. Create? y/n ')
        if create_answer == 'y':
            password_first = getpass.getpass("Set the password: ")
            password_second = getpass.getpass("Repeat the password: ")
            if password_first == password_second:
                new_password_base = []
                encode_and_save_data(new_password_base, password_first)
                start_data_grid(new_password_base, password_first)
            else:
                print("Passwords are different")
        else:
            print("Bye")

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

def encode_and_save_data(data_list, password):
    """ Encodes passed data and saves it"""
    with open(PASSWORD_BASE_PATH, 'wb') as data_file:
        stringified_data = json.dumps(data_list)
        encoded_data_string = aes.encode(password, stringified_data)
        encoded_data_bytes = encoded_data_string.encode()
        data_file.write(encoded_data_bytes)


def start_data_grid(data_list, password):
    """Represents data to the user and deals with changes"""
    exit_loop = False
    while not exit_loop:
        row_template = "| {0: <2} | {1: <18} | {2: <18} | {3: <18} |"
        horizontal_rule_template = "|{0:-<4}|{0:-<20}|{0:-<20}|{0:-<20}|"
        header = row_template.format("Id","Title", "Login", "Password")
        hor_break = horizontal_rule_template.format("")
        rows = [header, hor_break]
        for entry in data_list:
            row = row_template.format(entry['id'], entry['title'], entry['login'], entry['password'])
            rows.append(row)
        rows.append(hor_break)
        for row in rows:
            print(row)

        operation = input("\nc - create / d - delete / q - quit\n")
        if operation == 'c':
            entry_title = input("Title: ")
            entry_login = input("Login: ")
            entry_password = getpass.getpass("Password: ")
            new_entry = {
                'id': len(data_list) + 1,
                'title': entry_title, 
                'login': entry_login, 
                'password': entry_password}
            data_list.append(new_entry)
            encode_and_save_data(data_list, password)
        if operation == 'd':
            entry_id_to_delete = int(input("Id of the entry you want to delete: "))
            entries_found_by_id = [x for x in data_list if x['id'] == entry_id_to_delete]
            if(any(entries_found_by_id)):
                data_list.remove(entries_found_by_id[0])
            else:
                print('Wrong id')
        elif operation == 'q':
            exit_loop = True



if __name__ == "__main__":
    main()
