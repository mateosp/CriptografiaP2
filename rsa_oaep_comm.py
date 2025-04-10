from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

def generar_claves():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def cifrar_mensaje(public_key, mensaje):
    pubkey = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(pubkey)
    encrypted = cipher.encrypt(mensaje.encode())
    return base64.b64encode(encrypted)

def descifrar_mensaje(private_key, mensaje_cifrado):
    privkey = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(privkey)
    decrypted = cipher.decrypt(base64.b64decode(mensaje_cifrado))
    return decrypted.decode()

# Ejemplo de uso
if __name__ == "__main__":
    priv, pub = generar_claves()
    mensaje = "Hola desde RSA-OAEP!"
    cifrado = cifrar_mensaje(pub, mensaje)
    descifrado = descifrar_mensaje(priv, cifrado)
    
    print(f"Mensaje original: {mensaje}")
    print(f"Mensaje cifrado: {cifrado}")
    print(f"Mensaje descifrado: {descifrado}")
