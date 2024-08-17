# import json
# import time
# import base64
# import requests


# class Text2ImageAPI:

#     def __init__(self, url, api_key, secret_key):
#         self.URL = url
#         self.AUTH_HEADERS = {
#             'X-Key': f'Key {api_key}',
#             'X-Secret': f'Secret {secret_key}',
#         }

#     def get_model(self):
#         response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
#         data = response.json()
#         return data[0]['id']

#     def generate(self, prompt, model, images=1, width=1024, height=1024):
#         params = {
#             "type": "GENERATE",
#             "numImages": images,
#             "width": width,
#             "height": height,
#             "generateParams": {
#                 "query": f"{prompt}"
#             }
#         }

#         data = {
#             'model_id': (None, model),
#             'params': (None, json.dumps(params), 'application/json')
#         }
#         response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
#         data = response.json()
#         return data['uuid']

#     def check_generation(self, request_id, attempts=10, delay=10):
#         while attempts > 0:
#             response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
#             data = response.json()
#             if data['status'] == 'DONE':
#                 return data['images']

#             attempts -= 1
#             time.sleep(delay)


# if __name__ == '__main__':
#     api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'EFD7793C923FEE86E21A935C2EAAA365', 'CBBB9C649E0BB235E86FBC46CF625C1A')
#     model_id = api.get_model()
#     uuid = api.generate("Sun in sky", model_id)
#     images = api.check_generation(uuid)
#     # Здесь image_base64 - это строка с данными изображения в формате base64
#     image_base64 = images[0] # Вставьте вашу строку base64 сюда
#     # Декодируем строку base64 в бинарные данные
#     image_data = base64.b64decode(image_base64)
#     # Открываем файл для записи бинарных данных изображения
#     with open("image.jpg", "wb") as file:
#         file.write(image_data)
#         print("AAA")

# #Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.

import requests

API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney-v4"
headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content
image_bytes = query({
	"inputs": "Astronaut riding a horse",
})
# You can access the image with PIL.Image for example
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))