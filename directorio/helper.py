import json
import unicodedata
import requests
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

def send_whatsapp_message(message, phone):
    url = 'http://localhost:3001/lead'
    headers = {'Content-Type': 'application/json'}
    data = {
        'message': message,
        'phone': phone
    }
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            data=json.dumps(data),
            timeout=5  # Añadir timeout de 5 segundos
        )
        response.raise_for_status()
        return response
    except RequestException as e:
        logger.error(f"Error al enviar mensaje WhatsApp: {str(e)}")
        # No relanzar la excepción para que la aplicación continúe funcionando
        return None

def _unicode_ci_compare(s1, s2):
    normalized1 = unicodedata.normalize('NFKC', s1)
    normalized2 = unicodedata.normalize('NFKC', s2)

    return normalized1.casefold() == normalized2.casefold()

