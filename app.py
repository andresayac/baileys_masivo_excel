
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


print(f"Archivo Excel: {file_excel}")
print(f"Session Whatsapp: {session_id}")
print(f"Api URL: {api_url}")


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
        print("imprimiendo QR")
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

for row in data:
    phone_number = str(row[0])
    message = (row[1])
    tipo_mensaje = (row[2])
    if phone_number is None:
        continue
    print(f"Enviando mensaje a {phone_number} tipo {tipo_mensaje}")
    status = False
    """  match tipo_mensaje:
        case "TEXTO":
            status = send_text_message(api_url, session_id, phone_number, message)
        case "IMAGEN":
           status = send_image_message(api_url, session_id, phone_number, message)
        case "DOCUMENTO":
            status = send_document_message(api_url, session_id, phone_number, message)
        case "VIDEO":
            status = send_video_message(api_url, session_id, phone_number, message)
        case "GIF":
            status = send_gif_message(api_url, session_id, phone_number, message)
        case _:
            status = False
            continue """
    
    if not status:
        data_final.append([phone_number,message,tipo_mensaje,"ERROR"])
    else:
        data_final.append([phone_number,message,tipo_mensaje,"ENVIADO"])

create_xlsx_file(data_final, f"envio_final.xlsx")