#!/bin/python3

import pickle
import string
import secrets
from cryptography.fernet import Fernet


positive_array = ['y', 'yes', 's', 'sim', 'true', '1']
negative_array = ['no', 'nao', 'n', 'false', '0']
final_dict = {}
website_list = final_dict.keys()
user_pass_list = []

def create_key(filename):
    key = Fernet.generate_key()
    with open(filename, 'wb') as file:
        file.write(key)
    return key

def load_key(filename):
    with open(filename, 'rb') as file:
        key = file.read()
        return key

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return bytes(random_string, 'ascii')

def load_file(filename):
    try:
        with open(filename, 'rb') as file:
            data_dict = pickle.load(file)
        return data_dict
    except FileNotFoundError:
        return {}

def save_to_file(data_dict, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data_dict, file)

def new_user_protocol(website, key):
    print('Website not found!')
    while True:
            
        username = bytes(input('State Your Username: '), 'ascii')
        create_password = str(input('Do you wish to automaticaly generate a new password?:(y/n) '))

        # working as intended, The problem is in the encryption's encoding(?)
        if create_password in positive_array:
            password = generate_random_string(16)
            break
            
        elif create_password in negative_array:
            password = bytes(input('Enter Password: '), 'ascii')
            break

        else: 
            print('Please answer "yes" or "no"')

    encrypted_user_data = Fernet(key).encrypt(username + b":" + password)
   
    return encrypted_user_data

def known_user_protocol(website, key):

    return None





if __name__ == '__main__':
    key = load_key('key.txt')
    data_dict = load_file('passwords.txt')
    website = 'example.com'
    data = new_user_protocol(website, key)
    data_dict[website] = data

    save_to_file(data_dict, 'passwords.txt')
    print(load_file('passwords.txt'))
    for value in data_dict.values():
        Fernet(key).decrypt(value)
        print()

