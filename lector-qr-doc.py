import cv2 # Librería para procesamiento de video y visión por computadora
import mysql.connector # Librería para interactuar con bases de datos MySQL
import re 
import os # Librería para manipular rutas y archivos
import time # Librería para manejar tiempo y retardos
import threading  # Librería para ejecutar tareas en hilos
import pytesseract as tess # Librería para reconocimiento óptico de caracteres (OCR)
from PIL import Image # Librería para manejo de imágenes
from datetime import datetime # Librería para manejar fechas y horas

# Configuración de la ruta de instalación de Tesseract OCR (INSTALAR Tesseract OCR)
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Conexión a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",  
    user="root",             
    password="",             
    database="registro_ingresos" 
)

# Configuración del acceso a la cámara de video
cap = cv2.VideoCapture("http://192.168.1.2:4747/video")

# Función para escanear códigos QR
def escanear_qr(frame, conexion):
    cursor = conexion.cursor()
    # Verifica si se detectó un QR en el frame
    if ret_qr:
            # Dibuja los puntos de la región del QR detectado
            for point in points:
                color = (0, 255, 0)
                frame = cv2.polylines(frame, [point.astype(int)], True, color, 8)

            # Condicional si el Qr tiene datos
            if dato_qr:
                consulta_existencia = "SELECT id_llave FROM llaves WHERE dato_llave = %s"
                cursor.execute(consulta_existencia, (dato_qr[0],))
                resultado = cursor.fetchone()

                # Condicional de inserción a la base de datos si la llave no está registrada
                if resultado is None:
                    iUrl = "INSERT INTO llaves (llave_tipo, dato_llave, ruta_llave) VALUES (%s, %s, %s)"
                    try:
                        cursor.execute(iUrl, ("Qr", dato_qr[0], "Pendiente"))
                        conexion.commit()
                        print(f"Información insertada: {dato_qr[0]}")
                    except mysql.connector.Error as e:
                        print(f"Error al insertar la URL: {e}")
                        
                # Condicional si la llave está registrada. Inserta datos de ingreso
                else:
                    id_llave = resultado[0]
                    iIngreso = "INSERT INTO ingresos (llave_ingreso) VALUES (%s)"
                    try:
                        cursor.execute(iIngreso, (id_llave,))
                        conexion.commit()
                        print(f"Ingreso registrado para Qr: {dato_qr[0]}")
                    except mysql.connector.Error as e:
                        print(f"Error al registrar ingreso: {e}")
    return frame

# Función para procesar documentos detectados y extraer texto con OCR          
def procesar_imagen(doc_recortado, ruta_carpeta, conexion):
    cursor = conexion.cursor()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    ruta_imagen = os.path.join(ruta_carpeta, f'doc_imgp_{timestamp}.jpg')
    cv2.imwrite(ruta_imagen, doc_recortado)

    imagen = Image.open(ruta_imagen)
    texto = tess.image_to_string(imagen) # Extrae texto de la imagen usando OCR

    #Depuración de datos extraidos y busqueda de datos segun patrones
    texto_limpio = re.sub(r'\b(NUMERO|APELLIDO|NOMBRE)\b', '', texto, flags=re.IGNORECASE)

    matchCedula = re.search(r'\d{1,3}(?:\.\d{3}){2,3}', texto)
    cedula = matchCedula.group() if matchCedula else "No encontrada"

    matchApellidos = re.search(r'\d{1,3}(?:\.\d{3}){2,3}\n([A-ZÁÉÍÓÚÑ ]+)', texto)
    apellidos = matchApellidos.group(1).strip() if matchApellidos else "No encontrados"

    matchNombres = re.search(r'[A-ZÁÉÍÓÚÑ ]+\n[^\w]*\n([A-ZÁÉÍÓÚÑ ]+)', texto)
    nombres = matchNombres.group(1).strip() if matchNombres else "No encontrados"

    print('\n', '----Datos Extraídos----')
    print('Número de Cédula: ', cedula)
    print('Apellidos: ', apellidos)
    print('Nombres: ', nombres, '\n')

    # Validar si la variable "cedula" es deiferente al valor "No encontrada"
    if cedula != "No encontrada":
        cedula_depurada = cedula.replace(".", "")
        consulta_existencia = "SELECT id_llave FROM llaves WHERE dato_llave = %s"
        cursor.execute(consulta_existencia, (cedula_depurada,))
        resultado = cursor.fetchone()

        # Condicional de inserción a la base de datos si la llave no está registrada
        if resultado is None:
            iCedula = "INSERT INTO llaves (llave_tipo, dato_llave, ruta_llave) VALUES (%s, %s, %s)"
            try:
                cursor.execute(iCedula, ("Documento", cedula_depurada, ruta_imagen))
                conexion.commit()
                print(f"Documento insertado en la base de datos: {cedula_depurada}")
            except mysql.connector.Error as e:
                print(f"Error al insertar documento: {e}")

        # Condicional si la llave está registrada. Inserta datos de ingreso    
        else:
            id_llave = resultado[0]
            iIngreso = "INSERT INTO ingresos (llave_ingreso) VALUES (%s)"
            try:
                cursor.execute(iIngreso, (id_llave,))
                conexion.commit()
                print(f"Ingreso registrado para la cédula: {cedula_depurada}")
            except mysql.connector.Error as e:
                print(f"Error al registrar ingreso: {e}")
    else:
        print("Documento no encontrado, repita el escaneo")

# Configuración de la carpeta para guardar imágenes procesadas
ruta_carpeta = 'D:/Ideas-tico/tarea-1/cedulas' # Ruta donde se guardarán las imágenes de documentos
os.makedirs(ruta_carpeta, exist_ok=True)
ultimo_escaneo = 0 # Variable para controlar la frecuencia de escaneos

# Bucle principal para capturar video y procesar QR y documentos     
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar video")
        break

    qrCode = cv2.QRCodeDetector() # Inicializa el detector de códigos QR
    ret_qr, dato_qr, points, _ = qrCode.detectAndDecodeMulti(frame)

    imagenGris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imagenGris = cv2.GaussianBlur(imagenGris, (5, 5), 0)

    bordes = cv2.Canny(imagenGris, 50, 150) # Detecta bordes en la imagen

    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

     # Parámetros mínimos para considerar un contorno como un documento
    ancho_minimo = 150  
    alto_minimo = 100  

    documento_detectado = False

    # Recorre los contornos encontrados
    for contorno in contornos:
        epsilon = 0.02 * cv2.arcLength(contorno, True)
        aproximado = cv2.approxPolyDP(contorno, epsilon, True)

        if len(aproximado) == 4 and cv2.contourArea(aproximado) > 5000:
            x, y, w, h = cv2.boundingRect(aproximado)

            # Validación de tamaños para evitar identificar un Qr como documento
            if w >= ancho_minimo and h >= alto_minimo:
                documento_detectado = True
                doc_recortado = imagenGris[y:y+h, x:x+w]
                cv2.drawContours(frame, [aproximado], -1, (0, 255, 0), 3)
                break

    # Procesa el QR si fue detectado
    if ret_qr and dato_qr:
        tiempo_actual = time.time()
        if tiempo_actual - ultimo_escaneo >= 4: # Control de escaneo en intervalos de 4seg
            print(f"QR detectado: {dato_qr[0]}")
            frame = escanear_qr(frame, conexion) # Llama a la función para manejar el QR
            ultimo_escaneo = tiempo_actual

    # Procesa el documento si fue detectado
    elif documento_detectado:
        tiempo_actual = time.time()
        if tiempo_actual - ultimo_escaneo >= 4: # Control de escaneo en intervalos de 4seg
            cv2.imshow("Documento Detectado: ", doc_recortado) # Muestra el documento recortado
            threading.Thread(target=procesar_imagen, args=(doc_recortado, ruta_carpeta, conexion)).start()
            ultimo_escaneo = tiempo_actual

    # Muestra el video en tiempo real
    cv2.imshow("Lector!", frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Libera la captura de video y cierra todas las ventanas abiertas
cap.release()
cv2.destroyAllWindows()