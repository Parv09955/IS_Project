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

def password_checker(text, password):
    p = text[:6]
    p = p[3] + p[1] + p[5] + p[2] + p[0] + p[4]
    if p == password:
        return True
    else:
        return False

def create_blank_matrix(rows, columns):
    matrix = []
    for i in range(rows):
        row = [" "] * columns
        matrix.append(row)
    return matrix

def create_letter_matrix(rows, columns, cipher_txt):
    n = len(cipher_txt)
    matrix = create_blank_matrix(rows, columns)
    count = 0
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = cipher_txt[count]
            count += 1
    return matrix

def columnar_decryption(cipher_txt):
    plain_txt = ""
    cipher_txt = cipher_txt[6:]
    a = len(cipher_txt)
    rows = a//5
    if a%5 != 0:
        rows += 1
    mtx = create_letter_matrix(rows, 5, cipher_txt)

    for i in range(5):
        for j in range(rows):
            plain_txt = plain_txt + mtx[j][i]

    while True:
        if plain_txt[-1] == "X":
            plain_txt = plain_txt[:-1]
        else:
            break

    return plain_txt

def main(filename, password):
    cipher_txt = decode_qr(filename)
    if len(password) == 6:
        if password_checker(cipher_txt, password):
            plain_txt = columnar_decryption(cipher_txt)
            print("\nMessage: ", plain_txt)
        else:
            print("Invalid Password")
    else:
        print("Invalid Password")

print("23BIT055 - 23BIT056")
print("QR Decryptor with Password Protection")
fname = input("Enter QR Code Filename: ")
password = input("Enter Password: ")
main(fname, password)