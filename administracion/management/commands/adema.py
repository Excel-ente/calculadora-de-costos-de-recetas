from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from administracion.models import (
    Bien,
    BienReceta,
    Categoria,
    CategoriaReceta,
    PasosReceta,
    Producto,
    ProductoReceta,
    Receta,
)
from configuracion.models import Configuracion


class Command(BaseCommand):
    help = 'Carga una configuracion inicial con productos, bienes demo y una receta de ejemplo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Usuario al que se le asociaran los datos demo. Por defecto usa el primer superusuario.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Actualiza tambien los datos demo existentes con los valores por defecto.',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        force = options.get('force', False)
        user = self._get_target_user(username)

        with transaction.atomic():
            self._upsert_configuracion(user.username, force=force)
            categoria_productos, categoria_receta = self._upsert_categorias(user.username)
            productos = self._upsert_productos(user.username, categoria_productos, force=force)
            receta = self._upsert_receta(user.username, categoria_receta, force=force)
            bienes = self._upsert_bienes(user.username, force=force)
            self._upsert_ingredientes(receta, productos, force=force)
            self._upsert_bienes_receta(receta, bienes, force=force)
            self._upsert_pasos(receta, force=force)

        self.stdout.write(self.style.SUCCESS('Datos demo cargados correctamente.'))
        self.stdout.write(f'Usuario asociado: {user.username}')
        self.stdout.write('Se configuraron productos, bienes de ejemplo, una receta demo y la configuracion inicial.')

    def _get_target_user(self, username):
        User = get_user_model()

        if username:
            user = User.objects.filter(username=username).first()
            if user:
                return user
            raise CommandError(f'No existe un usuario con username={username}.')

        superusers = User.objects.filter(is_superuser=True)
        user = superusers.exclude(username__iexact='EXCEL-ENTE').order_by('-id').first()
        if user:
            return user

        user = superusers.order_by('-id').first()
        if user:
            return user

        user = User.objects.exclude(username__iexact='EXCEL-ENTE').order_by('-id').first()
        if user:
            return user

        user = User.objects.order_by('-id').first()
        if user:
            return user

        raise CommandError(
            'No hay usuarios creados. Ejecuta primero `python manage.py createsuperuser` y luego este comando.'
        )

    def _upsert_configuracion(self, username, force=False):
        configuracion = Configuracion.objects.order_by('id').first() or Configuracion()
        defaults = {
            'nombre_emprendimiento': 'ADEMA Demo',
            'telefono': '11 5555-0101',
            'redes_sociales': '@adema.demo',
            'moneda': '$',
            'precio_kwh': Decimal('125.50'),
            'redondeo': Decimal('2'),
            'usuario': username,
        }

        for field, value in defaults.items():
            current_value = getattr(configuracion, field, None)
            if force or current_value in (None, '', 0, Decimal('0')):
                setattr(configuracion, field, value)

        logo_path = Path(settings.MEDIA_ROOT) / 'img' / 'logo.png'
        if logo_path.exists() and (force or not configuracion.logo):
            with logo_path.open('rb') as logo_file:
                configuracion.logo.save('logo_demo.png', File(logo_file), save=False)

        configuracion.save()
        return configuracion

    def _upsert_categorias(self, username):
        categoria_productos, _ = Categoria.objects.get_or_create(
            nombre='Insumos demo',
            usuario=username,
        )
        categoria_receta, _ = CategoriaReceta.objects.get_or_create(
            nombre='Bizcochuelos',
            usuario=username,
        )
        return categoria_productos, categoria_receta

    def _upsert_productos(self, username, categoria, force=False):
        productos_demo = {
            'Harina 0000': {
                'descripcion': 'Harina de trigo para pasteleria.',
                'marca': 'Demo Molino',
                'unidad_de_medida': 'Kilos',
                'cantidad': Decimal('1.00'),
                'costo': Decimal('1200.00'),
            },
            'Azucar': {
                'descripcion': 'Azucar comun refinada.',
                'marca': 'Demo Dulce',
                'unidad_de_medida': 'Kilos',
                'cantidad': Decimal('1.00'),
                'costo': Decimal('1400.00'),
            },
            'Leche': {
                'descripcion': 'Leche entera larga vida.',
                'marca': 'Demo Lacteos',
                'unidad_de_medida': 'Litros',
                'cantidad': Decimal('1.00'),
                'costo': Decimal('1600.00'),
            },
            'Huevos': {
                'descripcion': 'Maple de huevos frescos.',
                'marca': 'Granja Demo',
                'unidad_de_medida': 'Unidades',
                'cantidad': Decimal('12.00'),
                'costo': Decimal('3600.00'),
            },
            'Manteca': {
                'descripcion': 'Manteca para reposteria.',
                'marca': 'Demo Cremosa',
                'unidad_de_medida': 'Gramos',
                'cantidad': Decimal('200.00'),
                'costo': Decimal('1800.00'),
            },
            'Polvo de hornear': {
                'descripcion': 'Leudante para bizcochuelos y tortas.',
                'marca': 'Demo Horno',
                'unidad_de_medida': 'Gramos',
                'cantidad': Decimal('50.00'),
                'costo': Decimal('900.00'),
            },
        }

        productos = {}
        for nombre, defaults in productos_demo.items():
            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                usuario=username,
                defaults={**defaults, 'categoria': categoria},
            )

            if force and not created:
                producto.descripcion = defaults['descripcion']
                producto.marca = defaults['marca']
                producto.unidad_de_medida = defaults['unidad_de_medida']
                producto.cantidad = defaults['cantidad']
                producto.costo = float(defaults['costo'])
                producto.categoria = categoria
                producto.save()
            elif created:
                producto.categoria = categoria
                producto.save(update_fields=['categoria'])

            productos[nombre] = producto

        return productos

    def _upsert_bienes(self, username, force=False):
        bienes_demo = {
            'Horno convector': {
                'descripcion': 'Equipo principal para coccion del bizcochuelo demo.',
                'costo_compra': Decimal('850000.00'),
                'vida_util_cantidad': Decimal('6000.00'),
                'vida_util_unidad': 'Horas',
                'potencia_watts': Decimal('2200.00'),
                'factor_uso_porcentaje': Decimal('60.00'),
                'activo': True,
            },
            'Licuadora': {
                'descripcion': 'Licuadora demo para mezclar preparaciones iniciales.',
                'costo_compra': Decimal('125000.00'),
                'vida_util_cantidad': Decimal('2500.00'),
                'vida_util_unidad': 'Horas',
                'potencia_watts': Decimal('800.00'),
                'factor_uso_porcentaje': Decimal('45.00'),
                'activo': True,
            },
        }

        bienes = {}
        for nombre, defaults in bienes_demo.items():
            bien, created = Bien.objects.get_or_create(
                nombre=nombre,
                usuario=username,
                defaults=defaults,
            )

            if force and not created:
                for field, value in defaults.items():
                    setattr(bien, field, value)
                bien.save()

            bienes[nombre] = bien

        return bienes

    def _upsert_receta(self, username, categoria_receta, force=False):
        defaults = {
            'descripcion': 'Bizcochuelo clasico esponjoso para tortas y meriendas.',
            'categoria': categoria_receta,
            'porciones': Decimal('12.00'),
            'rentabilidad': Decimal('35.00'),
            'comentarios': 'Receta demo para validar costos, porciones y precio sugerido.',
            'mostrar': False,
            'iva': Decimal('21.00'),
        }
        receta, created = Receta.objects.get_or_create(
            nombre='Bizcochuelo clasico',
            usuario=username,
            defaults=defaults,
        )

        if force and not created:
            for field, value in defaults.items():
                setattr(receta, field, value)
            receta.save()

        return receta

    def _upsert_ingredientes(self, receta, productos, force=False):
        ingredientes = [
            ('Harina 0000', Decimal('300.00'), 'Gramos'),
            ('Azucar', Decimal('250.00'), 'Gramos'),
            ('Huevos', Decimal('4.00'), 'Unidades'),
            ('Leche', Decimal('200.00'), 'Mililitros'),
            ('Manteca', Decimal('100.00'), 'Gramos'),
            ('Polvo de hornear', Decimal('15.00'), 'Gramos'),
        ]

        for nombre_producto, cantidad, medida_uso in ingredientes:
            producto = productos[nombre_producto]
            producto_receta = ProductoReceta.objects.filter(receta=receta, producto=producto).order_by('id').first()

            if producto_receta is None:
                ProductoReceta.objects.create(
                    receta=receta,
                    producto=producto,
                    cantidad=cantidad,
                    medida_uso=medida_uso,
                    usuario=receta.usuario,
                )
                continue

            if force:
                producto_receta.cantidad = cantidad
                producto_receta.medida_uso = medida_uso
                producto_receta.usuario = receta.usuario
                producto_receta.save()

    def _upsert_bienes_receta(self, receta, bienes, force=False):
        relaciones = [
            ('Horno convector', Decimal('40.00'), 'Minutos', True, True, 'Coccion principal del bizcochuelo demo.'),
            ('Licuadora', Decimal('4.00'), 'Minutos', True, True, 'Batido inicial de la mezcla demo.'),
        ]

        for nombre_bien, tiempo_uso_cantidad, tiempo_uso_unidad, incluir_depreciacion, incluir_electricidad, observaciones in relaciones:
            bien = bienes[nombre_bien]
            bien_receta = BienReceta.objects.filter(receta=receta, bien=bien).order_by('id').first()

            if bien_receta is None:
                BienReceta.objects.create(
                    receta=receta,
                    bien=bien,
                    tiempo_uso_cantidad=tiempo_uso_cantidad,
                    tiempo_uso_unidad=tiempo_uso_unidad,
                    incluir_depreciacion=incluir_depreciacion,
                    incluir_electricidad=incluir_electricidad,
                    observaciones=observaciones,
                    usuario=receta.usuario,
                )
                continue

            if force:
                bien_receta.tiempo_uso_cantidad = tiempo_uso_cantidad
                bien_receta.tiempo_uso_unidad = tiempo_uso_unidad
                bien_receta.incluir_depreciacion = incluir_depreciacion
                bien_receta.incluir_electricidad = incluir_electricidad
                bien_receta.observaciones = observaciones
                bien_receta.usuario = receta.usuario
                bien_receta.save()

    def _upsert_pasos(self, receta, force=False):
        pasos = [
            (
                'Preparar el molde',
                'Enmantecar y enharinar un molde redondo de 24 cm. Precalentar el horno a 180 C.',
            ),
            (
                'Batir huevos y azucar',
                'Batir los huevos con el azucar hasta lograr una mezcla espumosa y de color claro.',
            ),
            (
                'Incorporar liquidos',
                'Agregar la leche y la manteca derretida en forma de hilo mientras se sigue mezclando.',
            ),
            (
                'Sumar secos',
                'Tamizar harina y polvo de hornear. Integrar con movimientos envolventes para no bajar la mezcla.',
            ),
            (
                'Hornear y enfriar',
                'Volcar en el molde y hornear entre 35 y 40 minutos. Dejar enfriar antes de desmoldar.',
            ),
        ]

        for nombre, detalle in pasos:
            paso = PasosReceta.objects.filter(receta=receta, nombre=nombre).order_by('id').first()

            if paso is None:
                PasosReceta.objects.create(
                    receta=receta,
                    nombre=nombre,
                    detalle=detalle,
                    usuario=receta.usuario,
                )
                continue

            if force:
                paso.detalle = detalle
                paso.usuario = receta.usuario
                paso.save()