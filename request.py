from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import base64

uri = "mongodb+srv://root:123@cluster0.44vuc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

def enviar_json(dados):
    try:
        db = client["hackathon"] 
        collection = db["hackathon"] 
        resultado = collection.insert_one(dados)
        print(f"Documento inserido com ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"Erro ao inserir documento: {e}")
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def sendImage(img):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")

        json_exemplo = {
            "nr_lote": 1,
            "nr_ocorrencia": 3,
            "img_ocorrencia": image_to_base64(img)
        }
        enviar_json(json_exemplo)
    except Exception as e:
        print(e)
sendImage("frame.jpg")