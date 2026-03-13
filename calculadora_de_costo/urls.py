from django.contrib import admin
from django.urls import include, path
from administracion.views import *
from administracion.importar_exportar_views import importar_exportar_productos, importar_exportar_recetas
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler400, handler404
from administracion.views import logout_view
from django.shortcuts import redirect

handler400 = custom_bad_request
handler404 = custom_bad_request

urlpatterns = [
    path('', lambda request: redirect('/admin/')),  # Redirigir raíz al admin
    path('admin/', admin.site.urls, name='admin'),  # El admin ahora tiene el dashboard
    path('descargar/<int:id_receta>/', descargar, name='descargar'),
    path('fabricacion/simulador/', simulador_fabricacion, name='simulador_fabricacion'),
    path('productos/importar-exportar/', importar_exportar_productos, name='importar_exportar_productos'),
    path('recetas/importar-exportar/', importar_exportar_recetas, name='importar_exportar_recetas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

