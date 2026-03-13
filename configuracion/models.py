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

    def __str__(self):
        return f'{self.nombre_emprendimiento}'

    def clean(self):
        configuracion_existente = Configuracion.objects.exclude(pk=self.pk).first()
        if configuracion_existente:
            raise ValidationError('Solo puede existir una configuracion en el sistema.')

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pk and not Configuracion.objects.exists():
            self.pk = 1
        super().save(*args, **kwargs)
    
