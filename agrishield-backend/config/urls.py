from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # API routes
    path("api/users/", include("apps.users.urls")),
    path("api/data/", include("apps.data.urls")),
    path("api/integrations/", include("apps.integrations.urls")),
    
    # Core app routes (frontend pages)
    path("", include("apps.core.urls")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler404 = "apps.core.views.handler404"
handler500 = "apps.core.views.handler500"
