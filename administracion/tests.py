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


class SegundaMonedaTests(TestCase):
    """Tests integradores para la funcionalidad de segunda moneda y redondeo."""

    def setUp(self):
        self.config = Configuracion.objects.create(
            nombre_emprendimiento='TestEmpresa',
            moneda='$',
            precio_kwh=Decimal('150.00'),
            redondeo=2,
            usuario='tester',
            habilitar_segunda_moneda=True,
            segunda_moneda='USD',
            tipo_de_cambio=Decimal('0.001'),   # 1 ARS = 0.001 USD  →  1000 ARS = 1 USD
            redondeo_segunda_moneda=2,
        )
        self.categoria = CategoriaReceta.objects.create(nombre='Tortas', usuario='tester')
        self.producto = Producto.objects.create(
            nombre='Harina',
            unidad_de_medida='Gramos',
            cantidad=Decimal('1000'),
            costo=Decimal('2000'),   # costo unitario = 2 ARS/g
            usuario='tester',
        )
        self.receta = Receta.objects.create(
            nombre='Torta',
            descripcion='Receta de prueba segunda moneda',
            categoria=self.categoria,
            porciones=Decimal('10'),
            rentabilidad=Decimal('20'),
            usuario='tester',
        )
        ProductoReceta.objects.create(
            producto=self.producto,
            receta=self.receta,
            cantidad=Decimal('500'),   # 500 g × 2 ARS/g = 1000 ARS
            medida_uso='Gramos',
            usuario='tester',
        )

    # ------------------------------------------------------------------
    # Tests: campo redondeo_segunda_moneda en el modelo
    # ------------------------------------------------------------------
    def test_config_tiene_campo_redondeo_segunda_moneda(self):
        config = Configuracion.objects.first()
        self.assertTrue(hasattr(config, 'redondeo_segunda_moneda'))
        self.assertEqual(config.redondeo_segunda_moneda, Decimal('2'))

    def test_config_redondeo_segunda_moneda_default_es_2(self):
        """El default del campo debe ser 2 decimales."""
        self.assertEqual(self.config.redondeo_segunda_moneda, Decimal('2'))

    # ------------------------------------------------------------------
    # Tests: Producto.costo_unitario_segunda_moneda()
    # ------------------------------------------------------------------
    def test_producto_costo_unitario_segunda_moneda_calcula_correctamente(self):
        # Verifica que se aplica la fórmula correcta: costo_unitario × tipo_de_cambio, con redondeo
        tc = float(self.config.tipo_de_cambio)
        redondeo_2 = int(self.config.redondeo_segunda_moneda)
        expected = round(self.producto.costo_unitario() * tc, redondeo_2)
        val = self.producto.costo_unitario_segunda_moneda()
        self.assertIsNotNone(val)
        self.assertEqual(val, expected)

    def test_producto_costo_unitario_segunda_moneda_aplica_redondeo(self):
        # Con redondeo_segunda_moneda=2, round(0.002, 2) = 0.0
        val = self.producto.costo_unitario_segunda_moneda()
        self.assertEqual(val, round(0.002, 2))

    def test_producto_costo_unitario_segunda_moneda_redondeo_3(self):
        self.config.redondeo_segunda_moneda = Decimal('3')
        self.config.save()
        val = self.producto.costo_unitario_segunda_moneda()
        self.assertEqual(val, round(0.002, 3))

    def test_producto_costo_unitario_segunda_moneda_deshabilitada_retorna_none(self):
        self.config.habilitar_segunda_moneda = False
        self.config.save()
        self.assertIsNone(self.producto.costo_unitario_segunda_moneda())

    # ------------------------------------------------------------------
    # Tests: Receta.*_segunda_moneda()
    # ------------------------------------------------------------------
    def test_receta_costo_porcion_segunda_moneda(self):
        # costo_receta = 1000 ARS ; costo_porcion = 100 ARS ; × 0.001 = 0.1 USD
        val = self.receta.costo_porcion_segunda_moneda()
        self.assertIsNotNone(val)
        self.assertEqual(val, round(100 * 0.001, 2))   # 0.1, round to 2 → 0.1

    def test_receta_precio_venta_total_segunda_moneda(self):
        # Verifica que la fórmula aplicada sea: precio_venta_total × tipo_de_cambio, con redondeo
        tc = float(self.config.tipo_de_cambio)
        redondeo_2 = int(self.config.redondeo_segunda_moneda)
        expected = round(self.receta.precio_venta_total() * tc, redondeo_2)
        val = self.receta.precio_venta_total_segunda_moneda()
        self.assertIsNotNone(val)
        self.assertEqual(val, expected)

    def test_receta_precio_venta_porcion_segunda_moneda(self):
        # Verifica que la fórmula aplicada sea: precio_venta_porcion × tipo_de_cambio, con redondeo
        tc = float(self.config.tipo_de_cambio)
        redondeo_2 = int(self.config.redondeo_segunda_moneda)
        expected = round(self.receta.precio_venta_porcion_num() * tc, redondeo_2)
        val = self.receta.precio_venta_porcion_segunda_moneda()
        self.assertIsNotNone(val)
        self.assertEqual(val, expected)

    def test_receta_segunda_moneda_deshabilitada_retorna_none(self):
        self.config.habilitar_segunda_moneda = False
        self.config.save()
        self.assertIsNone(self.receta.costo_porcion_segunda_moneda())
        self.assertIsNone(self.receta.precio_venta_total_segunda_moneda())
        self.assertIsNone(self.receta.precio_venta_porcion_segunda_moneda())

    # ------------------------------------------------------------------
    # Tests: redondeo negativo (enteros)
    # ------------------------------------------------------------------
    def test_redondeo_negativo_redondea_a_decenas(self):
        """redondeo_segunda_moneda=-1 debe redondear a decenas."""
        self.config.tipo_de_cambio = Decimal('1')   # 1:1 para simplificar
        self.config.redondeo_segunda_moneda = Decimal('-1')
        self.config.save()
        # costo_porcion = 100 ARS × 1 = 100 ; round(100, -1) = 100
        val = self.receta.costo_porcion_segunda_moneda()
        self.assertEqual(val, round(100 * 1, -1))

    def test_redondeo_cero_retorna_entero(self):
        """redondeo_segunda_moneda=0 debe retornar un valor sin decimales."""
        self.config.tipo_de_cambio = Decimal('0.001')
        self.config.redondeo_segunda_moneda = Decimal('0')
        self.config.save()
        # costo_porcion = 100 × 0.001 = 0.1 ; round(0.1, 0) = 0.0
        val = self.receta.costo_porcion_segunda_moneda()
        self.assertEqual(val, round(100 * 0.001, 0))

    # ------------------------------------------------------------------
    # Tests: tipo de cambio = 0 (debe desactivarse automáticamente)
    # ------------------------------------------------------------------
    def test_tipo_de_cambio_cero_retorna_none(self):
        self.config.tipo_de_cambio = Decimal('0')
        # Bypass clean() to set an invalid state and test defensive code
        Configuracion.objects.filter(pk=self.config.pk).update(tipo_de_cambio=Decimal('0'))
        val = self.producto.costo_unitario_segunda_moneda()
        self.assertIsNone(val)