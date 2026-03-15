from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from django.contrib import admin, messages
from .models import BienReceta, GastosAdicionalesReceta, ProductoReceta, PasosReceta
from configuracion.models import Configuracion

# Colores y Estilos
BG_COLOR = HexColor('#FFF0F5')  # Rosa claro (LavenderBlush)
PRIMARY_COLOR = HexColor('#D81B60')  # Rosa oscuro/Fucsia para títulos
TEXT_COLOR = HexColor('#333333')  # Gris oscuro para texto
LINE_COLOR = HexColor('#D81B60')


def _fn(v, d=2):
    """Formato numérico argentino: punto para miles, coma para decimal."""
    s = f'{float(v):,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

def setup_canvas(response, title):
    p = canvas.Canvas(response, pagesize=A4)
    p.setTitle(title)
    return p

def draw_background(p, width, height):
    p.setFillColor(BG_COLOR)
    p.rect(0, 0, width, height, fill=1, stroke=0)

def draw_header(p, width, height, config):
    # Logo del emprendimiento
    if config and config.logo:
        try:
            logo_img = ImageReader(config.logo)
            # Mantener aspecto cuadrado o ajustar según necesidad
            p.drawImage(logo_img, 40, height - 100, width=80, height=80, mask='auto', preserveAspectRatio=True)
        except Exception:
            pass

    # Nombre del emprendimiento
    p.setFillColor(PRIMARY_COLOR)
    p.setFont("Helvetica-Bold", 22)
    nombre = config.nombre_emprendimiento if config else "Mi Emprendimiento"
    p.drawString(140, height - 60, nombre)

    # Redes sociales y contacto
    p.setFillColor(TEXT_COLOR)
    p.setFont("Helvetica", 10)
    y_info = height - 75
    
    if config:
        if config.telefono:
            p.drawString(140, y_info, f"Tel: {config.telefono}")
            y_info -= 12
        if config.redes_sociales:
            p.drawString(140, y_info, f"{config.redes_sociales}")

    # Línea separadora
    p.setStrokeColor(LINE_COLOR)
    p.setLineWidth(1)
    p.line(40, height - 110, width - 40, height - 110)
    
    return height - 140

def check_page_break(p, y, width, height, config):
    if y < 50:
        p.showPage()
        draw_background(p, width, height)
        # Opcional: Redibujar header pequeño o solo margen
        return height - 50
    return y

def build_pdf_costos(response, pedido, config):
    moneda = config.moneda if config else "$"
    width, height = A4
    p = setup_canvas(response, f"Receta {pedido.nombre}")
    desglose = pedido.desglose_costos()

    # Segunda moneda
    segunda_moneda_activa = bool(
        config and config.habilitar_segunda_moneda and float(config.tipo_de_cambio or 0) > 0
    )
    segunda_moneda = config.segunda_moneda if segunda_moneda_activa else ''
    tc = float(config.tipo_de_cambio) if segunda_moneda_activa else 1
    redondeo_2 = int(config.redondeo_segunda_moneda or 0) if segunda_moneda_activa else 2

    def fmt2(valor):
        """Formatea un valor en segunda moneda como texto entre paréntesis."""
        if not segunda_moneda_activa:
            return ''
        return f'  ({segunda_moneda} {_fn(float(valor) * tc, max(0, redondeo_2))})'
    
    draw_background(p, width, height)
    y = draw_header(p, width, height, config)

    # Título de la Receta
    p.setFillColor(PRIMARY_COLOR)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(40, y, pedido.nombre)
    y -= 25

    # Imagen de la receta (si existe)
    if pedido.imagen:
        try:
            img = ImageReader(pedido.imagen)
            img_width = 150
            img_height = 150
            # Dibujar imagen a la derecha
            p.drawImage(img, width - 190, y - 120, width=img_width, height=img_height, mask='auto', preserveAspectRatio=True)
        except Exception:
            pass

    # Descripción y Categoría
    p.setFillColor(TEXT_COLOR)
    p.setFont("Helvetica-Oblique", 12)
    p.drawString(40, y, f"{pedido.descripcion}")
    y -= 20
    
    if pedido.categoria:
        p.setFont("Helvetica-Bold", 10)
        p.setFillColor(PRIMARY_COLOR)
        p.drawString(40, y, f"Categoría: {pedido.categoria.nombre}")
        y -= 20

    p.setFillColor(TEXT_COLOR)
    p.setFont("Helvetica", 10)
    p.drawString(40, y, f"Porciones: {pedido.porciones}")
    y -= 30

    # --- Sección de Costos ---
    # Resumen Financiero
    p.setFillColor(PRIMARY_COLOR)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "RESUMEN DE COSTOS")
    y -= 20

    p.setFillColor(TEXT_COLOR)
    p.setFont("Helvetica", 10)
    
    costo_total = desglose['total']
    costo_porcion = pedido.costo_porcion()
    precio_venta = pedido.precio_venta_porcion()
    precio_total = pedido.precio_venta_total()

    p.drawString(40, y, f"Costo Total Receta: {moneda} {_fn(costo_total)}{fmt2(costo_total)}")
    y -= 15
    p.drawString(40, y, f"Costo Insumos: {moneda} {_fn(desglose['insumos'])}{fmt2(desglose['insumos'])}")
    y -= 15
    p.drawString(40, y, f"Gastos Adicionales: {moneda} {_fn(desglose['gastos_adicionales'])}{fmt2(desglose['gastos_adicionales'])}")
    y -= 15
    p.drawString(40, y, f"Bienes (Depreciacion + Electricidad): {moneda} {_fn(desglose['bienes_total'])}{fmt2(desglose['bienes_total'])}")
    y -= 15
    p.drawString(40, y, f"Depreciacion de Bienes: {moneda} {_fn(desglose['bienes_depreciacion'])}{fmt2(desglose['bienes_depreciacion'])}")
    y -= 15
    p.drawString(40, y, f"Electricidad de Bienes: {moneda} {_fn(desglose['bienes_electricidad'])}{fmt2(desglose['bienes_electricidad'])}")
    y -= 15
    p.drawString(40, y, f"Costo por Porción: {moneda} {_fn(costo_porcion)}{fmt2(costo_porcion)}")
    y -= 15
    p.drawString(40, y, f"Precio Venta Sugerido (Porción): {moneda} {_fn(precio_venta)}{fmt2(precio_venta)}")
    y -= 15
    p.drawString(40, y, f"Precio Venta Total: {moneda} {_fn(precio_total)}{fmt2(precio_total)}")
    y -= 30

    # Insumos (Ingredientes)
    insumos = ProductoReceta.objects.filter(receta=pedido)
    if insumos:
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "INGREDIENTES Y COSTOS")
        y -= 20
        
        p.setFillColor(TEXT_COLOR)
        for insumo in insumos:
            y = check_page_break(p, y, width, height, config)
            nombre_prod = insumo.producto.nombre.upper()
            precio_insumo = insumo.precio_total()
            detalle = f"{insumo.cantidad} {insumo.medida_uso} - {moneda} {_fn(precio_insumo)}{fmt2(precio_insumo)}"
            
            p.setFont("Helvetica-Bold", 9)
            p.drawString(50, y, f"• {nombre_prod}")
            
            p.setFont("Helvetica", 9)
            right_margin = width - 60
            p.drawRightString(right_margin, y, detalle) 
            
            # Generar línea de puntos
            start_x = 50 + p.stringWidth(f"• {nombre_prod}", "Helvetica-Bold", 9) + 5
            end_x = right_margin - p.stringWidth(detalle, "Helvetica", 9) - 5
            
            if end_x > start_x:
                dot_w = p.stringWidth(".", "Helvetica", 9)
                num_dots = int((end_x - start_x) / dot_w)
                dots = "." * num_dots
                while p.stringWidth(dots, "Helvetica", 9) > (end_x - start_x) and len(dots) > 0:
                    dots = dots[:-1]
                p.drawString(start_x, y, dots)
            
            y -= 15

    y -= 10

    # Gastos Adicionales
    gastos = GastosAdicionalesReceta.objects.filter(receta=pedido)
    if gastos:
        y = check_page_break(p, y, width, height, config)
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "GASTOS ADICIONALES")
        y -= 20
        
        p.setFillColor(TEXT_COLOR)
        for gasto in gastos:
            y = check_page_break(p, y, width, height, config)
            detalle_gasto = f"{moneda} {_fn(gasto.importe)}{fmt2(gasto.importe)}"
            
            p.setFont("Helvetica", 9)
            p.drawString(50, y, f"• {gasto.detalle}")
            
            right_margin = width - 60
            p.drawRightString(right_margin, y, detalle_gasto)
            
            # Generar línea de puntos para gastos también
            start_x = 50 + p.stringWidth(f"• {gasto.detalle}", "Helvetica", 9) + 5
            end_x = right_margin - p.stringWidth(detalle_gasto, "Helvetica", 9) - 5
            
            if end_x > start_x:
                dot_w = p.stringWidth(".", "Helvetica", 9)
                num_dots = int((end_x - start_x) / dot_w)
                dots = "." * num_dots
                while p.stringWidth(dots, "Helvetica", 9) > (end_x - start_x) and len(dots) > 0:
                    dots = dots[:-1]
                p.drawString(start_x, y, dots)

            y -= 15

    y -= 20

    bienes = BienReceta.objects.filter(receta=pedido).select_related('bien')
    if bienes:
        y = check_page_break(p, y, width, height, config)
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "BIENES DE PRODUCCION")
        y -= 20

        p.setFillColor(TEXT_COLOR)
        for bien in bienes:
            y = check_page_break(p, y, width, height, config)
            p.setFont("Helvetica-Bold", 9)
            p.drawString(50, y, f"• {bien.bien.nombre.upper()}")
            y -= 12

            p.setFont("Helvetica", 9)
            detalle = (
                f"Uso: {bien.tiempo_uso_label()} | "
                f"Depreciacion: {moneda} {_fn(bien.costo_depreciacion())}{fmt2(bien.costo_depreciacion())} | "
                f"Electricidad: {moneda} {_fn(bien.costo_electricidad())}{fmt2(bien.costo_electricidad())} | "
                f"Total: {moneda} {_fn(bien.costo_total())}{fmt2(bien.costo_total())}"
            )
            p.drawString(60, y, detalle[:110])
            y -= 18

    y -= 10

    # Pasos de la receta (Instrucciones)
    pasos = PasosReceta.objects.filter(receta=pedido)
    if pasos:
        y = check_page_break(p, y, width, height, config)
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(40, y, "INSTRUCCIONES")
        y -= 20
        
        p.setFillColor(TEXT_COLOR)
        for paso in pasos:
            y = check_page_break(p, y, width, height, config)
            p.setFont("Helvetica-Bold", 10)
            p.drawString(50, y, f"{paso.nombre}:")
            y -= 15
            
            # Manejo básico de texto largo para detalle
            p.setFont("Helvetica", 9)
            text_object = p.beginText(60, y)
            text_object.setFont("Helvetica", 9)
            # Dividir texto en líneas simples (muy básico, idealmente usar Paragraph de Platypus)
            words = paso.detalle.split()
            line = ""
            for word in words:
                if p.stringWidth(line + " " + word, "Helvetica", 9) < (width - 100):
                    line += " " + word
                else:
                    text_object.textLine(line)
                    y -= 12
                    line = word
            text_object.textLine(line)
            p.drawText(text_object)
            y -= 20 # Espacio extra después del bloque de texto
            
            y = check_page_break(p, y, width, height, config)

    p.save()

def build_pdf_sin_costos(response, pedido, config):
    width, height = A4
    p = setup_canvas(response, f"Receta {pedido.nombre}")
    
    draw_background(p, width, height)
    y = draw_header(p, width, height, config)

    # Título
    p.setFillColor(PRIMARY_COLOR)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(40, y, pedido.nombre)
    y -= 30

    # Imagen centrada o grande si es para compartir
    if pedido.imagen:
        try:
            img = ImageReader(pedido.imagen)
            # Imagen más grande y centrada
            img_width = 250
            img_height = 200
            p.drawImage(img, (width - img_width) / 2, y - 210, width=img_width, height=img_height, mask='auto', preserveAspectRatio=True)
            y -= 230
        except Exception:
            pass

    # Descripción
    p.setFillColor(TEXT_COLOR)
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width / 2, y, f"{pedido.descripcion}")
    y -= 30
    
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, y, f"Rinde: {pedido.porciones} porciones")
    y -= 40

    # Ingredientes (Solo cantidades)
    insumos = ProductoReceta.objects.filter(receta=pedido)
    if insumos:
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, y, "INGREDIENTES")
        y -= 25
        
        p.setFillColor(TEXT_COLOR)
        p.setFont("Helvetica", 11)
        for insumo in insumos:
            y = check_page_break(p, y, width, height, config)
            nombre_prod = insumo.producto.nombre
            cantidad = f"{insumo.cantidad} {insumo.medida_uso}"
            p.drawString(60, y, f"• {cantidad} de {nombre_prod}")
            y -= 18

    y -= 20

    # Instrucciones
    pasos = PasosReceta.objects.filter(receta=pedido)
    if pasos:
        y = check_page_break(p, y, width, height, config)
        p.setFillColor(PRIMARY_COLOR)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(40, y, "PREPARACIÓN")
        y -= 25
        
        p.setFillColor(TEXT_COLOR)
        for paso in pasos:
            y = check_page_break(p, y, width, height, config)
            p.setFont("Helvetica-Bold", 11)
            p.drawString(50, y, f"{paso.nombre}")
            y -= 15
            
            p.setFont("Helvetica", 10)
            # Simple text wrapping
            words = paso.detalle.split()
            line = ""
            for word in words:
                if p.stringWidth(line + " " + word, "Helvetica", 10) < (width - 100):
                    line += " " + word
                else:
                    p.drawString(60, y, line)
                    y -= 14
                    line = word
            p.drawString(60, y, line)
            y -= 25
            
            y = check_page_break(p, y, width, height, config)

    # Pie de página bonito
    p.setFillColor(PRIMARY_COLOR)
    p.setFont("Helvetica-Oblique", 10)
    p.drawCentredString(width / 2, 30, "¡Gracias por elegirnos!")

    p.save()

@admin.action(description="Descargar Receta (Con Costos)")
def generar_receta_costos(modeladmin, request, queryset):
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo una receta para generar el informe.")
        return
    
    pedido = queryset[0]
    config = Configuracion.objects.first()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receta_Costos_{pedido.nombre}.pdf"'

    build_pdf_costos(response, pedido, config)
    return response

@admin.action(description="Descargar Receta (Sin Costos - Para Compartir)")
def generar_receta_sin_costos(modeladmin, request, queryset):
    if len(queryset) != 1:
        messages.error(request, "Seleccione solo una receta para generar el informe.")
        return
    
    pedido = queryset[0]
    config = Configuracion.objects.first()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receta_{pedido.nombre}.pdf"'

    build_pdf_sin_costos(response, pedido, config)
    return response


