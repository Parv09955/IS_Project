import qrcode

def create_blank_matrix(rows, columns):
    matrix = []
    for i in range(rows):
        row = [" "] * columns
        matrix.append(row)
    return matrix

def create_letter_matrix(rows, columns, plain_txt):
    n = len(plain_txt)
    matrix = create_blank_matrix(rows, columns)
    count = 0
    for i in range(columns):
        for j in range(rows):
            if count >= n:
                matrix[j][i] = "X"
            else:
                matrix[j][i] = plain_txt[count]
            count += 1
    return matrix

def columnar_transposition(plain_txt):
    cipher_txt = ""
    a = len(plain_txt)
    rows = a//5
    if a%5 != 0:
        rows += 1

    mtx = create_letter_matrix(rows,5,plain_txt)

    for i in range(rows):
        for j in range(5):
            cipher_txt += mtx[i][j]

    return cipher_txt

def qr_generator(plain_txt, filename, password):
    text = columnar_transposition(plain_txt)
    text = password + text
    if filename[-4:] != ".png":
        filename = filename + ".png"

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_M,
        border = 4,
        box_size = 10,
    )
    qr.add_data(text)
    qr.make(fit = True)

    img = qr.make_image(fill_color = "black", back_color = "white")
    img.save(filename)
    print("\nQR Code Generated Successfully.")
    print(f"QR Code Saved As {filename}")

print("23BIT055 - 23BIT056")
print("Password Protected & Encrypted QR Code Generator")
txt = input("Enter Message: ")
fname = input("Enter Filename to save QR Code: ")
password = input("Enter Password (6 Digits): ")
qr_generator(txt, fname, password)