# utils/sms.py

from django.core.cache import cache
import vonage
from vonage import Auth
import random


VONAGE_API_KEY = "81b0b229"
VONAGE_API_SECRET = "4LiJV7YIeq20t6NX"

def send_sms_code(phone):
    code = str(random.randint(100000, 999999))

    auth = Auth(api_key=VONAGE_API_KEY, api_secret=VONAGE_API_SECRET)
    client = vonage.Vonage(auth)  # передаем объект Auth

    sms = client.sms  # у клиента есть свойство sms, через которое отправляем

    response = sms.send({
        "from_": "UzumMarket",
        "to": phone,
        "text": f"Ваш код подтверждения: {code}",
    })
    print("Response:", response)
    print("Response messages:", response.messages)
    first_message = response.messages[0]
    print("First message status:", first_message.status)

    if first_message.status != "0":
        # Попробуем вывести статус и сетевой код для диагностики
        raise Exception(f"Ошибка отправки: статус {first_message.status}, network {first_message.network}")

    cache.set(f"verify_code:{phone}", code, timeout=120)
    return code
