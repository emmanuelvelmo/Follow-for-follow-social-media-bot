import pyautogui
import numpy
import cv2
import pytesseract
import time
import datetime
import os
import re

# Escribir mensaje
def gen_escribir_msg(val_msg):
    pyautogui.typewrite(val_msg)
    pyautogui.press('enter')
    time.sleep(2)

# Buscar en txt y asignar valor a variable
def gen_busq_txt(ruta_txt, pos_linea):
    # Verifica si el archivo txt existe en su directorio
    if os.path.isfile(ruta_txt):
        # Leer el contenido del archivo
        with open(ruta_txt, 'r') as ref_txt:
            # Contador de líneas
            cont_linea = 0
            
            # Iterar cada línea del archivo
            for linea_tmp in ref_txt:
                # Moverse hasta la línea
                if cont_linea == pos_linea and linea_tmp != '':
                    # Limpiar espacios en blanco y retornar
                    return linea_tmp.strip()
                    
                cont_linea += 1

# Actualizar línea en txt
def gen_act_txt(ruta_txt, pos_linea, tmp_palabra):
    # Verifica si el archivo txt existe en su directorio
    if os.path.isfile(ruta_txt):
        # Leer el contenido del archivo
        with open(ruta_txt, 'r') as ref_txt:
            tmp_lineas = ref_txt.readlines()

        # Actualizar la línea en la posición deseada
        tmp_lineas[pos_linea] = tmp_palabra + '\n'

        # Escribir el contenido actualizado en el archivo
        with open(ruta_txt, 'w') as ref_txt:
            ref_txt.writelines(tmp_lineas)

# Diferencia de horas entre fecha actual y previa
def gen_dif_hr(fecha_tmp):
    # Obtener la fecha y hora actual
    fecha_act = datetime.datetime.now()
    
    # Convertir fecha previa de string a datetime
    fecha_prev = datetime.datetime.strptime(fecha_tmp, "%Y-%m-%d-%H:%M:%S")
    
    dif_hr = (fecha_act - fecha_prev).total_seconds() / 3600
    
    return dif_hr

# Guardar fecha actual en archivo
def gen_act_fecha(ruta_txt):
    # Obtener la fecha y hora actual
    fecha_act = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    
    # Actualizar fecha en txt
    gen_act_txt(ruta_txt, 0, fecha_act)

# Convertir imagen a escala de grises
def gen_escala_grises(tmp_img):
    # Convertir la imagen a un array de numpy
    arr_numpy = numpy.array(tmp_img)

    # Convertir la imagen de RGB a BGR
    img_bgr = cv2.cvtColor(arr_numpy, cv2.COLOR_RGB2BGR)

    # Convertir la imagen a escala de grises y retornar
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# Capturar pantalla y convertir a escala de grises
def gen_capt_pant():
    # Capturar la pantalla
    tmp_screenshot = pyautogui.screenshot()
    
    # Convertir a escala de grises y retornar
    return gen_escala_grises(tmp_screenshot)

# Capturar un área específica de la pantalla y convertir a escala de grises
def gen_capt_spec_pant(vis_box):
    # Captura una región específica de la pantalla
    tmp_screenshot = pyautogui.screenshot(region=(vis_box[0], vis_box[1], vis_box[2], vis_box[3]))
    
    # Convertir a escala de grises y retornar
    return gen_escala_grises(tmp_screenshot)

# Actualizar ratio entre seguidos y seguidores
def gen_act_ratio(val_seguidos, val_seguidores):
    # Evitar error de división entre cero
    if val_seguidores == 0: val_seguidores = 1
    
    return val_seguidos / val_seguidores

# Obtener texto de una imagen
def gen_text_img(tmp_img):
    # Usa pytesseract para extraer el texto de la imagen
    val_text = pytesseract.image_to_string(tmp_img)
    
    # Limpiar espacios en blanco y retornar
    return val_text.strip()

# Buscar una cifra anterior a una palabra
def gen_cifra_palabra(tmp_text, tmp_palabra):
    # Buscar la palabra en el texto usando expresión regular
    tmp_match = re.search(r'(\d+)(?=\s*' + re.escape(tmp_palabra) + r'\b)', tmp_text)
    
    # Si hay un punto, una K o una M a la derecha del último dígito de la cifra, anular cifra
    
    
    # Si se encuentra una coincidencia, devolver el número
    if tmp_match:
        return int(tmp_match.group(1))
    else:
        # Si no se encuentra la palabra o la cifra, retornar cero
        return 0

# Obtener una cifra a partir de imagen y una palabra
def gen_cifra(tmp_img, tmp_palabra):
    # Obtener texto de la imagen sin espacios
    tmp_text = gen_text_img(tmp_img)
    
    # Obtener número desde el texto y retornar
    return gen_cifra_palabra(tmp_text, tmp_palabra)

# Coordenadas del elemento a encontrar
gen_centro_xy = [0, 0]

# Cambiar coordenadas de la variable génerica de coordenadas
def gen_camb_coords(tmp_coords):
    global gen_centro_xy
    
    gen_centro_xy[0] = tmp_coords[0]
    gen_centro_xy[1] = tmp_coords[1]

# Hacer click sobre una posición específica
def gen_click_spec(val_tiempo):
    pyautogui.moveTo(gen_centro_xy[0], gen_centro_xy[1])
    
    pyautogui.click()
    time.sleep(val_tiempo)

# Hacer click sobre una posición específica y abrir en otra pestaña
def gen_ab_click_spec(val_tiempo):
    pyautogui.moveTo(gen_centro_xy[0], gen_centro_xy[1])
    
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    time.sleep(0.1)
    pyautogui.click()
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    time.sleep(val_tiempo)

# Calcular centro de un campo de captura
def gen_calc_cent(vis_box):
    global gen_centro_xy
    
    # Asinar puntos medios del rectángulo
    gen_centro_xy[0] = round(vis_box[0] + (vis_box[2] / 2))
    gen_centro_xy[1] = round(vis_box[1] + (vis_box[3] / 2))

# Calcular centro de un campo de captura y retornar coordenadas
def gen_calc_cent_rtn(vis_box):
    # Variable a retornar
    tmp_xy = [0,0]
    
    # Asinar puntos medios del rectángulo
    tmp_xy[0] = round(vis_box[0] + (vis_box[2] / 2))
    tmp_xy[1] = round(vis_box[1] + (vis_box[3] / 2))
    
    return tmp_xy

# Conservar primera línea con texto de una captura de texto
def gen_limp_text(tmp_text):
    # Eliminar líneas en blanco
    lins_text = [lin_it.strip() for lin_it in tmp_text.splitlines() if lin_it.strip()]
    
    # Eliminar todas las líneas excepto la primera
    if lins_text:
        prim_lin = lins_text[0]
    else:
        prim_lin = ''
    
    # Eliminar espacios en blanco para la línea conservada
    prim_lin_limp = prim_lin.strip()
    
    return prim_lin_limp

# Obtener la primera línea de texto de una captura de pantalla en área específica
def gen_prim_lin(tmp_img):
    # Obtener texto de la imagen
    tmp_text = gen_text_img(tmp_img)
    
    # Obtener primer línea del texto
    prim_lin = gen_limp_text(tmp_text)
    
    return prim_lin

gen_usr_ref = ''

# Asignar nombre del primer usuario en lista y asignar coordenadas
def gen_prim_usr(vis_box):
    global gen_usr_ref
    
    # Capturar un área específica de la pantalla
    tmp_img = gen_capt_spec_pant(vis_box)
    
    # Actualizar usuario de referencia
    gen_usr_ref = gen_prim_lin(tmp_img)
    
    # Calcular coordenas para el usuario de referencia
    gen_calc_pos_text(tmp_img, gen_usr_ref)
    
    # Corregir coordenadas
    gen_aj_coords(vis_box)

# Desplazar hacia el siguiente usuario
def gen_desp_usr(vis_box):
    while True:
        # Capturar región en pantalla
        tmp_img = gen_capt_spec_pant(vis_box)
        
        # Obtener texto de referencia
        tmp_text = gen_prim_lin(tmp_img)
        
        # Evaluar si el nombre del usuario está presente
        if tmp_text == gen_usr_ref:
            # Desplazar hacia abajo
            pyautogui.mouseDown(button='middle')
            pyautogui.moveRel(0, 20)
            time.sleep(0.25)
            pyautogui.mouseUp(button='middle')
            pyautogui.moveRel(0, -20)
        else:
            # Dejar de desplazar hacia abajo
            break

# Asignar coordenadas de un objeto en pantalla
def gen_coinc_imgs(base_img, ref_img):
    global gen_centro_xy
    
    #

# Asignar coordenadas de un texto en pantalla
def gen_calc_pos_text(tmp_img, text_ref):
    global gen_centro_xy
    
    # Realizar OCR y obtener textos
    texts_img = pytesseract.image_to_data(tmp_img, output_type=pytesseract.Output.DICT)
    
    # Obtener el número total de elementos tipo texto
    num_texts = len(texts_img['text'])
    
    # Iterar y comparar cada una de las palabras de la imagen
    for iter_elem in range(num_texts):
        if int(texts_img['conf'][iter_elem]) > 0:
            tmp_text = texts_img['text'][iter_elem].strip()
            
            if any(tmp_text in eval_ch for eval_ch in text_ref.split()):
                # Obtener las coordenadas X1,Y1, X4,Y4 del bloque de texto
                x1 = texts_img['left'][iter_elem]
                y1 = texts_img['top'][iter_elem]
                x4 = x1 + texts_img['width'][iter_elem]
                y4 = y1 + texts_img['height'][iter_elem]
                
                # Calcular coordenada central del objeto
                gen_centro_xy[0] = round((x1 + x4) / 2)
                gen_centro_xy[1] = round((y1 + y4) / 2)
                
                break

# Ajustar coordenadas
def gen_aj_coords(vis_box):
    global gen_centro_xy
    
    # Sumar a X,Y en gen_centro_xy X1,Y1 en campo de captura de imagen
    gen_centro_xy[0] += vis_box[0]
    gen_centro_xy[1] += vis_box[1]

gen_camb_bl = False

# Cambiar el valor del bool
def gen_f_camb_bl(val_bl):
    global gen_camb_bl
    
    gen_camb_bl = val_bl

# Evaluar cambio en el entorno
def gen_camb_entn(capt_1, capt_2):
    global gen_camb_bl
    
    if cv2.norm(capt_1, capt_2, cv2.NORM_L2) > 40000:
        gen_camb_bl = True
    else:
        gen_camb_bl = False

# Encontrar posición de un elemento visual
def gen_calc_pos_vis(capt_pant, nom_ref_img):
    # Cargar imagen de referencia
    with open('Autorun/TikTok/Refs/' + nom_ref_img, 'rb') as tmp_arch:
        tmp_img = tmp_arch.read()
    
    # Convertir imagen de referencia a escala de grises
    ref_img = gen_escala_grises(tmp_img)
    
    # Comparar imágenes y asignar coordenadas
    coords_fig = gen_coinc_imgs(capt_pant, ref_img)
    
    # Actualizar coordenadas del objeto encontrado
    gen_calc_cent(coords_fig)