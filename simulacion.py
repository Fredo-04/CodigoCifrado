import socket
import threading
import time
import melgar_cifrado as cipher # Importa el backend desarrollado previamente

# Variables estáticas para la red y el cifrado
CLUB_SIGNATURE = "FBC Melgar de Arequipa"
HOST = '127.0.0.1' # Interfaz de red local (localhost)
PORT = 65432 # Puerto de comunicación
CLAVE_SECRETA = "acceso_telematico_01"

def servidor_receptor():
    # Configuración del socket para escuchar conexiones entrantes (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept() # Acepta la conexión del cliente
        
        with conn:
            datos_recibidos = conn.recv(4096) # Tamaño del buffer de recepción
            if not datos_recibidos:
                return
            
            # Convierte los bytes de red a formato de texto Base64
            payload_interceptado = datos_recibidos.decode('utf-8')
            
            print("\nTráfico Interceptado (Vista del Atacante)")
            print(f"Carga útil capturada en la red: {payload_interceptado}")
            
            try:
                # Intento de descifrado en el destino
                mensaje_descifrado = cipher.decrypt_data(payload_interceptado, CLAVE_SECRETA, CLUB_SIGNATURE)
                print("\nMensaje Recibido y Descifrado (Vista del Receptor)")
                print(f"Contenido original: {mensaje_descifrado}")
            except ValueError as e:
                # Captura de errores si el atacante modificó los bits en tránsito
                print("\nError Crítico en Recepción")
                print(str(e))

def cliente_emisor(mensaje_original):
    time.sleep(1) # Espera sincronización para que el servidor inicie
    
    # Configuración del socket para enviar datos (TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT)) # Conecta al servidor
        
        print("Mensaje Preparado (Vista del Emisor)")
        print(f"Texto a enviar: {mensaje_original}")
        
        # Ejecuta el algoritmo de cifrado híbrido
        payload_cifrado = cipher.encrypt_data(mensaje_original, CLAVE_SECRETA, CLUB_SIGNATURE)
        
        print("\nMensaje Encriptado (Salida del Dispositivo)")
        print(f"Carga útil procesada: {payload_cifrado}")
        
        # Serializa el string en bytes y lo envía por la red
        s.sendall(payload_cifrado.encode('utf-8'))

if __name__ == "__main__":
    print("--- INICIANDO PRUEBA TELEMÁTICA CLIENTE/SERVIDOR ---")
    
    # Definición del texto plano a transmitir
    mensaje = "Operación confirmada. Iniciando despliegue en zona sur."
    
    # Levanta el nodo receptor en un hilo paralelo (background)
    hilo_servidor = threading.Thread(target=servidor_receptor)
    hilo_servidor.start()
    
    # Ejecuta el nodo emisor en el hilo principal (foreground)
    cliente_emisor(mensaje)
    
    # Espera a que finalice la transmisión
    hilo_servidor.join()
    print("\n--- TRANSMISIÓN FINALIZADA ---")