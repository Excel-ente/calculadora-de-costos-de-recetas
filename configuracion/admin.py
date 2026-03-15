# Administrador de Django - Configuraciones generales

# importaciones
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Configuracion

# -----------------------------------------------------------------------------
# # Registro del modelo GastosAdicionalesReceta en el admin de Django

@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    exclude = ('usuario',)
    list_display_links = ('id','nombre_emprendimiento','telefono','redes_sociales',)
    fieldsets = (
        ('Datos del emprendimiento', {
            'fields': ('nombre_emprendimiento', 'logo', 'telefono', 'redes_sociales', 'moneda','redondeo'),
        }),
        ('Precio Kwh', {
            'fields': ('precio_kwh',),
        }),
        ('Segunda moneda', {
            'fields': ('habilitar_segunda_moneda', 'segunda_moneda', 'tipo_de_cambio', 'redondeo_segunda_moneda'),
            'description': (
                'Activá esta sección para mostrar precios en dos monedas simultáneamente. '
                'Al desactivarla, el sistema funciona exactamente igual que antes sin ningún cambio.'
            ),
        }),
    )

    class Media:
        js = ('js/segunda_moneda_admin.js',)

    def changelist_view(self, request, extra_context=None):
        configuracion = Configuracion.objects.first()
        if configuracion:
            url = reverse('admin:configuracion_configuracion_change', args=[configuracion.pk])
            return HttpResponseRedirect(url)
        return super().changelist_view(request, extra_context=extra_context)


    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def get_list_display(self, request):
        # Mostrar el campo 'usuario' solo a los superusuarios
        if request.user.is_superuser:
            return ('id','nombre_emprendimiento','telefono','redes_sociales','moneda','precio_kwh',)
        return ('id','nombre_emprendimiento','telefono','redes_sociales','moneda','precio_kwh',)
    
    
    def get_list_filter(self, request):
        # Mostrar el campo 'usuario' solo a los superusuarios
        if request.user.is_superuser:
            return  ('id','nombre_emprendimiento', 'moneda',)
        return   ('id','nombre_emprendimiento', 'moneda')
    
    def has_delete_permission(self, request, obj=None):
        # Denegar la eliminación a todos los usuarios
        return False

    def has_add_permission(self, request, obj=None):
        return not Configuracion.objects.exists()

