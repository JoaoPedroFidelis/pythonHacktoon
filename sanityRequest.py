import requests
import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def includeSanity(fileName):
    project_id = "ffzuhqrr"
    dataset = "production"
    token = "skNRDchppdMIoLLX1xeWOwaggNCkqz5nHJCpNnTDa1tjIhJnGGsKEj8B5PHrrf0uPV2DfoeGJAP0SbjooZmQyRJ281t4RBqVahsVGVHlQFFMUFuAuV8vPuHFeql73nK6h4cLOHvqGcTZWfbkSljsitWuKrkGw3IeuVBso6QGZWPdhJwvHdMS"
    document_id = id

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    url = f"https://{project_id}.api.sanity.io/v1/data/mutate/{dataset}"
    payload = {
        "mutations": [
            {
                "createOrReplace": {
                    "_id": None,
                    "_type": "testeSanityBase",  # Substitua pelo tipo de documento do seu schema
                    "base64": image_to_base64(fileName)
                }
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()