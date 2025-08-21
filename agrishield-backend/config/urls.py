from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    path("api/users/", include("apps.users.urls")),
    path("api/data/", include("apps.data.urls")),
    path("api/integrations/", include("apps.integrations.urls")),

    # Core app routes (frontend pages)
    path("", include("apps.core.urls")),

    # Auth endpoints
    path("api/auth/", include("dj_rest_auth.urls")),                     # login/logout/password reset
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),  # signup
    path("api/auth/csrf-token/", views.get_csrf_token, name='get_csrf_token'),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/alerts/", include("apps.alerts.urls")),
    path("api/v1/integrations/", include("apps.integrations.urls")),
]


# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"
