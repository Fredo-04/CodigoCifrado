import socket
import melgar_cifrado as cipher

CLUB_SIGNATURE = "FBC Melgar de Arequipa"
HOST = '127.0.0.1'
PORT = 65432
CLAVE_SECRETA = "acceso_telematico_01"

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[SERVIDOR] Conexión establecida desde {addr}")
                datos_recibidos = conn.recv(4096)
                if not datos_recibidos:
                    continue
                
                payload_interceptado = datos_recibidos.decode('utf-8')
                print(f"[INTERCEPCIÓN DE RED]\nCarga capturada: {payload_interceptado}")
                
                try:
                    mensaje_descifrado = cipher.decrypt_data(payload_interceptado, CLAVE_SECRETA, CLUB_SIGNATURE)
                    print(f"[SERVIDOR]\nMensaje validado y descifrado: {mensaje_descifrado}\n")
                except ValueError as e:
                    print(f"[ALERTA DE SEGURIDAD] {e}\n")

if __name__ == "__main__":
    iniciar_servidor()