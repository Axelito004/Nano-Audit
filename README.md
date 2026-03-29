# 🛡️ NanoAudit v5.0

![Version](https://img.shields.io/badge/Version-5.1%20Final-blue)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![OS](https://img.shields.io/badge/OS-Kali%20Linux-red)
![AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-purple)

**NanoAudit** es una herramienta automatizada para consola (CLI) diseñada para la auditoría forense de archivos y el análisis de vulnerabilidades en red. Está asistida por Inteligencia Artificial para generar informes técnicos legibles y procesables.

Desarrollada como proyecto de ingeniería de sistemas, esta suite combina el poder de escáneres clásicos con análisis heurístico y reportes dinámicos.

---

## ✨ Características Principales

* 📡 **Módulo de Red Táctica:**
  * Escaneo de descubrimiento (Ping Sweep) y estimación de SO vía TTL.
  * Auditoría profunda de servicios y versiones (basado en Nmap).
  * Pruebas de estrés de red (Flood Mode) con monitoreo de logs en tiempo real.
* 💾 **Módulo de Análisis Forense de Disco:**
  * Búsqueda heurística de software de piratería, cracks y keygens.
  * Integración profunda con **ClamAV**, incluyendo un *wrapper* personalizado para extraer y analizar amenazas ocultas dentro de archivos comprimidos propietarios (RAR, ZIP, TAR).
  * Pruebas de estrés I/O de disco para evaluación de hardware.
* 🤖 **Análisis Asistido por IA (Gemini 2.5):**
  * Envío de logs crudos a la IA para obtener informes ejecutivos estructurados (Hallazgos, Impacto, Mitigación).
  * Exportación automática de informes técnicos en formato PDF.
* 🔊 **Feedback Audiovisual:** Animaciones de carga multihilo y alertas sonoras de sistema con bypass de privilegios root.

---

## 🛠️ Requisitos Previos

NanoAudit está diseñado para funcionar en entornos **Debian/Kali Linux**. Requiere privilegios de superusuario (`sudo`) para la ejecución de escaneos de red a bajo nivel.

---
## 🔑 RECUERDA QUE NECESITAS TU PROPIA API KEY
## 🔑 ¿Cómo obtener tu API Key de Google Gemini?

NanoAudit utiliza el modelo **Gemini 2.5 Flash** para generar los informes ejecutivos. Para que el módulo de IA funcione, necesitas tu propia clave de acceso gratuita. Sigue estos pasos:

1. Visita la página oficial para desarrolladores: [Google AI Studio](https://aistudio.google.com/).
2. Inicia sesión con tu cuenta de Google normal.
3. En el panel lateral izquierdo, haz clic en el botón **"Get API key"** (Obtener clave de API).
4. Haz clic en el botón azul **"Create API key"** y selecciona un proyecto (o crea uno nuevo si te lo pide).
5. Copia la larga cadena de texto generada.
6. En la carpeta de NanoAudit, crea un archivo llamado exactamente `.env` y pega tu clave con este formato:

   ```env
   GOOGLE_API_KEY=AIzaSyTuClaveSecretaGeneradaAqui...

### Dependencias del Sistema OS
Asegúrate de tener instalados los siguientes paquetes en tu distribución Linux:
```bash
sudo python3 -m pip  google-generativeai python-dotenv colorama pyfiglet python-nmap fpdf --break-system-packages
sudo apt update && sudo apt install clamav install rar alsa-utils sox libsox-fmt-all
