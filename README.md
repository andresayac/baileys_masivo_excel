# bio_planta

## Deploy WINDOWS python 3.8

1. Clone project
2. Setup venv with python 3.10 `py -3.10 -m venv ./venv`
3. Activate venv `.\venv\Scripts\activate`
4. Install requirements `pip install -r requirements.txt`
5. Create exe service for windows `pyinstaller --onefile --hidden-import win32timezone masivo_whatsapp.py`