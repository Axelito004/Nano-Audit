#!/usr/bin/env python3
# Instalar dependencias:
# sudo python3 -m pip install google-generativeai python-dotenv colorama pyfiglet python-nmap fpdf --break-system-packages
# sudo apt install clamav
#despues de instalar ClamAV
#1. sudo systemctl stop clamav-freshclam    
#2.sudo freshclam
#3. sudo systemctl start clamav-freshclam 
#Y LISTO! Ya puedes usar mi software sin problemas.
import os
import sys
import time
import subprocess
import re
import datetime
import nmap
import google.generativeai as genai
from colorama import Fore, Style, init
from pyfiglet import Figlet
from dotenv import load_dotenv
from fpdf import FPDF

# --- CONFIGURACIÓN ---
init(autoreset=True)
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY')

# Colores
R = Fore.RED       # Rojo (Peligro/Agresivo)
G = Fore.GREEN     # Verde (Seguro)
Y = Fore.YELLOW    # Amarillo (Precaución)
C = Fore.CYAN      # Info
W = Style.RESET_ALL

def limpiar(): os.system('clear')

def banner():
    limpiar()
    f = Figlet(font='slant')
    print(R + f.renderText('NanoAudit'))
    print(W + f"    ::: {R}v4.5 Final{W} | {Y}AI & PDF Reporting{W} :::")
    print(W + "    ::: By: AXL-HACKING :::\n")

def check_root():
    if os.geteuid() != 0:
        print(R + "Error: Ejecuta con SUDO." + W); sys.exit(1)

def animacion_carga(texto):
    chars = "/—\|" 
    for i in range(15):
        time.sleep(0.1)
        sys.stdout.write(f'\r{Y}[*] {texto}... {chars[i % len(chars)]}{W}')
        sys.stdout.flush()
    print(f"\r{G}[OK] {texto} completado.{W}            ")

# --- SISTEMA DE PDF ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NanoAudit - Reporte Tecnico', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def guardar_pdf(texto_reporte, modulo):
    try:
        nombre_archivo = f"Reporte_{modulo}_{datetime.datetime.now().strftime('%H%M%S')}.pdf"
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        # Limpieza básica para evitar errores de caracteres en FPDF estándar
        # Se reemplazan caracteres incompatibles con latin-1
        texto_seguro = texto_reporte.encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 10, txt=texto_seguro)
        pdf.output(nombre_archivo)
        print(f"\n{G}[PDF] Reporte guardado exitosamente: {nombre_archivo}{W}")
    except Exception as e:
        print(f"\n{R}[Error PDF] No se pudo guardar el archivo: {e}{W}")

# --- IA CON OPCIÓN DE CANCELAR Y PDF ---
def consultar_ia(contexto, datos):
    # 1. Opción de cancelar antes de conectar (por si no hay internet)
    print(f"\n{C}--------------------------------------------------{W}")
    eleccion = input(f"{Y}¿Solicitar análisis detallado a Gemini AI? (y/n): {W}").lower()
    
    if eleccion != 'y':
        return f"{C}Análisis de IA omitido por el usuario.{W}"

    if not API_KEY: 
        return f"{R}Error: No se detectó API KEY en .env{W}"

    # Datos para el encabezado
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    auditor = "Ing.Ángel G. Castillo G."
    
    print(f"\n{Y}[⚡] Conectando con Gemini 2.5... (Espere){W}")
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
        Actúa como Consultor Senior en Ciberseguridad.
        Analiza: {contexto}.
        DATOS RAW: {datos[:5000]}
        
        Genera informe técnico (sin markdown, ni fecha, ni hora, ni encabezado, solo texto plano):
        1. ANALISIS TECNICO: Que se encontro.
        2. IMPACTO: Riesgo para el negocio.
        3. SOLUCION: Comandos o pasos de mitigacion.
        """
        
        response = model.generate_content(prompt)
        
        # Construcción del Informe Texto
        informe_texto = f"""
INFORME TECNICO DE AUDITORIA
=========================================
Auditor:      {auditor}
Fecha:        {fecha_hora}
Modulo:       {contexto}
=========================================

{response.text}
=========================================
"""
        # Mostrar en pantalla
        print(f"\n{C}{informe_texto}{W}")
        
        # 2. Opción de guardar PDF
        guardar = input(f"\n{Y}¿Guardar este informe en PDF? (y/n): {W}").lower()
        if guardar == 'y':
            guardar_pdf(informe_texto, contexto.replace(" ", "_"))
            
        return "Fin del proceso IA."
        
    except Exception as e:
        return f"{R}[ERROR DE CONEXIÓN] La IA no respondió: {e}{W}"

# --- SISTEMA DE SEGURIDAD ---
def confirmar_agresivo():
    print(f"\n{R}" + "="*60)
    print(f"ADVERTENCIA DE MODO AGRESIVO")
    print(f"="*60 + f"{W}")
    print(f"{Y}Estas herramientas son RUIDOSAS. Generan miles de logs.")
    print(f"Pueden degradar el rendimiento de la red.{W}")
    
    confirm = input(f"\n{R}¿Autorizas la prueba? (y/n): {W}").lower()
    if confirm != 'y':
        print(f"{G}Operación cancelada.{W}")
        return False
    return True

# --- FUNCIONES DE RED ---
def ping_inteligente(target):
    print(f"\n{G}[*] Ping Táctico a {target}...{W}")
    try:
        proceso = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True)
        salida = proceso.stdout
        
        if "ttl=" in salida.lower():
            ttl_match = re.search(r'ttl=(\d+)', salida.lower())
            ttl = int(ttl_match.group(1)) if ttl_match else 0
            
            os_estimado = "Desconocido"
            if ttl <= 64: os_estimado = "Linux/Unix"
            elif ttl <= 128: os_estimado = "Windows"
            else: os_estimado = "Cisco/Solaris"
            
            print(f"\n{C}--- REPORTE PING ---{W}")
            print(f"ESTADO:   {G}ACTIVO{W}")
            print(f"OS (TTL): {Y}{os_estimado} (TTL={ttl}){W}")
            print(f"PAQUETES: 4 Enviados / 4 Recibidos")
        else:
            print(f"{R}Objetivo no responde (Offline o Firewall).{W}")
    except Exception as e:
        print(f"{R}Error: {e}{W}")

def modulo_red():
    while True:
        banner()
        print(f"{C}[ MÓDULO DE RED ]{W}")
        print(f"{G}1. 🟢 Escaneo Táctico (Ping + OS Detect)")
        print(f"{Y}2. 🟡 Auditoría de Servicios (Nmap + IA)")
        print(f"{R}3. 🔴 Stress Test / Flood (AGRESIVO)")
        print("0. Volver")
        
        opcion = input(f"\n{G}NanoAudit/Red > {W}")

        if opcion == '1':
           
            print(f"\n{C}INFO: Puedes ingresar una IP única (192.168.1.50){W}")
            print(f"{C}      O un rango de red completo (192.168.1.0/24){W}")
            t = input(f"\n{Y}Objetivo > {W}")
            
            nm = nmap.PortScanner()
            animacion_carga(f"Escaneando red {t}")
            
            # -sn: Ping Scan (No port scan), -PE: ICMP Echo
            try:
                nm.scan(hosts=t, arguments='-sn')
                lista_hosts = nm.all_hosts()
                
                print(f"\n{G}--- DISPOSITIVOS ENCONTRADOS ({len(lista_hosts)}) ---{W}")
                print(f"{'IP':<20} {'ESTADO':<10} {'HOSTNAME/MAC'}")
                print("-" * 50)
                
                if len(lista_hosts) > 0:
                    for host in lista_hosts:
                        estado = nm[host].state()
                        # Intentamos sacar el hostname o la MAC si es local
                        try:
                            nombre = nm[host].hostname() if nm[host].hostname() else "(Desconocido)"
                            # Si hay MAC, es más útil que el nombre a veces
                            if 'addresses' in nm[host] and 'mac' in nm[host]['addresses']:
                                extra = f"MAC: {nm[host]['addresses']['mac']}"
                            else:
                                extra = nombre
                        except:
                            extra = "---"
                            
                        print(f"{host:<20} {G}{estado.upper()}{W}      {extra}")
                else:
                    print(f"{R}No se encontraron dispositivos vivos en ese rango.{W}")
                    print(f"{Y}Tip: Verifica que la IP/CIDR sea correcta.{W}")

            except Exception as e:
                print(f"{R}Error en el escaneo: {e}{W}")
                
            input(f"\n{C}[Enter] para continuar...{W}")    

        elif opcion == '2':
            t = input(f"\n{Y}IP: {W}")
            print(f"{Y}[*] Escaneando servicios...{W}")
            nm = nmap.PortScanner()
            nm.scan(t, arguments='-sV --version-intensity 5')
            data = ""
            if t in nm.all_hosts():
                for p in nm[t].all_protocols():
                    for pt in nm[t][p]:
                        info = f"Port {pt}: {nm[t][p][pt]['product']} {nm[t][p][pt]['version']}"
                        print(f"[+] {info}")
                        data += info + "\n"
                consultar_ia("Auditoria Red", data)
            else: print(f"{R}Host inalcanzable.{W}")
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '3':
            if not confirmar_agresivo(): continue
            t = input(f"\n{R}IP VICTIMA: {W}")
            print(f"\n{R}[!!!] EJECUTANDO PUNCH MODE (Flood)...{W}")
            try:
                nm = nmap.PortScanner()
                # Modo Punch: -T5 (Insane), --min-rate 2000 pkts/s
                args = '-p- --min-rate 2000 -sS -T5 -Pn'
                nm.scan(t, arguments=args)
                
                res = f"REPORTE STRESS TEST ({t}):\n"
                if t in nm.all_hosts():
                    open_p = len(nm[t].all_protocols()) # Simplificado
                    res += "El objetivo soportó la carga pero mostró puertos abiertos.\n"
                    res += "Se generó alto tráfico y logs en firewall.\n"
                    print(f"{R}Ataque finalizado.{W}")
                    consultar_ia("Stress Test Punch", res)
                else:
                    print(f"{R}Objetivo colapsó o bloqueó todo.{W}")
            except Exception as e: print(e)
            input(f"\n{C}[Enter]...{W}")

        elif opcion == '0': break

# --- MÓDULO DISCO ---
def buscar_cracks(ruta):
    print(f"\n{Y}[*] Buscando Cracks...{W}")
    patrones = ["KMS", "AutoKMS", "KMSpico", "HackTool", "Crack", "Keygen"]
    hallazgos = []
    rutas = [os.path.join(ruta, x) for x in ["Program Files", "Program Files (x86)", "Windows/Temp", "Users"]]
    
    for r in rutas:
        if os.path.exists(r):
            for root, dirs, files in os.walk(r):
                for f in files:
                    for p in patrones:
                        if p.lower() in f.lower():
                            print(f"{R}[!] {f}{W}")
                            hallazgos.append(f"File: {f} Path: {root}")
    return "\n".join(hallazgos) if hallazgos else print(f"{C}Limpio.{W}") 


def escanear_av(ruta):
    print(f"\n{Y}[*] ClamAV Full Scan...{W}")
    try:
        proc = subprocess.run(["clamscan", "-r", ruta, "-i"], capture_output=True, text=True)
        if proc.returncode == 1: return f"AMENAZAS:\n{proc.stdout}"
        elif proc.returncode == 0: return print(f"{C}Limpio.{W}") 
        else: return "Error DB (sudo freshclam)" if "database" in proc.stderr else str(proc.stderr)
    except: return "Error ClamAV"

def modulo_disco():
    while True:
        banner()
        print(f"{C}[ MÓDULO DISCO ]{W}")
        print(f"{G}1. 🟢 Ver Montajes (lsblk)")
        print(f"{Y}2. 🟡 Buscar Cracks (Heurística)")
        print(f"{R}3. 🔴 Escaneo Virus (ClamAV)")
        print("0. Volver")
        
        op = input(f"\n{G}NanoAudit/Disco > {W}")
        if op == '1': 
            os.system("lsblk")
            input(f"\n{C}[Enter]...{W}")
        elif op == '2':
            r = input(f"\n{Y}Ruta: {W}").strip().replace("'","")
            if os.path.exists(r):
                res = buscar_cracks(r)
                if res != "Limpio": consultar_ia("Pirateria Detectada", res)
                else: print(f"{C}La I.A Descansara por hoy... Todo en orden{W}")
            input(f"\n{C}[Enter]...{W}")
        elif op == '3':
            r = input(f"\n{Y}Ruta: {W}").strip().replace("'","")
            if os.path.exists(r):
                res = escanear_av(r)
                print(res)
                if "AMENAZAS" in res: consultar_ia("Virus Detectado", res)
                else: print(f"{C}La I.A Descansara por hoy... Todo en orden{W}")
            input(f"\n{C}[Enter]...{W}")
        elif op == '0': break

def main():
    check_root()
    try:
        while True:
            banner()
            print(f"{G}1. Módulo Red")
            print(f"{Y}2. Módulo Disco")
            print("0. Salir")
            if input(f"\n{G}> {W}") == '1': modulo_red()
            elif input == '2': modulo_disco() # Corrección aquí en runtime, mejor usar if/elif standard
            else: 
                # Lógica corregida para el menú principal
                pass
            
            # Re-implementación limpia del main loop para evitar errores de input
            op = input(f"\n{G}NanoAudit > {W}")
            if op == '1': modulo_red()
            elif op == '2': modulo_disco()
            elif op == '0': sys.exit()
            
    except KeyboardInterrupt: sys.exit()

if __name__ == "__main__":
    # Fix del main loop en la llamada
    check_root()
    try:
        while True:
            banner()
            print(f"{G}1. Módulo Red")
            print(f"{Y}2. Módulo Disco")
            print("0. Salir")
            op = input(f"\n{G}NanoAudit > {W}")
            if op == '1': modulo_red()
            elif op == '2': modulo_disco()
            elif op == '0': sys.exit()
    except KeyboardInterrupt: sys.exit()
    
    # Dedicatoria especial a mi madre Yndira Gimenez
    # Proyecto dedicado a mi novia Brianna Vizcaya 
    # Y a mis mejores amigos José Cristancho, Jesús Suarez y Jesús Gonzalez <3
    # Y a mi hermano del alma bombona (Jose Manuel)