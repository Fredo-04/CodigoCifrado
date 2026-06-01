import socket
import melgar_cifrado as cipher

CLUB_SIGNATURE = "FBC Melgar de Arequipa"
HOST = '127.0.0.1'
PORT = 65432
CLAVE_SECRETA = "acceso_telematico_01"

def enviar_mensaje(mensaje_original):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("[CLIENTE] Error: El servidor receptor no está en línea.")
            return

        print(f"[CLIENTE] Texto original: {mensaje_original}")
        payload_cifrado = cipher.encrypt_data(mensaje_original, CLAVE_SECRETA, CLUB_SIGNATURE)
        
        print(f"[CLIENTE] Carga útil procesada enviada a la red: {payload_cifrado}")
        s.sendall(payload_cifrado.encode('utf-8'))

if __name__ == "__main__":
    while True:
        mensaje = input("\nIngrese mensaje a transmitir (o 'salir' para terminar): ")
        if mensaje.lower() == 'salir':
            break
        enviar_mensaje(mensaje)