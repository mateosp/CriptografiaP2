import socket
import os
from Crypto.PublicKey import ElGamal
from Crypto import Random
from Crypto.Util.number import inverse

def generar_claves():
    print("[Servidor] Generando claves ElGamal (esto puede tardar unos segundos)...")
    key = ElGamal.generate(512, Random.new().read)
    print("[Servidor] Clave generada con éxito.")
    return key, key.publickey()


# Cargar o generar claves
if os.path.exists("elgamal_pub.txt") and os.path.exists("elgamal_priv.txt"):
    with open("elgamal_pub.txt", "r") as f:
        p = int(f.readline())
        g = int(f.readline())
        y = int(f.readline())
    pubkey = ElGamal.construct((p, g, y))

    with open("elgamal_priv.txt", "r") as f:
        p = int(f.readline())
        g = int(f.readline())
        y = int(f.readline())
        x = int(f.readline())
    privkey = ElGamal.construct((p, g, y, x))
else:
    privkey, pubkey = generar_claves()
    with open("elgamal_pub.txt", "w") as f:
        f.write(f"{pubkey.p}\n{pubkey.g}\n{pubkey.y}")
    with open("elgamal_priv.txt", "w") as f:
        f.write(f"{privkey.p}\n{privkey.g}\n{privkey.y}\n{privkey.x}")

# Socket del servidor
HOST = 'localhost'
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("[Servidor] Esperando conexión...")
conn, addr = server.accept()
print(f"[Servidor] Conectado con {addr}")

while True:
    data = conn.recv(4096)
    if not data:
        break
    c1_str, c2_str = data.decode().split(",")
    c1 = int(c1_str)
    c2 = int(c2_str)

    # Descifrado manual
    s_inv = inverse(pow(int(c1), int(privkey.x), int(privkey.p)), int(privkey.p))
    m = (c2 * s_inv) % int(privkey.p)
    m_bytes = m.to_bytes(32, byteorder='big')
    print("[Servidor] Mensaje recibido (SHA-256):", m_bytes.hex())


conn.close()
server.close()
