from decimal import Decimal

from django.test import TestCase

from administracion.models import Bien, BienReceta, CategoriaReceta, Producto, ProductoReceta, Receta
from configuracion.models import Configuracion


class BienesRecetaTests(TestCase):
    def setUp(self):
        Configuracion.objects.create(
            nombre_emprendimiento='Demo',
            moneda='$',
            precio_kwh=Decimal('150.00'),
            redondeo=0,
            usuario='tester',
        )
        self.categoria = CategoriaReceta.objects.create(nombre='Postres', usuario='tester')
        self.receta = Receta.objects.create(
            nombre='Licuado',
            descripcion='Receta de prueba',
            categoria=self.categoria,
            porciones=Decimal('10'),
            rentabilidad=Decimal('20'),
            usuario='tester',
        )
        self.producto = Producto.objects.create(
            nombre='Azucar',
            unidad_de_medida='Gramos',
            cantidad=Decimal('1000'),
            costo=1000,
            usuario='tester',
        )
        ProductoReceta.objects.create(
            producto=self.producto,
            receta=self.receta,
            cantidad=Decimal('100'),
            medida_uso='Gramos',
            usuario='tester',
        )
        self.bien = Bien.objects.create(
            nombre='Licuadora',
            costo_compra=Decimal('120000'),
            vida_util_cantidad=Decimal('1200'),
            vida_util_unidad='Horas',
            potencia_watts=Decimal('1500'),
            factor_uso_porcentaje=Decimal('100'),
            usuario='tester',
        )

    def test_bien_receta_calcula_depreciacion_y_electricidad(self):
        bien_receta = BienReceta.objects.create(
            bien=self.bien,
            receta=self.receta,
            tiempo_uso_cantidad=Decimal('12'),
            tiempo_uso_unidad='Minutos',
            incluir_depreciacion=True,
            incluir_electricidad=True,
            usuario='tester',
        )

        self.assertAlmostEqual(bien_receta.costo_depreciacion(), 20.0, places=2)
        self.assertAlmostEqual(bien_receta.costo_electricidad(), 45.0, places=2)
        self.assertAlmostEqual(bien_receta.costo_total(), 65.0, places=2)

    def test_receta_incluye_bienes_en_total_y_porcion(self):
        BienReceta.objects.create(
            bien=self.bien,
            receta=self.receta,
            tiempo_uso_cantidad=Decimal('12'),
            tiempo_uso_unidad='Minutos',
            incluir_depreciacion=True,
            incluir_electricidad=True,
            usuario='tester',
        )

        self.assertAlmostEqual(self.receta.costo_receta(), 165.0, places=2)
        self.assertAlmostEqual(self.receta.costo_porcion(), 16.0, places=2)