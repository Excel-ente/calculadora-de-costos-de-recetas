from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import legal, A4
from reportlab.pdfgen import canvas
from django.contrib import admin

from .models import *
from configuracion.models import Configuracion
from django.db.models import Q, Count
from django.shortcuts import render
from django.shortcuts import render, redirect
import textwrap
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.db.models import Prefetch,Q
from .Reporte import build_pdf_costos


def _fn(v, d=2):
    """Formato numérico argentino: punto para miles, coma para decimal."""
    s = f'{float(v):,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import admin
import math
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor


@staff_member_required
def simulador_fabricacion(request):
    """Página para crear un plan de fabricación: seleccionar recetas y cantidades y generar PDF con insumos consolidados."""
    config = Configuracion.objects.first()

    if request.method == 'POST':
        receta_ids = request.POST.getlist('receta_id')
        cantidades = request.POST.getlist('cantidad')

        # Sanitize inputs and build plan list
        plan = []
        for rid, qty in zip(receta_ids, cantidades):
            try:
                r = Receta.objects.get(pk=int(rid))
                q = float(qty or 0)
                if q <= 0:
                    continue
                plan.append({'receta': r, 'cantidad': q})
            except Exception:
                continue

        if not plan:
            return render(request, 'admin/fabricacion_simulador.html', {
                'recetas': Receta.objects.all(),
                'error': 'Por favor ingrese al menos una receta y cantidad válida.',
                # IMPORTANTE: Mantener las apps del admin (para que el nav siga mostrando todo)
                'available_apps': admin.site.get_app_list(request),
            })

        # Aggregate ingredients
        aggregated = {}
        gastos_adicionales_total = 0.0

        for item in plan:
            receta = item['receta']
            factor = float(item['cantidad'])

            # Sum gastos adicionales per receta
            gastos = GastosAdicionalesReceta.objects.filter(receta=receta)
            gastos_adicionales_total += sum(float(g.importe or 0) * factor for g in gastos)

            productos_receta = ProductoReceta.objects.filter(receta=receta)
            for pr in productos_receta:
                # convertir cantidad a la unidad del producto
                cantidad_en_unidad_producto = float(pr.convertir_unidad() or 0) * factor
                prod = pr.producto
                key = prod.id

                if key not in aggregated:
                    aggregated[key] = {
                        'producto': prod,
                        'cantidad_total': 0.0
                    }

                aggregated[key]['cantidad_total'] += cantidad_en_unidad_producto

        # Convert aggregated dict to list and compute purchase info
        result = []
        for data in aggregated.values():
            prod = data['producto']
            need = float(data['cantidad_total'])
            pack_size = float(prod.cantidad or 1)  # paquete o unidad de compra
            cost_per_pack = float(prod.costo or 0)
            unit_price = cost_per_pack / pack_size if pack_size != 0 else 0
            packs_needed = need / pack_size if pack_size != 0 else 0
            packs_to_buy = math.ceil(packs_needed) if pack_size != 0 else 0
            cost_exact = need * unit_price
            cost_buy = packs_to_buy * cost_per_pack

            result.append({
                # IMPORTANTE: Mantener las apps del admin
                'available_apps': admin.site.get_app_list(request),
        
                'producto': prod,
                'need': need,
                'unit': prod.unidad_de_medida,
                'pack_size': pack_size,
                'cost_per_pack': cost_per_pack,
                'unit_price': unit_price,
                'packs_needed': packs_needed,
                'packs_to_buy': packs_to_buy,
                'cost_exact': cost_exact,
                'cost_buy': cost_buy,
            })

        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Simulador_Fabricacion.pdf"'
        build_simulador_pdf(response, plan, result, gastos_adicionales_total, config)
        return response

    # GET -> render form
    recetas = Receta.objects.all().order_by('nombre')
    return render(request, 'admin/fabricacion_simulador.html', {
        'recetas': recetas,
        # IMPORTANTE: Mantener las apps del admin (para que el nav siga mostrando todo)
        'available_apps': admin.site.get_app_list(request),
    })


def build_simulador_pdf(response, plan, aggregated_result, gastos_total, config):
    """Genera el PDF del plan de fabricación con insumos agregados."""
    # basic styling - reusing colors
    BG_COLOR = HexColor('#FFF8F9')
    PRIMARY = HexColor('#D81B60')
    TEXT_COLOR = HexColor('#333333')
    MUTED = HexColor('#6B7280')
    BORDER = HexColor('#E5E7EB')
    INFO_BG = HexColor('#FCE7F3')
    SUMMARY_BG = HexColor('#FFF1F2')
    SUCCESS_BG = HexColor('#ECFDF5')
    SUCCESS_TEXT = HexColor('#047857')
    WARNING_BG = HexColor('#FFF7ED')
    WARNING_TEXT = HexColor('#C2410C')
    currency = config.moneda if config else '$'

    width, height = A4
    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle('Simulador de Fabricacion')

    left = 40
    right = width - 40
    usable = right - left

    def draw_page_background():
        p.setFillColor(BG_COLOR)
        p.rect(0, 0, width, height, fill=1, stroke=0)

    def draw_logo():
        if config and config.logo:
            try:
                img = ImageReader(config.logo)
                p.drawImage(img, width - 140, height - 100, width=80, height=80, mask='auto')
            except Exception:
                pass

    def draw_page_header(current_y, continued=False):
        draw_page_background()
        p.setFillColor(PRIMARY)
        p.setFont('Helvetica-Bold', 18)
        p.drawString(left, height - 56, 'Simulador de Fabricación')
        p.setFillColor(MUTED)
        p.setFont('Helvetica', 9)
        subtitle = 'Informe consolidado de insumos, consumo real y presupuesto minimo de compra'
        p.drawString(left, height - 70, subtitle)
        if continued:
            p.setFillColor(TEXT_COLOR)
            p.setFont('Helvetica-Bold', 8)
            p.drawString(left, height - 82, 'Continuacion del detalle de insumos')
        draw_logo()
        return height - (96 if continued else 80)

    def draw_info_box(x, y_top, box_width, box_height, title, body, fill_color):
        p.setFillColor(fill_color)
        p.roundRect(x, y_top - box_height, box_width, box_height, 8, fill=1, stroke=0)
        p.setFillColor(TEXT_COLOR)
        p.setFont('Helvetica-Bold', 9)
        p.drawString(x + 8, y_top - 14, title)
        p.setFont('Helvetica', 7)
        wrapped_lines = textwrap.wrap(body, width=38)
        line_y = y_top - 25
        for line in wrapped_lines[:2]:
            p.drawString(x + 10, line_y, line)
            line_y -= 9

    def draw_table_header(current_y):
        p.setFillColor(PRIMARY)
        p.setFont('Helvetica-Bold', 9)
        p.drawString(product_left, current_y, 'Producto')
        p.drawCentredString((product_right + need_right) / 2, current_y, 'Necesario')
        p.drawCentredString((need_right + packunit_right) / 2, current_y, 'Compra')
        p.drawCentredString((packunit_right + packs_right) / 2, current_y, 'Paq.')
        p.drawCentredString((packs_right + cost_exact_right) / 2, current_y, 'Costo exacto')
        p.drawCentredString((cost_exact_right + cost_buy_right) / 2, current_y, 'Total compra')
        current_y -= 10
        p.setStrokeColor(BORDER)
        # p.line(left, current_y, right, current_y)
        p.setFillColor(TEXT_COLOR)
        return current_y - 6

    def ensure_space(current_y, required_height):
        if current_y - required_height < 70:
            p.showPage()
            new_y = draw_page_header(height - 60, continued=True)
            p.setFillColor(TEXT_COLOR)
            return draw_table_header(new_y - 8)
        return current_y

    def draw_summary_row(current_y, label, value, fill_color, value_color=TEXT_COLOR):
        box_height = 22
        p.setFillColor(fill_color)
        p.roundRect(left, current_y - box_height, usable, box_height, 6, fill=1, stroke=0)
        p.setFillColor(TEXT_COLOR)
        p.setFont('Helvetica-Bold', 10)
        p.drawString(left + 10, current_y - 14, label)
        p.setFillColor(value_color)
        p.drawRightString(right - 10, current_y - 14, value)
        p.setFillColor(TEXT_COLOR)
        return current_y - (box_height + 6)

    y = draw_page_header(height - 60)

    # date and summary
    p.setFillColor(TEXT_COLOR)
    p.setFont('Helvetica', 10)
    y -= 8
    p.setFont('Helvetica-Bold', 11)
    p.drawString(left, y, 'Como leer este informe')
    y -= 8
    draw_info_box(left, y, (usable / 2) - 6, 34, 'Costo exacto', 'Valor realmente consumido segun la produccion.', INFO_BG)
    draw_info_box(left + (usable / 2) + 6, y, (usable / 2) - 6, 34, 'Presupuesto de compra', 'Dinero minimo para comprar envases completos.', WARNING_BG)
    y -= 48

    p.setFont('Helvetica-Bold', 11)
    p.drawString(left, y, 'Plan cargado')
    y -= 20

    p.setFont('Helvetica', 9)
    for item in plan:
        receta_label = f"- {item['receta'].nombre} x {item['cantidad']}"
        p.drawString(left + 20, y, receta_label[:78])
        y -= 12

    y -= 10
    p.setFont('Helvetica-Bold', 12)
    p.drawString(left, y, 'Insumos consolidados')
    p.setFont('Helvetica', 8)
    p.setFillColor(MUTED)
    p.drawString(left + 162, y + 1, 'Necesario = consumo real | Paq. = envases minimos a comprar')
    p.setFillColor(TEXT_COLOR)
    y -= 14

    # table layout with fixed column widths so headers and values share the same boundaries
    column_widths = [0.32, 0.16, 0.16, 0.10, 0.13, 0.13]
    scaled_widths = [usable * portion for portion in column_widths]

    col_edges = [left]
    for col_width in scaled_widths:
        col_edges.append(col_edges[-1] + col_width)

    product_left = col_edges[0]
    product_right = col_edges[1]
    need_right = col_edges[2]
    packunit_right = col_edges[3]
    packs_right = col_edges[4]
    cost_exact_right = col_edges[5]
    cost_buy_right = col_edges[6]
    column_padding = 4

    y = draw_table_header(y)

    p.setFont('Helvetica', 9)
    total_cost_exact = 0.0
    total_cost_buy = 0.0

    for row in aggregated_result:
        prod = row['producto']
        need = row['need']
        unit = row['unit']
        pack_size = row['pack_size']
        packs_to_buy = row['packs_to_buy']
        cost_exact = row['cost_exact']
        cost_buy = row['cost_buy']

        total_cost_exact += cost_exact
        total_cost_buy += cost_buy

        # Row text
        y = ensure_space(y, 18)

        # product name (wrap if too long)
        name = prod.nombre if hasattr(prod, 'nombre') else str(prod)
        p.drawString(product_left, y, name[:34])
        p.drawRightString(need_right - column_padding, y, f"{_fn(need, 3)} {unit}")
        p.drawRightString(packunit_right - column_padding, y, f"{_fn(pack_size, 3)} {unit}")
        p.drawRightString(packs_right - column_padding, y, str(packs_to_buy))
        p.drawRightString(cost_exact_right - column_padding, y, f"{currency} {_fn(cost_exact)}")
        p.drawRightString(cost_buy_right - column_padding, y, f"{currency} {_fn(cost_buy)}")
        y -= 16

    total_purchase_budget = total_cost_buy + gastos_total

    y -= 4
    y = ensure_space(y, 130)

    p.setFont('Helvetica-Bold', 12)
    p.setFillColor(PRIMARY)
    p.drawString(left, y, 'Resumen final para decidir compra')
    y -= 10

    p.setFillColor(MUTED)
    p.setFont('Helvetica', 9)
    p.drawString(left, y, 'Este bloque diferencia lo que consumes realmente de lo que necesitas tener disponible para comprar.')
    y -= 18

    y = draw_summary_row(y, 'Costo exacto total de insumos usados', f'{currency} {_fn(total_cost_exact)}', INFO_BG)
    y = draw_summary_row(y, 'Compra minima por paquetes completos', f'{currency} {_fn(total_cost_buy)}', WARNING_BG, WARNING_TEXT)

    if gastos_total:
        y = draw_summary_row(y, 'Gastos adicionales del plan', f'{currency} {_fn(gastos_total)}', SUMMARY_BG)

    y = draw_summary_row(y, 'Monto recomendado para salir a comprar', f'{currency} {_fn(total_purchase_budget)}', SUCCESS_BG, SUCCESS_TEXT)

    y -= 4
    p.setFillColor(MUTED)
    p.setFont('Helvetica', 8)
    explanation_lines = [
        'Costo exacto: representa solo lo que realmente se usa en la produccion.',
        'Monto recomendado para salir a comprar: incluye paquetes minimos completos y gastos adicionales del plan.',
        'Ejemplo: si un producto viene en envases de 10 kilos, aunque uses menos, debes contar con el valor del envase completo.'
    ]
    for line in explanation_lines:
        p.drawString(left, y, line)
        y -= 10

    p.save()


def logout_view(request):
    auth_logout(request)
    return redirect('/')
    
# Función para dibujar texto con salto de línea si es necesario
def draw_text_with_wrapping(p, text, x, y, max_chars_per_line):
    lines = textwrap.wrap(text, width=max_chars_per_line)
    for line in lines:
        p.drawString(x, y, line)
        y -= 15  # Ajustar esta cantidad según el espacio que quieras entre líneas
    return y  # Devuelve la nueva posición y

def custom_bad_request(request, exception):
    return render(request, 'sin_acceso.html', {})#status=400

def descargar(request, id_receta):

    pedido = get_object_or_404(Receta, id=id_receta)
    config = Configuracion.objects.first()

    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receta_{pedido.nombre}.pdf"'

    build_pdf_costos(response, pedido, config)

    return response
