from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('core.urls')),  # Esto incluirá las rutas de 'core'
]
