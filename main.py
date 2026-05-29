import melgar_cifrado as cipher # Importa lógica del backend

CLUB_SIGNATURE = "FBC Melgar de Arequipa" # Marca registrada del club

def main():
    print("Sistema de Cifrado Simétrico") # Imprime título principal
    
    while True: # Inicia bucle infinito
        print("\n1. Encriptar") # Opción para encriptar
        print("2. Desencriptar") # Opción para desencriptar
        print("3. Salir") # Opción para salir
        
        opcion = input("Seleccione una acción: ") # Captura decisión del usuario
        
        if opcion == '3': # Evalúa condición de salida
            break # Finaliza ejecución del programa
            
        if opcion in ['1', '2']: # Verifica opción válida
            texto = input("Ingrese el texto o criptograma: ") # Solicita datos al usuario
            clave = input("Ingrese su clave secreta: ") # Solicita clave secreta
            
            try: # Inicia bloque de control
                if opcion == '1': # Procesa solicitud de cifrado
                    resultado = cipher.encrypt_data(texto, clave, CLUB_SIGNATURE) # Llama función encriptar
                    print(f"\nSalida Encriptada:\n{resultado}") # Muestra resultado final
                else: # Procesa solicitud de descifrado
                    resultado = cipher.decrypt_data(texto, clave, CLUB_SIGNATURE) # Llama función desencriptar
                    print(f"\nSalida Desencriptada:\n{resultado}") # Muestra texto original
            except ValueError as e: # Captura errores de integridad
                print(str(e)) # Muestra mensaje de error
        else:
            print("Opción no reconocida.") # Maneja entradas incorrectas

if __name__ == "__main__": # Verifica ejecución directa
    main() # Inicia función principal