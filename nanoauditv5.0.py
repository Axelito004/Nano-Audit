#!/usr/bin/env python3
# Dependencias: sudo python3 -m pip  google-generativeai python-dotenv colorama pyfiglet python-nmap fpdf --break-system-packages
# sudo apt update && sudo apt install clamav install rar alsa-utils sox libsox-fmt-all
# NOTA: Ejecutar con sudo para que Nmap funcione en modo Flood.

import os
import sys
import time
import subprocess
import re
import datetime
import threading
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
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
C = Fore.CYAN
W = Style.RESET_ALL

def limpiar(): os.system('clear')

def banner():
    limpiar()
    f = Figlet(font='slant')
    print(R + f.renderText('NanoAudit'))
    print(W + f"    ::: {R}v5.1 Final{W} | {Y}Potenciado por I.A & Reportes Automáticos{W} :::")
    print(W + "    ::: By: AXL-HACKING :::\n")

def check_root():
    if os.geteuid() != 0:
        print(R + "Error: Ejecuta con SUDO." + W); sys.exit(1)

# --- UTILIDADES VISUALES Y SONORAS (CORREGIDO) ---
def reproducir_sonido_fin():
    """Intenta reproducir sonido con múltiples reproductores"""
    # 1. Buscar el archivo WAV local
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_sonido = os.path.join(carpeta_actual, "alert2.wav")
    
    # 2. Obtener usuario real (para saltar bloqueo de root)
    usuario_real = os.getenv('SUDO_USER') or os.getenv('USER')

    if os.path.exists(ruta_sonido):
        # Lista de posibles reproductores en orden de preferencia
        reproductores = [
            f"runuser -u {usuario_real} -- aplay -q '{ruta_sonido}'",  # ALSA (Nativo)
            f"runuser -u {usuario_real} -- play -q '{ruta_sonido}'",   # SoX (Muy compatible)
            f"runuser -u {usuario_real} -- paplay '{ruta_sonido}'"     # PulseAudio (Gnome)
        ]
        
        exito = False
        for cmd in reproductores:
            try:
                # Intentamos ejecutar el comando en segundo plano (&)
                resultado = os.system(cmd + " >/dev/null 2>&1 &")
                if resultado == 0: # Si el comando se ejecutó sin error de "command not found"
                    exito = True
                    break 
            except:
                continue
        
        # Si ningún reproductor funcionó, usamos el Beep de la BIOS
        if not exito:
            sys.stdout.write('\a')
            sys.stdout.flush()
    else:
        # Si no existe el archivo alert.wav
        sys.stdout.write('\a')
        sys.stdout.flush()

class Spinner:
    """Animación de carga"""
    def __init__(self, mensaje="Procesando..."):
        self.mensaje = mensaje
        self.stop_running = False
        self.thread = threading.Thread(target=self._animate)

    def _animate(self):
        chars = "/-\|"
        i = 0
        while not self.stop_running:
            sys.stdout.write(f'\r{Y}[*] {self.mensaje} {chars[i % 4]}{W}')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        self.stop_running = False
        self.thread.start()

    def stop(self):
        self.stop_running = True
        self.thread.join()
        sys.stdout.write('\r' + ' ' * (len(self.mensaje) + 10) + '\r')
        sys.stdout.flush()

# --- SISTEMA PDF ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NanoAudit - Informe Tecnico', 0, 1, 'C')
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
        texto_seguro = texto_reporte.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=texto_seguro)
        pdf.output(nombre_archivo)
        print(f"\n{G}[PDF] Reporte guardado exitosamente: {nombre_archivo}{W}")
    except Exception as e:
        print(f"\n{R}[Error PDF] No se pudo guardar el archivo: {e}{W}")

# --- IA ---
def consultar_ia(contexto, datos):
    print(f"\n{C}--------------------------------------------------{W}")
    eleccion = input(f"{Y}¿Solicitar análisis detallado a Gemini AI? (y/n): {W}").lower()
    
    if eleccion != 'y':
        return f"{C}Análisis de IA omitido.{W}"

    if not API_KEY: 
        return f"{R}Error: No se detectó API KEY en .env{W}"

    spin = Spinner("Consultando a Gemini 2.5...")
    spin.start()
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        prompt = f"""
        Actúa como Consultor Senior en Ciberseguridad.
        Analiza: {contexto}.
        DATOS RAW: {datos[:5000]}
        Responde en Texto Plano (Sin Markdown):
        1. ANALISIS TECNICO.
        2. IMPACTO.
        3. SOLUCION.
        """
        response = model.generate_content(prompt)
        spin.stop()
        reproducir_sonido_fin()

        informe = f"""
INFORME TECNICO
Fecha: {datetime.datetime.now()}
Modulo: {contexto}
=========================================
{response.text}
=========================================
"""
        print(f"\n{C}{informe}{W}")
        if input(f"\n{Y}¿Guardar PDF? (y/n): {W}").lower() == 'y':
            guardar_pdf(informe, contexto.replace(" ", "_"))
            reproducir_sonido_fin()
        return "Fin IA."
    except Exception as e:
        spin.stop()
        return f"{R}Error IA: {e}{W}"

# --- SEGURIDAD ---
def confirmar_agresivo():
    print(f"\n{R}ADVERTENCIA: MODO AGRESIVO (Flood / Stress){W}")
    if input(f"{R}¿Autorizas? (y/n): {W}").lower() != 'y': return False
    return True

# --- MODULO RED ---
def modulo_red():
    while True:
        banner()
        print(f"{C}[ MÓDULO DE RED ]{W}")
        print(f"{G}1. 🟢 Escaneo Táctico (Ping + OS)")
        print(f"{Y}2. 🟡 Auditoría Servicios (Nmap + IA)")
        print(f"{R}3. 🔴 Network Stress Test (Logs en Vivo)")
        print("0. Volver")
        
        op = input(f"\n{G}NanoAudit/Red > {W}")

        if op == '1':
            t = input(f"\n{Y}Objetivo (IP/Rango) > {W}")
            nm = nmap.PortScanner()
            spin = Spinner(f"Ping Sweep a {t}")
            spin.start()
            try:
                nm.scan(hosts=t, arguments='-sn')
                lista = nm.all_hosts()
                spin.stop()
                reproducir_sonido_fin() # ¡Sonido aquí!
                
                print(f"\n{G}--- RESULTADOS ---{W}")
                for host in lista:
                    try:
                        mac = nm[host]['addresses'].get('mac', '---')
                        vendor = nm[host]['vendor'].get(mac, '')
                        print(f"{host:<15} {G}UP{W} | MAC: {mac} ({vendor})")
                    except: print(f"{host} UP")
            except Exception as e:
                spin.stop()
                print(e)
            input(f"\n{C}[Enter]...{W}")

        elif op == '2':
            t = input(f"\n{Y}IP: {W}")
            spin = Spinner("Analizando Servicios (-sV)...")
            spin.start()
            nm = nmap.PortScanner()
            nm.scan(t, arguments='-sV --version-intensity 5')
            spin.stop()
            reproducir_sonido_fin() # ¡Sonido aquí!
            
            data = ""
            if t in nm.all_hosts():
                for p in nm[t].all_protocols():
                    for pt in nm[t][p]:
                        row = f"Port {pt}: {nm[t][p][pt]['product']} {nm[t][p][pt]['version']}"
                        print(f"[+] {row}")
                        data += row + "\n"
                consultar_ia("Auditoria Servicios", data)
            else: print(f"{R}Host Down{W}")
            input(f"\n{C}[Enter]...{W}")

        elif op == '3':
            # STRESS TEST RED: LOGS EN VIVO (CORREGIDO)
            if not confirmar_agresivo(): continue
            t = input(f"\n{R}IP VICTIMA: {W}")
            print(f"\n{R}[!!!] INICIANDO FLOOD (Logs en tiempo real)...{W}")
            
            # Usamos nmap con -v (verbose) y --stats-every para ver progreso
            # -p- (todos puertos), --min-rate 3000 (muy agresivo)
            cmd = ["nmap", "-p-", "--min-rate", "3000", "-sS", "-Pn", "-v", "--stats-every", "1s", t]
            
            try:
                # Popen para streaming de logs
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                log_acumulado = ""
                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        # Filtramos lineas vacías
                        l = line.strip()
                        if l:
                            print(f"{G}>> {l}{W}") # Imprime cada paquete/evento
                            log_acumulado += l + "\n"
                
                reproducir_sonido_fin() # ¡Sonido al terminar el flood!
                print(f"\n{C}Ataque finalizado.{W}")
                
                # Opcional: Mandar resumen a IA
                if len(log_acumulado) > 100:
                    consultar_ia("Network Stress Test Log", log_acumulado[-2000:]) # Solo ultimas lineas
                    
            except Exception as e:
                print(f"{R}Error ejecutando flood: {e}{W}")
            input(f"\n{C}[Enter]...{W}")

        elif op == '0': break

def escanear_av(ruta):
        print(f"\n{Y}[*] Iniciando Motor de Análisis (ClamAV + UnRAR Wrapper)...{W}")
    
    # Carpeta temporal para descomprimir RARs (Oculta)
        carpeta_temp = os.path.join(ruta, ".temp_scan_rar")
        
        spin = Spinner("Analizando estructura de archivos...")
        spin.start()
        
        # 1. BÚSQUEDA Y EXTRACCIÓN MANUAL DE RARs
        try:
            hay_rars = False
            if os.path.exists(ruta):
                # Buscar archivos .rar
                archivos_rar = []
                for root, dirs, files in os.walk(ruta):
                    for f in files:
                        if f.lower().endswith(".rar"):
                            archivos_rar.append(os.path.join(root, f))
                
                if archivos_rar:
                    hay_rars = True
                    if not os.path.exists(carpeta_temp):
                        os.makedirs(carpeta_temp)
                    
                    # Descomprimir cada RAR encontrado usando 'unrar' del sistema
                    # e = extract, -p- = sin contraseña, -y = sí a todo, -inul = silencio
                    for rar_file in archivos_rar:
                        subprocess.run(["unrar", "e", "-p-", "-y", "-inul", rar_file, carpeta_temp])

        except Exception as e:
            # Si falla la extracción manual, seguimos con el escaneo normal
            pass

        spin.stop()
        
        # 2. ESCANEO CON CLAMAV (Escanea la ruta original Y la temporal)
        spin = Spinner("Buscando firmas de virus (Deep Scan)...")
        spin.start()
        
        scan_output = ""
        amenaza_detectada = False
        
        try:
            # Escaneamos la ruta original
            proc1 = subprocess.run(["clamscan", "-r", ruta, "-i"], capture_output=True, text=True)
            
            # Escaneamos la carpeta temporal (donde está lo de adentro del RAR)
            proc2 = None
            if hay_rars:
                proc2 = subprocess.run(["clamscan", "-r", carpeta_temp, "-i"], capture_output=True, text=True)
            
            spin.stop()
            reproducir_sonido_fin() 

            # 3. PROCESAR RESULTADOS
            resultado_final = ""
            
            # Resultados Ruta Original
            if proc1.returncode == 1:
                amenaza_detectada = True
                resultado_final += f"{R}AMENAZAS EN ARCHIVOS VISIBLES:{W}\n{proc1.stdout}\n"
            
            # Resultados RARs Descomprimidos
            if proc2 and proc2.returncode == 1:
                amenaza_detectada = True
                # Limpiamos la ruta fea temporal para que se vea bonito en el reporte
                texto_limpio = proc2.stdout.replace(carpeta_temp, "[DENTRO DEL RAR]")
                resultado_final += f"{R}AMENAZAS OCULTAS (RAR):{W}\n{texto_limpio}\n"

            # 4. LIMPIEZA (Borrar carpeta temporal)
            if os.path.exists(carpeta_temp):
                import shutil
                shutil.rmtree(carpeta_temp)

            if amenaza_detectada:
                return resultado_final
            elif proc1.returncode == 0 and (not proc2 or proc2.returncode == 0):
                return "Limpio"
            else:
                return f"Error en motor antivirus: {proc1.stderr}"

        except Exception as e:
            spin.stop()
            return f"Error crítico: {e}"

# --- MODULO DISCO ---
def modulo_disco():
    while True:
        banner()
        print(f"{C}[ MÓDULO DISCO ]{W}")
        print(f"{G}1. 🟢 Ver Montajes")
        print(f"{Y}2. 🟡 Buscar Cracks")
        print(f"{R}3. 🔴 Escaneo Virus (ClamAV)")
        print("0. Volver")
        
        op = input(f"\n{G}NanoAudit/Disco > {W}")
        
        if op == '1': 
            os.system("lsblk")
            reproducir_sonido_fin()
            input(f"\n{C}[Enter]...{W}")

        elif op == '2':
            r = input(f"\n{Y}Ruta: {W}").replace("'","").strip()
            spin = Spinner("Buscando Cracks...")
            spin.start()
            # Logica simple de busqueda
            found = []
            if os.path.exists(r):
                for root, dirs, files in os.walk(r):
                    for f in files:
                        if any(x in f.lower() for x in ['crack', 'keygen', 'kms', 'patch']):
                            found.append(os.path.join(root, f))
            spin.stop()
            reproducir_sonido_fin() # ¡Sonido aquí!
            
            if found:
                for f in found: print(f"{R}[!] {f}{W}")
                consultar_ia("Pirateria Hallada", "\n".join(found))
            else: print(f"{G}Limpio.{W}")
            input(f"\n{C}[Enter]...{W}")

        elif op == '3':
            ruta = input(f"\n{Y}Ruta: {W}").strip().replace("'","")
            if os.path.exists(ruta):
                res = escanear_av(ruta)
                print(res)
                if "AMENAZAS" in res: consultar_ia("Virus Detectado", res)
                else: print(f"{C}La I.A Descansara por hoy... Todo en orden{W}")
            input(f"\n{C}[Enter]...{W}")      

        elif op == '0': break

# --- MAIN ---
if __name__ == "__main__":
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
    except KeyboardInterrupt:
        sys.exit()
    # Dedicatoria especial a mi madre Yndira Gimenez
    # Proyecto dedicado a mi novia Brianna Vizcaya 
    # Y a mis mejores amigos José Cristancho, Jesús Suarez y Jesús Gonzalez <3
    # Y a mi hermano del alma bombona (Jose Manuel)
    #   Dedicatoria a mis panas y colegas Erwin Mujica y Gabriel Zuleta por sus consejos a la hora de la realizacion de este codigo    
    #   Dedicatoria a la Ing. Maille Altue por apoyar y corregir este proyecto