import socket
from Crypto.PublicKey import ElGamal
from Crypto.Hash import SHA256
from Crypto.Random.random import randint

# Cargar clave pública
with open("elgamal_pub.txt", "r") as f:
    p = int(f.readline())
    g = int(f.readline())
    y = int(f.readline())

pubkey = ElGamal.construct((p, g, y))

# Conexión al servidor
HOST = 'localhost'
PORT = 5002

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("[Cliente] Conectado al servidor. Escribe mensajes (escribe 'salir' para terminar):")

while True:
    message = input(">> ")
    if message.lower() == "salir":
        break

    # Hash del mensaje
    h = SHA256.new(message.encode()).digest()
    m = int.from_bytes(h, byteorder='big')

    # Cifrado manual ElGamal
    k = randint(1, int(pubkey.p) - 2)
    c1 = pow(pubkey.g, k, pubkey.p)
    s = pow(pubkey.y, k, pubkey.p)
    c2 = (m * int(s)) % int(pubkey.p)

    msg = f"{c1},{c2}".encode()
    client.sendall(msg)

client.close()
