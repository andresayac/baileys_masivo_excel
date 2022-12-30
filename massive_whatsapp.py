
import warnings
import argparse
import os
from functions import *
import time
from datetime import datetime

warnings.simplefilter(action='ignore', category=UserWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True)
parser.add_argument("-s", "--session", required=False)
parser.add_argument("-a", "--api", required=False)


args = parser.parse_args()

file_excel =  args.file if args.file is not None else 'Template_Masivo.xlsx'
session_id = args.session if args.session is not None else 'tmpsession'
api_url = args.api if args.api is not None else 'http://127.0.0.1:8000'

print(f"-----------------------------------------------------")
print(f"Archivo Excel: {file_excel}")
print(f"Session Whatsapp: {session_id}")
print(f"Api URL: {api_url}")
print(f"-----------------------------------------------------")

if not os.path.isfile(file_excel):
    print(f"El archivo de excel {file_excel} no existe")
    exit()

if not validate_session_name(session_id):
    print(f"El nombre de la session {session_id} no es valido utiliza solo letras y numeros")
    exit()

if not valid_session(api_url, session_id):
    print(f"La session {session_id} no es valida")
    print(f"Creando session {session_id}")
    data_create = create_session(api_url, session_id)
    if data_create['success']:
        retry = 0
        print("Imprimiendo QR")
        while retry< 5:           
            retry += 1
            print(f"Tiempo de espera para un nuevo qr: 60 segundos intento: {retry} de 5")
            genera_qr((data_create['data']['qr']).replace('data:image/png;base64,', ''))
            if sleep_check_session(api_url, session_id):
                break   
            if retry == 5:
                exit("No se pudo crear la session intentos maximos alcanzados")

            data_create = create_session(api_url, session_id)    

data = read_xlsx_file(file_excel)
data_final = []
print(f"-----------------------------------------------------")
for row in data:
    phone_number = str(row[0])
    message = (row[1])
    tipo_mensaje = (row[2])
    if phone_number is None:
        continue
    print(f"Enviando mensaje a {phone_number} tipo {tipo_mensaje}")
    status = False
    res_message = ""
    match tipo_mensaje:
        case "TEXTO":
            responde = send_text_message(api_url, session_id, phone_number, message)
            status = responde['success']
            res_message = responde['message']
        case "IMAGEN":
            responde = send_image_message(api_url, session_id, phone_number, message)
            status = responde['success']
            res_message = responde['message']
        case "DOCUMENTO":
            responde = send_document_message(api_url, session_id, phone_number, message)
            status = responde['success']
            res_message = responde['message']
        case "VIDEO":
            responde = send_video_message(api_url, session_id, phone_number, message)
            status = responde['success']
            res_message = responde['message']
        case "GIF":
            responde = send_gif_message(api_url, session_id, phone_number, message)
            status = responde['success']
            res_message = responde['message']
        case _:
            status = False
            res_message = "Tipo de mensaje no valido"
            continue
    
    if not status:
        data_final.append([phone_number,message,tipo_mensaje,"ERROR",res_message])
    else:
        data_final.append([phone_number,message,tipo_mensaje,"ENVIADO",res_message])

print(f"-----------------------------------------------------")
print(f"     Archivo  de resultados: envio_final.xlsx        ")
print(f"-----------------------------------------------------")

create_xlsx_file(data_final, f"envio_final.xlsx")