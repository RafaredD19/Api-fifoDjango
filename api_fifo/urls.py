# api_fifo/urls.py
from django.contrib import admin
from django.urls import path, include
from core.views import home_view  # Importa la vista de inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('core.urls')),  # Incluye las rutas de 'core'
    path('', home_view, name='home'),  # Página de inicio en la raíz
]
