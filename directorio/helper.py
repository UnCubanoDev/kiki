import json
import unicodedata
import requests

def send_whatsapp_message(message, phone):
    url = 'http://207.244.233.96:3001/lead'
    headers = {'Content-Type': 'application/json'}
    data = {
        'message': message,
        'phone': phone
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code

def _unicode_ci_compare(s1, s2):
    normalized1 = unicodedata.normalize('NFKC', s1)
    normalized2 = unicodedata.normalize('NFKC', s2)

    return normalized1.casefold() == normalized2.casefold()

