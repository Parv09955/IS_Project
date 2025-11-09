from PIL import Image
from pyzbar.pyzbar import decode

def decode_qr(filename):
    if filename[-4:] != ".png":
        filename = filename + ".png"
    img = Image.open(filename)
    decoded_text = decode(img)

    if decoded_text:
        for obj in decoded_text:
            text = obj.data.decode("utf-8")
    else:
        print("No QR Code detected")

    return text

def create_blank_matrix(rows, columns):
    matrix = []
    for i in range(rows):
        row = [" "] * columns
        matrix.append(row)
    return matrix

def create_letter_matrix(rows, columns, text, key):
    n = len(text)
    matrix = create_blank_matrix(rows, columns)
    count = 0
    for i in key:
        for j in range(rows):
            matrix[j][i] = text[count]
            count += 1
    return matrix

def key_generator(key):
    key_list = list(key)
    for i in range(4):
        key_list[i] = ord(key_list[i])
    key_sorted = sorted(key_list)
    reduced_key = key_list
    for i in range(4):
        if key_sorted[i] in key_list:
            reduced_key[key_list.index(key_sorted[i])] = i

    return reduced_key

def check_password(plain_txt,entered_password):
    password = plain_txt[0:8]
    if password == entered_password:
        return True
    else:
        return False

def columnar_decryption(cipher_txt, key):
    plain_txt = ""
    a = len(cipher_txt)
    columns = 4
    rows = a//columns
    if a%columns != 0:
        rows += 1
    matrix = create_letter_matrix(rows, columns, cipher_txt, key)

    for i in range(rows):
        for j in range(columns):
            plain_txt += matrix[i][j]
    return plain_txt

def main(filename, password):
    cipher_txt = decode_qr(filename)
    key1 = password[0:4]
    key2 = password[4:8]
    key1 = key_generator(key1)
    key2 = key_generator(key2)
    plain_txt = columnar_decryption(cipher_txt, key2)
    plain_txt = columnar_decryption(plain_txt, key1)
    while True:
        if plain_txt[-1] == "~":
            plain_txt = plain_txt[:-1]
        else:
            break
    if len(password) == 8:
        if check_password(plain_txt, password):
            print("Message: " + plain_txt[8:])
        else:
            print("Incorrect Password!!!")
    else:
        print("Invalid Password Length!!!")

print("23BIT055 - 23BIT056 - 23BIT057")
print("QR Decryptor with Password Protection")
fname = input("Enter QR Code Filename: ")
password = input("Enter Password: ")
main(fname, password)