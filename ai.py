import requests
import asyncio
from config import GIGACHAT_TOKEN


def process_text(text: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GIGACHAT_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Отредактируй текст:
1. Расставь знаки препинания
2. Добавь ударения символом +
3. Сделай текст пригодным для озвучки

Текст:
{text}
"""

    data = {
        "model": "GigaChat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()["choices"][0]["message"]["content"]
