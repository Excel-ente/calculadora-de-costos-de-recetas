from decimal import Decimal

from configuracion.models import Configuracion


ZERO = Decimal('0')
TIME_UNIT_CHOICES = [
    ('Minutos', 'Minutos'),
    ('Horas', 'Horas'),
    ('Dias', 'Dias'),
    ('Semanas', 'Semanas'),
    ('Meses', 'Meses'),
    ('Anios', 'Anios'),
]
TIME_UNIT_TO_HOURS = {
    'Minutos': Decimal('0.0166666667'),
    'Horas': Decimal('1'),
    'Dias': Decimal('24'),
    'Semanas': Decimal('168'),
    'Meses': Decimal('720'),
    'Anios': Decimal('8760'),
}


def _to_decimal(value, default=ZERO):
    if value is None or value == '':
        return default
    return Decimal(str(value))


def obtener_configuracion(usuario=None):
    if usuario:
        configuracion = Configuracion.objects.filter(usuario=usuario).first()
        if configuracion:
            return configuracion
    return Configuracion.objects.first()


def obtener_precio_kwh(usuario=None):
    configuracion = obtener_configuracion(usuario)
    if not configuracion:
        return ZERO
    return _to_decimal(getattr(configuracion, 'precio_kwh', ZERO))


def convertir_tiempo_a_horas(cantidad, unidad):
    cantidad_decimal = _to_decimal(cantidad)
    factor = TIME_UNIT_TO_HOURS.get(unidad, ZERO)
    return cantidad_decimal * factor


def formatear_tiempo(cantidad, unidad):
    cantidad_decimal = _to_decimal(cantidad)
    return f'{cantidad_decimal.normalize()} {unidad}'


def calcular_costo_bien_receta(bien, tiempo_uso_cantidad, tiempo_uso_unidad, precio_kwh=None,
                               incluir_depreciacion=True, incluir_electricidad=True):
    horas_uso = convertir_tiempo_a_horas(tiempo_uso_cantidad, tiempo_uso_unidad)
    vida_util_horas = convertir_tiempo_a_horas(bien.vida_util_cantidad, bien.vida_util_unidad)
    costo_compra = _to_decimal(bien.costo_compra)
    potencia_watts = _to_decimal(bien.potencia_watts)
    factor_uso_porcentaje = _to_decimal(bien.factor_uso_porcentaje, Decimal('100'))
    precio_kwh = _to_decimal(precio_kwh if precio_kwh is not None else obtener_precio_kwh(bien.usuario))

    costo_hora_depreciacion = ZERO
    if vida_util_horas > ZERO:
        costo_hora_depreciacion = costo_compra / vida_util_horas

    depreciacion = costo_hora_depreciacion * horas_uso if incluir_depreciacion else ZERO

    potencia_kw = potencia_watts / Decimal('1000') if potencia_watts > ZERO else ZERO
    factor_uso = factor_uso_porcentaje / Decimal('100') if factor_uso_porcentaje > ZERO else ZERO
    consumo_kwh = potencia_kw * horas_uso * factor_uso if incluir_electricidad else ZERO
    costo_electricidad = consumo_kwh * precio_kwh if incluir_electricidad else ZERO
    costo_total = depreciacion + costo_electricidad

    return {
        'horas_uso': horas_uso,
        'vida_util_horas': vida_util_horas,
        'costo_hora_depreciacion': costo_hora_depreciacion,
        'depreciacion': depreciacion,
        'potencia_kw': potencia_kw,
        'factor_uso': factor_uso,
        'consumo_kwh': consumo_kwh,
        'costo_electricidad': costo_electricidad,
        'costo_total': costo_total,
    }


def calcular_totales_bienes_receta(receta):
    from administracion.models import BienReceta

    precio_kwh = obtener_precio_kwh(receta.usuario)
    relaciones = BienReceta.objects.filter(receta=receta).select_related('bien')

    total_depreciacion = ZERO
    total_electricidad = ZERO
    total_bienes = ZERO
    detalles = []

    for relacion in relaciones:
        calculo = calcular_costo_bien_receta(
            relacion.bien,
            relacion.tiempo_uso_cantidad,
            relacion.tiempo_uso_unidad,
            precio_kwh=precio_kwh,
            incluir_depreciacion=relacion.incluir_depreciacion,
            incluir_electricidad=relacion.incluir_electricidad,
        )
        total_depreciacion += calculo['depreciacion']
        total_electricidad += calculo['costo_electricidad']
        total_bienes += calculo['costo_total']
        detalles.append({
            'relacion': relacion,
            'calculo': calculo,
        })

    return {
        'precio_kwh': precio_kwh,
        'total_depreciacion': total_depreciacion,
        'total_electricidad': total_electricidad,
        'total_bienes': total_bienes,
        'detalles': detalles,
    }