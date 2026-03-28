from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import struct

# Create server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# Connected clients
clients = []


def recv_full(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + cipher_text

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    cipher_text = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return decrypted_message.decode()

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")

    # Send server's public key
    client_socket.send(server_key.publickey().export_key(format='PEM'))

    # Receive client's public key
    client_received_key = RSA.import_key(client_socket.recv(2048))

    # Generate AES key
    aes_key = get_random_bytes(16)

    # Encrypt AES key with client's public key
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    clients.append((client_socket, aes_key))

    while True:
        try:
            # ===== FIX: nhận độ dài =====
            raw_len = recv_full(client_socket, 4)
            if not raw_len:
                break

            msg_len = struct.unpack("!I", raw_len)[0]

            # nhận đúng dữ liệu
            encrypted_message = recv_full(client_socket, msg_len)

            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(decrypted_message)

            # broadcast
            for sock, key in clients:
                encrypted = encrypt_message(key, decrypted_message)

                # ===== FIX: gửi kèm độ dài =====
                sock.sendall(struct.pack("!I", len(encrypted)))
                sock.sendall(encrypted)

            if decrypted_message == "exit":
                break

        except:
            break

    clients.remove((client_socket, aes_key))
    client_socket.close()
    print("Connection with client closed")

# Accept clients
while True:
    client_socket, client_address = server_socket.accept()
    print("New connection from", client_address)

    client_thread = threading.Thread(
        target=handle_client,
        args=(client_socket, client_address),
        daemon=True  # FIX nhỏ
    )
    client_thread.start()