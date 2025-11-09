import qrcode

def create_blank_matrix(rows, columns):
    matrix = []
    for i in range(rows):
        row = [" "] * columns
        matrix.append(row)
    return matrix

def create_letter_matrix(rows, columns, text):
    n = len(text)
    matrix = create_blank_matrix(rows, columns)
    count = 0
    for i in range(rows):
        for j in range(columns):
            if count >= n:
                matrix[i][j] = "~"
            else:
                matrix[i][j] = text[count]
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

def columnar_transposition(plain_txt, key):
    cipher_txt = ""
    a = len(plain_txt)
    columns = 4
    rows = a//columns
    if a%columns != 0:
        rows += 1
    matrix = create_letter_matrix(rows,columns,plain_txt)

    for i in key:
        for j in range(rows):
            cipher_txt += matrix[j][i]

    return cipher_txt

def qr_generator(plain_txt, filename, password):
    if len(password) == 8:
        key1 = password[0:4]
        key2 = password[4:8]
        text = password + plain_txt
        key1 = key_generator(key1)
        key2 = key_generator(key2)
        encrypted_text = columnar_transposition(text, key1)
        encrypted_text = columnar_transposition(encrypted_text, key2)
        if filename[-4:] != ".png":
            filename = filename + ".png"

        qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_M,
            border = 4,
            box_size = 10,
        )
        qr.add_data(encrypted_text)
        qr.make(fit = True)

        img = qr.make_image(fill_color = "black", back_color = "white")
        img.save(filename)
        print("\nQR Code Generated Successfully.")
        print(f"QR Code Saved As {filename}")
    else:
        print("Password Length Error.")

print("23BIT055 - 23BIT056 - 23BIT057")
print("Password Protected & Encrypted QR Code Generator")
txt = input("Enter Message: ")
fname = input("Enter Filename to save QR Code: ")
password = input("Enter Password (8 Digits): ")
qr_generator(txt, fname, password)