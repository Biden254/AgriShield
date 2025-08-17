from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json

from .providers import send_sms


@method_decorator(csrf_exempt, name="dispatch")
class SendSMSView(View):
    """
    API endpoint to send SMS.
    Expects JSON body: {"phone_number": "<recipient>", "message": "<text>"}
    """

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body.decode("utf-8"))
            phone_number = body.get("phone_number")
            message = body.get("message")

            if not phone_number or not message:
                return JsonResponse(
                    {"success": False, "error": "phone_number and message are required."},
                    status=400,
                )

            success = send_sms(phone_number, message)

            if success:
                return JsonResponse(
                    {"success": True, "message": f"SMS sent to {phone_number}."},
                    status=200,
                )
            else:
                return JsonResponse(
                    {"success": False, "error": "Failed to send SMS. Check logs."},
                    status=500,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON payload."}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"Unexpected error: {str(e)}"},
                status=500,
            )


# Simple health-check endpoint (useful for debugging providers)
@require_http_methods(["GET"])
def sms_health_check(request):
    return JsonResponse({"status": "ok", "provider": "active"})
