import cv2
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

    print(f"Bienvenido {nombre} - {fecha} - {hora} - Verificado")

def iniciar_sistema():
    cap = cv2.VideoCapture(0)
    print("Camara iniciada, buscando rostro...")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error al acceder a la camara")
            break

        cv2.imshow("Sistem de asistencia", frame)
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
                        return

        except Exception as e:
            pass

        if cv2. waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Sistema de Asistencia facial")
    print("Presiona 'q' para salir")
    iniciar_sistema()