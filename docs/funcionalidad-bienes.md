# README - Funcionalidad de Bienes, Depreciación y Costo Eléctrico

## Objetivo

Este documento define la funcionalidad completa que debe implementarse en la otra aplicación para incorporar bienes de producción, su depreciación y el costo de electricidad asociado al uso en recetas o fabricaciones.

La finalidad es que una receta pueda cotizar correctamente:

- costo de insumos
- costo de subrecetas
- costos adicionales
- costo de electricidad de los bienes usados
- depreciación de los bienes usados

Y, si el negocio lo desea, también poder reflejar:

- depreciación lineal por paso del tiempo
- consumo eléctrico continuo de bienes no ligados a una receta puntual
- baja contable de bienes

Este README está pensado como especificación funcional para que otro agente o desarrollador implemente el módulo desde cero en una app que ya tiene productos y recetas.

## Alcance recomendado

Implementar estos bloques:

1. Maestro de bienes
2. Asociación de bienes a recetas
3. Cálculo de depreciación por uso
4. Cálculo de costo eléctrico por uso
5. Integración del costo del bien al costo total de la receta
6. Integración opcional con fabricaciones o lotes
7. Reportes de vida útil, valor residual y reemplazo
8. Baja de bienes
9. Soporte opcional para depreciación lineal y costo eléctrico lineal por período

## Definiciones

### Bien

Un bien es un activo o equipo usado para producir una receta.

Ejemplos:

- horno
- amasadora
- licuadora
- heladera
- freidora
- batidora

### Depreciación por uso

El bien pierde valor según las horas reales que se usa en recetas o fabricaciones.

Ejemplo:

- costo del bien: 1.200.000
- vida útil: 6.000 horas
- costo por hora de depreciación: 200

Si una receta usa ese bien 0,5 horas, la depreciación imputable a esa receta es 100.

### Depreciación lineal

El bien pierde valor por el paso del tiempo desde su fecha de compra, independientemente de cuántas recetas se fabriquen.

Esto sirve más para análisis contable o financiero que para costear una receta puntual.

### Costo eléctrico

Es el costo de energía consumida por el bien durante su uso.

Se calcula a partir de:

- potencia en watts
- tiempo de uso
- factor de uso
- precio del kWh configurado en la empresa

### Factor de uso

Es el porcentaje real del tiempo en que el equipo consume energía mientras se lo considera en uso.

Ejemplos:

- licuadora: 100%
- amasadora: 100%
- heladera: 33%
- horno que cicla resistencia: 60%

## Principios de diseño

La implementación nueva debe respetar estas reglas:

1. El costo por porción de la receta debe incluir bienes. No solo el costo total de receta.
2. El factor de uso eléctrico debe aplicarse siempre en el cálculo de electricidad.
3. La depreciación por uso y el costo eléctrico deben poder activarse o desactivarse por cada bien asociado a la receta.
4. La depreciación lineal no debe mezclarse automáticamente con el costo variable de la receta salvo que el negocio lo pida explícitamente.
5. El cálculo debe ser determinístico y reutilizable desde servicios, reportes, admin, API y ventas.
6. El costo del producto final fabricado debe tomar el costo por porción corregido, incluyendo bienes cuando estén activos.

## Modelo de datos recomendado

### 1. Configuración global

Entidad sugerida: `ConfiguracionEmpresa` o equivalente.

Campos mínimos:

- `precio_kwh`: decimal
- `moneda_codigo`: string opcional
- `moneda_simbolo`: string opcional

Uso:

- sirve como base del cálculo eléctrico

### 2. Bien

Entidad sugerida: `Bien`

Campos mínimos:

- `id`
- `nombre`
- `descripcion`
- `costo_compra`
- `tipo_depreciacion`: `USO` o `LINEAL`
- `vida_util_horas`
- `potencia_watts`
- `factor_uso_porcentaje`
- `fecha_compra` nullable
- `activo`
- `factura_compra_url` opcional
- `fecha_alta`
- `fecha_actualizacion`

Reglas:

- `vida_util_horas` debe ser mayor a 0 si se quiere depreciar
- `potencia_watts` puede ser 0 si no se quiere costear electricidad
- `factor_uso_porcentaje` debe estar entre 0 y 100
- `fecha_compra` es obligatoria si `tipo_depreciacion = LINEAL`

### 3. Bien asociado a receta

Entidad sugerida: `BienReceta`

Campos mínimos:

- `id`
- `bien_id`
- `receta_id`
- `minutos_uso`
- `incluir_depreciacion`: boolean
- `incluir_electricidad`: boolean
- `observaciones` opcional

Reglas:

- una receta puede tener muchos bienes
- un bien puede estar en muchas recetas
- `minutos_uso` debe ser mayor a 0

### 4. Uso real de bien en fabricación

Entidad sugerida: `UsoBienProduccion` o `UsoBienFabricacion`

Campos mínimos:

- `id`
- `fabricacion_id` o `produccion_id`
- `bien_receta_id`
- `horas_consumidas`
- `costo_depreciacion`
- `costo_electricidad`
- `costo_total`
- `fecha_uso`

Uso:

- historial real de uso
- base para depreciación por uso acumulada
- auditoría y reportes

### 5. Baja de bien

Entidad sugerida: `BajaBien`

Campos mínimos:

- `id`
- `bien_id`
- `fecha_baja`
- `motivo`
- `observaciones`
- `valor_residual`
- `perdida_contable`
- `usuario_id` opcional

## Fórmulas oficiales

### 1. Horas de uso de un bien en receta

$$
horas\_uso = \frac{minutos\_uso}{60}
$$

### 2. Costo por hora de depreciación

$$
costo\_hora\_depreciacion = \frac{costo\_compra}{vida\_util\_horas}
$$

Si `vida_util_horas <= 0`, el valor debe ser 0.

### 3. Depreciación imputable a la receta

$$
depreciacion\_receta = costo\_hora\_depreciacion \times horas\_uso
$$

Si `incluir_depreciacion = false`, el valor debe ser 0.

### 4. Potencia en kW

$$
potencia\_kw = \frac{potencia\_watts}{1000}
$$

### 5. Factor de uso real

$$
factor\_uso = \frac{factor\_uso\_porcentaje}{100}
$$

### 6. Consumo energético de la receta

$$
consumo\_kwh = potencia\_kw \times horas\_uso \times factor\_uso
$$

### 7. Costo eléctrico imputable a la receta

$$
costo\_electricidad = consumo\_kwh \times precio\_kwh
$$

Si `incluir_electricidad = false`, el valor debe ser 0.

### 8. Costo total del bien en la receta

$$
costo\_bien\_receta = depreciacion\_receta + costo\_electricidad
$$

### 9. Costo total de receta

$$
costo\_total\_receta = insumos + subrecetas + gastos\_adicionales + bienes
$$

Donde:

$$
bienes = \sum costo\_bien\_receta
$$

### 10. Costo por porción

$$
costo\_porcion = \frac{costo\_total\_receta}{porciones}
$$

Esta fórmula debe incluir bienes. Este punto es obligatorio.

## Reglas funcionales obligatorias

### Regla 1. La receta debe costear bienes en total y por porción

El sistema debe mostrar:

- costo de bienes por receta
- costo total de receta
- costo por porción

Y ambos, total y porción, deben incluir depreciación y electricidad si están activadas.

### Regla 2. El producto fabricado debe heredar el costo por porción completo

Si existe un producto asociado a una receta, el costo base del producto debe salir del costo por porción corregido de la receta.

Eso implica que el producto final también incorpora:

- insumos
- subrecetas
- adicionales
- depreciación
- electricidad

### Regla 3. Depreciación por uso y electricidad deben poder ser opcionales

Por cada bien en la receta, se debe poder:

- imputar solo depreciación
- imputar solo electricidad
- imputar ambas
- no imputar ninguna temporalmente

### Regla 4. El factor de uso debe participar en todos los cálculos eléctricos

No solo en reportes. También en:

- costo en pantalla
- costo en receta
- costo en fabricación
- costo persistido
- reportes

### Regla 5. La fabricación debe poder persistir los costos del bien

Si la app tiene entidad `Fabricacion` o `Produccion`, al cerrar una producción se debe registrar el uso real:

- horas reales consumidas por cantidad producida
- depreciación consumida
- electricidad consumida
- costo total de bien en esa producción

### Regla 6. No duplicar imputación

Si una fabricación ya generó registros de uso de bienes, no volver a generarlos para la misma fabricación salvo que exista una reversión explícita.

## Comportamiento en recetas

### Alta de bien en receta

Al agregar un bien a una receta, el usuario debe poder cargar:

- bien
- minutos de uso
- incluir depreciación
- incluir electricidad

El sistema debe calcular y mostrar en tiempo real:

- horas de uso
- depreciación estimada
- electricidad estimada
- total estimado

### Edición de receta

Si cambia:

- costo del bien
- vida útil
- potencia
- factor de uso
- precio kWh
- minutos de uso

entonces deben recalcularse los costos estimados de la receta.

## Comportamiento en producción o fabricación

Si la app tiene fabricación por lotes, el comportamiento recomendado es:

### Al finalizar una fabricación

Por cada `BienReceta`:

1. tomar minutos de uso definidos en la receta
2. convertir a horas
3. multiplicar por la cantidad fabricada si la cantidad representa lotes/recetas producidas
4. calcular depreciación real
5. calcular electricidad real
6. persistir un registro `UsoBienFabricacion`

### Fórmulas para fabricación

Si `cantidad_fabricada` representa número de recetas/lotes:

$$
horas\_fabricacion = horas\_uso\_receta \times cantidad\_fabricada
$$

$$
depreciacion\_fabricacion = depreciacion\_receta \times cantidad\_fabricada
$$

$$
electricidad\_fabricacion = electricidad\_receta \times cantidad\_fabricada
$$

### Reversión

Si una fabricación finalizada se elimina o revierte, deben eliminarse o anularse los registros de uso del bien generados por esa fabricación.

## Vida útil, valor residual y alertas

El sistema debe poder calcular para cada bien:

### Horas usadas

Si es `USO`:

- sumar `horas_consumidas` del historial de producción

Si es `LINEAL`:

- calcular horas transcurridas desde `fecha_compra`

### Horas restantes

$$
horas\_restantes = max(0, vida\_util\_horas - horas\_usadas)
$$

### Porcentaje de vida útil restante

$$
vida\_util\_restante\_pct = \frac{horas\_restantes}{vida\_util\_horas} \times 100
$$

### Valor residual

$$
valor\_residual = costo\_compra \times \frac{vida\_util\_restante\_pct}{100}
$$

### Alerta de reemplazo

El sistema debe alertar cuando el bien llegue al 20% o menos de vida útil restante.

## Depreciación lineal

La depreciación lineal debe implementarse como módulo opcional.

### Cuándo usarla

- para reportes financieros
- para tablero de costos fijos
- para análisis de resultado por período

### Cuándo no usarla por defecto

- no meterla automáticamente dentro del costo variable de una receta puntual

### Fórmula de depreciación lineal por período

Si el período tiene `horas_periodo`:

$$
depreciacion\_lineal\_periodo = costo\_hora\_depreciacion \times horas\_periodo
$$

Si el bien además consume energía en forma continua:

$$
electricidad\_lineal\_periodo = potencia\_kw \times horas\_periodo \times factor\_uso \times precio\_kwh
$$

## Baja de bienes

Debe existir la posibilidad de dar de baja un bien.

Motivos sugeridos:

- fin de vida útil
- rotura
- obsolescencia
- venta
- otro

Al dar de baja:

1. calcular valor residual actual
2. calcular pérdida contable
3. marcar el bien como inactivo
4. mantener historial de la baja

### Fórmula sugerida de pérdida contable

$$
perdida\_contable = costo\_compra - valor\_residual
$$

## Pantallas mínimas sugeridas

### 1. Maestro de bienes

Debe permitir:

- alta
- edición
- baja lógica
- ver vida útil restante
- ver horas usadas
- ver valor residual
- ver alertas de reemplazo

### 2. Receta

Debe permitir agregar bienes con:

- selector de bien
- minutos de uso
- switches de incluir depreciación e incluir electricidad
- cálculo estimado en vivo

### 3. Producción o fabricación

Debe permitir:

- registrar producción
- cerrar/finalizar
- persistir consumos de bienes
- consultar historial de uso

### 4. Reporte de bien

Debe mostrar:

- datos generales
- depreciación acumulada
- electricidad estimada por hora
- costo total por hora
- vida útil restante
- historial de usos
- historial de bajas

## Reportes mínimos sugeridos

### Reporte de receta

Debe desglosar:

- insumos
- subrecetas
- gastos adicionales
- bienes: depreciación y electricidad por separado
- total receta
- costo por porción

### Reporte de producción

Debe desglosar:

- costo de insumos consumidos
- costo de gastos adicionales
- costo de bienes consumidos
- total de fabricación
- costo unitario resultante

### Reporte global de bienes

Debe permitir ver por período:

- depreciación por uso
- electricidad por uso
- depreciación lineal
- electricidad lineal
- bajas de bienes
- total general

## Servicio de cálculo recomendado

La implementación debe concentrar la lógica en un servicio reutilizable. No repartir fórmulas entre vistas, admin, serializers y templates.

Sugerencia de servicios:

- `calcular_costo_bien_receta(bien, minutos_uso, precio_kwh, incluir_depreciacion, incluir_electricidad)`
- `calcular_totales_bienes_receta(receta)`
- `calcular_costo_total_receta(receta)`
- `calcular_costo_porcion_receta(receta)`
- `registrar_uso_bienes_produccion(produccion)`
- `calcular_estado_bien(bien)`

Salida recomendada del cálculo por bien:

- horas_uso
- costo_hora_depreciacion
- depreciacion
- potencia_kw
- factor_uso
- consumo_kwh
- costo_electricidad
- costo_total

## Criterios de aceptación

La implementación se considera correcta si cumple todo esto:

1. Una receta con bienes muestra su depreciación y electricidad correctamente.
2. El costo por porción incluye bienes.
3. El producto final ligado a la receta toma ese costo completo.
4. El factor de uso afecta siempre el cálculo eléctrico.
5. La producción finalizada registra histórico de uso de bienes sin duplicar.
6. Los bienes muestran vida útil consumida, restante y valor residual.
7. La baja de bienes guarda pérdida contable e inactiva el bien.
8. La depreciación lineal funciona en reportes si se habilita.

## Casos de prueba mínimos

### Caso 1. Licuadora con uso directo

Datos:

- costo compra: 120000
- vida útil: 1200 horas
- potencia: 1500 W
- factor uso: 100%
- precio kWh: 150
- minutos uso receta: 12

Resultado esperado:

- horas uso: 0,2
- costo hora depreciación: 100
- depreciación receta: 20
- potencia kW: 1,5
- consumo kWh: 0,3
- electricidad: 45
- total bien receta: 65

### Caso 2. Heladera con factor de uso parcial

Datos:

- costo compra: 900000
- vida útil: 30000 horas
- potencia: 250 W
- factor uso: 33
- precio kWh: 150
- minutos uso receta: 180

Resultado esperado:

- horas uso: 3
- potencia kW: 0,25
- factor: 0,33
- consumo kWh: 0,2475
- electricidad: 37,125

### Caso 3. Bien sin depreciación

Si `incluir_depreciacion = false`, la depreciación debe ser 0 aunque el bien tenga vida útil.

### Caso 4. Bien sin electricidad

Si `incluir_electricidad = false`, el costo eléctrico debe ser 0 aunque el bien tenga potencia y precio kWh.

### Caso 5. Receta completa

Si una receta tiene:

- insumos = 1000
- subrecetas = 500
- gastos adicionales = 200
- bienes = 300
- porciones = 10

Resultado esperado:

- costo total receta = 2000
- costo por porción = 200

## Decisiones recomendadas para evitar errores

1. Usar `Decimal` para dinero y cantidades sensibles.
2. Centralizar las fórmulas en servicios puros.
3. No mezclar cálculo teórico de receta con cálculo histórico de fabricación.
4. No duplicar lógica en frontend y backend sin una fuente de verdad clara.
5. Aplicar siempre factor de uso en electricidad.
6. Hacer que el costo por porción y el costo de producto final salgan del mismo cálculo base.

## Orden sugerido de implementación

1. Configuración global de precio kWh
2. Modelo `Bien`
3. Modelo `BienReceta`
4. Servicio de cálculo por bien
5. Integración al costo total de receta
6. Integración al costo por porción
7. Actualización del costo del producto final
8. Registro de uso por producción
9. Reportes de bienes
10. Bajas de bienes
11. Depreciación lineal opcional

## Resumen ejecutivo

La funcionalidad a implementar debe permitir que una receta no solo consuma insumos, sino también activos de producción, imputando de manera controlada:

- depreciación por uso
- gasto eléctrico por uso
- seguimiento de vida útil
- valor residual
- historial de uso
- bajas

La clave de la implementación correcta es esta:

- el costo del bien debe poder participar en el costo de la receta
- el costo por porción debe incluirlo
- el producto final debe heredar ese costo
- la electricidad debe calcularse con factor de uso
- la depreciación lineal debe quedar como capa contable opcional, no como costo variable obligatorio de receta
