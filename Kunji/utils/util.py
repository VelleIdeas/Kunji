import random


def generatePassword():
    #minimum 8 character long with atleast One UpperCase Character,
    # 1 LowerCase Character and 1 digit.
    password = ''
    password = password + ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 6))
    password = password + ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 1))
    password = password + ''.join(random.sample('1234567890', 1))
    return password
