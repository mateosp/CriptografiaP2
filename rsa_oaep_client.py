import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import time

HOST = '127.0.0.1'
PORT = 65432

# Esperar que la clave exista
time.sleep(1)
with open("rsa_pub.pem", "rb") as f:
    public_key = f.read()

cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[Cliente] Conectado. Escribe mensajes para enviar ('salir' para terminar):")
    while True:
        mensaje = input(">> ")
        if not mensaje:
            continue
        ciphertext = cipher_rsa.encrypt(mensaje.encode())
        encoded = base64.b64encode(ciphertext)
        s.sendall(encoded)
        if mensaje.lower() == "salir":
            print("[Cliente] Finalizando conexión...")
            break
