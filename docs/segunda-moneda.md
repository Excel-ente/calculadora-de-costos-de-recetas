# Implementación: Segunda Moneda (Doble Divisa)

**Estado:** Implementado y en producción  
**Autor:** Kevin Turkienich / Excel-ente  
**Fecha de diseño:** Marzo 2026  
**Última actualización:** Marzo 2026

---

## Resumen ejecutivo

Esta funcionalidad permite mostrar todos los costos y precios del sistema en **dos monedas simultáneamente**: la moneda principal ya existente (ej. `$` / ARS) y una segunda moneda configurable (ej. `USD`, `€`, etc.) con su propio tipo de cambio y control de decimales.

El modo de segunda moneda es **completamente opcional** y se activa/desactiva con un simple checkbox en la Configuración de Empresa, sin afectar el funcionamiento actual del sistema.

---

## 1. Cambios en el modelo `Configuracion` (`configuracion/models.py`)

Se añaden **cuatro campos** al modelo singleton `Configuracion`:

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `habilitar_segunda_moneda` | `BooleanField` | `False` | Activa/desactiva toda la funcionalidad de segunda moneda |
| `segunda_moneda` | `CharField(max_length=10)` | `'USD'` | Símbolo o código de la segunda moneda (ej. `USD`, `€`, `BTC`) |
| `tipo_de_cambio` | `DecimalField(max_digits=20, decimal_places=8)` | `1.0` | Factor de conversión: cuántas unidades de segunda moneda equivalen a 1 unidad de moneda principal |
| `redondeo_segunda_moneda` | `DecimalField(max_digits=5, decimal_places=2)` | `2` | Decimales a mostrar en segunda moneda. Soporta valores negativos para redondear a decenas/centenas |

### Fórmula de conversión

```
precio_en_segunda_moneda = precio_en_moneda_principal × tipo_de_cambio
```

**Ejemplo:**
- Moneda principal: `$` (ARS)
- Segunda moneda: `USD`
- Tipo de cambio: `0.00068966` (1 ARS = 0.00068966 USD)
- Costo de un ingrediente: `$ 1.536 ARS` × `0.00068966` = `USD 1,059`

### Redondeo de segunda moneda

El campo `redondeo_segunda_moneda` usa la función estándar `round(valor, n)` de Python, que acepta valores negativos:

| `redondeo_segunda_moneda` | Comportamiento | Ejemplo (valor 1234.56) |
|--------------------------|----------------|------------------------|
| `3` | 3 decimales | `1.234,567` |
| `2` | 2 decimales (centavos) | `1.234,57` |
| `1` | 1 decimal | `1.234,6` |
| `0` | Número entero | `1.235` |
| `-1` | Redondea a decenas | `1.230` |
| `-2` | Redondea a centenas | `1.200` |

### Validaciones del modelo

- `tipo_de_cambio` debe ser mayor a `0` cuando la segunda moneda está habilitada.
- `segunda_moneda` no puede estar vacía si `habilitar_segunda_moneda` es `True`.
- Ambos campos son ignorados cuando `habilitar_segunda_moneda` es `False`.

---

## 2. Migraciones de base de datos

| Migración | Descripción |
|-----------|-------------|
| `configuracion/migrations/0002_configuracion_segunda_moneda.py` | Añade `habilitar_segunda_moneda`, `segunda_moneda`, `tipo_de_cambio` |
| `configuracion/migrations/0003_alter_configuracion_tipo_de_cambio.py` | Ajusta precisión de `tipo_de_cambio` a `decimal_places=8` |
| `configuracion/migrations/0004_configuracion_redondeo_segunda_moneda.py` | Añade `redondeo_segunda_moneda` |

---

## 3. Cambios en `configuracion/admin.py`

El formulario de Configuración de Empresa incluye la sección **"Segunda Moneda"**:

```
[ ] Habilitar segunda moneda
Segunda moneda:           [USD      ]
Tipo de cambio:           [0.00068966]   ← Cuántas USD por 1 ARS
Redondeo segunda moneda:  [2        ]   ← Decimales a mostrar
```

Los campos `segunda_moneda`, `tipo_de_cambio` y `redondeo_segunda_moneda` se deshabilitan visualmente (via JavaScript) cuando `habilitar_segunda_moneda` está en `False`.

---

## 4. Cambios en `administracion/models.py`

### 4.1 Modelo `Producto`

Método `costo_unitario_segunda_moneda()`:

```python
def costo_unitario_segunda_moneda(self):
    config = Configuracion.objects.first()
    if not config or not config.habilitar_segunda_moneda:
        return None
    tc = float(config.tipo_de_cambio)
    if tc <= 0:
        return None
    redondeo_2 = int(config.redondeo_segunda_moneda or 0)
    return round(self.costo_unitario() * tc, redondeo_2)
```

### 4.2 Modelo `Receta`

Cuatro métodos calculados, todos siguen el mismo patrón de `× tc` + `round(..., redondeo_2)`:

| Método | Base | Resultado |
|--------|------|-----------|
| `costo_porcion_segunda_moneda()` | `costo_porcion()` | Costo por porción en segunda moneda |
| `precio_venta_porcion_segunda_moneda()` | `precio_venta_porcion_num()` | Precio venta por porción en segunda moneda |
| `precio_venta_total_segunda_moneda()` | `precio_venta_total()` | Precio venta total en segunda moneda |

Todos retornan `None` si la segunda moneda no está habilitada o el tipo de cambio es ≤ 0.

---

## 5. Cambios en `administracion/admin.py`

### 5.1 `ProductoAdmin`

- Campo readonly `Costo_Unitario_Segunda_Moneda` en el formulario de edición, con decimales dinámicos según `redondeo_segunda_moneda`.
- Columna en la lista de productos, visible solo cuando la segunda moneda está activa.

### 5.2 `ProductoRecetaInline` (subformulario de ingredientes en receta)

- El subtotal del ingrediente muestra un segundo renglón con el valor en segunda moneda usando `format_html`, con decimales dinámicos.

### 5.3 `RecetaAdmin`

- `Precio_venta` (list_display): muestra precio principal + segunda moneda en segundo renglón (formato `<small>`), con decimales dinámicos.
- `Precio_venta_segunda_moneda`: columna propia con el precio total en segunda moneda.
- `Precio_porcion_segunda_moneda`: columna propia con el precio por porción en segunda moneda.

### Lógica de formato numérico

Todos los valores de segunda moneda en admin usan la función `_fn(valor, decimales)` que aplica formato argentino (punto de miles, coma decimal) y respeta los decimales configurados:

```python
redondeo_2 = int(config.redondeo_segunda_moneda or 0)
return f'{config.segunda_moneda} {_fn(val, max(0, redondeo_2))}'
```

> **Nota:** Para el formato de texto (`_fn`), si `redondeo_2 < 0` se usa `max(0, redondeo_2) = 0` ya que los strings no admiten decimales negativos. El redoneo correcto ya fue aplicado por el modelo antes de llegar al admin.

---

## 6. Cambios en `administracion/Reporte.py`

En la función de generación de PDF (`generar_receta_pdf`) se define un helper `fmt2()` que aplica el tipo de cambio y el redondeo configurado:

```python
redondeo_2 = int(config.redondeo_segunda_moneda or 0) if segunda_moneda_activa else 2

def fmt2(valor):
    if not segunda_moneda_activa:
        return ''
    return f'  ({segunda_moneda} {_fn(float(valor) * tc, max(0, redondeo_2))})'
```

Los valores en segunda moneda aparecen entre paréntesis junto a cada precio del PDF:
```
Costo total:         $ 1.536,00   (USD 1,06)
Costo por porción:   $ 153,60     (USD 0,11)
Precio de venta:     $ 192,00     (USD 0,13)
```

---

## 7. Cambios en `administracion/dashboard_views.py`

Se añade una variable `redondeo_2` a la configuración inicial de la vista:

```python
redondeo_2 = int(config.redondeo_segunda_moneda or 0) if config else 0
```

Todos los valores de segunda moneda en las métricas del dashboard usan `redondeo_2`:

```python
'costo_total_2':   round(costo * tipo_de_cambio, redondeo_2),
'costo_porcion_2': round(costo_porcion_val * tipo_de_cambio, redondeo_2),
'precio_venta_2':  round(precio_venta * tipo_de_cambio, redondeo_2),
```

---

## 8. Tests integradores (`administracion/tests.py`)

Se añadió la clase `SegundaMonedaTests` con **13 tests** que cubren:

| Test | Qué verifica |
|------|-------------|
| `test_config_tiene_campo_redondeo_segunda_moneda` | El campo existe en el modelo |
| `test_config_redondeo_segunda_moneda_default_es_2` | El default es 2 |
| `test_producto_costo_unitario_segunda_moneda_calcula_correctamente` | Fórmula `× tc` con redondeo aplicado |
| `test_producto_costo_unitario_segunda_moneda_aplica_redondeo` | Resultado redondeado según config |
| `test_producto_costo_unitario_segunda_moneda_redondeo_3` | Redondeo con 3 decimales |
| `test_producto_costo_unitario_segunda_moneda_deshabilitada_retorna_none` | `None` cuando deshabilitado |
| `test_receta_costo_porcion_segunda_moneda` | Costo porción × tc con redondeo |
| `test_receta_precio_venta_total_segunda_moneda` | Precio total × tc con redondeo |
| `test_receta_precio_venta_porcion_segunda_moneda` | Precio porción × tc con redondeo |
| `test_receta_segunda_moneda_deshabilitada_retorna_none` | Los 3 métodos retornan `None` |
| `test_redondeo_negativo_redondea_a_decenas` | `redondeo_2=-1` redondea a decenas |
| `test_redondeo_cero_retorna_entero` | `redondeo_2=0` retorna entero |
| `test_tipo_de_cambio_cero_retorna_none` | `tipo_de_cambio=0` retorna `None` |

Para correr los tests:
```bash
python manage.py test administracion.tests.SegundaMonedaTests -v 2
```

---

## 9. Archivos modificados — Resumen completo

| Archivo | Descripción del cambio |
|---------|------------------------|
| `configuracion/models.py` | Añade `redondeo_segunda_moneda` (+ los 3 campos de segunda moneda) |
| `configuracion/admin.py` | Fieldset "Segunda Moneda" con JS habilitador; incluye `redondeo_segunda_moneda` |
| `configuracion/migrations/0002_configuracion_segunda_moneda.py` | Migración: 3 campos de segunda moneda |
| `configuracion/migrations/0003_alter_configuracion_tipo_de_cambio.py` | Migración: ajuste de precisión del tipo de cambio |
| `configuracion/migrations/0004_configuracion_redondeo_segunda_moneda.py` | Migración: `redondeo_segunda_moneda` |
| `administracion/models.py` | Métodos `*_segunda_moneda()` en `Producto` y `Receta` con rounding dinámico |
| `administracion/admin.py` | Campos readonly + columnas con decimales dinámicos via `redondeo_segunda_moneda` |
| `administracion/Reporte.py` | `fmt2()` con redondeo dinámico en PDFs |
| `administracion/dashboard_views.py` | Variable `redondeo_2` y su uso en todas las métricas de segunda moneda |
| `administracion/tests.py` | Clase `SegundaMonedaTests` con 13 tests integradores |
| `static/js/segunda_moneda_admin.js` | JS para habilitar/deshabilitar campos en admin según el checkbox |

---

## 10. Archivos NO modificados

| Archivo | Razón |
|---------|-------|
| `administracion/services_bienes.py` | Los costos de bienes se convierten a nivel de presentación |
| `administracion/views.py` | El simulador de fabricación no requiere segunda moneda |
| `administracion/importar_exportar_views.py` | Importaciones/exportaciones Excel operan en moneda principal |
| `templates/admin/fabricacion_simulador.html` | Fuera del alcance |
| `templates/admin/importar_exportar_*.html` | Fuera del alcance |

---

## 11. Flujo de usuario

### Activar la segunda moneda

1. Ir a **Configuración de Empresa** (`/admin/configuracion/configuracion/1/change/`).
2. En la sección **"Segunda moneda"**, activar **"Habilitar segunda moneda"**.
3. Ingresar el símbolo (ej. `USD`) y el tipo de cambio (ej. `0.00068966` si 1 ARS = 0.00068966 USD).
4. Configurar **"Redondeo segunda moneda"**: `2` para centavos, `0` para enteros, `-2` para centenas.
5. Guardar.

### Resultado inmediato

- En el formulario de cada **Producto/insumo**: campo readonly **"Costo unitario (2ª moneda)"**.
- En la **lista de Productos**: columna adicional con el costo en segunda moneda.
- En la **lista de Recetas**: precio de venta con equivalente en segunda moneda.
- En el **formulario de Receta** (ingredientes): cada subtotal muestra ambas monedas.
- En el **Dashboard**: las tarjetas de recetas muestran precios en ambas monedas.
- En los **PDFs de costos**: cada precio imprime el equivalente en segunda moneda entre paréntesis.

### Desactivar la segunda moneda

Desmarcar **"Habilitar segunda moneda"** y guardar. El sistema vuelve a comportarse exactamente como antes: sin columnas extra, sin valores en segunda moneda en PDFs ni dashboard.

---

## Resumen ejecutivo

Esta funcionalidad permite mostrar todos los costos y precios del sistema en **dos monedas simultáneamente**: la moneda principal ya existente (ej. `$` / ARS) y una segunda moneda configurable (ej. `USD`, `€`, etc.) con su propio tipo de cambio.

El modo de segunda moneda es **completamente opcional** y se activa/desactiva con un simple checkbox en la Configuración de Empresa, sin afectar el funcionamiento actual del sistema.

---

## 1. Cambios en el modelo `Configuracion` (`configuracion/models.py`)

Se agregan **tres campos nuevos** al modelo singleton `Configuracion`:

| Campo | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `habilitar_segunda_moneda` | `BooleanField` | `False` | Activa/desactiva toda la funcionalidad de segunda moneda |
| `segunda_moneda` | `CharField(max_length=10)` | `'USD'` | Símbolo o código de la segunda moneda (ej. `USD`, `€`, `BTC`) |
| `tipo_de_cambio` | `DecimalField(max_digits=18, decimal_places=6)` | `1.0` | Cuántas unidades de moneda principal equivalen a 1 unidad de segunda moneda. Ej: si `1 USD = 1000 ARS`, ingresar `1000` |

### Fórmula de conversión

```
precio_en_segunda_moneda = precio_en_moneda_principal / tipo_de_cambio
```

**Ejemplo:**
- Moneda principal: `$` (ARS)
- Segunda moneda: `USD`
- Tipo de cambio: `1000` (1 USD = 1000 ARS)
- Costo de un ingrediente: `$5000 ARS` → `$5.00 USD`

### Validaciones del modelo

- `tipo_de_cambio` debe ser mayor a `0` (no puede dividirse por cero).
- `segunda_moneda` no puede estar vacía si `habilitar_segunda_moneda` es `True`.
- El campo `segunda_moneda` es ignorado cuando `habilitar_segunda_moneda` es `False`.

---

## 2. Migración de base de datos

Se genera la migración `0002_configuracion_segunda_moneda.py` en `configuracion/migrations/`:

```python
# Campos nuevos añadidos a Configuracion:
migrations.AddField('Configuracion', 'habilitar_segunda_moneda', models.BooleanField(default=False)),
migrations.AddField('Configuracion', 'segunda_moneda', models.CharField(default='USD', max_length=10)),
migrations.AddField('Configuracion', 'tipo_de_cambio', models.DecimalField(default=1, decimal_places=6, max_digits=18)),
```

---

## 3. Cambios en `configuracion/admin.py`

El formulario de Configuración de Empresa mostrará la nueva sección **"Segunda Moneda"** como un fieldset colapsable:

```
[ ] Habilitar segunda moneda
Segunda moneda: [USD      ]
Tipo de cambio: [1000.000000]   ← Cuántos $ equivalen a 1 USD
```

- El campo `segunda_moneda` y `tipo_de_cambio` se **muestran como deshabilitados** cuando `habilitar_segunda_moneda` está en `False` (via JavaScript en el admin).
- Se añade `help_text` explicando la fórmula: *"Ingresá cuántas unidades de moneda principal equivalen a 1 unidad de la segunda moneda. Ej: si 1 USD = 1000 $, ingresá 1000."*

---

## 4. Cambios en `administracion/models.py`

### 4.1 Modelo `Producto` (insumos)

Se agrega un **método calculado `costo_unitario_segunda_moneda()`** (no es campo de base de datos):

```python
def costo_unitario_segunda_moneda(self):
    """
    Retorna el costo unitario en la segunda moneda configurada.
    Retorna None si la segunda moneda no está habilitada o no hay config.
    """
    from configuracion.models import Configuracion
    try:
        config = Configuracion.objects.get(pk=1)
        if not config.habilitar_segunda_moneda or config.tipo_de_cambio <= 0:
            return None
        return self.costo_unitario() / config.tipo_de_cambio
    except Configuracion.DoesNotExist:
        return None
```

### 4.2 Modelo `Receta`

Se agregan métodos calculados:

```python
def costo_porcion_segunda_moneda(self):
    """Costo por porción en segunda moneda."""

def precio_venta_porcion_segunda_moneda(self):
    """Precio de venta por porción en segunda moneda."""

def precio_venta_total_segunda_moneda(self):
    """Precio de venta total en segunda moneda."""
```

Todos siguen el mismo patrón: obtienen `config.tipo_de_cambio`, dividen el valor en moneda principal, y retornan `None` si el modo no está habilitado.

---

## 5. Cambios en `administracion/admin.py`

### 5.1 `ProductoAdmin`

- Se agrega `costo_unitario_segunda_moneda` como campo `readonly` en el formulario de edición de producto. Aparece **junto al `costo_unitario`** existente como campo de solo lectura que se actualiza al guardar.
- En la **lista de productos** (`list_display`), se agrega una columna adicional que muestra el costo unitario en segunda moneda (solo visible cuando `habilitar_segunda_moneda = True`). Esto se logra con un método que verifica la config antes de mostrar el valor.

### 5.2 `RecetaAdmin`

- En el **change form** de receta, los campos readonly de precios incluirán las versiones en segunda moneda.
- En la **lista de recetas** (`list_display`), junto al precio de venta por porción se mostrará el equivalente en segunda moneda entre paréntesis o en una columna separada.

### Lógica de visibilidad

Todos los métodos de admin que muestran segunda moneda verifican `config.habilitar_segunda_moneda` antes de retornar un valor. Si está deshabilitado, retornan un guión `—` para no confundir al usuario.

---

## 6. Cambios en `administracion/Reporte.py`

### 6.1 PDF con costos (`build_pdf_costos`)

En la sección **RESUMEN DE COSTOS**, cada línea de precio mostrará ambas monedas:

```
Costo total de la receta:    $5.000,00       (USD 5,00)
Costo por porción:            $500,00         (USD 0,50)
Precio de venta sugerido:    $1.250,00       (USD 1,25)
```

El valor en segunda moneda se muestra entre paréntesis, en un color más suave (gris) para indicar que es secundario.

En la sección **INGREDIENTES Y COSTOS**, cada ingrediente mostrará:
```
Harina 000  -  500g  ............  $250,00  (USD 0,25)
```

### 6.2 PDF sin costos (`build_pdf_sin_costos`)

Este PDF no muestra costos (es para compartir con clientes), por lo que **no se modifica**.

### Condición de renderizado

Ambas funciones reciben el objeto `config` como parámetro (ya lo hacen actualmente). Se agrega la verificación:

```python
mostrar_segunda_moneda = (
    config and 
    config.habilitar_segunda_moneda and 
    config.tipo_de_cambio > 0
)
```

Si `mostrar_segunda_moneda` es `False`, los PDFs se generan exactamente igual que antes.

---

## 7. Cambios en `administracion/dashboard_views.py`

El contexto del dashboard incluirá la configuración de segunda moneda para que el template pueda renderizar los valores convertidos:

```python
context['config_segunda_moneda'] = {
    'habilitada': config.habilitar_segunda_moneda if config else False,
    'simbolo': config.segunda_moneda if config else '',
    'tipo_cambio': config.tipo_de_cambio if config else 1,
}
```

Las métricas de recetas en el dashboard (top5 más caras, top5 más baratas, etc.) mostrarán el precio en segunda moneda debajo del precio principal, como texto secundario.

---

## 8. Cambios en `templates/admin/dashboard_home.html`

### Cards de recetas (top5 más caras/baratas/etc.)

Cada receta en el dashboard que muestra un precio pasará de:

```html
<span class="badge">{{ moneda }}{{ receta.precio_venta }}</span>
```

a:

```html
<span class="badge">{{ moneda }}{{ receta.precio_venta }}</span>
{% if config_segunda_moneda.habilitada %}
<small class="text-muted d-block">
    {{ config_segunda_moneda.simbolo }} {{ receta.precio_en_segunda_moneda }}
</small>
{% endif %}
```

### Tabla de insumos (top10 por costo)

Similar tratamiento: el costo del insumo mostrará debajo el equivalente en segunda moneda.

---

## 9. Archivos modificados — Resumen completo

| Archivo | Tipo de cambio |
|---------|---------------|
| `configuracion/models.py` | Agregar 3 campos al modelo `Configuracion` |
| `configuracion/admin.py` | Agregar fieldset "Segunda Moneda" con JS para habilitar/deshabilitar campos |
| `configuracion/migrations/0002_*.py` | Nueva migración (generada automáticamente) |
| `administracion/models.py` | Agregar métodos `*_segunda_moneda()` en `Producto` y `Receta` |
| `administracion/admin.py` | Mostrar campos de segunda moneda como readonly; agregar columnas a list_display |
| `administracion/Reporte.py` | Mostrar ambas monedas en PDFs con costos |
| `administracion/dashboard_views.py` | Pasar config de segunda moneda al contexto del dashboard |
| `templates/admin/dashboard_home.html` | Mostrar segunda moneda en cards de recetas e insumos |

---

## 10. Archivos NO modificados

| Archivo | Razón |
|---------|-------|
| `administracion/services_bienes.py` | No necesita cambios; los costos de bienes se convierten a nivel de presentación |
| `administracion/views.py` | El simulador de fabricación no requiere segunda moneda en esta versión |
| `administracion/importar_exportar_views.py` | Las importaciones/exportaciones Excel operan en moneda principal |
| `templates/admin/fabricacion_simulador.html` | Fuera del alcance de esta versión |
| `templates/admin/importar_exportar_*.html` | Fuera del alcance |
| `calculadora_de_costo/urls.py` | Sin nuevas URLs necesarias |
| `calculadora_de_costo/settings.py` | Sin cambios necesarios |

---

## 11. Flujo de usuario

### Activar la segunda moneda

1. Ir a **Configuración de Empresa** (`/admin/configuracion/configuracion/1/change/`).
2. En la sección **"Segunda Moneda"**, activar el checkbox **"Habilitar segunda moneda"**.
3. Ingresar el símbolo (ej. `USD`) y el tipo de cambio (ej. `1000` si 1 USD = 1000 $).
4. Guardar.

### Resultado inmediato

- En el formulario de cada **Producto/insumo**, aparece un campo readonly **"Costo unitario en USD"** calculado automáticamente.
- En la **lista de Productos**, hay una columna adicional con el costo en USD.
- En la **lista de Recetas**, el precio de venta muestra el equivalente en USD.
- En el **Dashboard**, las tarjetas de recetas muestran el precio en ambas monedas.
- Al generar **PDFs de costos**, se imprimen ambas monedas.

### Desactivar la segunda moneda

1. Desactivar el checkbox en Configuración.
2. Guardar.
3. Todo vuelve a funcionar exactamente como antes — ningún dato se pierde.

---

## 12. Consideraciones técnicas

### Rendimiento

- El tipo de cambio se lee **una sola vez por request** desde el modelo `Configuracion` (singleton `pk=1`).
- No hay campos adicionales en la base de datos para almacenar precios convertidos; todo es **calculado en tiempo real** a partir del tipo de cambio.
- El dashboard ya carga `Configuracion` al inicio del request; se reutiliza el mismo objeto.

### Precisión numérica

- Se usa `Decimal` en toda la cadena de cálculo para evitar errores de punto flotante.
- El tipo de cambio se almacena con 6 decimales de precisión (`decimal_places=6`), suficiente para criptomonedas y divisas exóticas.
- Los valores en segunda moneda se redondean al mismo `redondeo` configurado en `Configuracion.redondeo`.

### Seguridad

- No se exponen rutas nuevas; todo es presentación en el admin ya autenticado.
- Los valores en segunda moneda son de solo lectura (readonly en admin), el usuario no puede manipularlos directamente.
- La validación de `tipo_de_cambio > 0` previene división por cero.

### Retrocompatibilidad

- Si `habilitar_segunda_moneda = False` (valor por defecto), **ninguna pantalla cambia**. Los nuevos métodos retornan `None` y los templates usan `{% if %}` para no renderizar nada.
- La migración es `null=True, blank=True` donde corresponde, por lo que no rompe instancias existentes de la BD.

---

## 13. Orden de implementación recomendado

1. **Migración** — `configuracion/models.py` + `makemigrations` + `migrate`
2. **Admin config** — agregar fieldset en `configuracion/admin.py`
3. **Métodos en modelos** — `administracion/models.py` (Producto + Receta)
4. **Admin productos/recetas** — `administracion/admin.py` (readonly fields + list_display)
5. **Dashboard** — `dashboard_views.py` + `dashboard_home.html`
6. **PDFs** — `administracion/Reporte.py`
7. **Test manual** — activar modo, verificar todos los puntos de la UI

---

## 14. Casos de prueba

| Escenario | Resultado esperado |
|-----------|-------------------|
| `habilitar_segunda_moneda = False` | Todo igual que hoy, sin columnas ni textos adicionales |
| `tipo_de_cambio = 1000`, `segunda_moneda = 'USD'`, producto costo $5000 | Muestra `USD 5.00` |
| `tipo_de_cambio` cambia de 1000 a 1200 | Todos los valores se actualizan automáticamente al guardar |
| Generar PDF con segunda moneda habilitada | PDF muestra ambas monedas en sección de costos |
| Generar PDF sin costos con segunda moneda habilitada | PDF sin cambios (no muestra costos) |
| Desactivar segunda moneda y regenerar PDF | PDF vuelve a mostrar solo moneda principal |
| `tipo_de_cambio = 0` | Validación impide guardar; mensaje de error en el form |

---

*Documento generado como guía de implementación para el proyecto Calculadora de Costos de Recetas.*
