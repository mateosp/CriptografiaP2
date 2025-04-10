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

# Guardar clave pública
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
        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
        while True:
            data = conn.recv(4096)
            if not data:
                break

            print(f"\n[Servidor] Mensaje cifrado recibido (base64):\n{data.decode()}")

            try:
                mensaje = cipher_rsa.decrypt(base64.b64decode(data)).decode()
                if mensaje.lower() == "salir":
                    print("[Servidor] El cliente finalizó la conexión.")
                    break
                print(f"[Servidor] Mensaje recibido y descifrado: {mensaje}")
            except Exception as e:
                print(f"[Servidor] Error al descifrar: {e}")
