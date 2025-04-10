import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

HOST = '127.0.0.1'
PORT = 65432

# Generar claves
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Guardar clave pública para que el cliente la use
with open("rsa_pub.pem", "wb") as f:
    f.write(public_key)

# Iniciar servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("[Servidor] Esperando conexión...")
    conn, addr = s.accept()
    with conn:
        print(f"[Servidor] Conectado con {addr}")
        data = conn.recv(4096)
        if data:
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
            decrypted = cipher_rsa.decrypt(base64.b64decode(data))
            print(f"[Servidor] Mensaje recibido y descifrado: {decrypted.decode()}")
