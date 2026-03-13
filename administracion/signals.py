from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Bien, BienReceta, Producto, ProductoReceta, Receta
from django.db import transaction

@receiver(post_save, sender=Producto)
def recalcular_recetas(sender, instance, **kwargs):
    """
    Signal que se ejecuta cuando cambia un Producto.
    Recalcula todas las recetas relacionadas al producto modificado.
    """
    # Buscar todas las relaciones ProductoReceta con el producto modificado
    recetas_relacionadas = ProductoReceta.objects.filter(producto=instance)

    for relacion in recetas_relacionadas:
        receta = relacion.receta
        receta.costo_receta()  # Recalcula el costo de la receta
        receta.save()  # Guarda los cambios en la receta


@receiver(post_save, sender=Bien)
def recalcular_recetas_por_bien(sender, instance, **kwargs):
    relaciones = BienReceta.objects.filter(bien=instance).select_related('receta')

    for relacion in relaciones:
        receta = relacion.receta
        receta.costo_receta()
        receta.save()


@receiver(post_save, sender=BienReceta)
@receiver(post_delete, sender=BienReceta)
def actualizar_receta_bien_relacion(sender, instance, **kwargs):
    receta = instance.receta
    receta.costo_receta()
    receta.save()

# Variable global para controlar la desconexión temporal de la señal
signal_temporarily_disabled = False

@receiver(post_save, sender=Receta)
def actualizar_recetas_y_productos(sender, instance, **kwargs):
    """
    Signal para actualizar automáticamente el costo total y los precios de todos los productos y recetas relacionados
    después de guardar una receta.
    """
    global signal_temporarily_disabled

    if signal_temporarily_disabled:
        return

    try:
        # Desconectar temporalmente la señal para evitar recursión
        signal_temporarily_disabled = True

        with transaction.atomic():
            # Actualizar todos los productos de la receta guardada
            productos = ProductoReceta.objects.filter(receta=instance)

            # Recalcular los precios totales de cada producto
            for producto in productos:
                producto.precio_total()  # Solo ejecuta el método para recalcular

            # Actualizar la receta misma
            instance.costo_receta()  # Calcula el costo total de la receta
            instance.costo_porcion()  # Calcula el costo por porción
            instance.save()

    except Exception as e:
        print(f"Error al actualizar recetas y productos relacionados: {e}")

    finally:
        # Reconectar la señal
        signal_temporarily_disabled = False

