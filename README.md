# Detector de Phishing (En Desarrollo)

Este proyecto es una herramienta en proceso de creación diseñada para analizar correos electrónicos y detectar posibles intentos de phishing o suplantación de identidad. El objetivo final de la aplicación será evaluar remitentes, enlaces y contenidos sospechosos para alertar al usuario sobre posibles fraudes antes de que interactúe con ellos.

## Estado Actual del Proyecto

Actualmente, el proyecto se encuentra en sus fases iniciales de desarrollo. El código escrito hasta ahora se enfoca en establecer una base de ejecución robusta, segura y completamente automatizada.

### ¿Qué hace el código actual?

El script actual funciona como un **Autoconfigurador de Entorno (Bootstrap)**. Dado que el análisis de correos requiere manipular archivos y hacer peticiones de red, es vital aislar las dependencias del sistema operativo del usuario. El código actual se encarga de lo siguiente:

1. **Aislamiento Automático de Seguridad:** Detecta si el usuario está ejecutando el programa en su instalación global de Python. Para evitar conflictos, crea automáticamente un entorno virtual aislado llamado `entorno_correos`.
2. **Instalación de Dependencias Core:** El script se asegura de que las librerías que darán vida al detector estén instaladas antes de continuar. Las librerías preparadas son:
   * `extract_msg`: Será el motor para leer y extraer metadatos, enlaces y texto de archivos de correo de Outlook (.msg).
   * `requests`: Se utilizará para analizar la reputación de las URLs extraídas o realizar consultas a bases de datos de amenazas.
   * `rich`: Se encargará de renderizar la interfaz en la terminal, mostrando advertencias de seguridad e informes de forma clara y estructurada.
3. **Transición Transparente:** Utiliza llamadas de bajo nivel (`os.execv`) para reiniciar el programa internamente dentro del entorno seguro, de modo que el usuario no tenga que activar el entorno manualmente.
4. **Validación de Módulos:** Revisa módulo por módulo que la instalación haya sido exitosa antes de pasar el control a lo que será la lógica principal del detector.

## Requisitos Previos

*   **Python 3.6 o superior.**
*   *Nota para usuarios de Linux (Debian/Ubuntu):* Si el sistema falla al intentar crear el entorno virtual, es probable que necesites instalar el módulo venv del sistema operativo. Puedes hacerlo ejecutando: `sudo apt install python3-venv`

## Uso

Para probar la fase actual del proyecto e inicializar el entorno de trabajo, ejecuta el script desde tu terminal:

> python analizador_de_correos.py

Tambien funciona con permisos de ejecucion:

> analizador_de_correos.py

El sistema te guiará de forma interactiva. Acepta la creación del entorno y la instalación de dependencias. Una vez finalizado el proceso, el sistema estará listo para recibir los próximos módulos de análisis de correos.

## Fuentes y Referencias

**Herramientas y Librerías:**
*   [Python 3 (Documentación Oficial)](https://docs.python.org/3/)
*   [extract-msg (PyPI)](https://pypi.org/project/extract-msg/)
*   [Requests (Documentación HTTP for Humans)](https://requests.readthedocs.io/)
*   [Rich (Documentación de interfaz de terminal)](https://rich.readthedocs.io/)

**Ciberseguridad e Inteligencia de Amenazas:**
*   [MITRE ATT&CK Framework - Técnica T1566 (Phishing)](https://attack.mitre.org/techniques/T1566/)
*   [APWG (Anti-Phishing Working Group)](https://apwg.org/)
*   [OWASP (Open Worldwide Application Security Project)](https://owasp.org/)
*   [Keepnet Labs - Ejemplos más comunes de correos de phishing](https://keepnetlabs.com/blog/most-common-phishing-email-examples-keepnet)