# -----------------------------------------------------------------------------
# Project Programacion para mortales
# Desarrollador : Kevin Turkienich
# 2024
# -----------------------------------------------------------------------------
# Admin Override - Reemplaza el index del admin con dashboard personalizado

from django.contrib import admin
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Avg, Q
from administracion.dashboard_access import construir_contexto_acceso_movil
from administracion.models import Receta, Producto, ProductoReceta, Categoria, CategoriaReceta, GastosAdicionalesReceta
from configuracion.models import Configuracion
from decimal import Decimal


def custom_admin_index(request, extra_context=None):
    """
    Vista personalizada del index del admin que muestra el dashboard con métricas.
    """
    if extra_context is None:
        extra_context = {}
    
    # Obtener usuario actual
    usuario = request.user.username if request.user.is_authenticated else None
    
    # MOSTRAR TODOS los datos (sin filtrar por usuario)
    # El sistema es multi-usuario pero el dashboard muestra estadísticas globales
    recetas_query = Receta.objects.all()
    productos_query = Producto.objects.all()
    
    # ========== MÉTRICAS GENERALES ==========
    total_recetas = recetas_query.count()
    total_productos = productos_query.count()
    total_categorias_receta = CategoriaReceta.objects.count()
    total_categorias_producto = Categoria.objects.count()
    
    # ========== RECETAS MÁS CARAS Y MÁS BARATAS ==========
    recetas_con_costo = []
    for receta in recetas_query:
        try:
            costo = receta.costo_receta()
            precio_venta = receta.precio_venta_porcion()
            recetas_con_costo.append({
                'receta': receta,
                'costo_total': costo,
                'costo_porcion': receta.costo_porcion(),
                'precio_venta': precio_venta,
                'rentabilidad': receta.rentabilidad,
                'porciones': receta.porciones,
            })
        except Exception as e:
            print(f"Error calculando costo de {receta.nombre}: {e}")
            pass
    
    # Ordenar por costo
    recetas_mas_caras = sorted(recetas_con_costo, key=lambda x: x['costo_total'], reverse=True)[:5]
    recetas_mas_baratas = sorted(recetas_con_costo, key=lambda x: x['costo_total'])[:5]
    
    # ========== RECETAS CON MAYOR Y MENOR RENTABILIDAD ==========
    recetas_mayor_rentabilidad = sorted(recetas_con_costo, key=lambda x: float(x['rentabilidad']), reverse=True)[:5]
    recetas_menor_rentabilidad = sorted(recetas_con_costo, key=lambda x: float(x['rentabilidad']))[:5]
    
    # ========== ALERTAS: RECETAS CON PROBLEMAS ==========
    recetas_problematicas = []
    # Alertas: mostrar solo inconsistencias reales que requieren corrección humana
    for item in recetas_con_costo:
        receta = item['receta']
        problemas = []

        productos_receta = ProductoReceta.objects.filter(receta=receta)
        cant_ingredientes = productos_receta.count()
        if cant_ingredientes == 0:
            problemas.append("Sin ingredientes: la receta no tiene productos asociados")

        # Ingredientes con costo 0
        ingredientes_costo_cero = [pr for pr in productos_receta if (pr.producto.costo is None or float(pr.producto.costo) == 0)]
        if len(ingredientes_costo_cero) > 0:
            nombres = ", ".join([pr.producto.nombre for pr in ingredientes_costo_cero[:4]])
            msg = f"Ingredientes con costo $0: {nombres}"
            if len(ingredientes_costo_cero) > 4:
                msg += f" (+{len(ingredientes_costo_cero)-4} más)"
            problemas.append(msg)

        # Ingredientes con cantidad inválida
        ingredientes_cantidad_invalid = [pr for pr in productos_receta if float(pr.cantidad or 0) <= 0]
        if len(ingredientes_cantidad_invalid) > 0:
            nombres = ", ".join([pr.producto.nombre for pr in ingredientes_cantidad_invalid[:4]])
            msg = f"Ingredientes con cantidad inválida: {nombres}"
            if len(ingredientes_cantidad_invalid) > 4:
                msg += f" (+{len(ingredientes_cantidad_invalid)-4} más)"
            problemas.append(msg)

        # Costo total 0 (pero tiene ingredientes)
        try:
            if item['costo_total'] == 0 and cant_ingredientes > 0:
                problemas.append("Costo total calculado igual a $0 — revisar precios de los ingredientes")
        except Exception:
            pass

        # Unidades incompatibles
        ingredientes_incompatibles = []
        valid_conversions = {
            'Unidades': ['Unidades'],
            'Kilos': ['Kilos', 'Gramos'],
            'Gramos': ['Kilos', 'Gramos'],
            'Litros': ['Litros', 'Mililitros'],
            'Mililitros': ['Litros', 'Mililitros'],
            'Mt2s': ['Mt2s'],
            'Onzas': ['Onzas', 'Libras'],
            'Libras': ['Onzas', 'Libras'],
            'Metros': ['Metros', 'Centimetros'],
            'Centimetros': ['Metros', 'Centimetros'],
        }

        for pr in productos_receta:
            try:
                u_prod = pr.producto.unidad_de_medida
                u_uso = pr.medida_uso
            except Exception:
                continue

            if u_prod in valid_conversions:
                if u_uso not in valid_conversions[u_prod]:
                    ingredientes_incompatibles.append(f"{pr.producto.nombre} ({u_prod}→{u_uso})")
            else:
                if u_prod != u_uso:
                    ingredientes_incompatibles.append(f"{pr.producto.nombre} ({u_prod}→{u_uso})")

        if ingredientes_incompatibles:
            max_show = 4
            mostrar = ", ".join(ingredientes_incompatibles[:max_show])
            if len(ingredientes_incompatibles) > max_show:
                mostrar += f" (+{len(ingredientes_incompatibles)-max_show} más)"
            problemas.append(f"Unidades incompatibles: {mostrar}")

        if problemas:
            recetas_problematicas.append({
                'receta': receta,
                'problema': 'Inconsistencias detectadas',
                'tipo': 'danger',
                'detalle': '; '.join(problemas)
            })
    
    # ========== INSUMOS MÁS Y MENOS USADOS ==========
    productos_en_recetas = ProductoReceta.objects.filter(receta__in=recetas_query)
    
    uso_productos = {}
    
    for pr in productos_en_recetas:
        producto_id = pr.producto.id
        if producto_id not in uso_productos:
            uso_productos[producto_id] = {
                'producto': pr.producto,
                'veces_usado': 0,
                'cantidad_total': Decimal('0'),
                'costo_total': Decimal('0')
            }
        
        uso_productos[producto_id]['veces_usado'] += 1
        uso_productos[producto_id]['cantidad_total'] += pr.cantidad
        try:
            uso_productos[producto_id]['costo_total'] += Decimal(str(pr.precio_total()))
        except:
            pass
    
    # Convertir a lista y ordenar
    productos_usados = list(uso_productos.values())
    productos_mas_usados = sorted(productos_usados, key=lambda x: x['veces_usado'], reverse=True)[:10]
    productos_menos_usados = sorted(productos_usados, key=lambda x: x['veces_usado'])[:10]
    
    # ========== INSUMOS NO UTILIZADOS ==========
    productos_ids_usados = set(uso_productos.keys())
    todos_productos_ids = set(productos_query.values_list('id', flat=True))
    productos_sin_usar_ids = todos_productos_ids - productos_ids_usados
    productos_sin_usar = productos_query.filter(id__in=productos_sin_usar_ids)
    
    # ========== ESTADÍSTICAS DE COSTOS ==========
    if recetas_con_costo:
        promedio_costo_receta = sum(r['costo_total'] for r in recetas_con_costo) / len(recetas_con_costo)
        promedio_rentabilidad = sum(float(r['rentabilidad']) for r in recetas_con_costo) / len(recetas_con_costo)
        promedio_porciones = sum(float(r['porciones']) for r in recetas_con_costo) / len(recetas_con_costo)
    else:
        promedio_costo_receta = 0
        promedio_rentabilidad = 0
        promedio_porciones = 0
    
    # ========== DISTRIBUCIÓN POR CATEGORÍAS ==========
    recetas_por_categoria = {}
    for receta in recetas_query:
        cat_nombre = receta.categoria.nombre if receta.categoria else 'Sin categoría'
        if cat_nombre not in recetas_por_categoria:
            recetas_por_categoria[cat_nombre] = 0
        recetas_por_categoria[cat_nombre] += 1
    
    productos_por_categoria = {}
    for producto in productos_query:
        cat_nombre = producto.categoria.nombre if producto.categoria else 'Sin categoría'
        if cat_nombre not in productos_por_categoria:
            productos_por_categoria[cat_nombre] = 0
        productos_por_categoria[cat_nombre] += 1
    
    # ========== DISTRIBUCIÓN POR UNIDAD DE MEDIDA ==========
    productos_por_unidad = {}
    for producto in productos_query:
        unidad = producto.unidad_de_medida
        if unidad not in productos_por_unidad:
            productos_por_unidad[unidad] = 0
        productos_por_unidad[unidad] += 1
    
    # ========== TOP INGREDIENTES POR COSTO ==========
    ingredientes_por_costo = sorted(productos_usados, key=lambda x: float(x['costo_total']), reverse=True)[:10]
    
    # ========== RECETAS CON MÁS INGREDIENTES ==========
    recetas_con_ingredientes = []
    for receta in recetas_query:
        num_ingredientes = ProductoReceta.objects.filter(receta=receta).count()
        num_gastos = GastosAdicionalesReceta.objects.filter(receta=receta).count()
        recetas_con_ingredientes.append({
            'receta': receta,
            'num_ingredientes': num_ingredientes,
            'num_gastos': num_gastos,
            'total_items': num_ingredientes + num_gastos
        })
    
    recetas_mas_ingredientes = sorted(recetas_con_ingredientes, key=lambda x: x['num_ingredientes'], reverse=True)[:5]
    
    # Obtener configuración para moneda
    config = Configuracion.objects.first()
    moneda = config.moneda if config else '$'
    
    # ========== ACTUALIZAR CONTEXTO ==========
    extra_context.update({
        # IMPORTANTE: Mantener las apps del admin
        'available_apps': admin.site.get_app_list(request),
        
        # Generales
        'total_recetas': total_recetas,
        'total_productos': total_productos,
        'total_categorias_receta': total_categorias_receta,
        'total_categorias_producto': total_categorias_producto,
        'moneda': moneda,
        
        # Recetas destacadas
        'recetas_mas_caras': recetas_mas_caras,
        'recetas_mas_baratas': recetas_mas_baratas,
        'recetas_mayor_rentabilidad': recetas_mayor_rentabilidad,
        'recetas_menor_rentabilidad': recetas_menor_rentabilidad,
        'recetas_mas_ingredientes': recetas_mas_ingredientes,
        
        # Alertas
        'recetas_problematicas': recetas_problematicas[:10],
        'tiene_alertas': len(recetas_problematicas) > 0,
        
        # Productos/Insumos
        'productos_mas_usados': productos_mas_usados,
        'productos_menos_usados': productos_menos_usados,
        'productos_sin_usar': productos_sin_usar[:20],
        'ingredientes_por_costo': ingredientes_por_costo,
        
        # Estadísticas
        'promedio_costo_receta': promedio_costo_receta,
        'promedio_rentabilidad': promedio_rentabilidad,
        'promedio_porciones': promedio_porciones,
        
        # Distribuciones
        'recetas_por_categoria': recetas_por_categoria,
        'productos_por_categoria': productos_por_categoria,
        'productos_por_unidad': productos_por_unidad,
        
        # Usuario
        'usuario': usuario,
    })

    extra_context.update(construir_contexto_acceso_movil(request))

    
    return TemplateResponse(request, "admin/dashboard_home.html", extra_context)


# Reemplazar el index del admin con nuestro dashboard
admin.site.index = custom_admin_index
