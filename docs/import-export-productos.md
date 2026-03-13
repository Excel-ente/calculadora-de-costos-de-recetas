# Tutorial Paso a Paso: Importar y Exportar Productos en Excel

Este documento explica, de manera simple, clara y detallada, cómo usar la función de importar y exportar productos de forma masiva.

Está pensado para personas que no están acostumbradas a trabajar con sistemas, archivos de Excel o procesos de carga de datos.

La idea es que usted pueda:

1. Descargar una plantilla vacía para cargar productos nuevos.
2. Exportar sus productos actuales a un archivo de Excel.
3. Editar ese archivo con calma.
4. Volver a subirlo al sistema para crear o actualizar productos.

---

## 1. Qué significa exportar y qué significa importar

Antes de usar esta herramienta, conviene entender estas dos palabras.

### Exportar

Exportar significa sacar información del sistema y guardarla en un archivo.

En este caso:

- el sistema toma los productos cargados,
- los coloca en un archivo de Excel,
- y ese archivo se descarga en su computadora.

Piense en esto como: "bajar una copia de mis productos".

### Importar

Importar significa hacer el camino contrario.

En este caso:

- usted toma un archivo de Excel,
- lo sube al sistema,
- y el sistema lee esa información para crear productos nuevos o actualizar productos existentes.

Piense en esto como: "subir al sistema los cambios que hice en el Excel".

---

## 2. Para qué sirve esta función

Esta función sirve para trabajar con muchos productos de una sola vez.

Por ejemplo:

- cargar un catálogo completo de insumos,
- cambiar precios de muchos productos juntos,
- corregir nombres o descripciones en bloque,
- actualizar cantidades,
- ordenar categorías.

Si quiere cambiar un solo producto, puede hacerlo manualmente en el sistema.

Si quiere trabajar con muchos productos juntos, esta herramienta es mucho más práctica.

---

## 3. Dónde encontrar esta opción en el sistema

Dentro del panel de administración, busque la pantalla llamada:

**Importar / Exportar Productos**

En esa pantalla verá tres áreas principales:

1. Descargar plantilla vacía.
2. Exportar todos los productos.
3. Importar desde Excel.

También verá una tabla con la estructura del archivo Excel y las columnas esperadas.

---

## 4. Qué tipo de archivo hay que usar

El sistema acepta archivos de Excel con extensión:

**.xlsx**

Esto significa que:

- un archivo `.xlsx` sí sirve,
- un archivo `.xls` viejo puede no servir,
- un archivo `.csv` no sirve,
- un archivo de Word no sirve,
- una imagen no sirve.

Ejemplo correcto:

`productos.xlsx`

Ejemplo incorrecto:

`productos.csv`

---

## 5. Cómo es el archivo de productos

En el caso de productos, el archivo trabaja con una hoja principal llamada:

**Productos**

Esa hoja contiene una fila de encabezados arriba, con los nombres de cada columna.

Cada fila de abajo representa un producto.

En otras palabras:

- una fila = un producto.

---

## 6. Cuáles son las columnas del archivo

La hoja `Productos` tiene estas columnas:

1. `ID`
2. `Código`
3. `Nombre`
4. `Descripción`
5. `Categoría`
6. `Marca`
7. `Unidad de Medida`
8. `Cantidad`
9. `Costo`

Más abajo vamos a explicar cada una de ellas, una por una.

---

## 7. Primera manera de empezar: descargar una plantilla vacía

Esta opción sirve cuando quiere empezar desde cero y cargar productos nuevos.

### Paso a paso

1. Entre a la pantalla **Importar / Exportar Productos**.
2. Busque el bloque **Descargar plantilla vacía**.
3. Haga clic en **Descargar plantilla**.
4. Espere a que el archivo se descargue.
5. Busque el archivo en su computadora, normalmente en la carpeta **Descargas**.
6. Ábralo con Excel.

### Qué va a ver

Va a ver una hoja llamada `Productos`.

También puede ver una fila de ejemplo en color gris o más suave.

Esa fila sirve solo de guía para mostrar cómo se completa cada columna.

Puede usarla como modelo y luego borrarla si lo desea.

---

## 8. Segunda manera de empezar: exportar sus productos actuales

Esta opción sirve cuando usted ya tiene productos cargados y quiere:

- hacer una copia de seguridad,
- cambiar precios,
- actualizar cantidades,
- corregir nombres,
- volver a importar el archivo con cambios.

### Paso a paso

1. Entre a la pantalla **Importar / Exportar Productos**.
2. Busque el bloque **Exportar todos los productos**.
3. Haga clic en **Exportar productos**.
4. Espere a que se descargue el archivo.
5. Abra el archivo con Excel.

### Qué contiene ese archivo

Ese archivo ya trae los productos que usted tiene en el sistema.

Esto es muy útil porque así puede trabajar sobre datos reales en lugar de escribir todo desde cero.

---

## 9. Qué significa el campo ID

La columna `ID` es el identificador interno del sistema.

Piense en él como el número de documento del producto.

Sirve para que el sistema sepa exactamente qué registro debe actualizar.

### Regla simple

- Si el producto ya existe y quiere actualizarlo, conviene dejar el `ID` tal como está.
- Si el producto es nuevo, puede dejar el `ID` vacío.

### Importante

El sistema también puede identificar productos por otras columnas, como veremos más adelante.

Pero el `ID` es la forma más precisa.

---

## 10. Cómo identifica el sistema a un producto existente

Cuando usted importa el archivo, el sistema intenta encontrar si ese producto ya existe.

Lo hace en este orden:

1. primero por `ID`,
2. si no hay `ID`, por `Código`,
3. si no hay `Código`, por `Nombre`.

Esto significa que si el sistema encuentra un producto existente, lo actualiza.

Y si no lo encuentra, lo crea como nuevo.

---

## 11. Explicación de cada columna

Ahora vamos a ver una por una las columnas del Excel.

### 11.1 ID

- Puede quedar vacío si el producto es nuevo.
- Si viene desde una exportación del sistema, conviene no modificarlo.

### 11.2 Código

Es un código interno para identificar el producto.

Ejemplos:

- `HAR-001`
- `AZU-010`
- `MANT-05`

No es obligatorio, pero es muy útil para ordenar el catálogo.

Si el sistema no encuentra el producto por ID, puede intentar encontrarlo por código.

### 11.3 Nombre

Es el nombre del producto.

Ejemplos:

- Harina 000
- Azúcar
- Manteca
- Chocolate cobertura

Este campo es obligatorio.

Eso significa que no puede quedar vacío.

### 11.4 Descripción

Es un texto explicativo opcional.

Ejemplos:

- Harina común para repostería
- Azúcar blanca refinada
- Manteca sin sal

No es obligatoria.

### 11.5 Categoría

Sirve para clasificar el producto.

Ejemplos:

- Almacén
- Lácteos
- Chocolates
- Envases

Si la categoría no existe, el sistema la crea automáticamente.

### 11.6 Marca

Es la marca comercial del producto.

Ejemplos:

- Molinos
- Ledesma
- Ilolay

No es obligatoria.

### 11.7 Unidad de Medida

Esta columna indica la unidad con la que se compra o maneja el producto.

Debe ser una unidad válida del sistema.

Las unidades aceptadas son:

- `Unidades`
- `Kilos`
- `Gramos`
- `Litros`
- `Mililitros`
- `Mt2s`
- `Onzas`
- `Libras`
- `Metros`
- `Centimetros`

Este campo es obligatorio.

### 11.8 Cantidad

Esta columna indica la cantidad comprada o contenida en esa unidad de producto.

Debe ser un número mayor que 0.

Ejemplos:

- `1`
- `5`
- `25`
- `1000`

Ejemplos incorrectos:

- `0`
- `-2`
- `mucho`

### 11.9 Costo

Esta columna indica el costo total del producto, no el costo unitario.

Debe ser un número igual o mayor que 0.

Ejemplos válidos:

- `0`
- `350`
- `1200.50`

Ejemplos incorrectos:

- `-1`
- `caro`

---

## 12. Qué significa que el costo es total y no unitario

Esto es importante.

El sistema espera el costo total de compra del producto.

Ejemplo:

Si compra una bolsa de harina de 25 kilos por 800 pesos:

- `Unidad de Medida`: Kilos
- `Cantidad`: 25
- `Costo`: 800

Eso quiere decir que el sistema después calculará el costo unitario a partir de esos datos.

No hace falta que usted escriba el costo por kilo manualmente.

---

## 13. Qué no conviene hacer en el Excel

Para evitar errores, conviene no hacer estas cosas:

1. No cambie el nombre de la hoja `Productos`.
2. No borre la fila de encabezados.
3. No cambie el orden de las columnas.
4. No escriba texto donde deberían ir números.
5. No invente unidades de medida que no están en la lista.
6. No borre IDs si el objetivo es actualizar productos existentes.

Lo más seguro es partir siempre de la plantilla o de un archivo exportado por el sistema.

---

## 14. Cómo completar un producto nuevo

Supongamos que quiere cargar un producto nuevo.

Ejemplo:

- `ID`: vacío
- `Código`: HAR-001
- `Nombre`: Harina 000
- `Descripción`: Harina común tipo 000
- `Categoría`: Almacén
- `Marca`: Molinos
- `Unidad de Medida`: Kilos
- `Cantidad`: 25
- `Costo`: 800

Como el `ID` está vacío, el sistema entiende que se trata de un producto nuevo.

---

## 15. Cómo actualizar un producto existente

Supongamos que exportó sus productos y quiere cambiar el precio de uno que ya existe.

Si el producto ya viene con un `ID`, lo más conveniente es dejar ese `ID` como está y modificar solo el dato que necesita.

Por ejemplo:

- deja el mismo `ID`,
- deja el mismo nombre,
- cambia `Costo` de `800` a `920`.

Cuando vuelva a importar, el sistema entenderá que debe actualizar ese producto en vez de crear otro nuevo.

---

## 16. Cómo importar el archivo paso a paso

Ahora vemos el proceso completo para subir el archivo al sistema.

### Paso 1

Abra la pantalla **Importar / Exportar Productos**.

### Paso 2

En el bloque **Importar desde Excel**, haga clic sobre el área donde se selecciona el archivo.

### Paso 3

Busque en su computadora el archivo `.xlsx` que desea subir.

### Paso 4

Haga doble clic en el archivo, o selecciónelo y pulse **Abrir**.

### Paso 5

Verifique que en pantalla aparezca el nombre del archivo seleccionado.

### Paso 6

Pulse el botón **Importar productos**.

En ese momento, el sistema leerá el archivo y procesará cada fila.

---

## 17. Qué hace el sistema cuando usted importa el archivo

El sistema revisa varias cosas:

1. que el archivo sea `.xlsx`,
2. que pueda abrirse correctamente,
3. que cada fila tenga nombre,
4. que la unidad de medida sea válida,
5. que la cantidad sea un número positivo,
6. que el costo sea un número igual o mayor que 0.

Después de eso, intenta crear o actualizar cada producto.

---

## 18. Importante: la importación de productos no tiene paso de previsualización

En el caso de productos, el sistema no hace una pantalla intermedia de confirmación como en recetas.

Eso significa que cuando usted pulsa **Importar productos**, el sistema directamente procesa el archivo.

Por eso conviene:

1. revisar bien el Excel antes de subirlo,
2. trabajar primero con pocos productos si es su primera vez,
3. guardar una copia del archivo antes de importar.

---

## 19. Qué pasa si una fila tiene error

Si una fila tiene un problema, el sistema la informa como error.

Pero eso no significa que se detenga todo el archivo.

La lógica actual es esta:

- las filas correctas se procesan,
- las filas con error se informan,
- y al final aparece un resumen.

Esto es útil porque no obliga a rehacer toda la carga por un solo error.

---

## 20. Qué mensajes puede mostrar el sistema al final

Después de importar, el sistema puede mostrar diferentes tipos de mensajes.

### Mensaje de éxito

Indica cuántos productos se crearon y cuántos se actualizaron.

Ejemplo:

"Importación completada: 5 productos nuevos, 12 actualizados."

### Mensajes de advertencia

Muestran errores encontrados en filas puntuales.

El sistema muestra una cantidad limitada de errores visibles para no llenar la pantalla.

### Mensaje informativo

Si el archivo no tenía filas con datos, puede aparecer un mensaje indicando que no se encontraron datos para importar.

---

## 21. Problemas frecuentes y cómo entenderlos

### "Debe seleccionar un archivo Excel"

No se eligió ningún archivo antes de pulsar el botón de importación.

Solución:

- seleccione un archivo primero,
- verifique que el nombre aparezca en pantalla,
- y luego importe.

### "Solo se aceptan archivos .xlsx"

El archivo no es del formato correcto.

Solución:

- use un archivo Excel `.xlsx`,
- o guarde nuevamente el archivo con esa extensión.

### "No se pudo leer el archivo"

El archivo puede estar dañado, mal guardado o no ser realmente un Excel válido.

Solución:

- vuelva a abrirlo en Excel,
- guárdelo nuevamente,
- y vuelva a subirlo.

### "Nombre es obligatorio"

Hay una fila sin nombre de producto.

Solución:

- complete el nombre en esa fila.

### "Unidad de medida no válida"

La unidad escrita no coincide con las unidades aceptadas por el sistema.

Solución:

- use solo una unidad de la lista válida,
- preferentemente copiando la que aparece en la plantilla.

### "Cantidad debe ser un número positivo"

La cantidad está vacía, tiene texto o tiene un valor menor o igual a 0.

Solución:

- escriba un número válido mayor que 0.

### "Costo debe ser un número mayor o igual a 0"

El costo está vacío, tiene texto o tiene un valor negativo.

Solución:

- escriba un número válido,
- usando 0 o un valor positivo.

---

## 22. Ejemplo completo de una pequeña carga

Supongamos que quiere cargar estos 3 productos:

### Producto 1

- `ID`: vacío
- `Código`: HAR-001
- `Nombre`: Harina 000
- `Descripción`: Harina común tipo 000
- `Categoría`: Almacén
- `Marca`: Molinos
- `Unidad de Medida`: Kilos
- `Cantidad`: 25
- `Costo`: 800

### Producto 2

- `ID`: vacío
- `Código`: AZU-001
- `Nombre`: Azúcar
- `Descripción`: Azúcar blanca refinada
- `Categoría`: Almacén
- `Marca`: Ledesma
- `Unidad de Medida`: Kilos
- `Cantidad`: 10
- `Costo`: 600

### Producto 3

- `ID`: vacío
- `Código`: MANT-001
- `Nombre`: Manteca
- `Descripción`: Manteca sin sal
- `Categoría`: Lácteos
- `Marca`: Ilolay
- `Unidad de Medida`: Kilos
- `Cantidad`: 1
- `Costo`: 350

Después:

1. guarda el Excel,
2. vuelve al sistema,
3. selecciona el archivo,
4. pulsa **Importar productos**,
5. revisa el mensaje final.

---

## 23. Consejos prácticos para trabajar más seguro

1. Siempre guarde una copia del archivo antes de importarlo.
2. Si va a modificar productos existentes, primero expórtelos desde el sistema.
3. No cambie encabezados ni nombres de columnas.
4. Revise bien los números en cantidad y costo.
5. Use siempre unidades válidas del sistema.
6. Si es la primera vez, haga una prueba con 2 o 3 productos antes de cargar muchos.

---

## 24. Resumen corto del proceso completo

Si quiere una versión resumida, el proceso es este:

1. Descargar plantilla o exportar productos actuales.
2. Abrir el archivo Excel.
3. Completar o corregir los datos.
4. Guardar el archivo como `.xlsx`.
5. Seleccionarlo en la pantalla de importación.
6. Pulsar **Importar productos**.
7. Revisar el mensaje final con resultados y errores.

---

## 25. Recomendación final

Si nunca usó esta herramienta, conviene empezar con una prueba chica.

Por ejemplo:

1. exporte sus productos actuales,
2. cambie uno solo,
3. vuelva a importarlo,
4. revise el resultado.

Cuando ya vea cómo funciona, puede usarla con más confianza para cargas más grandes.

---

## 26. En una frase simple

La lógica de esta herramienta es:

**descargar, editar, guardar, subir e importar.**

Si trabaja con calma y revisa bien cada columna, el proceso es mucho más sencillo.

---

## 27. Atribución

Este proyecto es traído por **EXCEL-ENTE** en colaboración con **ADEMA Sistemas**.