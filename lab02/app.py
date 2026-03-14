from flask import Flask, render_template, request

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= CAESAR =================
@app.route("/caesar", methods=["GET", "POST"])
def caesar():

    result = None

    if request.method == "POST":

        cipher = CaesarCipher()

        if "encrypt" in request.form:
            text = request.form["inputPlainText"]
            key = int(request.form["inputKeyPlain"])

            result = cipher.encrypt_text(text, key)

        elif "decrypt" in request.form:
            text = request.form["inputCipherText"]
            key = int(request.form["inputKeyCipher"])

            result = cipher.decrypt_text(text, key)

    return render_template("caesar.html", result=result)


# ================= VIGENERE =================
@app.route("/vigenere", methods=["GET", "POST"])
def vigenere():

    result = None

    if request.method == "POST":

        cipher = VigenereCipher()

        if "encrypt" in request.form:

            text = request.form["inputPlainText"]
            key = request.form["inputKeyPlain"]

            text = ''.join(filter(str.isalpha, text))
            key = ''.join(filter(str.isalpha, key))

            result = cipher.vigenere_encrypt(text, key)

        elif "decrypt" in request.form:

            text = request.form["inputCipherText"]
            key = request.form["inputKeyCipher"]

            text = ''.join(filter(str.isalpha, text))
            key = ''.join(filter(str.isalpha, key))

            result = cipher.vigenere_decrypt(text, key)

    return render_template("vigenere.html", result=result)


# ================= RAILFENCE =================
@app.route("/railfence", methods=["GET", "POST"])
def railfence():

    result = None

    if request.method == "POST":

        cipher = RailFenceCipher()

        if "encrypt" in request.form:

            text = request.form["inputPlainText"]
            key = int(request.form["inputKeyPlain"])

            result = cipher.rail_fence_encrypt(text, key)

        elif "decrypt" in request.form:

            text = request.form["inputCipherText"]
            key = int(request.form["inputKeyCipher"])

            result = cipher.rail_fence_decrypt(text, key)

    return render_template("railfence.html", result=result)


# ================= PLAYFAIR =================
@app.route("/playfair", methods=["GET", "POST"])
def playfair():

    result = None
    matrix = None

    cipher = PlayFairCipher()

    if request.method == "POST":

        # CREATE MATRIX
        if "create_matrix" in request.form:

            key = request.form.get("inputKeyPlain", "")
            key = ''.join(filter(str.isalpha, key)).upper()

            matrix = cipher.create_playfair_matrix(key)

        # ENCRYPT
        elif "encrypt" in request.form:

            text = request.form["inputPlainText"]
            key = request.form["inputKeyPlain"]

            text = ''.join(filter(str.isalpha, text)).upper()
            key = ''.join(filter(str.isalpha, key)).upper()

            matrix_temp = cipher.create_playfair_matrix(key)

            result = cipher.playfair_encrypt(text, matrix_temp)

        # DECRYPT
        elif "decrypt" in request.form:

            text = request.form["inputCipherText"]
            key = request.form["inputKeyCipher"]

            text = ''.join(filter(str.isalpha, text)).upper()
            key = ''.join(filter(str.isalpha, key)).upper()

            matrix_temp = cipher.create_playfair_matrix(key)

            result = cipher.playfair_decrypt(text, matrix_temp)

    return render_template("playfair.html", result=result, matrix=matrix)


# ================= TRANSPOSITION =================
@app.route("/transposition", methods=["GET", "POST"])
def transposition():

    result = None

    if request.method == "POST":

        cipher = TranspositionCipher()

        if "encrypt" in request.form:

            text = request.form["inputPlainText"]
            key = int(request.form["inputKeyPlain"])

            result = cipher.encrypt(text, key)

        elif "decrypt" in request.form:

            text = request.form["inputCipherText"]
            key = int(request.form["inputKeyCipher"])

            result = cipher.decrypt(text, key)

    return render_template("transposition.html", result=result)


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)