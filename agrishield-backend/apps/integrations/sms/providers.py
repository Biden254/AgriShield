import requests
import logging
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class SMSProvider:
    """Abstract base class for SMS providers."""

    def send(self, phone_number: str, message: str) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")


class AfricaTalkingProvider(SMSProvider):
    """Africa's Talking SMS provider implementation."""

    BASE_URL = "https://api.africastalking.com/version1/messaging"

    def __init__(self):
        self.api_key = getattr(settings, "AT_API_KEY", None)
        self.username = getattr(settings, "AT_USERNAME", None)
        self.sender_id = getattr(settings, "SMS_SENDER_ID", None)

        if not all([self.api_key, self.username, self.sender_id]):
            logger.warning("⚠️ Missing Africa's Talking configuration in settings.")

    def send(self, phone_number: str, message: str) -> bool:
        headers = {
            "ApiKey": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "username": self.username,
            "to": phone_number,
            "message": message,
            "from": self.sender_id,
        }

        try:
            response = requests.post(
                self.BASE_URL,
                headers=headers,
                data=data,
                timeout=10,
            )
            response.raise_for_status()

            result = response.json()
            logger.info(
                f"✅ SMS sent to {phone_number} at {timezone.now()}. "
                f"Response: {result}"
            )
            return True

        except requests.RequestException as e:
            logger.error(f"❌ Request error while sending SMS to {phone_number}: {e}")
        except Exception as e:
            logger.exception(f"❌ Unexpected error sending SMS to {phone_number}: {e}")

        return False


# Factory function to get active provider
def get_sms_provider() -> SMSProvider:
    provider_name = getattr(settings, "SMS_PROVIDER", "").upper()

    if provider_name == "AFRICASTALKING":
        return AfricaTalkingProvider()

    raise ValueError(f"Unknown SMS provider: {provider_name}")


def send_sms(phone_number: str, message: str) -> bool:
    """Main function to send SMS via configured provider."""
    provider = get_sms_provider()
    return provider.send(phone_number, message)
