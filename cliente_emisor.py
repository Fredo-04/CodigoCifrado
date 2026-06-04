import socket
import melgar_cifrado as cipher

CLUB_SIGNATURE = "FBC Melgar de Arequipa"
HOST = '172.17.0.1'
PORT = 65432
CLAVE_SECRETA = "acceso_telematico_01"

def enviar_mensaje(mensaje_original):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("[ERROR] El servidor receptor en Kali Linux no está en línea o el puerto está bloqueado.")
            return

        print(f"\n[PROCESO] Texto original: {mensaje_original}")
        payload_cifrado = cipher.encrypt_data(mensaje_original, CLAVE_SECRETA, CLUB_SIGNATURE)
        
        print(f"[PROCESO] Carga útil encriptada lista para transmisión:\n{payload_cifrado}")
        s.sendall(payload_cifrado.encode('utf-8'))
        print("[SISTEMA] Paquete TCP enviado con éxito.")

if __name__ == "__main__":
    print("--- TERMINAL DE COMUNICACIÓN ENCRIPTADA ---")
    while True:
        mensaje = input("\nIngrese mensaje a transmitir (o 'salir' para terminar): ")
        if mensaje.lower() == 'salir':
            break
        enviar_mensaje(mensaje)