from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse


class HealthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "service": "agrishield-core",
                "env": getattr(settings, "ENV_NAME", "unknown"),
            }
        )


class VersionView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "version": getattr(settings, "RELEASE_VERSION", "0.0.1"),
                "commit": getattr(settings, "GIT_COMMIT", None),
            }
        )


def home(request):
    return HttpResponse("Welcome to AgriShield Core API")


# ----------------------------
# Custom error handlers
# ----------------------------
def handler404(request, exception=None):
    return HttpResponse("404 Not Found", status=404)


def handler500(request):
    return HttpResponse("500 Internal Server Error", status=500)
