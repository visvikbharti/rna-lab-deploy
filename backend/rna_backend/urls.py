from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    # The following URLs are already included in api.urls and don't need to be duplicated here
    # path("api/quality/", include("api.quality.urls")),
    # path("api/feedback/", include("api.feedback.urls")),
]

# Add media serving capability in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)