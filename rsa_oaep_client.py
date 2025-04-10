import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import time

HOST = '127.0.0.1'
PORT = 65432

# Esperar que el servidor haya guardado la clave
time.sleep(1)

# Leer la clave pública del servidor
with open("rsa_pub.pem", "rb") as f:
    public_key = f.read()

cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
mensaje = "Hola desde el cliente usando RSA-OAEP!"
ciphertext = cipher_rsa.encrypt(mensaje.encode())
encoded = base64.b64encode(ciphertext)

# Enviar mensaje
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(encoded)
    print("[Cliente] Mensaje enviado cifrado.")
