#sudo python3 -m pip install google-generativeai python-dotenv colorama pyfiglet python-nmap --break-system-packages
#sudo apt install clamav
import os
import sys
import time
import subprocess
import nmap
import google.generativeai as genai
from colorama import Fore, Style, init
from pyfiglet import Figlet
from dotenv import load_dotenv

# --- CONFIGURACIÓN ---
init(autoreset=True)
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

# Colores
R = Fore.RED; G = Fore.GREEN; C = Fore.CYAN; Y = Fore.YELLOW; W = Style.RESET_ALL

def limpiar(): os.system('clear')

def banner():
    limpiar()
    f = Figlet(font='small')
    print(C + f.renderText('NanoAudit'))
    print(W + "    ::: v3.1 | NANO AUDIT:::\n")
    print(W + "    ::: v3.1 | Full Disk Scan + IA :::\n")
    print(W + "    ::: v3.1 (Stable) | By: AXL-HACKING (ANGELITO PARA LOS AMIGOS) :::\n")

def check_root():
    if os.geteuid() != 0:
        print(R + "Error: Ejecuta con SUDO." + W); sys.exit(1)

def animacion_carga(texto):
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f'\r{Y}[*] {texto}... {W}')
        sys.stdout.flush()
    print(f"\r{G}[OK] {texto} completado.{W}    ")

# --- IA (Gemini 2.5) ---
def consultar_ia(contexto, datos):
    if not API_KEY: return f"{R}Falta API Key.{W}"
    if len(datos) < 5: return f"{Y}Sin datos relevantes para IA.{W}"
    
    print(f"\n{Y}[⚡] Consultando a Gemini 2.5...{W}")
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        prompt = f"""
        Rol: Experto en Ciberseguridad informatica y protección de datos.
        Contexto: Auditoría de {contexto}.
        
        Hallazgos Técnicos:
        {datos[:4000]} (Resumen)
        
        Genera reporte:
        1. ANÁLISIS: ¿Qué amenazas hay? (Virus, Cracks, Backdoors).
        2. RIESGO: ¿Qué pueden hacerle al sistema?
        3. ACCIÓN: ¿Borrar, Cuarentena o Ignorar?
        """
        response = model.generate_content(prompt)
        return f"\n{C}--- REPORTE INTELIGENTE ---{W}\n{response.text}\n{C}---------------------------{W}"
    except Exception as e:
        return f"{R}Error IA: {e}{W}"
    
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

# --- NUEVAS FUNCIONES DE DISCO ---

def buscar_cracks_y_activadores(ruta_montaje):
    """Busca archivos típicos de piratería de Windows/Office"""
    print(f"\n{Y}[*] Buscando rastros de Activadores (KMS, Cracks)...{W}")
    
    # Patrones comunes de nombres de archivos de cracks
    patrones = ["KMS", "AutoKMS", "KMSAuto", "KMSpico", "HackTool", "Crack", "Keygen", "Activator"]
    hallazgos = []
    
    # Buscamos en toda la partición (os.walk es recursivo)
    # Limitamos la búsqueda para no tardar años (ej: Program Files y Windows)
    rutas_clave = [
        os.path.join(ruta_montaje, "Program Files"),
        os.path.join(ruta_montaje, "Program Files (x86)"),
        os.path.join(ruta_montaje, "Windows", "Temp"),
        os.path.join(ruta_montaje, "Users") # Descargas suele estar aquí
    ]

    count = 0
    for ruta_base in rutas_clave:
        if os.path.exists(ruta_base):
            for root, dirs, files in os.walk(ruta_base):
                for file in files:
                    # Comprobamos si el nombre contiene algún patrón sospechoso
                    for patron in patrones:
                        if patron.lower() in file.lower():
                            ruta_full = os.path.join(root, file)
                            hallazgos.append(f"Posible Crack: {file} en {root}")
                            print(f"{R}[!] Detectado: {file}{W}")
                count += 1
                if count % 5000 == 0:
                    sys.stdout.write(f'\r{C}    Archivos escaneados: {count}...{W}')
                    sys.stdout.flush()

    return "\n".join(hallazgos) if hallazgos else "No se encontraron activadores comunes por nombre."

def escanear_antivirus_completo(ruta_montaje):
    """Ejecuta ClamAV sobre la partición montada con manejo de errores de DB"""
    print(f"\n{Y}[*] Iniciando Motor Antivirus (ClamAV) sobre toda la partición...{W}")
    print(f"{C}    Esto puede tardar minutos. Si es la primera vez, asegúrate de haber actualizado la DB.{W}")
    
    # Comando: clamscan -r (recursivo) -i (solo infectados)
    comando = ["clamscan", "-r", ruta_montaje, "-i"]
    
    try:
        proceso = subprocess.run(comando, capture_output=True, text=True)
        salida = proceso.stdout
        error_log = proceso.stderr

        # --- CASO 1: AMENAZAS ENCONTRADAS (Exit Code 1) ---
        if proceso.returncode == 1: 
            print(f"\n{R}[!!!] AMENAZAS DETECTADAS:{W}")
            print(salida)
            return salida
        
        # --- CASO 2: SISTEMA LIMPIO (Exit Code 0) ---
        elif proceso.returncode == 0:
            return "Escaneo completado exitosamente. Sistema limpio (Según ClamAV)."
        
        # --- CASO 3: ERROR DE BASE DE DATOS (Exit Code 2 generalmente) ---
        else:
            # Buscamos el error específico de "No supported database"
            if "No supported database files" in error_log:
                print(f"\n{R}[ERROR CRÍTICO] ClamAV no tiene base de datos de virus.{W}")
                print(f"{Y}SOLUCIÓN: Ejecuta estos comandos en una terminal aparte y vuelve a intentar:{W}")
                print(f"{C}1. sudo systemctl stop clamav-freshclam{W}")
                print(f"{C}2. sudo freshclam{W}")
                return "Error: Base de datos de virus vacía. Se requiere actualización manual (freshclam)."
            else:
                return f"Error desconocido en ClamAV: {error_log}"
            
    except FileNotFoundError:
        return "ERROR: ClamAV no está instalado. Ejecuta: sudo apt install clamav"

# --- MÓDULOS ---

def modulo_disco():
    while True:
        banner()
        print(f"{G}[ MÓDULO DISCO: FORENSE PROFUNDO ]{W}")
        print("1. Identificar punto de montaje (lsblk)")
        print("2. 🏴‍☠️  Buscar Cracks/Activadores (KMS, Office, Windows)")
        print("3. ☣️  Escaneo TOTAL de Virus (Usa motor ClamAV)")
        print("0. Volver")
        
        opcion = input(f"\n{G}NanoAudit/Disco > {W}")

        if opcion == '1':
            os.system("lsblk")
            print(f"\n{C}Tu ruta es la columna MOUNTPOINTS. Ej: /media/kali/Windows{W}")
            input(f"{C}[Enter]...{W}")

        elif opcion == '2':
            ruta = input(f"\n{Y}Ruta de montaje (Arrastra carpeta aquí): {W}").strip().replace("'", "")
            if os.path.exists(ruta):
                animacion_carga("Iniciando búsqueda de patrones")
                resultado = buscar_cracks_y_activadores(ruta)
                print(f"\n{G}Resumen:{W}\n{resultado}")
                if "Posible Crack" in resultado:
                    print(consultar_ia("Búsqueda de Piratería/Cracks", resultado))
            else:
                print(f"{R}Ruta inválida.{W}")
            input(f"{C}[Enter]...{W}")

        elif opcion == '3':
            ruta = input(f"\n{Y}Ruta de montaje (Arrastra carpeta aquí): {W}").strip().replace("'", "")
            if os.path.exists(ruta):
                animacion_carga("Cargando base de datos de virus")
                resultado = escanear_antivirus_completo(ruta)
                print(f"\n{G}Resultado Antivirus:{W}\n{resultado}")
                
                # Solo mandamos a la IA si encontró algo o dio error
                if "FOUND" in resultado or "ERROR" in resultado:
                    print(consultar_ia("Escaneo Antivirus Completo", resultado))
                else:
                    print(f"\n{G}¡El sistema parece limpio! La IA descansa por hoy.{W}")
            else:
                print(f"{R}Ruta inválida.{W}")
            input(f"{C}[Enter]...{W}")

        elif opcion == '0':
            break

def main():
    check_root()
    try:
        while True:
            banner()
            print("1. Escáner de Red")
            print("2. Forense de Disco (NUEVO: Cracks + Virus)")
            print("0. Salir")
            opt = input(f"\n{G}NanoAudit > {W}")
            if opt == '1': modulo_red()
            elif opt == '2': modulo_disco()
            elif opt == '0': sys.exit()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
     #Dedicatoria especial a mi madre Yndira Gimenez
     #Proyecto dedicado a mi novia Brianna Vizcaya 
     #Y a mis mejores amigos José Cristancho, Jesús Suarez y Jesús Gonzalez <3
     #Y a mi hermano del alma bombona (Jose Manuel)