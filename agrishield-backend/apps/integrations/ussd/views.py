from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.users.models import Farmer, Village

@csrf_exempt
def ussd_callback(request):
    """
    USSD callback endpoint for Africa's Talking.
    Handles user input step by step.
    """
    session_id = request.POST.get("sessionId")
    service_code = request.POST.get("serviceCode")
    phone_number = request.POST.get("phoneNumber")
    text = request.POST.get("text", "").strip()

    # Split the user input into steps
    parts = text.split("*") if text else []

    # MAIN MENU
    if text == "":
        response = (
            "CON Welcome to AgriShield\n"
            "1. Register for alerts\n"
            "2. Report flood signs\n"
            "3. Check flood risk"
        )

    # REGISTRATION FLOW
    elif parts[0] == "1":
        if len(parts) == 1:
            # Step 1: Ask for village name
            response = "CON Enter your village name"
        elif len(parts) == 2:
            # Step 2: Process village name
            village_name = parts[1].strip()
            try:
                village = Village.objects.get(name__iexact=village_name)
                farmer, created = Farmer.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={"village": village},
                )
                if not created:
                    farmer.village = village
                    farmer.save()

                response = "END ✅ Registration successful! You will now receive flood alerts."
            except Village.DoesNotExist:
                response = "END ❌ Invalid village name. Please try again."

    # REPORT FLOOD SIGNS FLOW (placeholder for now)
    elif parts[0] == "2":
        response = "END Thank you. Flood signs reporting will be available soon."

    # CHECK FLOOD RISK FLOW (placeholder for now)
    elif parts[0] == "3":
        response = "END Flood risk info will be available soon."

    # INVALID INPUT
    else:
        response = "END ❌ Invalid choice. Please try again."

    return HttpResponse(response, content_type="text/plain")
