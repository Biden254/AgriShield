from django.shortcuts import render
import africastalking
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def ussd_callback(request):
    """
    Handles the USSD callback from Africa's Talking.
    """
    session_id = request.POST.get("sessionId")
    phone_number = request.POST.get("phoneNumber")
    text = request.POST.get("text")

    # Basic validation to ensure we have a phone number to reply to.
    if phone_number is None:
        logger.error("USSD callback received without a phone number.")
        # Return a generic error response, as we can't proceed.
        return HttpResponse("END An error occurred. Please try again later.", content_type="text/plain")

    logger.info(
        f"Incoming USSD request from {phone_number}: "
        f"sessionId={session_id}, text='{text}'"
    )

    response = ""

    if text == "":
        # This is the first request. Note how we start the response with CON
        response = "CON Welcome to AgriShield. What would you like to do?\n"
        response += "1. Check Weather Forecast\n"
        response += "2. Report Pest/Disease"

    elif text == "1":
        # Business logic for first level response
        response = "END The weather will be sunny for the next 3 days."

    elif text == "2":
        # Business logic for first level response
        response = "END Thank you for your report. A confirmation SMS will be sent to you shortly."
        # This part REQUIRES africastalking.initialize() to have been called,
        # typically at application startup using your .env variables.
        try:
            sms = africastalking.SMS
            sms.send("Your AgriShield pest/disease report has been received and is being processed.", [phone_number])
            logger.info(f"Sent confirmation SMS to {phone_number}")
        except Exception as e:
            logger.error(f"Failed to send confirmation SMS to {phone_number}: {e}")

    else:
        response = "END Invalid choice. Please try again."

    logger.info(f"USSD response for {phone_number}: '{response}'")

    # Send the response back to Africa's Talking
    return HttpResponse(response, content_type="text/plain")
