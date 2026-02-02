#sudo python3 -m pip install google-generativeai python-dotenv colorama pyfiglet python-nmap --break-system-packages
import os
import sys
import time
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
    print(W + "    ::: v2.5 (beta) | By: AXL-HACKING (ANGELITO PARA LOS AMIGOS) :::\n")

def check_root():
    if os.geteuid() != 0:
        banner()
        print(R + "[!] ERROR: Necesitas ser ROOT (sudo).")
        sys.exit(1)

def animacion_carga(texto):
    chars = "/—\|" 
    for i in range(15):
        time.sleep(0.1)
        sys.stdout.write(f'\r{Y}[*] {texto}... {chars[i % len(chars)]}{W}')
        sys.stdout.flush()
    print(f"\r{G}[OK] {texto} completado.{W}            ")

# --- 4. INTELIGENCIA ARTIFICIAL (CORREGIDA) ---
# --- 4. INTELIGENCIA ARTIFICIAL (ROBUSTA) ---
# --- 4. INTELIGENCIA ARTIFICIAL (VERSIÓN 2026) ---
def consultar_ia(contexto, datos_tecnicos):
    if not API_KEY:
        return f"{R}[Error] No hay API KEY en .env{W}"

    # Si los datos están vacíos, no molestamos a la IA
    if len(datos_tecnicos) < 5:
        return f"{Y}Información insuficiente para análisis de IA.{W}"

    print(f"\n{Y}[⚡] Analizando con Gemini 2.5 Flash...{W}")
    
    try:
        genai.configure(api_key=API_KEY)
        
        # AQUÍ ESTÁ LA MAGIA: Usamos el modelo que SÍ tienes en tu lista
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
        Actúa como un Experto en Ciberseguridad Ofensiva.
        Analiza estos datos de auditoría ({contexto}):
        
        DATA:
        {datos_tecnicos}
        
        Genera un reporte conciso:
        1. 🧐 ANÁLISIS: ¿Qué es esto?
        2. 💀 RIESGO: Nivel y explicación.
        3. 🛡️ SOLUCIÓN: Comando o mitigación exacta.
        """
        
        response = model.generate_content(prompt)
        return f"\n{C}--- 🤖 REPORTE IA 2.5 ---{W}\n{response.text}\n{C}-----------------------{W}"
        
    except Exception as e:
        return f"{R}[ERROR] Falló el modelo Gemini 2.5: {e}{W}"

# --- 5. MÓDULO DE RED (MEJORADO CON IA FORZADA) ---
def modulo_red():
    while True:
        banner()
        print(f"{G}[ MÓDULO DE RED ]{W}")
        print("1. Escaneo Rápido (Discovery)")
        print("2. Auditoría Completa + IA (Versiones + Vulns)")
        print("0. Volver")
        
        opcion = input(f"\n{G}NanoAudit/Red > {W}")

        if opcion == '1':
            target = input(f"\n{Y}IP/Rango: {W}")
            nm = nmap.PortScanner()
            animacion_carga("Ping Sweep")
            nm.scan(hosts=target, arguments='-sn')
            for host in nm.all_hosts():
                print(f"{G}[+] Vivo: {host} ({nm[host].hostname()}){W}")
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '2':
            target = input(f"\n{Y}IP Objetivo: {W}")
            print(f"{Y}[*] Escaneando a fondo (Versiones + Scripts)... esto tarda.{W}")
            
            nm = nmap.PortScanner()
            # Escaneo agresivo pero enfocado
            nm.scan(target, arguments='-sV --script vuln')
            
            reporte_tecnico = ""
            
            if target in nm.all_hosts():
                print(f"\n{G}--- RESULTADOS RAW ---{W}")
                
                # 1. Recopilar Versiones
                for proto in nm[target].all_protocols():
                    lport = nm[target][proto].keys()
                    for port in sorted(lport):
                        srv = nm[target][proto][port]
                        info_puerto = f"Puerto {port}/{proto}: {srv['name']} {srv['product']} {srv['version']}"
                        print(f"[+] {info_puerto}")
                        reporte_tecnico += info_puerto + "\n"
                        
                        # 2. Recopilar Vulnerabilidades (Script output)
                        if 'script' in srv:
                            for script_name, output in srv['script'].items():
                                info_vuln = f"    -> ALERTA VULN ({script_name}): {output}"
                                print(f"{R}{info_vuln}{W}")
                                reporte_tecnico += info_vuln + "\n"
                
                # 3. LLAMADA A LA IA (Siempre, haya vulns o no)
                print(consultar_ia("Red y Servicios", reporte_tecnico))
            else:
                print(f"{R}Host caído o bloquea ping.{W}")
            
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '0':
            break

# --- 6. MÓDULO DE DISCO (SOLUCIÓN API) ---
def buscar_backdoor(ruta):
    sethc = os.path.join(ruta, "Windows/System32/sethc.exe")
    cmd = os.path.join(ruta, "Windows/System32/cmd.exe")
    
    if os.path.exists(sethc) and os.path.exists(cmd):
        if os.path.getsize(sethc) == os.path.getsize(cmd):
            return "CRÍTICO: 'sethc.exe' tiene el mismo tamaño que 'cmd.exe'. Backdoor Sticky Keys ACTIVO."
        else:
            return "SISTEMA LIMPIO: 'sethc.exe' parece original (tamaño correcto)."
    return "Error: No se encuentran archivos de sistema. ¿Ruta correcta?"

def modulo_disco():
    while True:
        banner()
        print(f"{G}[ MÓDULO DE DISCO ]{W}")
        print("1. Listar Discos")
        print("2. Analizar Windows (Backdoor check + IA)")
        print("0. Volver")
        
        opcion = input(f"\n{G}NanoAudit/Disco > {W}")

        if opcion == '1':
            os.system("lsblk")
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '2':
            ruta = input(f"\n{Y}Arrastra carpeta Windows aquí: {W}").strip().replace("'", "")
            
            if os.path.exists(ruta):
                animacion_carga("Analizando System32")
                hallazgo = buscar_backdoor(ruta)
                print(f"\n{G}Hallazgo Técnico:{W} {hallazgo}")
                
                # Llamamos a la IA con el hallazgo específico
                print(consultar_ia("Sistema de Archivos Windows", hallazgo))
            else:
                print(f"{R}Ruta inválida.{W}")
            
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '0':
            break

# --- MAIN ---
def main():
    check_root()
    try:
        while True:
            banner()
            print("1. Escáner de Red")
            print("2. Forense de Disco")
            print("0. Salir")
            opt = input(f"\n{G}NanoAudit > {W}")
            if opt == '1': modulo_red()
            elif opt == '2': modulo_disco()
            elif opt == '0': sys.exit()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
    #Proyecto dedicado a mi novia Brianna Vizcaya y a mi mejor amigo José Cristancho <3