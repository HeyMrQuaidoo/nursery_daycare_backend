import json
import requests
from app.core.config import settings


class WhatsAppService:
    def __init__(self, access_token: str = settings.WHATSAPP_KEY):
        self.url = "https://graph.facebook.com/v21.0/493482393845710/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def send_message(
        self,
        recipient: str,
        template_name: str,
        header_text: str,
        language_code: str = "en",
    ):
        """
        Sends a WhatsApp template message.

        :param recipient: Recipient's phone number in international format (e.g., 233591906002).
        :param template_name: Name of the WhatsApp template to use (e.g., "onboarding").
        :param header_text: Text to be sent as the header parameter in the template.
        :param language_code: Language code for the template (default is "en").
        :return: Response object from the API call.
        """
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": [
                    {
                        "type": "header",
                        "parameters": [{"type": "text", "text": header_text}],
                    }
                ],
            },
        }

        try:
            response = requests.post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
