from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api_urls')),
    path('web/', include('core.web_urls')),
    path('legacy-json/', include('core.urls')),
]

