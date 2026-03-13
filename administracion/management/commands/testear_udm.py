# -----------------------------------------------------------------------------
# Command: testear_udm
# Desarrollador : Kevin Turkienich
# 2024
# -----------------------------------------------------------------------------
# Management command para testear todas las unidades de medida y sus conversiones
# Verifica que las validaciones funcionen correctamente

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from administracion.models import Producto, Receta, ProductoReceta, Categoria, CategoriaReceta
from decimal import Decimal

# Colorama es opcional - solo para colores en terminal
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

class Command(BaseCommand):
    help = 'Testea todas las unidades de medida creando recetas de prueba y validando conversiones'

    def __init__(self):
        super().__init__()
        self.test_results = {
            'passed': [],
            'failed': [],
            'total': 0
        }

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Limpia todas las recetas y productos de prueba antes de ejecutar',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('INICIANDO TESTS DE UNIDADES DE MEDIDA'.center(80)))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))

        # Limpiar datos de prueba si se especifica
        if options['limpiar']:
            self.limpiar_datos_prueba()

        # Crear categorías de prueba
        categoria_prod, categoria_receta = self.crear_categorias()

        # Tests principales por unidad de medida
        self.stdout.write(self.style.WARNING('\n--- TESTS POR UNIDAD DE MEDIDA ---\n'))
        
        # 1. Test de Unidades (no permite conversión)
        self.test_unidades(categoria_prod, categoria_receta)
        
        # 2. Test de Kilos y Gramos
        self.test_peso_kilos_gramos(categoria_prod, categoria_receta)
        
        # 3. Test de Litros y Mililitros
        self.test_volumen_litros_mililitros(categoria_prod, categoria_receta)
        
        # 4. Test de Onzas y Libras
        self.test_peso_onzas_libras(categoria_prod, categoria_receta)
        
        # 5. Test de Metros y Centímetros
        self.test_longitud_metros_centimetros(categoria_prod, categoria_receta)
        
        # 6. Test de Mt2s (no permite conversión)
        self.test_metros_cuadrados(categoria_prod, categoria_receta)

        # 7. Test de conversiones inválidas
        self.test_conversiones_invalidas(categoria_prod, categoria_receta)

        # Mostrar resumen
        self.mostrar_resumen()

    def limpiar_datos_prueba(self):
        """Elimina todos los datos de prueba anteriores"""
        self.stdout.write(self.style.WARNING('\nLimpiando datos de prueba anteriores...'))
        
        ProductoReceta.objects.filter(usuario='TEST_USER').delete()
        Receta.objects.filter(usuario='TEST_USER').delete()
        Producto.objects.filter(usuario='TEST_USER').delete()
        Categoria.objects.filter(usuario='TEST_USER').delete()
        CategoriaReceta.objects.filter(usuario='TEST_USER').delete()
        
        self.stdout.write(self.style.SUCCESS('✓ Datos de prueba eliminados\n'))

    def crear_categorias(self):
        """Crea categorías de prueba"""
        categoria_prod, _ = Categoria.objects.get_or_create(
            nombre='TEST_Productos',
            defaults={'usuario': 'TEST_USER'}
        )
        categoria_receta, _ = CategoriaReceta.objects.get_or_create(
            nombre='TEST_Recetas',
            defaults={'usuario': 'TEST_USER'}
        )
        return categoria_prod, categoria_receta

    def crear_producto(self, nombre, unidad, cantidad=1000, costo=100, categoria=None):
        """Crea un producto de prueba"""
        return Producto.objects.create(
            codigo=f'TEST-{nombre[:10]}',
            nombre=nombre,
            descripcion=f'Producto de prueba para {unidad}',
            categoria=categoria,
            unidad_de_medida=unidad,
            cantidad=Decimal(str(cantidad)),
            costo=costo,
            usuario='TEST_USER'
        )

    def crear_receta(self, nombre, descripcion, categoria=None):
        """Crea una receta de prueba"""
        return Receta.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            porciones=Decimal('10'),
            rentabilidad=Decimal('30'),
            usuario='TEST_USER',
            mostrar=False,  # Sin imagen, no mostrar
            iva=Decimal('21')
        )

    def agregar_producto_a_receta(self, receta, producto, cantidad, medida_uso, esperar_error=False):
        """Intenta agregar un producto a una receta y valida"""
        try:
            prod_receta = ProductoReceta(
                producto=producto,
                receta=receta,
                cantidad=Decimal(str(cantidad)),
                medida_uso=medida_uso,
                usuario='TEST_USER'
            )
            prod_receta.full_clean()  # Ejecuta validaciones
            prod_receta.save()
            
            if esperar_error:
                return False, f"Se esperaba error pero se guardó correctamente"
            
            # Verificar que el cálculo de precio funcione
            precio = prod_receta.precio_total()
            if precio is None or precio < 0:
                return False, f"Cálculo de precio inválido: {precio}"
            
            return True, f"OK - Precio total: ${precio:,.2f}"
            
        except ValidationError as e:
            if esperar_error:
                return True, f"Error esperado: {e.message_dict if hasattr(e, 'message_dict') else str(e)}"
            return False, f"ValidationError: {e.message_dict if hasattr(e, 'message_dict') else str(e)}"
        except Exception as e:
            return False, f"Exception: {str(e)}"

    def registrar_test(self, nombre_test, exito, mensaje):
        """Registra el resultado de un test"""
        self.test_results['total'] += 1
        if exito:
            self.test_results['passed'].append((nombre_test, mensaje))
            self.stdout.write(self.style.SUCCESS(f'  ✓ {nombre_test}: {mensaje}'))
        else:
            self.test_results['failed'].append((nombre_test, mensaje))
            self.stdout.write(self.style.ERROR(f'  ✗ {nombre_test}: {mensaje}'))

    def test_unidades(self, categoria_prod, categoria_receta):
        """Test 1: Unidades - Solo puede usar Unidades"""
        self.stdout.write(self.style.HTTP_INFO('\n1. TEST: UNIDADES'))
        self.stdout.write('-' * 80)
        
        producto = self.crear_producto('Huevos', 'Unidades', cantidad=12, costo=120, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Unidades', 'Receta con productos en unidades', categoria_receta)
        
        # Test válido: Unidades -> Unidades
        exito, msg = self.agregar_producto_a_receta(receta, producto, 6, 'Unidades')
        self.registrar_test('Unidades -> Unidades', exito, msg)
        
        # Test inválido: Unidades -> Kilos
        exito, msg = self.agregar_producto_a_receta(receta, producto, 1, 'Kilos', esperar_error=True)
        self.registrar_test('Unidades -> Kilos (debe fallar)', exito, msg)
        
        # Test inválido: Unidades -> Litros
        exito, msg = self.agregar_producto_a_receta(receta, producto, 1, 'Litros', esperar_error=True)
        self.registrar_test('Unidades -> Litros (debe fallar)', exito, msg)

    def test_peso_kilos_gramos(self, categoria_prod, categoria_receta):
        """Test 2: Kilos y Gramos - Conversión bidireccional"""
        self.stdout.write(self.style.HTTP_INFO('\n2. TEST: KILOS Y GRAMOS'))
        self.stdout.write('-' * 80)
        
        # Producto en Kilos
        prod_kilos = self.crear_producto('Harina', 'Kilos', cantidad=1, costo=50, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Peso (Kilos)', 'Receta con productos en kilos', categoria_receta)
        
        # Test válido: Kilos -> Kilos
        exito, msg = self.agregar_producto_a_receta(receta, prod_kilos, 0.5, 'Kilos')
        self.registrar_test('Kilos -> Kilos', exito, msg)
        
        # Test válido: Kilos -> Gramos
        exito, msg = self.agregar_producto_a_receta(receta, prod_kilos, 250, 'Gramos')
        self.registrar_test('Kilos -> Gramos', exito, msg)
        
        # Producto en Gramos
        prod_gramos = self.crear_producto('Levadura', 'Gramos', cantidad=100, costo=20, categoria=categoria_prod)
        receta2 = self.crear_receta('Test Receta Peso (Gramos)', 'Receta con productos en gramos', categoria_receta)
        
        # Test válido: Gramos -> Gramos
        exito, msg = self.agregar_producto_a_receta(receta2, prod_gramos, 50, 'Gramos')
        self.registrar_test('Gramos -> Gramos', exito, msg)
        
        # Test válido: Gramos -> Kilos
        exito, msg = self.agregar_producto_a_receta(receta2, prod_gramos, 0.05, 'Kilos')
        self.registrar_test('Gramos -> Kilos', exito, msg)
        
        # Test inválido: Kilos -> Litros
        exito, msg = self.agregar_producto_a_receta(receta, prod_kilos, 1, 'Litros', esperar_error=True)
        self.registrar_test('Kilos -> Litros (debe fallar)', exito, msg)

    def test_volumen_litros_mililitros(self, categoria_prod, categoria_receta):
        """Test 3: Litros y Mililitros - Conversión bidireccional"""
        self.stdout.write(self.style.HTTP_INFO('\n3. TEST: LITROS Y MILILITROS'))
        self.stdout.write('-' * 80)
        
        # Producto en Litros
        prod_litros = self.crear_producto('Leche', 'Litros', cantidad=1, costo=80, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Volumen (Litros)', 'Receta con productos en litros', categoria_receta)
        
        # Test válido: Litros -> Litros
        exito, msg = self.agregar_producto_a_receta(receta, prod_litros, 0.5, 'Litros')
        self.registrar_test('Litros -> Litros', exito, msg)
        
        # Test válido: Litros -> Mililitros
        exito, msg = self.agregar_producto_a_receta(receta, prod_litros, 250, 'Mililitros')
        self.registrar_test('Litros -> Mililitros', exito, msg)
        
        # Producto en Mililitros
        prod_ml = self.crear_producto('Esencia Vainilla', 'Mililitros', cantidad=100, costo=150, categoria=categoria_prod)
        receta2 = self.crear_receta('Test Receta Volumen (ML)', 'Receta con productos en mililitros', categoria_receta)
        
        # Test válido: Mililitros -> Mililitros
        exito, msg = self.agregar_producto_a_receta(receta2, prod_ml, 10, 'Mililitros')
        self.registrar_test('Mililitros -> Mililitros', exito, msg)
        
        # Test válido: Mililitros -> Litros
        exito, msg = self.agregar_producto_a_receta(receta2, prod_ml, 0.02, 'Litros')
        self.registrar_test('Mililitros -> Litros', exito, msg)
        
        # Test inválido: Litros -> Gramos
        exito, msg = self.agregar_producto_a_receta(receta, prod_litros, 100, 'Gramos', esperar_error=True)
        self.registrar_test('Litros -> Gramos (debe fallar)', exito, msg)

    def test_peso_onzas_libras(self, categoria_prod, categoria_receta):
        """Test 4: Onzas y Libras - Conversión bidireccional"""
        self.stdout.write(self.style.HTTP_INFO('\n4. TEST: ONZAS Y LIBRAS'))
        self.stdout.write('-' * 80)
        
        # Producto en Libras
        prod_libras = self.crear_producto('Chocolate', 'Libras', cantidad=1, costo=200, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Peso Imperial (Libras)', 'Receta con productos en libras', categoria_receta)
        
        # Test válido: Libras -> Libras
        exito, msg = self.agregar_producto_a_receta(receta, prod_libras, 0.5, 'Libras')
        self.registrar_test('Libras -> Libras', exito, msg)
        
        # Test válido: Libras -> Onzas
        exito, msg = self.agregar_producto_a_receta(receta, prod_libras, 8, 'Onzas')
        self.registrar_test('Libras -> Onzas', exito, msg)
        
        # Producto en Onzas
        prod_onzas = self.crear_producto('Mantequilla', 'Onzas', cantidad=16, costo=180, categoria=categoria_prod)
        receta2 = self.crear_receta('Test Receta Peso Imperial (Onzas)', 'Receta con productos en onzas', categoria_receta)
        
        # Test válido: Onzas -> Onzas
        exito, msg = self.agregar_producto_a_receta(receta2, prod_onzas, 4, 'Onzas')
        self.registrar_test('Onzas -> Onzas', exito, msg)
        
        # Test válido: Onzas -> Libras
        exito, msg = self.agregar_producto_a_receta(receta2, prod_onzas, 0.5, 'Libras')
        self.registrar_test('Onzas -> Libras', exito, msg)
        
        # Test inválido: Libras -> Kilos
        exito, msg = self.agregar_producto_a_receta(receta, prod_libras, 0.5, 'Kilos', esperar_error=True)
        self.registrar_test('Libras -> Kilos (debe fallar)', exito, msg)

    def test_longitud_metros_centimetros(self, categoria_prod, categoria_receta):
        """Test 5: Metros y Centímetros - Conversión bidireccional"""
        self.stdout.write(self.style.HTTP_INFO('\n5. TEST: METROS Y CENTÍMETROS'))
        self.stdout.write('-' * 80)
        
        # Producto en Metros
        prod_metros = self.crear_producto('Cinta Decorativa', 'Metros', cantidad=10, costo=50, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Longitud (Metros)', 'Receta con productos en metros', categoria_receta)
        
        # Test válido: Metros -> Metros
        exito, msg = self.agregar_producto_a_receta(receta, prod_metros, 2, 'Metros')
        self.registrar_test('Metros -> Metros', exito, msg)
        
        # Test válido: Metros -> Centímetros
        exito, msg = self.agregar_producto_a_receta(receta, prod_metros, 50, 'Centimetros')
        self.registrar_test('Metros -> Centímetros', exito, msg)
        
        # Producto en Centímetros
        prod_cm = self.crear_producto('Papel Encerado', 'Centimetros', cantidad=1000, costo=100, categoria=categoria_prod)
        receta2 = self.crear_receta('Test Receta Longitud (CM)', 'Receta con productos en centímetros', categoria_receta)
        
        # Test válido: Centímetros -> Centímetros
        exito, msg = self.agregar_producto_a_receta(receta2, prod_cm, 30, 'Centimetros')
        self.registrar_test('Centímetros -> Centímetros', exito, msg)
        
        # Test válido: Centímetros -> Metros
        exito, msg = self.agregar_producto_a_receta(receta2, prod_cm, 0.5, 'Metros')
        self.registrar_test('Centímetros -> Metros', exito, msg)
        
        # Test inválido: Metros -> Mt2s
        exito, msg = self.agregar_producto_a_receta(receta, prod_metros, 1, 'Mt2s', esperar_error=True)
        self.registrar_test('Metros -> Mt2s (debe fallar)', exito, msg)

    def test_metros_cuadrados(self, categoria_prod, categoria_receta):
        """Test 6: Mt2s - Solo puede usar Mt2s"""
        self.stdout.write(self.style.HTTP_INFO('\n6. TEST: METROS CUADRADOS (Mt2s)'))
        self.stdout.write('-' * 80)
        
        producto = self.crear_producto('Papel Aluminio', 'Mt2s', cantidad=10, costo=100, categoria=categoria_prod)
        receta = self.crear_receta('Test Receta Mt2s', 'Receta con productos en metros cuadrados', categoria_receta)
        
        # Test válido: Mt2s -> Mt2s
        exito, msg = self.agregar_producto_a_receta(receta, producto, 2, 'Mt2s')
        self.registrar_test('Mt2s -> Mt2s', exito, msg)
        
        # Test inválido: Mt2s -> Metros
        exito, msg = self.agregar_producto_a_receta(receta, producto, 2, 'Metros', esperar_error=True)
        self.registrar_test('Mt2s -> Metros (debe fallar)', exito, msg)
        
        # Test inválido: Mt2s -> Unidades
        exito, msg = self.agregar_producto_a_receta(receta, producto, 1, 'Unidades', esperar_error=True)
        self.registrar_test('Mt2s -> Unidades (debe fallar)', exito, msg)

    def test_conversiones_invalidas(self, categoria_prod, categoria_receta):
        """Test 7: Conversiones inválidas entre diferentes tipos de medida"""
        self.stdout.write(self.style.HTTP_INFO('\n7. TEST: CONVERSIONES INVÁLIDAS ENTRE TIPOS'))
        self.stdout.write('-' * 80)
        
        # Crear varios productos con diferentes unidades
        prod_kilos = self.crear_producto('Azúcar', 'Kilos', cantidad=1, costo=60, categoria=categoria_prod)
        prod_litros = self.crear_producto('Agua', 'Litros', cantidad=1, costo=30, categoria=categoria_prod)
        prod_onzas = self.crear_producto('Queso Crema', 'Onzas', cantidad=16, costo=120, categoria=categoria_prod)
        
        receta = self.crear_receta('Test Conversiones Inválidas', 'Intentar conversiones no permitidas', categoria_receta)
        
        # Tests inválidos entre diferentes sistemas
        tests_invalidos = [
            (prod_kilos, 'Litros', 'Kilos -> Litros'),
            (prod_kilos, 'Onzas', 'Kilos -> Onzas'),
            (prod_kilos, 'Metros', 'Kilos -> Metros'),
            (prod_litros, 'Gramos', 'Litros -> Gramos'),
            (prod_litros, 'Libras', 'Litros -> Libras'),
            (prod_litros, 'Centimetros', 'Litros -> Centímetros'),
            (prod_onzas, 'Kilos', 'Onzas -> Kilos'),
            (prod_onzas, 'Mililitros', 'Onzas -> Mililitros'),
        ]
        
        for producto, medida_invalida, nombre_test in tests_invalidos:
            exito, msg = self.agregar_producto_a_receta(receta, producto, 1, medida_invalida, esperar_error=True)
            self.registrar_test(f'{nombre_test} (debe fallar)', exito, msg)

    def mostrar_resumen(self):
        """Muestra el resumen final de todos los tests"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*80))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE TESTS'.center(80)))
        self.stdout.write(self.style.SUCCESS('='*80 + '\n'))
        
        total = self.test_results['total']
        passed = len(self.test_results['passed'])
        failed = len(self.test_results['failed'])
        
        self.stdout.write(f'Total de tests ejecutados: {total}')
        self.stdout.write(self.style.SUCCESS(f'✓ Tests exitosos: {passed}'))
        
        if failed > 0:
            self.stdout.write(self.style.ERROR(f'✗ Tests fallidos: {failed}\n'))
            self.stdout.write(self.style.ERROR('Tests que fallaron:'))
            for nombre, mensaje in self.test_results['failed']:
                self.stdout.write(self.style.ERROR(f'  - {nombre}: {mensaje}'))
        else:
            self.stdout.write(self.style.SUCCESS('\n¡Todos los tests pasaron exitosamente! ✓'))
        
        porcentaje = (passed / total * 100) if total > 0 else 0
        self.stdout.write(f'\nÉxito: {porcentaje:.1f}%')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*80 + '\n'))
