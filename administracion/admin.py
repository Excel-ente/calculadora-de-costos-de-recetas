from django.contrib import admin
from django import VERSION as DJANGO_VERSION
from .models import Bien, BienReceta, Categoria, PasosReceta, Producto, Receta, GastosAdicionalesReceta, ProductoReceta, CategoriaReceta

# django-import-export (actual) puede romperse con Django 6 en changelist_view.
# Fallback a ModelAdmin para evitar que se caiga el admin en produccion.
if DJANGO_VERSION >= (6, 0):
    ImportExportModelAdmin = admin.ModelAdmin
else:
    from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields, widgets
from configuracion.models import Configuracion
from .Reporte import generar_receta_costos, generar_receta_sin_costos
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from import_export.formats.base_formats import XLSX


def _fn(v, d=2):
    """Formato numérico argentino: punto para miles, coma para decimal."""
    s = f'{float(v):,.{d}f}'
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


# -----------------------------------------------------------------------------
# # Herramienta para configurar el reporte de descarga de la receta
         
class RecetaResource(resources.ModelResource):

        nombre = fields.Field(attribute='nombre', column_name='nombre')
        descripcion = fields.Field(attribute='descripcion',  column_name='descripcion')
        categoria = fields.Field(attribute='categoria', column_name='categoria',)
        porciones = fields.Field(attribute='porciones', column_name='porciones')
        rentabilidad = fields.Field(attribute='rentabilidad',  column_name='rentabilidad')
        comentarios= fields.Field(attribute='comentarios', column_name='comentarios')
        costo_receta = fields.Field(column_name='costo_receta')
        costo_porcion = fields.Field(column_name='costo_porcion')
        precio_venta_porcion = fields.Field(column_name='precio_venta_porcion')
        precio_venta_total = fields.Field(column_name='precio_venta_total')

        class Meta:
                model = Receta

        def dehydrate_costo_receta(self, receta):
            return receta.costo_receta() if receta.pk else None

        def dehydrate_costo_porcion(self, receta):
            return receta.costo_porcion() if receta.pk else None

        def dehydrate_precio_venta_porcion(self, receta):
            valor = receta.precio_venta_porcion_num() if receta.pk else None
            return valor

        def dehydrate_precio_venta_total(self, receta):
            valor = float(receta.precio_venta_porcion_num()) * float(receta.porciones)
            return valor



# -----------------------------------------------------------------------------
# # Herramienta para configurar el reporte de descarga del producto
         
class ProductoResource(resources.ModelResource):

        codigo = fields.Field(attribute='codigo',  column_name='codigo')
        nombre = fields.Field(attribute='nombre', column_name='nombre')
        descripcion = fields.Field(attribute='descripcion',  column_name='descripcion')
        categoria = fields.Field(attribute='categoria', column_name='categoria',)
        marca = fields.Field(attribute='marca', column_name='marca')
        unidad_de_medida = fields.Field(attribute='unidad_de_medida',  column_name='unidad_de_medida')
        cantidad= fields.Field(attribute='cantidad', column_name='cantidad')
        costo= fields.Field(attribute='costo', column_name='costo')
        
        class Meta:
                model = Producto


        
# -----------------------------------------------------------------------------
# # Herramienta para configurar el reporte de descarga del producto
         
class ProductoRecetaResource(resources.ModelResource):

        class Meta:
                model = ProductoReceta


# -----------------------------------------------------------------------------
# # Registro del modelo GastosAdicionalesReceta en el admin de Django

@admin.register(CategoriaReceta)
class CategoriaRecetaAdmin(ImportExportModelAdmin):
    exclude = ('usuario',)
    list_display = ('id','nombre',)
    search_fields = ('nombre',)
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_export_formats(self):
        return [XLSX]  # Solo permitir la exportación en formato XLSX

    def get_import_formats(self):
        return [XLSX]  # Solo permitir la importación en formato XLSX
    
# -----------------------------------------------------------------------------
# Registro del modelo Categoria en el admin de Django

@admin.register(Categoria)
class CategoriaAdmin(ImportExportModelAdmin):
    exclude = ('usuario',)
    search_fields = ('nombre',)
    list_display = ('id','nombre',)
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_export_formats(self):
        return [XLSX]  # Solo permitir la exportación en formato XLSX

    def get_import_formats(self):
        return [XLSX]  # Solo permitir la importación en formato XLSX
    
# -----------------------------------------------------------------------------
# Inline para ProductoReceta, para ser usado dentro del admin de Receta

class PasosRecetaInline(admin.StackedInline):
    model = PasosReceta
    extra = 1  # Número de formularios vacíos adicionales que se muestran
    fields = ('nombre','detalle')
    exclude = ('usuario',)
    
# -----------------------------------------------------------------------------
# Inline para ProductoReceta, para ser usado dentro del admin de Receta

class ProductoRecetaInline(admin.StackedInline):
    model = ProductoReceta
    extra = 1  # Número de formularios vacíos adicionales que se muestran
    readonly_fields = ('Subtotal',)
    exclude = ('usuario',)

    # metodo para calcular el subtotal
    def Subtotal(self, obj):
        config = Configuracion.objects.first()
        moneda = config.moneda if config else '$'
        costo_total = float(obj.precio_total())
        valor = f'{moneda} {_fn(costo_total)}'
        if config and config.habilitar_segunda_moneda:
            tc = float(config.tipo_de_cambio or 0)
            if tc > 0:
                val2 = costo_total * tc
                redondeo_2 = int(config.redondeo_segunda_moneda or 0)
                return format_html(
                    '{}<br><small style="color:#6c757d;">{} {}</small>',
                    valor, config.segunda_moneda, _fn(val2, max(0, redondeo_2))
                )
        return valor


class BienRecetaInline(admin.StackedInline):
    model = BienReceta
    extra = 1
    exclude = ('usuario',)
    readonly_fields = ('Tiempo_en_horas', 'Costo_depreciacion', 'Costo_electricidad', 'Costo_total')
    fields = (
        'bien',
        'tiempo_uso_cantidad',
        'tiempo_uso_unidad',
        'incluir_depreciacion',
        'incluir_electricidad',
        'Tiempo_en_horas',
        'Costo_depreciacion',
        'Costo_electricidad',
        'Costo_total',
        'observaciones',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'bien':
            kwargs['queryset'] = Bien.objects.filter(usuario=request.user, activo=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        help_texts = {
            'bien': 'Elegí la máquina o herramienta que usaste en esta receta. Ejemplo: licuadora, horno o batidora.',
            'tiempo_uso_cantidad': 'Escribí cuánto tiempo se usa ese bien para hacer esta receta. Ejemplo: 12.',
            'tiempo_uso_unidad': 'Elegí la unidad del tiempo que escribiste. Ejemplo: Minutos, Horas o Días.',
            'incluir_depreciacion': 'Marcá esto si querés que el desgaste del equipo se sume al costo de la receta.',
            'incluir_electricidad': 'Marcá esto si querés que el consumo de luz del equipo se sume al costo de la receta.',
            'observaciones': 'Opcional. Acá podés anotar una aclaración simple, por ejemplo: usar solo en el batido inicial.',
        }
        if field and db_field.name in help_texts:
            field.help_text = help_texts[db_field.name]
        return field

    def Tiempo_en_horas(self, obj):
        if not obj.pk:
            return '-'
        return f'{_fn(obj.horas_uso())} h'

    def Costo_depreciacion(self, obj):
        if not obj.pk:
            return '-'
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_depreciacion())}'

    def Costo_electricidad(self, obj):
        if not obj.pk:
            return '-'
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_electricidad())}'

    def Costo_total(self, obj):
        if not obj.pk:
            return '-'
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_total())}'
    
# -----------------------------------------------------------------------------
# Inline para GastosAdicionalesReceta, para ser usado dentro del admin de Receta
class GastosAdicionalesRecetaInline(admin.TabularInline):
    model = GastosAdicionalesReceta
    extra = 0  # Número de formularios vacíos adicionales que se muestran
    exclude = ('usuario',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "receta":
            # Filtrar las categorías basadas en el usuario actual
            kwargs["queryset"] = Receta.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
# -----------------------------------------------------------------------------
# Registro del modelo Producto en el admin de Django


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    list_display = ('id','nombre','categoria','Cantidad','unidad_de_medida','Costo','Costo_Unitario')
    list_display_links = ('id', 'nombre','categoria','Cantidad','unidad_de_medida','Costo','Costo_Unitario')
    search_fields = ('nombre', 'marca')
    readonly_fields = ('Costo_Unitario',)
    list_filter = ('id','codigo','categoria', 'unidad_de_medida','usuario')
    resource_class = ProductoResource
    exclude = ('usuario',)
    list_per_page = 15

    def _config(self, obj):
        return Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()

    def Costo_Unitario(self, obj):
        config = self._config(obj)
        moneda = config.moneda if config else '$'
        cu = obj.costo_unitario()
        valor = f'{moneda} {_fn(cu, 3)}'
        if config and config.habilitar_segunda_moneda:
            tc = float(config.tipo_de_cambio or 0)
            if tc > 0:
                val2 = cu * tc
                redondeo_2 = int(config.redondeo_segunda_moneda or 0)
                return format_html(
                    '{}<br><small style="color:#6c757d;">{} {}</small>',
                    valor, config.segunda_moneda, _fn(val2, max(0, redondeo_2))
                )
        return valor
    Costo_Unitario.short_description = 'Costo unitario'

    def Costo_Unitario_Segunda_Moneda(self, obj):
        config = Configuracion.objects.first()
        if not config or not config.habilitar_segunda_moneda:
            return '—'
        val = obj.costo_unitario_segunda_moneda()
        if val is None:
            return '—'
        redondeo_2 = int(config.redondeo_segunda_moneda or 0)
        return f'{config.segunda_moneda} {_fn(val, max(0, redondeo_2))}'
    Costo_Unitario_Segunda_Moneda.short_description = 'Costo unitario (2ª moneda)'

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj))
        if 'Costo_Unitario' not in base:
            base.append('Costo_Unitario')

        return base

    def Costo(self, obj):
        config = self._config(obj)
        moneda = config.moneda if config else '$'
        costo = float(obj.costo)
        valor = f'{moneda} {_fn(costo)}'
        if config and config.habilitar_segunda_moneda:
            tc = float(config.tipo_de_cambio or 0)
            if tc > 0:
                val2 = costo * tc
                redondeo_2 = int(config.redondeo_segunda_moneda or 0)
                return format_html(
                    '{}<br><small style="color:#6c757d;">{} {}</small>',
                    valor, config.segunda_moneda, _fn(val2, max(0, redondeo_2))
                )
        return valor

    def Cantidad(self,obj):
          return _fn(obj.cantidad)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            # Filtrar las categorías basadas en el usuario actual
            kwargs["queryset"] = Categoria.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_list_display(self, request):
        base = ['nombre', 'Cantidad', 'unidad_de_medida', 'Costo', 'Costo_Unitario']

        return base

    def get_list_filter(self, request):
        # Mostrar el campo 'usuario' solo a los superusuarios
        if request.user.is_superuser:
            return   ('id','codigo','categoria', 'unidad_de_medida',)
        return   ('id','codigo','categoria', 'unidad_de_medida',)
    
    def get_export_formats(self):
        return [XLSX]  # Solo permitir la exportación en formato XLSX

    def get_import_formats(self):
        return [XLSX]  # Solo permitir la importación en formato XLSX


@admin.register(Bien)
class BienAdmin(ImportExportModelAdmin):
    list_display = (
        'nombre',
        'Vida_util',
        'Costo_compra',
        'Potencia',
        'Factor_uso',
        'Costo_hora',
        'Costo_electrico_hora',
        'activo',
    )
    search_fields = ('nombre', 'descripcion')
    list_filter = ('activo',)
    exclude = ('usuario',)
    list_per_page = 15
    readonly_fields = ('Explicacion_de_carga',)
    fieldsets = (
        ('Datos del bien', {
            'fields': (
                'nombre',
                'descripcion',
                'costo_compra',
                'vida_util_cantidad',
                'vida_util_unidad',
                'potencia_watts',
                'factor_uso_porcentaje',
                'activo',
            ),
        }),
        ('Guia simple para completar', {
            'fields': ('Explicacion_de_carga',),
            'description': 'Explicación pensada para usuarios que cargan el bien por primera vez.',
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        help_texts = {
            'nombre': 'Poné el nombre del equipo. Ejemplo: Licuadora Philips, Horno eléctrico o Batidora.',
            'descripcion': 'Opcional. Podés aclarar marca, modelo o para qué lo usás. Ejemplo: Licuadora de 2 litros.',
            'costo_compra': 'Es el precio que te costó comprar este bien completo. No va el costo por uso, va el valor total de compra.',
            'vida_util_cantidad': 'Escribí cuánto pensás que dura este equipo antes de quedar gastado. Ejemplo: 5.',
            'vida_util_unidad': 'Elegí en qué unidad querés medir esa duración. Ejemplo: Años, Meses, Días u Horas.',
            'potencia_watts': 'Es la potencia eléctrica del equipo en watts. Si no la sabés, podés verla en la etiqueta del producto. Ejemplo: 250.',
            'factor_uso_porcentaje': 'Es qué tanto consume luz mientras lo usás. Si consume todo el tiempo, dejalo en 100. Si trabaja por ciclos, podés bajar ese valor.',
            'activo': 'Dejá esto marcado si el bien sigue en uso. Desmarcalo solo si ya no querés usarlo en nuevas recetas.',
        }
        if field and db_field.name in help_texts:
            field.help_text = help_texts[db_field.name]
        return field

    def Explicacion_de_carga(self, obj=None):
        return mark_safe(
            '<div style="max-width:900px; line-height:1.6;">'
            '<p><strong>Cómo llenar este formulario, bien simple:</strong></p>'
            '<p>1. En <strong>Nombre</strong> escribí qué máquina es. Ejemplo: licuadora.</p>'
            '<p>2. En <strong>Costo compra</strong> poné cuánto te salió comprarla completa.</p>'
            '<p>3. En <strong>Vida útil</strong> pensá cuánto tiempo te debería durar. '
            'Ejemplo: 5 años.</p>'
            '<p>4. En <strong>Potencia watts</strong> cargá el consumo eléctrico que figura en la etiqueta o manual.</p>'
            '<p>5. En <strong>Factor uso porcentaje</strong> normalmente podés dejar 100. '
            'Solo bajalo si el equipo no consume todo el tiempo mientras está en uso.</p>'
            '<p><strong>Ejemplo real:</strong> una licuadora que costó 5000, dura 5 años y consume 250 watts.</p>'
            '<p>Después, cuando la agregues a una receta, el sistema reparte una parte de su desgaste y una parte de su luz dentro del costo de esa receta.</p>'
            '</div>'
        )

    Explicacion_de_carga.short_description = 'Explicación paso a paso'

    def Vida_util(self, obj):
        return obj.vida_util_label()

    def Costo_compra(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_compra)}'

    def Potencia(self, obj):
        return f'{_fn(obj.potencia_watts)} W'

    def Factor_uso(self, obj):
        return f'{_fn(obj.factor_uso_porcentaje)}%'

    def Costo_hora(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_hora_depreciacion())}'

    def Costo_electrico_hora(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        precio_kwh = configuracion.precio_kwh if configuracion else 0
        return f'{moneda} {_fn(obj.costo_electricidad_por_hora(precio_kwh=precio_kwh))}'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_export_formats(self):
        return [XLSX]

    def get_import_formats(self):
        return [XLSX]
    

# -----------------------------------------------------------------------------
# Registro del modelo Receta en el admin de Django
@admin.register(Receta)
class RecetaAdmin(ImportExportModelAdmin):
    list_display = ('categoria','nombre','Costo_total','rentabilidad','Precio_venta','Descargar','mostrar',)
    list_display_links = ('nombre','Costo_total','rentabilidad','Precio_venta','Descargar','mostrar',)
    list_filter = ('categoria','mostrar')
    search_fields = ('nombre',)
    inlines = [ProductoRecetaInline, BienRecetaInline, GastosAdicionalesRecetaInline, PasosRecetaInline,]
    resource_class = RecetaResource
    actions = [generar_receta_costos, generar_receta_sin_costos]
    exclude = ('usuario',)
    list_per_page = 15
    ordering = ('nombre',)

    readonly_fields = (
        'Costo_bienes',
        'Costo_bienes_depreciacion',
        'Costo_bienes_electricidad',
        'Precio_venta',
        'Precio_porcion',      # nuevos
    )

    def Costo_porcion(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first()
        if configuracion:
            moneda = configuracion.moneda
            return f'{moneda} {_fn(obj.costo_porcion())}'
        return _fn(obj.costo_porcion())

    # metodo para calcular el subtotal
    def Costo_total(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        costo = obj.costo_receta()
        valor = f'{moneda} {_fn(costo)}'
        if configuracion and configuracion.habilitar_segunda_moneda:
            tc = float(configuracion.tipo_de_cambio or 0)
            if tc > 0:
                val2 = float(costo) * tc
                redondeo_2 = int(configuracion.redondeo_segunda_moneda or 0)
                return format_html(
                    '{}<br><small style="color:#6c757d;">{} {}</small>',
                    valor, configuracion.segunda_moneda, _fn(val2, max(0, redondeo_2))
                )
        return valor

    def Costo_bienes(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_bienes())}'

    def Costo_bienes_depreciacion(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_bienes_depreciacion())}'

    def Costo_bienes_electricidad(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        return f'{moneda} {_fn(obj.costo_bienes_electricidad())}'

    # metodo para calcular el precio de venta
    def Precio_venta(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
        moneda = configuracion.moneda if configuracion else '$'
        valor = f'{moneda} {_fn(obj.precio_venta_total())}'
        if configuracion and configuracion.habilitar_segunda_moneda:
            tc = float(configuracion.tipo_de_cambio or 0)
            if tc > 0:
                val2 = obj.precio_venta_total() * tc
                redondeo_2 = int(configuracion.redondeo_segunda_moneda or 0)
                return format_html(
                    '{}<br><small style="color:#6c757d;">{} {}</small>',
                    valor, configuracion.segunda_moneda, _fn(val2, max(0, redondeo_2))
                )
        return valor
    Precio_venta.short_description = 'Precio venta'
    
    def Precio_porcion(self, obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first()
        if configuracion:
            moneda = configuracion.moneda
            return f'{moneda} {_fn(obj.precio_venta_porcion_num())}'
        return _fn(obj.precio_venta_porcion_num())

    # método para botón de descargar
    def Precio_venta_segunda_moneda(self, obj):
        config = Configuracion.objects.first()
        if not config or not config.habilitar_segunda_moneda:
            return '—'
        val = obj.precio_venta_total_segunda_moneda()
        if val is None:
            return '—'
        redondeo_2 = int(config.redondeo_segunda_moneda or 0)
        return f'{config.segunda_moneda} {_fn(val, max(0, redondeo_2))}'
    Precio_venta_segunda_moneda.short_description = 'Precio venta total (2ª moneda)'

    def Precio_porcion_segunda_moneda(self, obj):
        config = Configuracion.objects.first()
        if not config or not config.habilitar_segunda_moneda:
            return '—'
        val = obj.precio_venta_porcion_segunda_moneda()
        if val is None:
            return '—'
        redondeo_2 = int(config.redondeo_segunda_moneda or 0)
        return f'{config.segunda_moneda} {_fn(val, max(0, redondeo_2))}'
    Precio_porcion_segunda_moneda.short_description = 'Precio porción (2ª moneda)'

    def get_readonly_fields(self, request, obj=None):
        base = list(super().get_readonly_fields(request, obj))
        config = Configuracion.objects.first()
        if config and config.habilitar_segunda_moneda:
            for campo in ('Precio_venta_segunda_moneda', 'Precio_porcion_segunda_moneda'):
                if campo not in base:
                    base.append(campo)
        return base
    def Descargar(self, obj):
        return format_html('<a class="btn btn-secondary" href="{}">⬇️ PDF</a>', reverse('descargar', args=[obj.id]))
    Descargar.short_description = "Acciones"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria":
            # Filtrar las categorías basadas en el usuario actual
            kwargs["queryset"] = CategoriaReceta.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def get_export_formats(self):
        return [XLSX]  # Solo permitir la exportación en formato XLSX

    def get_import_formats(self):
        return [XLSX]  # Solo permitir la importación en formato XLSX


# @admin.register(BienReceta)
# class BienRecetaAdmin(ImportExportModelAdmin):
#     list_display = ('bien', 'receta', 'Tiempo_uso', 'Costo_depreciacion', 'Costo_electricidad', 'Costo_total')
#     exclude = ('usuario',)
#     list_filter = ('bien', 'receta')
#     search_fields = ('bien__nombre', 'receta__nombre')
#     list_per_page = 15

#     def Tiempo_uso(self, obj):
#         return obj.tiempo_uso_label()

#     def Costo_depreciacion(self, obj):
#         configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
#         moneda = configuracion.moneda if configuracion else '$'
#         return f'{moneda} {obj.costo_depreciacion():,.2f}'

#     def Costo_electricidad(self, obj):
#         configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
#         moneda = configuracion.moneda if configuracion else '$'
#         return f'{moneda} {obj.costo_electricidad():,.2f}'

#     def Costo_total(self, obj):
#         configuracion = Configuracion.objects.filter(usuario=obj.usuario).first() or Configuracion.objects.first()
#         moneda = configuracion.moneda if configuracion else '$'
#         return f'{moneda} {obj.costo_total():,.2f}'

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == 'bien':
#             kwargs['queryset'] = Bien.objects.filter(usuario=request.user, activo=True)
#         if db_field.name == 'receta':
#             kwargs['queryset'] = Receta.objects.filter(usuario=request.user)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             obj.usuario = request.user
#         super().save_model(request, obj, form, change)

#     def get_export_formats(self):
#         return [XLSX]

#     def get_import_formats(self):
#         return [XLSX]
    
# # -----------------------------------------------------------------------------
# # Registro del modelo Producto receta en el admin de Django
@admin.register(ProductoReceta)
class ProductoRecetaAdmin(ImportExportModelAdmin):
    list_display = ('Producto', 'receta','Cantidad','medida_uso','Costo_Unitario','Total',)
    readonly_fields = ('producto', 'receta','Cantidad','medida_uso','Costo_Unitario','Total',)
    exclude = ( 'receta''medida_uso','usuario','cantidad','producto',)
    search_fields = ('codigo', 'nombre', 'marca')
    list_filter = ('id','producto__nombre', 'receta')
    resource_class = ProductoRecetaResource
    list_per_page = 15

    def Producto(self,obj):
        return f'{obj.producto.nombre} {obj.producto.descripcion}'

    def Costo_Unitario(self,obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first()
        if configuracion:
            moneda = configuracion.moneda
            return f'{moneda} {_fn(obj.precio_unitario())}'
        return _fn(obj.precio_unitario())

    def Total(self,obj):
        configuracion = Configuracion.objects.filter(usuario=obj.usuario).first()
        if configuracion:
            moneda = configuracion.moneda
            return f'{moneda} {_fn(obj.precio_total())}'
        return _fn(obj.precio_total())

    def Cantidad(self,obj):
        return _fn(obj.cantidad)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "producto":
            # Filtrar las categorías basadas en el usuario actual
            kwargs["queryset"] = Producto.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "receta":
            # Filtrar las categorías basadas en el usuario actual
            kwargs["queryset"] = Receta.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
     
    def save_model(self, request, obj, form, change):
        # Asignar automáticamente el usuario al registro
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


    def get_export_formats(self):
        return [XLSX]  # Solo permitir la exportación en formato XLSX

    def get_import_formats(self):
        return [XLSX]  # Solo permitir la importación en formato XLSX


# -----------------------------------------------------------------------------
# Importar admin_override para reemplazar el index del admin con dashboard
from . import admin_override
