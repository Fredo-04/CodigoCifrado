import os # Acceso a entropía del sistema
import hashlib # Funciones hash criptográficas
import base64 # Codificación de binarios

def _generate_keystream(key: str, iv: bytes, signature: str, length: int) -> bytes:
    seed = key.encode() + iv + signature.encode() # Concatena semilla inicial
    keystream = bytearray() # Inicializa arreglo dinámico
    
    while len(keystream) < length: # Bucle hasta alcanzar tamaño
        seed = hashlib.sha256(seed).digest() # Hashea la semilla iterativamente
        keystream.extend(seed) # Agrega bytes al flujo
        
    return bytes(keystream[:length]) # Retorna tamaño exacto requerido

def encrypt_data(plaintext: str, key: str, signature: str) -> str:
    data_bytes = plaintext.encode('utf-8') # Convierte texto a bytes
    iv = os.urandom(16) # Genera IV aleatorio
    
    keystream = _generate_keystream(key, iv, signature, len(data_bytes)) # Crea flujo cifrante
    
    ciphertext = bytearray() # Prepara arreglo para cifrado
    for i in range(len(data_bytes)): # Itera sobre cada byte
        ciphertext.append(data_bytes[i] ^ keystream[i]) # Aplica operación XOR
        
    hmac = hashlib.sha256(key.encode() + ciphertext).digest() # Calcula firma de integridad
    
    payload = iv + hmac + ciphertext # Ensambla paquete final
    return base64.b64encode(payload).decode('utf-8') # Codifica salida segura

def decrypt_data(payload_b64: str, key: str, signature: str) -> str:
    try:
        payload = base64.b64decode(payload_b64) # Decodifica entrada Base64
    except Exception:
        raise ValueError("Error: Formato Base64 inválido.") # Rechaza datos corruptos
        
    if len(payload) < 48: # Verifica tamaño mínimo requerido
        raise ValueError("Error: Paquete de datos incompleto.") # Rechaza estructuras inválidas
        
    iv = payload[:16] # Extrae Vector Inicialización
    hmac_received = payload[16:48] # Extrae firma recibida
    ciphertext = payload[48:] # Extrae texto cifrado
    
    hmac_calculated = hashlib.sha256(key.encode() + ciphertext).digest() # Recalcula firma esperada
    
    if hmac_received != hmac_calculated: # Compara firmas de integridad
        raise ValueError("Alerta: Integridad comprometida o clave incorrecta.") # Aborta si hay manipulación
        
    keystream = _generate_keystream(key, iv, signature, len(ciphertext)) # Recrea flujo cifrante
    
    plaintext = bytearray() # Prepara arreglo descifrado
    for i in range(len(ciphertext)): # Itera sobre texto cifrado
        plaintext.append(ciphertext[i] ^ keystream[i]) # Revierte operación XOR
        
    return plaintext.decode('utf-8') # Decodifica bytes a texto