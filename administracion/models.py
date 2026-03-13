# -----------------------------------------------------------------------------
# Project Programacion para mortales
# Desarrollador : Kevin Turkienich
# 2024
# -----------------------------------------------------------------------------
# APP para calcular el costo y manejar diferentes recetas

# -----------------------------------------------------------------------------
# Listas para unidad de medida de producto
UNIDADES_DE_MEDIDA = [
    ('Unidades', 'Unidades'),
    ('Kilos', 'Kilos'),
    ('Gramos', 'Gramos'),
    ('Litros', 'Litros'),
    ('Mililitros', 'Mililitros'),
    ('Mt2s', 'Mt2s'),
    ('Onzas', 'Onzas'),
    ('Libras', 'Libras'),
    ('Metros', 'Metros'),
    ('Centimetros', 'Centimetros'),
]

# -----------------------------------------------------------------------------
# Importaciones

from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from configuracion.models import Configuracion
from .services_bienes import (
    TIME_UNIT_CHOICES,
    calcular_costo_bien_receta,
    calcular_totales_bienes_receta,
    convertir_tiempo_a_horas,
    formatear_tiempo,
)
# -----------------------------------------------------------------------------
# Validacion para que la imagen sea de 500 x 500 pixeles
def validate_image_size(value):
    """ Valida que la imagen tenga un tamaño de 500x500 píxeles. """
    width, height = value.width, value.height
    if width != 500 or height != 500:
        raise ValidationError('La imagen debe ser de 500x500 píxeles.')

# -----------------------------------------------------------------------------
# Modulo de categorias de productos
class CategoriaReceta(models.Model):
    """ Modelo que representa una categoría de productos. """
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    def clean(self):
        # Validación para asegurar que el usuario no edite registros de otros usuarios
        if self.pk and self.usuario != self._current_user:
            raise ValidationError('No puedes editar registros que no te pertenecen.')
    
# -----------------------------------------------------------------------------
# Modulo de categorias de productos
class Categoria(models.Model):
    """ Modelo que representa una categoría de productos. """
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def clean(self):
        # Validación para asegurar que el usuario no edite registros de otros usuarios
        if self.pk and self.usuario != self._current_user:
            raise ValidationError('No puedes editar registros que no te pertenecen.')
# -----------------------------------------------------------------------------
# Modulo de productos
class Producto(models.Model):
    """ Modelo que representa un producto con sus detalles. """
    codigo = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.CharField(max_length=200, blank=True, null=True)
    unidad_de_medida = models.CharField(max_length=50, choices=UNIDADES_DE_MEDIDA, blank=False, null=False, default="Unidades")
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    costo = models.FloatField(default=0, blank=True, null=True)
    usuario = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f'{self.nombre} x {self.cantidad} {self.unidad_de_medida} | costo unitario {self.costo_unitario():,.2f}'

    def costo_unitario(self):
        """ Calcula el costo unitario del producto. """
        return float(self.costo) / float(self.cantidad)

    def clean(self):
        if self.costo < 0:
            raise ValidationError("El costo no puede ser menor a 0.")


class Bien(models.Model):
    """Modelo que representa equipamiento productivo usado por las recetas."""
    nombre = models.CharField(max_length=150, blank=False, null=False)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    costo_compra = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    vida_util_cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    vida_util_unidad = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES, default='Horas')
    potencia_watts = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    factor_uso_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=100, blank=False, null=False)
    activo = models.BooleanField(default=True)
    usuario = models.CharField(max_length=120, null=True, blank=True)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'bien'
        verbose_name_plural = 'Bienes'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre

    def vida_util_horas(self):
        return float(convertir_tiempo_a_horas(self.vida_util_cantidad, self.vida_util_unidad))

    def vida_util_label(self):
        return formatear_tiempo(self.vida_util_cantidad, self.vida_util_unidad)

    def costo_hora_depreciacion(self):
        calculo = calcular_costo_bien_receta(self, 1, 'Horas', incluir_electricidad=False)
        return float(calculo['costo_hora_depreciacion'])

    def costo_electricidad_por_hora(self, precio_kwh=None):
        calculo = calcular_costo_bien_receta(
            self,
            1,
            'Horas',
            precio_kwh=precio_kwh,
            incluir_depreciacion=False,
            incluir_electricidad=True,
        )
        return float(calculo['costo_electricidad'])

    def clean(self):
        if self.costo_compra < 0:
            raise ValidationError('El costo de compra no puede ser menor a 0.')
        if self.vida_util_cantidad <= 0:
            raise ValidationError('La vida util debe ser superior a 0.')
        if self.potencia_watts < 0:
            raise ValidationError('La potencia no puede ser menor a 0.')
        if self.factor_uso_porcentaje < 0 or self.factor_uso_porcentaje > 100:
            raise ValidationError('El factor de uso debe estar entre 0 y 100.')
        

# -----------------------------------------------------------------------------
# Modulo de recetas
class Receta(models.Model):
    """ Modelo que representa una receta con sus detalles. """
    imagen = models.ImageField(
        upload_to='img/recetas/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), validate_image_size]
    )
    nombre = models.CharField(max_length=150,  blank=False, null=False,)
    descripcion = models.CharField(max_length=150,blank=False, null=False)
    categoria = models.ForeignKey(CategoriaReceta, on_delete=models.SET_NULL, null=True, blank=True)
    porciones = models.DecimalField(max_digits=15, decimal_places=2, default=1, blank=False, null=False)
    rentabilidad = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=False, null=False)
    comentarios = models.TextField(null=True, blank=True)
    mostrar = models.BooleanField(default=True,help_text="Permite mostrar la receta o producto")
    usuario = models.CharField(max_length=120, null=True, blank=True)
    iva = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=21,
        help_text="Selecciona la alícuota que corresponde a esta receta"
    )

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = 'receta'
        verbose_name_plural = 'Recetas'

    def obtener_configuracion(self):
        return Configuracion.objects.filter(usuario=self.usuario).first() or Configuracion.objects.first()

    def desglose_costos(self):
        total_productos = 0
        adicionales = GastosAdicionalesReceta.objects.filter(receta=self)
        suma_adicionales = sum(float(adicional.importe) if adicional.importe is not None else 0 for adicional in adicionales)

        productos = ProductoReceta.objects.filter(receta=self)
        for producto in productos:
            total_productos += producto.precio_total()

        totales_bienes = calcular_totales_bienes_receta(self)
        total_bienes = float(totales_bienes['total_bienes'])

        return {
            'insumos': total_productos,
            'gastos_adicionales': suma_adicionales,
            'bienes_depreciacion': float(totales_bienes['total_depreciacion']),
            'bienes_electricidad': float(totales_bienes['total_electricidad']),
            'bienes_total': total_bienes,
            'bienes_detalle': totales_bienes['detalles'],
            'total': total_productos + suma_adicionales + total_bienes,
        }

    def costo_receta(self):
        """ Calcula el costo total de la receta sumando el costo de los productos, subrecetas y gastos adicionales. """
        return self.desglose_costos()['total']

    def costo_bienes(self):
        return self.desglose_costos()['bienes_total']

    def costo_bienes_depreciacion(self):
        return self.desglose_costos()['bienes_depreciacion']

    def costo_bienes_electricidad(self):
        return self.desglose_costos()['bienes_electricidad']

    def costo_porcion(self):
        """ Calcula el costo por porción de la receta. """
        configuracion = self.obtener_configuracion()
        redondeo = int(configuracion.redondeo or 0) if configuracion else 0
        total = float(self.costo_receta())
        return round(float(total) / float(self.porciones),redondeo)

    def precio_venta_porcion_num(self):
        """ Calcula el precio por porción de la receta. """
        configuracion = self.obtener_configuracion()
        redondeo = int(configuracion.redondeo or 0) if configuracion else 0
        rentabilidad = Decimal(self.rentabilidad or 0)  # Asegurarte de que sea Decimal
        if rentabilidad >= 100:
            raise ValueError("La rentabilidad no puede ser igual o mayor al 100%, ya que causa divisiones por cero.")
        total = float(self.costo_porcion()) / float(100 - rentabilidad) * 100
     
        total = total * (1 + float(self.iva) / 100)
        return round(total,redondeo) 

    def precio_venta_porcion(self):
        """ Calcula el precio por porción de la receta. """
        configuracion = self.obtener_configuracion()
        redondeo = int(configuracion.redondeo or 0) if configuracion else 0
        total = float(float(self.costo_porcion())/ float(100 - self.rentabilidad) * 100)
        if self.iva:
            total = total * (1 + float(self.iva) / 100)
        return round(total,redondeo) 

    def precio_venta_total(self):
        """ Calcula el precio total de la receta. """
        configuracion = self.obtener_configuracion()
        redondeo = int(configuracion.redondeo or 0) if configuracion else 0
        total = float(self.precio_venta_porcion()) * float(self.porciones)
        return round(total,redondeo)
    
    def clean(self):
        # Validar que rentabilidad sea un número válido
        if not isinstance(self.rentabilidad, Decimal):
            raise ValidationError("La rentabilidad debe ser un número decimal.")
        
        if self.rentabilidad < 0:
            raise ValidationError("La rentabilidad no puede ser negativa.")
        
        if self.rentabilidad >= 100:
            raise ValidationError("La rentabilidad no puede ser igual o mayor al 100%.")

        if self.mostrar == True and not self.imagen:
            raise ValidationError("Para publicar la receta debe colocarle una imagen.")
        
# -----------------------------------------------------------------------------
# Modulo de gastos adicionales de receta
class GastosAdicionalesReceta(models.Model):
    """ Modelo que representa los gastos adicionales de una receta. """
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=50, blank=False, null=False)
    importe = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=False, null=False)
    usuario = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'gasto'
        verbose_name_plural = 'Gastos adicionales'

    def __str__(self):
        return str(self.detalle)

    def clean(self):
        """ Valida que el importe del gasto adicional sea mayor que 0. """
        if self.importe <= 0:
            raise ValidationError("El importe del gasto adicional no puede ser inferior o igual a 0.")
        super().clean()

# -----------------------------------------------------------------------------
# Modulo producto<>receta 
# Este modulo, se utiliza como relacion intermedia entre el producto y la receta
class ProductoReceta(models.Model):
    """ Modelo que representa la relación entre un producto y una receta, incluyendo la cantidad y la medida de uso. """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    medida_uso = models.CharField(max_length=50, choices=UNIDADES_DE_MEDIDA, blank=False, null=False, default="Unidades")
    usuario = models.CharField(max_length=120, null=True, blank=True)
    
    def save(self, *args, **kwargs): 
        if not self.usuario:
            self.usuario = self.receta.usuario
        super(ProductoReceta, self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = 'producto incluido'
        verbose_name_plural = 'Productos incluidos'

    def __str__(self):
        return str(self.producto.nombre)

    def clean(self):
        """ Valida que la cantidad y la unidad de medida sean correctas. """
        if self.cantidad <= 0:
            raise ValidationError("Por favor ingrese una cantidad superior a 0.")

        if self.producto.unidad_de_medida == 'Unidades' and self.medida_uso != 'Unidades':
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Unidades'.")

        if self.producto.unidad_de_medida == 'Mt2s' and self.medida_uso != 'Mt2s':
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Mt2s'.")

        if self.producto.unidad_de_medida == 'Kilos' and self.medida_uso not in ['Kilos', 'Gramos']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Kilos' o 'Gramos'.")

        if self.producto.unidad_de_medida == 'Litros' and self.medida_uso not in ['Litros', 'Mililitros']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Litros' o 'Mililitros'.")

        if self.producto.unidad_de_medida == 'Gramos' and self.medida_uso not in ['Kilos', 'Gramos']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Kilos' o 'Gramos'.")

        if self.producto.unidad_de_medida == 'Mililitros' and self.medida_uso not in ['Litros', 'Mililitros']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Litros' o 'Mililitros'.")

        if self.producto.unidad_de_medida == 'Onzas' and self.medida_uso not in ['Onzas', 'Libras']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Onzas' o 'Libras'.")

        if self.producto.unidad_de_medida == 'Libras' and self.medida_uso not in ['Onzas', 'Libras']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Onzas' o 'Libras'.")

        if self.producto.unidad_de_medida == 'Metros' and self.medida_uso not in ['Metros', 'Centimetros']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Metros' o 'Centimetros'.")

        if self.producto.unidad_de_medida == 'Centimetros' and self.medida_uso not in ['Metros', 'Centimetros']:
            raise ValidationError("Debido a la medida de uso de tu producto solo puedes usar 'Centimetros' o 'Metros'.")
        
    def precio_unitario(self):
        """
        Calcula el precio unitario ajustado según la unidad de medida de uso.
        
        Si la unidad del producto difiere de la unidad de uso, realiza la conversión:
        - Metros/Centímetros: 1 Metro = 100 Centímetros
        - Kilos/Gramos: 1 Kilo = 1000 Gramos
        - Litros/Mililitros: 1 Litro = 1000 Mililitros
        - Libras/Onzas: 1 Libra = 16 Onzas
        """
        total = 0
        if self.producto.unidad_de_medida != self.medida_uso:
            # Conversión Metros/Centímetros
            if self.producto.unidad_de_medida == "Centimetros":
                # Producto en CM, usar en Metros: multiplicar por 100 (100 CM = 1 Metro)
                total = (float(self.producto.costo_unitario()) * 100) 
            elif self.producto.unidad_de_medida == "Metros":
                # Producto en Metros, usar en CM: dividir por 100 (1 Metro = 100 CM)
                total = (float(self.producto.costo_unitario()) / 100) 

            # Conversión Kilos/Gramos
            elif self.producto.unidad_de_medida == "Kilos":
                # Producto en Kilos, usar en Gramos: dividir por 1000 (1 Kilo = 1000 Gramos)
                total = (float(self.producto.costo_unitario()) / 1000) 
            elif self.producto.unidad_de_medida == "Gramos":
                # Producto en Gramos, usar en Kilos: multiplicar por 1000 (1000 Gramos = 1 Kilo)
                total = (float(self.producto.costo_unitario()) * 1000) 
                
            # Conversión Litros/Mililitros
            elif self.producto.unidad_de_medida == "Litros":
                # Producto en Litros, usar en Mililitros: dividir por 1000 (1 Litro = 1000 ML)
                total = (float(self.producto.costo_unitario()) / 1000) 
            elif self.producto.unidad_de_medida == "Mililitros":
                # Producto en Mililitros, usar en Litros: multiplicar por 1000 (1000 ML = 1 Litro)
                total = (float(self.producto.costo_unitario()) * 1000) 
                
            # Conversión Libras/Onzas
            elif self.producto.unidad_de_medida == "Libras":
                # Producto en Libras, usar en Onzas: dividir por 16 (1 Libra = 16 Onzas)
                total = (float(self.producto.costo_unitario()) / 16)
            elif self.producto.unidad_de_medida == "Onzas":
                # Producto en Onzas, usar en Libras: multiplicar por 16 (16 Onzas = 1 Libra)
                total = (float(self.producto.costo_unitario()) * 16) 
        else:
            total = float(self.producto.costo_unitario()) 

        return total

    def precio_total(self):
        """ Calcula el costo total del producto en la receta. """
        return self.precio_unitario() * float(self.cantidad)

    def convertir_unidad(self):
        """
        Convierte la cantidad a la unidad de medida del producto si es necesario.
        """
        conversiones = {
            ('Metros', 'Centimetros'): lambda x: x / 100,
            ('Centimetros', 'Metros'): lambda x: x * 100,
            ('Kilos', 'Gramos'): lambda x: x / 1000,
            ('Gramos', 'Kilos'): lambda x: x * 1000,
            ('Litros', 'Mililitros'): lambda x: x / 1000,
            ('Mililitros', 'Litros'): lambda x: x * 1000,
            ('Libras', 'Onzas'): lambda x: x / 16,
            ('Onzas', 'Libras'): lambda x: x * 16,
        }

        key = (self.producto.unidad_de_medida, self.medida_uso)
        if key in conversiones:
            return conversiones[key](float(self.cantidad))
        return float(self.cantidad)


class BienReceta(models.Model):
    """Relacion entre una receta y un bien productivo."""
    bien = models.ForeignKey(Bien, on_delete=models.CASCADE)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    tiempo_uso_cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=1, blank=False, null=False)
    tiempo_uso_unidad = models.CharField(max_length=20, choices=TIME_UNIT_CHOICES, default='Minutos')
    incluir_depreciacion = models.BooleanField(default=True)
    incluir_electricidad = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    usuario = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'bien incluido'
        verbose_name_plural = 'Bienes incluidos'

    def __str__(self):
        return f'{self.bien.nombre} en {self.receta.nombre}'

    def save(self, *args, **kwargs):
        if not self.usuario:
            self.usuario = self.receta.usuario
        super(BienReceta, self).save(*args, **kwargs)

    def calculo(self):
        return calcular_costo_bien_receta(
            self.bien,
            self.tiempo_uso_cantidad,
            self.tiempo_uso_unidad,
            incluir_depreciacion=self.incluir_depreciacion,
            incluir_electricidad=self.incluir_electricidad,
        )

    def tiempo_uso_label(self):
        return formatear_tiempo(self.tiempo_uso_cantidad, self.tiempo_uso_unidad)

    def horas_uso(self):
        return float(self.calculo()['horas_uso'])

    def costo_depreciacion(self):
        return float(self.calculo()['depreciacion'])

    def costo_electricidad(self):
        return float(self.calculo()['costo_electricidad'])

    def costo_total(self):
        return float(self.calculo()['costo_total'])

    def clean(self):
        if self.tiempo_uso_cantidad <= 0:
            raise ValidationError('El tiempo de uso debe ser superior a 0.')


# -----------------------------------------------------------------------------
# Modulo producto<>receta 
# Este modulo, se utiliza como relacion intermedia entre el producto y la receta
class PasosReceta(models.Model):
    """ Modelo que representa la relación entre un producto y una receta, incluyendo la cantidad y la medida de uso. """
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255,blank=False,null=False)
    detalle = models.TextField(blank=False, null=False)
    usuario = models.CharField(max_length=120, null=True, blank=True)
    
    def save(self, *args, **kwargs): 
        if not self.usuario:
            self.usuario = self.receta.usuario
        super(PasosReceta, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'pasos'
        verbose_name_plural = 'Pasos'

    def __str__(self):
        return str(self.nombre)

