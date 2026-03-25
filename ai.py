from gigachat import GigaChat
from config import GIGACHAT_TOKEN

def process_text(text):

    prompt = f"""
Отредактируй текст:

1. Расставь все знаки препинания
2. Добавь ударения (используй символ ´ после гласной)
3. Сделай текст максимально читабельным

Текст:
{text}
"""

    with GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False) as giga:
        response = giga.chat(prompt)
        return response.choices[0].message.content