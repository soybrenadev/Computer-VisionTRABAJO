import cv2
import time
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os

CARPETA_PERSONAS = "personas"
ARCHIVO_REGISTROS = "registros.csv"

def registrar_asistencia(nombre):
    ahora = datetime.now()
    fecha =ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    datos = {
        "Nombre": nombre,
        "Fecha": fecha,
        "Hora": hora,
        "Verificacion": "Verificado por reconocimiento facial"
    }

    df = pd.DataFrame([datos])

    if not os.path.exists(ARCHIVO_REGISTROS):
        df.to_csv(ARCHIVO_REGISTROS, index=False)
    else:
        df.to_csv(ARCHIVO_REGISTROS, mode='a', header=False, index=False)

    print(f"Bienvenido {nombre} - {fecha} - {hora} - Verificado exitoso")
    print(f"📧 Notificando al encargado sobre la asistencia de {nombre}...")


def registrar_persona():
    nombre = input("Ingresa el nombre de la persona: ")

    ruta = os.path.join(CARPETA_PERSONAS, nombre)
    os.makedirs(ruta, exist_ok=True)

    cap = cv2.VideoCapture(0)
    print(f"Camara lista. Presiona 'c' para tomar la foto...")

    while True:

        ret, frame = cap.read()
        cv2.imshow("Registrar persona", frame)

        if cv2. waitKey(1) & 0xFF == ord('c'):
            ruta_foto = os.path.join(ruta, "foto1.jpg")
            cv2.imwrite(ruta_foto, frame)
            print(f"{nombre} registrado correctamente")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


def iniciar_sistema():
    cap = cv2.VideoCapture(0)
    print("Camara iniciada, buscando rostro...")

    # Muestra cámara fluida por 4 segundos primero
    inicio = time.time()
    while time.time() - inicio < 4:
        ret, frame = cap.read()
        cv2.imshow("Sistem de asistencia", frame)
        cv2.waitKey(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al acceder a la camara")
            break

        cv2.putText(frame, "Verificando en 4 segundos...", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Sistem de asistencia", frame)
        cv2.waitKey(500)

        try:
            for persona in os.listdir(CARPETA_PERSONAS):
                ruta_persona = os.path.join(CARPETA_PERSONAS, persona)

                if os.path.isdir(ruta_persona):
                    resultado = DeepFace.find(
                        img_path=frame,
                        db_path=ruta_persona,
                        enforce_detection=False,
                        silent=True
                    )

                    if len(resultado) > 0 and not resultado[0].empty:
                        registrar_asistencia(persona)
                        cap.release()
                        cv2.destroyAllWindows()
                        cv2.waitKey(1)
                        return

        except Exception as e:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":

    os.makedirs(CARPETA_PERSONAS, exist_ok=True)

    while True:
        print("---------Sistema de Asistencia Facial-----------")
        print("1. Registrar persona nueva")
        print("2. Verificar asistencia")
        print("3. Salir")

        opcion = input("Elige una opcion: ")

        if opcion == "1":
            registrar_persona()
        elif opcion == "2":
            if len(os.listdir(CARPETA_PERSONAS)) == 0:
                print("No hay personas registradas, primero registras a alguien")
            else:
                iniciar_sistema()
        elif opcion == "3":
            print("Hasta luego!")
            break
        else:
            print("Opcion no valida")