from pymongo import MongoClient
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os.path

# Configuración de la conexión a MongoDB
client = MongoClient(
    'mongodb+srv://admin:admin@clustertfm.foevo.mongodb.net/tfm?retryWrites=true&w=majority')
db = client['tfm']

# Configuración de autenticación con Google Drive
if not os.path.exists("credenciales.txt"): # Si no existe fichero de credenciales, pedir autenticación al usuario
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile("credenciales.txt")