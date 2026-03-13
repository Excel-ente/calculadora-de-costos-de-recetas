# 📊 Dashboard de Métricas

## 🎯 Descripción

Dashboard completo con todas las métricas del emprendimiento, diseñado para tener una visión general del negocio de repostería/cocina.

---

## ✨ Características

### 📈 Estadísticas Generales
- **Total de recetas** en el sistema
- **Total de productos/insumos** disponibles
- **Costo promedio** de las recetas
- **Rentabilidad promedio** del negocio

### 🍰 Análisis de Recetas

#### Top 5 Recetas Más Caras
Muestra las recetas con mayor costo total, ideal para:
- Identificar productos premium
- Analizar estrategias de precios
- Revisar costos de ingredientes costosos

#### Top 5 Recetas Más Económicas
Recetas con menor costo, útil para:
- Productos de entrada
- Maximizar márgenes
- Opciones económicas para clientes

#### Top 5 Mayor Rentabilidad
Recetas que generan más ganancia, perfecto para:
- Priorizar productos estrella
- Estrategias de marketing
- Optimizar catálogo

#### Top 5 Menor Rentabilidad
Recetas con menor margen, importante para:
- Detectar productos poco rentables
- Revisar precios
- Decidir si mantener o eliminar

#### Recetas con Más Ingredientes
Recetas complejas, útil para:
- Planificar preparación
- Gestionar tiempo
- Identificar recetas elaboradas

### 🚨 Alertas Inteligentes

El dashboard ahora marca recetas que muestran inconsistencias reales en los datos — es decir, casos que probablemente requieran corrección humana:

- ⚠️ Sin ingredientes: la receta no tiene productos asociados
- ⚠️ Ingredientes con costo = $0: insumos sin precio cargado
- ⚠️ Cantidades inválidas: ingredientes con cantidad 0 o negativa
- ⚠️ Unidades incompatibles: unidad del producto distinta a la unidad usada en la receta (ej. Litros → Kilos)
- ⚠️ Costo total = $0: la suma de los costos calculados da 0 a pesar de tener ingredientes

### 📦 Análisis de Insumos

#### Top 10 Insumos Más Usados
- Productos utilizados frecuentemente
- Cantidad total usada
- Costo acumulado

### ⚠️ Inconsistencias de Datos
Cuando se detectan inconsistencia (lista arriba), el dashboard marcará la receta en la sección de alertas para que revises y corrijas los insumos o cantidades.
- Ideal para planificar compras

#### Top 10 Insumos Menos Usados
- Productos raramente utilizados
- Considerar eliminar del inventario
- Optimizar stock

#### Top 10 Ingredientes que Más Cuestan
- Insumos que más impactan en costos
- En cuántas recetas se usan
- Cantidad total consumida
- Costo total acumulado

#### Insumos No Utilizados
- Productos en inventario sin uso
- Candidatos para eliminar
- Optimizar inventario

### 📊 Distribuciones

#### Recetas por Categoría
Visualización con barras de progreso que muestra:
- Cantidad de recetas por categoría
- Porcentaje del total
- Identificar categorías dominantes

#### Productos por Unidad de Medida
Distribución de insumos por tipo de medida:
- Kilos, Gramos
- Litros, Mililitros
- Unidades
- Onzas, Libras
- Metros, Centímetros
- Mt2s

---

## 🚀 Acceso al Dashboard

### URL Principal:
```
http://localhost:8000/
```

El dashboard es ahora la **página de inicio** de la aplicación.

### Desde el Admin:
1. Hacer clic en el logo "Excel-ente"
2. Seleccionar "Dashboard" en el menú de usuario

---

## 🎨 Características Visuales

### Cards Interactivos
- Efectos hover
- Colores distintivos por sección
- Iconos Font Awesome

### Estadísticas Destacadas
- Cajas grandes con gradientes de color
- Números grandes y legibles
- Labels descriptivos

### Barras de Progreso
- Distribuciones visuales
- Porcentajes automáticos
- Colores animados

### Sistema de Badges
- 🔵 Azul: Información general
- 🟢 Verde: Datos positivos
- 🟡 Amarillo: Advertencias
- 🔴 Rojo: Alertas

### Responsive Design
- Se adapta a móviles y tablets
- Grid flexible
- Scroll suave en listas largas

---

## 📋 Casos de Uso

### 1. Revisión Diaria
**Objetivo:** Ver el estado general del negocio

**Qué revisar:**
- Estadísticas generales (arriba)
- Alertas (si hay)
- Recetas más caras/baratas

**Tiempo:** 2-3 minutos

### 2. Planificación de Compras
**Objetivo:** Saber qué insumos comprar

**Qué revisar:**
- Top insumos más usados
- Ingredientes que más cuestan
- Insumos sin usar (para no comprar)

**Tiempo:** 5 minutos

### 3. Optimización de Catálogo
**Objetivo:** Mejorar rentabilidad

**Qué revisar:**
- Recetas con menor rentabilidad
- Alertas de rentabilidad baja
- Recetas más complejas (evaluar simplificar)

**Tiempo:** 10 minutos

### 4. Análisis de Productos
**Objetivo:** Decidir qué promocionar

**Qué revisar:**
- Mayor rentabilidad
- Recetas más económicas
- Distribución por categoría

**Tiempo:** 5-7 minutos

### 5. Limpieza de Inventario
**Objetivo:** Eliminar productos innecesarios

**Qué revisar:**
- Insumos no utilizados
- Insumos menos usados
- Considerar eliminar del inventario

**Tiempo:** 10 minutos

---

## 💡 Tips de Uso

### Para Maximizar Ganancias:
1. **Promover** recetas con mayor rentabilidad
2. **Revisar precios** de recetas con baja rentabilidad
3. **Optimizar** recetas muy costosas

### Para Reducir Costos:
1. **Analizar** ingredientes que más cuestan
2. **Buscar alternativas** más económicas
3. **Eliminar** insumos no utilizados

### Para Mejorar Eficiencia:
1. **Priorizar** insumos más usados en compras
2. **Simplificar** recetas con muchos ingredientes
3. **Estandarizar** unidades de medida

### Para Tomar Decisiones:
1. **Revisar alertas** regularmente
2. **Comparar** costos vs. precios de venta
3. **Monitorear** tendencias en el tiempo

---

## 🔧 Configuración

### Personalizar Alertas

Editar `administracion/dashboard_views.py`:

```python
# Línea ~95 - Cambiar umbral de rentabilidad
if float(item['rentabilidad']) < 10:  # Cambiar 10 por tu valor

# Línea ~101 - Cambiar umbral de costo alto
if item['costo_porcion'] > 5000:  # Cambiar 5000 por tu valor
```

### Cambiar Top N

Por defecto muestra Top 5 y Top 10. Para cambiar:

```python
# Líneas ~75-78 - Cambiar de Top 5 a Top 10
recetas_mas_caras = sorted(...)[:10]  # Cambiar 5 por 10
recetas_mas_baratas = sorted(...)[:10]
recetas_mayor_rentabilidad = sorted(...)[:10]
recetas_menor_rentabilidad = sorted(...)[:10]

# Línea ~115 - Cambiar Top 10 insumos
productos_mas_usados = sorted(...)[:20]  # Cambiar 10 por 20
```

### Filtrar por Usuario

El dashboard ya filtra automáticamente por el usuario logueado. Para ver todo:

Comentar las líneas en `dashboard_views.py`:
```python
# if usuario:
#     recetas_query = recetas_query.filter(usuario=usuario)
#     productos_query = productos_query.filter(usuario=usuario)
```

---

## 📊 Métricas Calculadas

### Costo Total de Receta
```python
costo = suma(productos) + suma(gastos_adicionales)
```

### Costo por Porción
```python
costo_porcion = costo_total / porciones
```

### Precio de Venta por Porción
```python
precio = (costo_porcion / (100 - rentabilidad) * 100) * (1 + IVA/100)
```

### Rentabilidad Real
```
ganancia = precio_venta - costo_porcion
rentabilidad_real = (ganancia / costo_porcion) * 100
```

---

## 🎯 Próximas Mejoras Sugeridas

### Gráficos Interactivos
- [ ] Chart.js para gráficos
- [ ] Gráficos de torta para distribuciones
- [ ] Gráficos de línea para tendencias

### Exportación
- [ ] Exportar a PDF
- [ ] Exportar a Excel
- [ ] Enviar por email

### Filtros
- [ ] Filtrar por fecha
- [ ] Filtrar por categoría
- [ ] Comparar períodos

### Análisis Avanzado
- [ ] Tendencias en el tiempo
- [ ] Proyecciones
- [ ] Análisis de temporada
- [ ] Comparación mes a mes

### Notificaciones
- [ ] Alertas por email
- [ ] Notificaciones push
- [ ] Resumen semanal

---

## 🐛 Troubleshooting

### El dashboard no carga
**Causa:** Error en cálculo de métricas

**Solución:**
```bash
python manage.py shell
```
```python
from administracion.models import Receta
for r in Receta.objects.all():
    try:
        r.costo_receta()
    except Exception as e:
        print(f"Error en {r.nombre}: {e}")
```

### Números no se ven correctos
**Causa:** Redondeo o formato

**Solución:** Verificar configuración de redondeo en `Configuracion`

### Faltan recetas o productos
**Causa:** Filtro por usuario

**Solución:** Verificar que estés logueado con el usuario correcto

---

## 📚 Archivos del Dashboard

### Backend:
- `administracion/dashboard_views.py` - Lógica y cálculos
- `calculadora_de_costo/urls.py` - Rutas
- `calculadora_de_costo/settings.py` - Configuración Jazzmin

### Frontend:
- `templates/admin/dashboard_home.html` - Template HTML/CSS

### Modelos Utilizados:
- `Receta` - Recetas y cálculos
- `Producto` - Insumos
- `ProductoReceta` - Relación y conversiones
- `GastosAdicionalesReceta` - Gastos extra
- `Configuracion` - Moneda y redondeo

---

## 🎓 Entendiendo las Métricas

### ¿Qué es "Costo Total"?
El costo de preparar toda la receta (todos los ingredientes + gastos adicionales).

### ¿Qué es "Costo por Porción"?
El costo de cada porción individual (costo_total / porciones).

### ¿Qué es "Rentabilidad"?
El porcentaje de ganancia sobre el costo. 
- 30% = por cada $100 de costo, vendes en $130
- 50% = por cada $100 de costo, vendes en $150

### ¿Por qué importan los "Insumos Más Usados"?
- Son críticos para el negocio
- Nunca deben faltar
- Priorizar en compras
- Buscar mejores proveedores

### ¿Qué hacer con "Insumos No Utilizados"?
- Evaluar si realmente se necesitan
- Considerar eliminar del inventario
- Liberar espacio y capital

---

## ✅ Checklist de Revisión Semanal

- [ ] Revisar alertas de recetas problemáticas
- [ ] Verificar insumos más usados (stock)
- [ ] Analizar recetas con menor rentabilidad
- [ ] Revisar insumos no utilizados
- [ ] Comparar costos promedio
- [ ] Identificar tendencias en categorías
- [ ] Actualizar precios si es necesario
- [ ] Planificar compras de la semana

---

## 🚀 Inicio Rápido

1. **Iniciar servidor:**
   ```bash
   python manage.py runserver
   ```

2. **Abrir navegador:**
   ```
   http://localhost:8000/
   ```

3. **¡Explorar el dashboard!**

---

## 📞 Soporte

**Desarrollador:** Kevin Turkienich  
**Dashboard:** Claude AI (2024)  
**Framework:** Django + Jazzmin

---

## 🎉 ¡Listo para Usar!

El dashboard está completamente funcional y listo para usar. Explora todas las métricas y toma mejores decisiones para tu emprendimiento.

**¡Mucha suerte!** 🍰
