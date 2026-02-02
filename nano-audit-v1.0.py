
#sudo python3 -m pip install google-generativeai python-dotenv colorama pyfiglet python-nmap --break-system-packages
import os
import sys
import time
import hashlib
import subprocess
import shutil
import nmap
import google.generativeai as genai
from colorama import Fore, Style, init
from pyfiglet import Figlet
from dotenv import load_dotenv
# Asegúrate de importar esto al inicio
import sys 
import time

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---
init(autoreset=True) # Colores
load_dotenv() # Variables de entorno

# --- 2. VARIABLES GLOBALES Y ESTILOS ---
API_KEY = os.getenv('GOOGLE_API_KEY')
R = Fore.RED       # Error/Peligro
G = Fore.GREEN     # Éxito/Menú
C = Fore.CYAN      # Info
Y = Fore.YELLOW    # Alerta/Proceso
W = Style.RESET_ALL

# --- 3. FUNCIONES AUXILIARES ---
def limpiar():
    os.system('clear')

def banner():
    limpiar()
    f = Figlet(font='slant')
    print(C + f.renderText('NanoAudit'))
    print(W + "    ::: Ciberseguridad Ofensiva & Forense con IA :::")
    print(W + "    ::: v2.0 (Stable) | By: AXL-HACKING (ANGELITO PARA LOS AMIGOS) :::\n")

def check_root():
    if os.geteuid() != 0:
        banner()
        print(R + "[!] ERROR CRÍTICO: Se requieren permisos de ROOT.")
        print(W + "    El acceso a hardware y redes de bajo nivel lo requiere.")
        print(W + "    Ejecuta: " + Y + "sudo python3 nanoaudit.py")
        sys.exit(1)

# --- 4. INTELIGENCIA ARTIFICIAL (GEMINI) ---
def consultar_ia(tipo_hallazgo, datos_tecnicos):
    if not API_KEY:
        return f"{R}[Error] No se detectó API KEY en el archivo .env{W}"

    print(f"\n{Y}[⚡] Enviando datos a Gemini AI para análisis forense...{W}")
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Actúa como un Analista de Ciberseguridad Senior.
        He realizado una auditoría {tipo_hallazgo} y encontré esto:
        
        DATOS TÉCNICOS:
        "{datos_tecnicos}"
        
        Por favor, genera un reporte breve para un cliente con:
        1. 🛡️ ¿Qué significa esto? (Explicación clara)
        2. 💀 Nivel de Riesgo (Bajo/Medio/Crítico) y Por qué.
        3. 🔧 Pasos exactos para solucionar o desinfectar.
        """
        
        response = model.generate_content(prompt)
        return f"\n{C}--- REPORTE DE INTELIGENCIA ARTIFICIAL ---{W}\n{response.text}\n{C}------------------------------------------{W}"
    except Exception as e:
        return f"{R}Fallo en conexión con IA: {e}{W}"

# --- 5. MÓDULO DE RED (LEGION STYLE) ---


# --- MÓDULO DE RED AVANZADO (TIPO LEGION/NESSUS) ---
def animacion_carga(texto):
    """Efecto visual de carga hacker"""
    chars = "/—\|" 
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f'\r{Y}[*] {texto}... {chars[i % len(chars)]}{W}')
        sys.stdout.flush()
    print(f"\r{G}[OK] {texto} completado.{W}            ")

def modulo_red():
    while True:
        banner()
        print(f"{G}[ MÓDULO DE RED: NIVEL INGENIERÍA ]{W}")
        print(f"1. 🔍 Escaneo Rápido (Discovery)")
        print(f"2. 🛡️  Auditoría de Servicios (Standard)")
        print(f"3. ☢️  Análisis de VULNERABILIDADES (Aggressive)")
        print(f"0. 🔙 Volver")
        
        opcion = input(f"\n{G}NanoAudit/Red > {W}")

        if opcion == '1':
            target = input(f"\n{Y}IP o Rango: {W}")
            nm = nmap.PortScanner()
            animacion_carga("Mapeando la red")
            nm.scan(hosts=target, arguments='-sn')
            
            print(f"\n{C}{'IP ADDRESS':<20} {'ESTADO':<10} {'HOSTNAME'}{W}")
            print("-" * 50)
            for host in nm.all_hosts():
                hostname = nm[host].hostname() if nm[host].hostname() else "(Desconocido)"
                print(f"{host:<20} {G}UP{W}         {hostname}")
            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '2':
            # Escaneo de Versiones (Como el anterior, pero limpio)
            target = input(f"\n{Y}IP Objetivo: {W}")
            animacion_carga("Identificando S.O. y Versiones")
            
            nm = nmap.PortScanner()
            nm.scan(target, arguments='-sV -O --version-intensity 5')
            
            raw_data = ""
            print(f"\n{C}RESULTADOS TÉCNICOS:{W}")
            
            if target in nm.all_hosts():
                # Detectar SO
                if 'osmatch' in nm[target] and nm[target]['osmatch']:
                    os_guess = nm[target]['osmatch'][0]['name']
                    print(f"{Y}[SISTEMA OPERATIVO]:{W} {os_guess}")
                    raw_data += f"Sistema Operativo detectado: {os_guess}\n"

                for proto in nm[target].all_protocols():
                    print(f"\n{C}PROTOCOL: {proto.upper()}{W}")
                    print(f"{'PORT':<8} {'STATE':<10} {'SERVICE':<15} {'VERSION'}")
                    print("-" * 60)
                    
                    lport = nm[target][proto].keys()
                    for port in sorted(lport):
                        srv = nm[target][proto][port]
                        version = srv['version'] if srv['version'] else "Desconocida"
                        row = f"{port:<8} {G}{srv['state']:<10}{W} {srv['name']:<15} {version}"
                        print(row)
                        raw_data += f"Puerto {port}: {srv['name']} versión {version}. "
                
                print(consultar_ia("Auditoría de Servicios", raw_data))
            else:
                print(f"{R}Host inalcanzable.{W}")
            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '3':
            # MODO HACKER: Busca CVEs reales
            target = input(f"\n{Y}IP Objetivo (Cuidado, esto es ruidoso): {W}")
            print(f"\n{R}[ADVERTENCIA] Esto ejecutará scripts de detección de exploits (CVE).{W}")
            print(f"{Y}Puede tardar varios minutos. No cierres el programa.{W}")
            
            animacion_carga("Cargando base de datos de Vulnerabilidades (Nmap Scripting Engine)")
            
            nm = nmap.PortScanner()
            # -sV para versiones, --script vuln para buscar fallos de seguridad
            nm.scan(target, arguments='-sV --script vuln')
            
            scan_result = ""
            if target in nm.all_hosts():
                for proto in nm[target].all_protocols():
                    lport = nm[target][proto].keys()
                    for port in sorted(lport):
                        # Verificar si hay salida de scripts (vulnerabilidades)
                        if 'script' in nm[target][proto][port]:
                            vulns = nm[target][proto][port]['script']
                            print(f"\n{R}[!] VULNERABILIDAD POTENCIAL EN PUERTO {port}:{W}")
                            for name, output in vulns.items():
                                print(f"{Y}Script: {name}{W}")
                                print(f"{output}")
                                scan_result += f"Vuln en puerto {port}: {name} - {output}\n"
                        else:
                            print(f"{G}[+] Puerto {port} limpio (sin vulns obvias detectadas).{W}")
            
            if scan_result:
                print(consultar_ia("Análisis de Vulnerabilidades Críticas (CVE)", scan_result))
            else:
                print(f"\n{G}No se encontraron vulnerabilidades conocidas automáticamente.{W}")
                print("El sistema parece estar parcheado o tiene un firewall activo.")

            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '0':
            break

# --- 6. MÓDULO DE DISCO (FORENSE WINDOWS REAL) ---
def buscar_backdoor_sticky_keys(punto_montaje):
    """Compara el tamaño de sethc.exe con cmd.exe para detectar hack"""
    ruta_system32 = os.path.join(punto_montaje, "Windows", "System32")
    
    sethc = os.path.join(ruta_system32, "sethc.exe")
    cmd = os.path.join(ruta_system32, "cmd.exe")

    if os.path.exists(sethc) and os.path.exists(cmd):
        size_sethc = os.path.getsize(sethc)
        size_cmd = os.path.getsize(cmd)
        
        # Si sethc mide igual que cmd, es un 99% probable que sea un backdoor
        if size_sethc == size_cmd:
            return f"CRÍTICO: Se detectó Backdoor 'Sticky Keys'. El archivo sethc.exe tiene el mismo tamaño ({size_sethc} bytes) que cmd.exe."
        else:
            return "El archivo sethc.exe parece legítimo (tamaño diferente a cmd.exe)."
    return "No se encontraron los archivos de sistema. ¿Es la partición correcta?"

def escanear_inicio(punto_montaje):
    """Busca ejecutables en la carpeta de Inicio de Windows"""
    # Ruta típica de Startup en Windows 10/11
    ruta_startup = os.path.join(punto_montaje, "ProgramData", "Microsoft", "Windows", "Start Menu", "Programs", "StartUp")
    hallazgos = []
    
    if os.path.exists(ruta_startup):
        archivos = os.listdir(ruta_startup)
        for archivo in archivos:
            hallazgos.append(f"Archivo en inicio automático: {archivo}")
    
    return "\n".join(hallazgos) if hallazgos else "Carpeta de inicio limpia."

def modulo_disco():
    while True:
        banner()
        print(f"{G}[ MÓDULO DE DISCO: FORENSE WINDOWS ]{W}")
        print(f"{Y}Nota: Debes tener la partición de Windows montada.{W}")
        print("1. Identificar punto de montaje (Listar discos)")
        print("2. Buscar Backdoors (Sticky Keys Hack)")
        print("3. Auditar carpeta de Inicio (Persistencia de Malware)")
        print("0. Volver al Menú Principal")
        
        opcion = input(f"\n{G}NanoAudit/Disco > {W}")

        if opcion == '1':
            print(f"\n{Y}--- Discos y Particiones ---{W}")
            os.system("lsblk")
            print(f"\n{C}Busca tu partición de Windows (normalmente la más grande NTFS).")
            print(f"Si no está montada, móntala desde el explorador de archivos de Kali.{W}")
            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '2':
            mount_path = input(f"\n{Y}Arrastra la carpeta de Windows aquí o escribe la ruta (ej: /media/kali/OS): {W}").strip().replace("'", "")
            if os.path.exists(mount_path):
                print(f"{Y}[*] Analizando System32...{W}")
                resultado = buscar_backdoor_sticky_keys(mount_path)
                print(f"\n{G}Resultado Técnico:{W} {resultado}")
                
                if "CRÍTICO" in resultado:
                    print(consultar_ia("de Sistema de Archivos (Backdoor)", resultado))
            else:
                print(f"{R}Ruta no encontrada.{W}")
            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '3':
            mount_path = input(f"\n{Y}Ruta de la partición Windows: {W}").strip().replace("'", "")
            if os.path.exists(mount_path):
                print(f"{Y}[*] Analizando persistencia...{W}")
                resultado = escanear_inicio(mount_path)
                print(f"\n{G}Archivos encontrados:{W}\n{resultado}")
                
                if "Archivo" in resultado:
                    print(consultar_ia("de Persistencia (Startup)", resultado))
            else:
                print(f"{R}Ruta no encontrada.{W}")
            input(f"\n{C}[Enter] para continuar...{W}")

        elif opcion == '0':
            break

# --- 7. BUCLE PRINCIPAL (MAIN) ---
def main():
    check_root()
    try:
        while True:
            banner()
            print(f"{G}[ MENÚ PRINCIPAL ]{W}")
            print(f"{G}[1]{W} Escáner de Red (Network)")
            print(f"{G}[2]{W} Forense de Disco (Windows Offline)")
            print(f"{G}[0]{W} Salir del Sistema")
            
            opcion = input(f"\n{G}NanoAudit > {W}")

            if opcion == '1':
                modulo_red()
            elif opcion == '2':
                modulo_disco()
            elif opcion == '0':
                print(f"\n{R}Apagando NanoAudit... Hasta luego.{W}")
                sys.exit()
            else:
                print(f"{R}Opción no válida.{W}")
                time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{R}Salida forzada por usuario.{W}")
        sys.exit()

if __name__ == "__main__":
    main()