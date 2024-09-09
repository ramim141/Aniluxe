from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),  # Home app URLs
    path('product/', include('products.urls')),  # Products app URLs
    path('accounts/', include('accounts.urls')),  # Accounts app URLs
    path('admin/', admin.site.urls),  # Admin site URL
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
