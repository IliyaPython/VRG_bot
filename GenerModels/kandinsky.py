import requests, time, base64, json, os

from aiogram.types import FSInputFile

class Image:
    """Класс для генерации изображений при помощи Kandinsky."""

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        """Возвращает ИД модели для взаимодйествия с ней."""
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        print(data)
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

async def generate_image(Model: Image,
                   prompt: str = "Flowers",
                   filename: str = "ABEME"):
    print(prompt)
    model_id = Model.get_model()
    uuid = Model.generate(prompt, model_id)
    images = Model.check_generation(uuid)
    print(images)
    # Здесь image_base64 - это строка с данными изображения в формате base64
    image_base64 = images[0] # Вставьте вашу строку base64 сюда

    # Декодируем строку base64 в бинарные данные
    image_data = base64.b64decode(image_base64)

    # Открываем файл для записи бинарных данных изображения
    with open(f"{filename}.jpg", "wb") as file:
        file.write(image_data)
        print("SUCCESFULLY")

    image = FSInputFile(f"{filename}.jpg")
    return image

API = os.environ["Kand API Key"]
SECRET = os.environ["Kand Secret Key"]

Kandinsky = Image('https://api-key.fusionbrain.ai/', API, SECRET)