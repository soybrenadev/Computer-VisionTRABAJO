# Proyecto 6: Computer Vision

# Sistema de Asistencia con Reconocimiento Facial 🎓

## Descripción
Este proyecto implementa un sistema de asistencia automatizada 
con reconocimiento facial, pensado para estudiantes. El alumno 
solo debe posar frente a la cámara y el programa verifica si 
está registrado. En caso de estarlo, confirma su asistencia y 
notifica al encargado de su llegada.

## Requisitos
- Python 3.9 o superior
- Cámara web o cámara integrada

## Instalación

1. Haz fork de este repositorio y clónalo:
git clone url_de_tu_repositorio

2. Ve a la carpeta del proyecto y crea tu entorno virtual:
python3 -m venv .venv

3. Activa el entorno virtual:
source .venv/bin/activate

4. Instala las dependencias:
pip install -r requirements.txt

## Uso

Ejecuta el programa:
python main.py

Sigue el menú:
- 1 — Registrar persona nueva
- 2 — Verificar asistencia
- 3 — Salir

## Nota
La primera vez que ejecutes el programa, deepface descargará 
su modelo de reconocimiento facial automáticamente. 
Esto solo ocurre una vez.