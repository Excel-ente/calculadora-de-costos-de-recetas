# -----------------------------------------------------------------------------
# Project Programacion para mortales
# Desarrollador : Kevin Turkienich
# 2024
# -----------------------------------------------------------------------------
# APP para calcular el costo y manejar diferentes recetas

# -----------------------------------------------------------------------------
# Importaciones

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# -----------------------------------------------------------------------------
# Importaciones

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
# -----------------------------------------------------------------------------
# Validacion para que la imagen sea de 500 x 500 pixeles
def validate_image_size(value):
    """ Valida que la imagen tenga un tamaño de 500x500 píxeles. """
    width, height = value.width, value.height
    if width != 500 or height != 500:
        raise ValidationError('La imagen debe ser de 500x500 píxeles.')

# -----------------------------------------------------------------------------
# Modulo de configuracion
class Configuracion(models.Model):
    """ Modelo para configuraciones generales """
    nombre_emprendimiento = models.CharField(max_length=20, blank=False, null=False)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    redes_sociales = models.CharField(max_length=200, blank=True, null=True)
    moneda = models.CharField(max_length=200, blank=False, null=False,default='$')
    precio_kwh = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    logo = models.ImageField(
        upload_to='img/logo/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_size]
    )
    usuario = models.CharField(max_length=120, null=True, blank=True)
    redondeo = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=False, null=False)

    # --- Segunda moneda ---
    habilitar_segunda_moneda = models.BooleanField(
        default=False,
        help_text='Activá esta opción para mostrar precios en dos monedas en todo el sistema.'
    )
    segunda_moneda = models.CharField(
        max_length=10, blank=True, default='USD',
        help_text='Símbolo o código de la segunda moneda (ej: USD, €, BTC).'
    )
    tipo_de_cambio = models.DecimalField(
        max_digits=20, decimal_places=8, default=Decimal('1'),
        help_text='Cuántos USD (o segunda moneda) equivalen a 1 unidad de moneda principal. Ej: si 1 $ = 0,00069 USD, ingresá 0.00069.'
    )
    redondeo_segunda_moneda = models.DecimalField(
        max_digits=5, decimal_places=2, default=2, blank=False, null=False,
        help_text='Decimales para mostrar en segunda moneda. Usá 2 para centavos, 0 para enteros, -2 para redondear a centenas.'
    )

    def __str__(self):
        return f'{self.nombre_emprendimiento}'

    def clean(self):
        configuracion_existente = Configuracion.objects.exclude(pk=self.pk).first()
        if configuracion_existente:
            raise ValidationError('Solo puede existir una configuracion en el sistema.')
        if self.habilitar_segunda_moneda:
            if not (self.segunda_moneda or '').strip():
                raise ValidationError('Debe ingresar el símbolo de la segunda moneda.')
            if self.tipo_de_cambio <= 0:
                raise ValidationError('El tipo de cambio debe ser mayor a 0.')

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk and not Configuracion.objects.exists():
            self.pk = 1
        super().save(*args, **kwargs)
    
