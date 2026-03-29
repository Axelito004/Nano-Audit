# 🛡️ NanoAudit v5.1

![Version](https://img.shields.io/badge/Version-5.1%20Final-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
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

### Dependencias del Sistema OS
Asegúrate de tener instalados los siguientes paquetes en tu distribución Linux:
```bash
sudo apt update
sudo apt install clamav nmap stress-ng unrar alsa-utils sox -y
