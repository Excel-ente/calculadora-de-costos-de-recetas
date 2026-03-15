# -----------------------------------------------------------------------------
# Project Programacion para mortales
# Desarrollador : Kevin Turkienich
# 2024
# -----------------------------------------------------------------------------
# Dashboard con métricas completas de recetas e insumos

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Avg, Q, F, DecimalField
from django.db.models.functions import Coalesce
from administracion.dashboard_access import construir_contexto_acceso_movil
from administracion.models import Receta, Producto, ProductoReceta, Categoria, CategoriaReceta, GastosAdicionalesReceta
from configuracion.models import Configuracion
from decimal import Decimal
from collections import Counter


@staff_member_required
def dashboard_home(request):
    """
    Vista principal del dashboard con todas las métricas del emprendimiento.
    """

    # Obtener usuario actual
    usuario = request.user.username if request.user.is_authenticated else None

    # Filtrar por usuario si existe
    recetas_query = Receta.objects.all()
    productos_query = Producto.objects.all()

    if usuario:
        recetas_query = recetas_query.filter(usuario=usuario)
        productos_query = productos_query.filter(usuario=usuario)

    # ========== CONFIGURACIÓN (1 sola query, antes era 1 por cada receta) ==========
    config = Configuracion.objects.first()
    moneda = config.moneda if config else '$'
    redondeo = int(config.redondeo or 0) if config else 0
    redondeo_2 = int(config.redondeo_segunda_moneda or 0) if config else 0

    # ========== SEGUNDA MONEDA ==========
    segunda_moneda_habilitada = bool(
        config and config.habilitar_segunda_moneda and float(config.tipo_de_cambio or 0) > 0
    )
    segunda_moneda_simbolo = config.segunda_moneda if (config and config.habilitar_segunda_moneda) else ''
    tipo_de_cambio = float(config.tipo_de_cambio) if (config and float(config.tipo_de_cambio or 0) > 0) else 1

    # ========== MÉTRICAS GENERALES ==========
    total_recetas = recetas_query.count()
    total_productos = productos_query.count()
    total_categorias_receta = CategoriaReceta.objects.filter(usuario=usuario).count() if usuario else CategoriaReceta.objects.count()
    total_categorias_producto = Categoria.objects.filter(usuario=usuario).count() if usuario else Categoria.objects.count()

    # ========== PREFETCH MASIVO: 2 queries para todos los datos de recetas ==========
    # En vez de hacer 2 queries POR RECETA dentro del loop, traemos todo de una vez.
    all_pr = list(
        ProductoReceta.objects.filter(receta__in=recetas_query).select_related('producto')
    )
    all_gastos = list(
        GastosAdicionalesReceta.objects.filter(receta__in=recetas_query)
    )

    pr_by_receta = {}
    for pr in all_pr:
        pr_by_receta.setdefault(pr.receta_id, []).append(pr)

    gastos_by_receta = {}
    for g in all_gastos:
        gastos_by_receta.setdefault(g.receta_id, []).append(g)

    # ========== RECETAS MÁS CARAS Y MÁS BARATAS ==========
    # select_related('categoria') evita N+1 al acceder receta.categoria.nombre más adelante
    recetas_con_costo = []
    for receta in recetas_query.select_related('categoria'):
        try:
            pr_list = pr_by_receta.get(receta.id, [])
            gastos_list = gastos_by_receta.get(receta.id, [])

            # Calcular costo total sin tocar la BD (usa datos ya prefetcheados)
            total_productos = sum(pr.precio_total() for pr in pr_list)
            suma_adicionales = sum(
                float(g.importe) if g.importe is not None else 0
                for g in gastos_list
            )
            costo = total_productos + suma_adicionales

            porciones = float(receta.porciones) if receta.porciones else 1
            costo_porcion_val = round(costo / porciones, redondeo)

            rent = float(receta.rentabilidad or 0)
            iva = float(receta.iva or 0)
            if rent < 100:
                precio_venta = round(
                    costo_porcion_val / (100 - rent) * 100 * (1 + iva / 100),
                    redondeo,
                )
            else:
                precio_venta = 0

            recetas_con_costo.append({
                'receta': receta,
                'costo_total': costo,
                'costo_porcion': costo_porcion_val,
                'precio_venta': precio_venta,
                'rentabilidad': receta.rentabilidad,
                'porciones': receta.porciones,
                'costo_total_2': round(costo * tipo_de_cambio, redondeo_2) if segunda_moneda_habilitada else None,
                'costo_porcion_2': round(costo_porcion_val * tipo_de_cambio, redondeo_2) if segunda_moneda_habilitada else None,
                'precio_venta_2': round(precio_venta * tipo_de_cambio, redondeo_2) if segunda_moneda_habilitada else None,
            })
        except Exception:
            pass

    # Ordenar por costo
    recetas_mas_caras = sorted(recetas_con_costo, key=lambda x: x['costo_total'], reverse=True)[:5]
    recetas_mas_baratas = sorted(recetas_con_costo, key=lambda x: x['costo_total'])[:5]

    # ========== RECETAS CON MAYOR Y MENOR RENTABILIDAD ==========
    recetas_mayor_rentabilidad = sorted(recetas_con_costo, key=lambda x: float(x['rentabilidad']), reverse=True)[:5]
    recetas_menor_rentabilidad = sorted(recetas_con_costo, key=lambda x: float(x['rentabilidad']))[:5]

    # ========== ALERTAS: RECETAS CON PROBLEMAS ==========
    # Usa los datos ya prefetcheados — 0 queries adicionales en este loop
    recetas_problematicas = []
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

    for item in recetas_con_costo:
        receta = item['receta']
        problemas = []

        # Usar lista ya prefetcheada — sin query BD
        productos_receta = pr_by_receta.get(receta.id, [])
        cant_ingredientes = len(productos_receta)
        if cant_ingredientes == 0:
            problemas.append("Sin ingredientes: la receta no tiene productos asociados")

        # Ingredientes con costo 0
        ingredientes_costo_cero = [
            pr for pr in productos_receta
            if (pr.producto.costo is None or float(pr.producto.costo) == 0)
        ]
        if ingredientes_costo_cero:
            nombres = ", ".join([pr.producto.nombre for pr in ingredientes_costo_cero[:4]])
            msg = f"Ingredientes con costo $0: {nombres}"
            if len(ingredientes_costo_cero) > 4:
                msg += f" (+{len(ingredientes_costo_cero)-4} más)"
            problemas.append(msg)

        # Ingredientes con cantidad inválida (0 o negativa)
        ingredientes_cantidad_invalid = [
            pr for pr in productos_receta if float(pr.cantidad or 0) <= 0
        ]
        if ingredientes_cantidad_invalid:
            nombres = ", ".join([pr.producto.nombre for pr in ingredientes_cantidad_invalid[:4]])
            msg = f"Ingredientes con cantidad inválida: {nombres}"
            if len(ingredientes_cantidad_invalid) > 4:
                msg += f" (+{len(ingredientes_cantidad_invalid)-4} más)"
            problemas.append(msg)

        # Costo total 0 (pero tiene ingredientes)
        if item['costo_total'] == 0 and cant_ingredientes > 0:
            problemas.append("Costo total calculado igual a $0 — revisar precios de los ingredientes")

        # Inconsistencia: Unidades de medida incompatibles
        ingredientes_incompatibles = []
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
    # Reutiliza all_pr (ya en memoria) — 0 queries adicionales
    uso_productos = {}
    for pr in all_pr:
        producto_id = pr.producto.id
        if producto_id not in uso_productos:
            uso_productos[producto_id] = {
                'producto': pr.producto,
                'veces_usado': 0,
                'cantidad_total': Decimal('0'),
                'costo_total': Decimal('0'),
            }
        uso_productos[producto_id]['veces_usado'] += 1
        uso_productos[producto_id]['cantidad_total'] += pr.cantidad
        try:
            uso_productos[producto_id]['costo_total'] += Decimal(str(pr.precio_total()))
        except Exception:
            pass

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
    # recetas_query ya fue evaluada con select_related('categoria') arriba — 0 queries extra
    recetas_por_categoria = {}
    for item in recetas_con_costo:
        receta = item['receta']
        cat_nombre = receta.categoria.nombre if receta.categoria else 'Sin categoría'
        recetas_por_categoria[cat_nombre] = recetas_por_categoria.get(cat_nombre, 0) + 1

    # select_related('categoria') para evitar N+1 al acceder producto.categoria.nombre
    productos_por_categoria = {}
    productos_por_unidad = {}
    for producto in productos_query.select_related('categoria'):
        cat_nombre = producto.categoria.nombre if producto.categoria else 'Sin categoría'
        productos_por_categoria[cat_nombre] = productos_por_categoria.get(cat_nombre, 0) + 1
        unidad = producto.unidad_de_medida
        productos_por_unidad[unidad] = productos_por_unidad.get(unidad, 0) + 1

    # ========== TOP INGREDIENTES POR COSTO ==========
    ingredientes_por_costo = sorted(productos_usados, key=lambda x: float(x['costo_total']), reverse=True)[:10]
    # Agregar costo en segunda moneda a ingredientes
    if segunda_moneda_habilitada:
        for item in ingredientes_por_costo:
            item['costo_total_2'] = round(float(item['costo_total']) * tipo_de_cambio, redondeo_2)
    # Agregar costo en segunda moneda a productos sin usar
    if segunda_moneda_habilitada:
        for p in productos_sin_usar:
            pass  # Se calcula en template via .costo / tipo_de_cambio (se usan los valores del modelo)

    # ========== RECETAS CON MÁS INGREDIENTES ==========
    # Usa los dicts ya en memoria — 0 queries adicionales
    recetas_con_ingredientes = []
    for item in recetas_con_costo:
        receta = item['receta']
        num_ingredientes = len(pr_by_receta.get(receta.id, []))
        num_gastos = len(gastos_by_receta.get(receta.id, []))
        recetas_con_ingredientes.append({
            'receta': receta,
            'num_ingredientes': num_ingredientes,
            'num_gastos': num_gastos,
            'total_items': num_ingredientes + num_gastos,
        })

    recetas_mas_ingredientes = sorted(recetas_con_ingredientes, key=lambda x: x['num_ingredientes'], reverse=True)[:5]
    
    context = {
        # Generales
        'total_recetas': total_recetas,
        'total_productos': total_productos,
        'total_categorias_receta': total_categorias_receta,
        'total_categorias_producto': total_categorias_producto,
        'moneda': moneda,

        # Segunda moneda
        'segunda_moneda_habilitada': segunda_moneda_habilitada,
        'segunda_moneda_simbolo': segunda_moneda_simbolo,
        'tipo_de_cambio': tipo_de_cambio,
        
        # Recetas destacadas
        'recetas_mas_caras': recetas_mas_caras,
        'recetas_mas_baratas': recetas_mas_baratas,
        'recetas_mayor_rentabilidad': recetas_mayor_rentabilidad,
        'recetas_menor_rentabilidad': recetas_menor_rentabilidad,
        'recetas_mas_ingredientes': recetas_mas_ingredientes,
        
        # Alertas
        'recetas_problematicas': recetas_problematicas[:10],  # Limitar a 10
        'tiene_alertas': len(recetas_problematicas) > 0,
        
        # Productos/Insumos
        'productos_mas_usados': productos_mas_usados,
        'productos_menos_usados': productos_menos_usados,
        'productos_sin_usar': productos_sin_usar[:20],  # Limitar a 20
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
    }

    context.update(construir_contexto_acceso_movil(request))
    
    return render(request, 'admin/dashboard_home.html', context)
