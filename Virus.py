import os
import zipfile
import subprocess
import sys

# --- CONFIGURACIÓN DE RUTA FIJA ---
# Usuario específico solicitado: axelito004
RUTA_BASE = "/home/axelito004/Documentos/Nano-Audit"
NOMBRE_CARPETA = "Laboratorio_Infectado"
RUTA_COMPLETA = os.path.join(RUTA_BASE, NOMBRE_CARPETA)

# Cadena EICAR oficial (NO MODIFICAR)
EICAR = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

def crear_laboratorio():
    print(f"\n[+] Iniciando protocolo de infección controlada...")
    print(f"[+] Destino: {RUTA_COMPLETA}")

    # 1. Crear la carpeta si no existe
    if not os.path.exists(RUTA_COMPLETA):
        try:
            os.makedirs(RUTA_COMPLETA)
            print(f"    -> Carpeta creada exitosamente.")
        except PermissionError:
            print(f"[ERROR] No tengo permisos para escribir en {RUTA_BASE}.")
            print("Prueba ejecutar con 'sudo python3 generar_laboratorio.py'")
            sys.exit(1)
    else:
        print(f"    -> La carpeta ya existe (se sobrescribirán archivos).")

    # 2. Crear virus ejecutable falso (.exe)
    # Simula un troyano de Windows
    path_exe = os.path.join(RUTA_COMPLETA, "Game_Crack_Setup.exe")
    with open(path_exe, "w") as f:
        f.write(EICAR)
    print(f"    -> Generado: Game_Crack_Setup.exe")

    # 3. Crear virus comprimido en ZIP (.zip)
    # Simula documentos ocultos
    path_zip = os.path.join(RUTA_COMPLETA, "Facturas_Pendientes.zip")
    with zipfile.ZipFile(path_zip, 'w') as z:
        z.writestr("payload_oculto.txt", EICAR)
    print(f"    -> Generado: Facturas_Pendientes.zip")

    # 4. Crear virus comprimido en RAR (.rar)
    # Simula fotos personales comprimidas
    path_rar = os.path.join(RUTA_COMPLETA, "Fotos_Privadas.rar")
    
    # Creamos un archivo temporal para comprimirlo
    temp_file = "temp_virus.txt"
    with open(temp_file, "w") as f: 
        f.write(EICAR)
    
    try:
        # Usamos el comando 'rar' del sistema para empaquetar
        # a = add, -ep = exclude paths (para que no guarde toda la ruta de carpetas)
        subprocess.run(["rar", "a", "-ep", path_rar, temp_file], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL)
        
        if os.path.exists(path_rar):
            print(f"    -> Generado: Fotos_Privadas.rar")
        else:
            print(f"    [!] Error: No se creó el RAR. ¿Instalaste 'sudo apt install rar'?")
    except FileNotFoundError:
        print(f"    [!] Error: El comando 'rar' no existe. Instala: sudo apt install rar")
    
    # Limpieza
    if os.path.exists(temp_file): os.remove(temp_file)

    print(f"\n{'-'*50}")
    print(f"✅ LABORATORIO LISTO PARA PRUEBAS")
    print(f"Ruta para copiar y pegar en NanoAudit:")
    print(f"{RUTA_COMPLETA}")
    print(f"{'-'*50}")

if __name__ == "__main__":
    crear_laboratorio()
