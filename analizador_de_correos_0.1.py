#!/usr/bin/env python3

import sys
import os
import subprocess
import importlib.util
import time
from time import sleep

def en_entorno_virtual():
    # Compara el prefijo actual con el prefijo base de la instalación de Python.
    # Si son diferentes, significa que estamos dentro de un entorno virtual.
    return sys.prefix != sys.base_prefix

def verificar_dependencias():
    nombre_venv = "entorno_correos"
    venv_dir = os.path.abspath(nombre_venv)
    
    # Detección del sistema operativo para definir la ruta correcta del ejecutable de Python.
    # 'nt' corresponde a Windows, de lo contrario se asume un sistema tipo Unix (Linux/macOS).
    if os.name == 'nt':
        venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(venv_dir, "bin", "python")

    # Diccionario con las librerías requeridas: 'nombre_modulo': 'nombre_paquete_pip'
    dependencias = {
        'rich': 'rich', 
        'extract_msg': 'extract-msg', 
        'requests': 'requests'
    }
    todos_los_paquetes = list(dependencias.values())

    # Bloque 1: Gestión del entorno virtual si no estamos dentro de uno
    if not en_entorno_virtual():
        # Si el entorno ya existe físicamente, nos cambiamos a él sin preguntar.
        if os.path.exists(venv_python):
            print(f"Entorno virtual '{nombre_venv}' detectado. Cambiando a él de forma segura...")
            sleep(2)
            # os.execv reemplaza el proceso actual por el nuevo, evitando procesos anidados.
            os.execv(venv_python, [venv_python] + sys.argv)
            return
        
        # Si no existe, informamos al usuario y pedimos confirmación para crearlo.
        print("Analizador de correos v0.1")
        print("Para evitar errores de seguridad, el programa debe ejecutarse en un Entorno Virtual.")
        respuesta = input(f"¿Deseas que el programa cree el entorno '{nombre_venv}' y se configure automáticamente? (s/N): ").strip().lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            print(f"\n\tCreando entorno virtual aislado en la carpeta '{nombre_venv}'...")
            # Llamada al sistema para crear el entorno virtual usando el módulo venv.
            resultado = subprocess.run([sys.executable, "-m", "venv", nombre_venv])
            
            # Manejo de error común en Linux (ej. Ubuntu) donde python3-venv no viene preinstalado.
            if resultado.returncode != 0:
                print("\n\tTu sistema operativo requiere que instales el gestor de entornos primero.")
                print("\n\t\t\"sudo apt install python3-venv\"\n")
                sys.exit(1)
                
            print("\tInstalando TODAS las librerías necesarias en el entorno nuevo... (por favor espera)")
            try:
                # Instalación silenciosa de las dependencias usando pip.
                subprocess.check_call(
                    [venv_python, "-m", "pip", "install"] + todos_los_paquetes,
                    stdout=subprocess.DEVNULL, # Oculta los mensajes normales
                    stderr=subprocess.DEVNULL  # Oculta los mensajes de error
                )
                print("\tEntorno preparado con éxito.")
                sleep(1.3)
                print("\tRelanzando el programa de forma segura...\n")
                sleep(2)
                # Reiniciamos el script, pero ahora usando el Python del nuevo entorno virtual.
                os.execv(venv_python, [venv_python] + sys.argv)
            except subprocess.CalledProcessError:
                print("\n\tHubo un error al instalar los paquetes en el entorno virtual.")
                sys.exit(1)
        else:
            # Salida controlada con efecto visual de puntos suspensivos.
            print("\n\tSaliendo.", end="", flush=True)
            sleep(1)
            print(".", end="",flush=True)
            sleep(0.7)
            print(".")
            sleep(0.7)
            sys.exit(1)

    # Bloque 2: Verificación de dependencias (se ejecuta si ya estamos en un entorno)
    faltantes = []
    for modulo, paquete in dependencias.items():
        # importlib verifica si el módulo está disponible sin necesidad de importarlo realmente.
        if importlib.util.find_spec(modulo) is None:
            faltantes.append(paquete)

    # Si no falta ninguna librería, terminamos la verificación y el programa principal puede continuar.
    if not faltantes:
        return 
        
    # Si faltan librerías dentro del entorno, pedimos permiso para instalarlas.
    print("\tFaltan requisitos previos en este entorno virtual:")
    print(f"\t\tLibrerías faltantes: {', '.join(faltantes)}\n")
    
    respuesta = input("¿Deseas instalar las dependencias faltantes ahora? (s/N): ").strip().lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n\tInstalando dependencias... (por favor espera)")
        
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install"] + faltantes,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("\tInstalación completada. Relanzando...\n")
        # Reiniciamos para que Python reconozca las librerías recién instaladas.
        os.execv(sys.executable, [sys.executable] + sys.argv)
    else:
        print("\n\tEl programa no puede continuar. Saliendo...")
        sys.exit(1)

# Punto de entrada de la verificación
verificar_dependencias()