import requests
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID

def text_to_speech(text):

    url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    data = {
        "text": text,
        "lang": "ru-RU",
        "voice": "alena",
        "format": "oggopus"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        with open("voice.ogg", "wb") as f:
            f.write(response.content)
        return "voice.ogg"
    else:
        return None