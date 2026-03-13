# Tutorial Paso a Paso: Importar y Exportar Recetas en Excel

Este documento explica, de forma simple y bien detallada, cómo usar la función de importar y exportar recetas en la calculadora.

Está pensado para personas que no trabajan habitualmente con Excel o con sistemas administrativos.

La idea es que usted pueda:

1. Descargar sus recetas a un archivo de Excel.
2. Editarlas con tranquilidad.
3. Volver a subir ese archivo al sistema.
4. Revisar un resumen antes de confirmar los cambios.

---

## 1. Qué significa "exportar" y qué significa "importar"

Antes de empezar, conviene entender estas dos palabras.

### Exportar

"Exportar" significa sacar información del sistema y guardarla en un archivo.

En este caso:

- el sistema toma sus recetas,
- las coloca en un archivo de Excel,
- y ese archivo se descarga en su computadora.

Piense en esto como: "bajar una copia de mis recetas para verla o editarla".

### Importar

"Importar" significa hacer el camino inverso:

- usted toma un archivo de Excel,
- lo sube al sistema,
- y el sistema lee esa información para crear o actualizar recetas.

Piense en esto como: "subir al sistema los cambios que hice en el archivo".

---

## 2. Para qué sirve esta herramienta

Esta herramienta sirve para trabajar con muchas recetas de una sola vez.

Por ejemplo:

- cargar varias recetas nuevas sin escribirlas una por una,
- corregir nombres o descripciones en bloque,
- modificar porciones, IVA o rentabilidad de varias recetas,
- agregar o editar ingredientes desde Excel,
- cargar o actualizar bienes de producción,
- vincular bienes a las recetas,
- actualizar el costo del kWh usado para calcular electricidad.

Si usted solo quiere cambiar una receta puntual, puede hacerlo manualmente desde el panel normal.

Si quiere trabajar con varias recetas juntas, esta herramienta le ahorra mucho tiempo.

---

## 3. Dónde está esta función dentro del sistema

Dentro del panel de administración, busque la sección de recetas.

La pantalla se llama:

**Importar / Exportar Recetas**

En esa pantalla va a encontrar tres bloques principales:

1. Descargar plantilla vacía.
2. Exportar todas las recetas.
3. Importar desde Excel.

Más abajo, cuando usted analice un archivo, va a aparecer un cuarto bloque:

4. Previsualización de importación.

Y si el archivo está correcto, verá también el botón:

5. Confirmar importación.

---

## 4. Qué tipo de archivo se usa

El sistema trabaja con archivos de Excel con extensión:

**.xlsx**

Esto significa que:

- un archivo `.xlsx` sí sirve,
- un archivo `.xls` viejo puede no servir,
- un archivo `.csv` no sirve,
- un archivo de Word no sirve,
- una foto no sirve.

Si tiene dudas, mire el nombre del archivo al final.

Ejemplo correcto:

`mis_recetas.xlsx`

Ejemplo incorrecto:

`mis_recetas.csv`

---

## 5. Cómo está armado el archivo de Excel

El archivo tiene **6 hojas**.

Una hoja de Excel es cada pestaña que aparece abajo dentro del archivo.

Las 6 hojas son:

1. `Recetas`
2. `Recetas-Productos`
3. `Bienes`
4. `Recetas-Bienes`
5. `Configuracion`
6. `Productos`

Vamos a ver cada una.

### Hoja 1: Recetas

Esta hoja guarda los datos generales de cada receta.

Por ejemplo:

- nombre,
- descripción,
- categoría,
- porciones,
- rentabilidad,
- IVA,
- comentarios.

### Hoja 2: Recetas-Productos

Esta hoja guarda los ingredientes de cada receta.

Acá se indica:

- a qué receta pertenece el ingrediente,
- qué producto se usa,
- qué cantidad se usa,
- en qué unidad se usa.

### Hoja 3: Bienes

Esta hoja guarda los bienes o equipos de producción.

Por ejemplo:

- hornos,
- batidoras,
- amasadoras,
- freidoras,
- heladeras.

Acá se indica:

- nombre del bien,
- costo de compra,
- vida útil,
- potencia en watts,
- factor de uso,
- si está activo o no.

### Hoja 4: Recetas-Bienes

Esta hoja relaciona cada receta con los bienes que usa.

Acá se indica:

- a qué receta pertenece el bien,
- qué bien se usa,
- cuánto tiempo se usa,
- si se incluye depreciación,
- si se incluye electricidad,
- observaciones opcionales.

### Hoja 5: Configuracion

Esta hoja sirve para indicar el valor del:

- `Precio kWh`

Ese valor se usa para calcular el costo eléctrico de los bienes.

### Hoja 6: Productos

Esta hoja es una hoja de ayuda.

Sirve para que usted vea los productos existentes y pueda tomar como referencia:

- el nombre del producto,
- el ID,
- la unidad de medida,
- la categoría,
- la marca,
- la cantidad,
- el costo.

Muy importante:

**La hoja `Productos` no se importa.**

Eso significa que usted puede mirarla como referencia, pero no está pensada para cargar cambios desde ahí.

---

## 6. Primera forma de uso: descargar una plantilla vacía

Esta opción sirve cuando usted quiere empezar de cero.

### Paso a paso

1. Entre a la pantalla **Importar / Exportar Recetas**.
2. Busque el bloque **Descargar plantilla vacía**.
3. Haga clic en el botón **Descargar plantilla**.
4. Espere a que el archivo se descargue.
5. Busque ese archivo en su computadora, normalmente en la carpeta **Descargas**.
6. Ábralo con Excel.

### Qué va a ver

Va a ver las 6 hojas explicadas antes.

También puede aparecer una fila de ejemplo, en color más suave o gris.

Esa fila sirve solo como guía para mostrarle cómo completar los datos.

Puede usarla como modelo.

---

## 7. Segunda forma de uso: exportar sus recetas actuales

Esta opción sirve cuando usted ya tiene recetas cargadas y quiere:

- hacer una copia de seguridad,
- editar varias recetas juntas,
- agregar ingredientes tomando como base lo que ya existe.

### Paso a paso

1. Entre a la pantalla **Importar / Exportar Recetas**.
2. Busque el bloque **Exportar todas las recetas**.
3. Haga clic en el botón **Exportar recetas**.
4. Espere a que se descargue el archivo.
5. Abra el archivo en Excel.

### Qué contiene ese archivo

Ese archivo ya trae:

- sus recetas actuales,
- los ingredientes de cada receta,
- los bienes actuales,
- las relaciones entre recetas y bienes,
- el precio kWh actual,
- la hoja de referencia de productos.

Esta es la opción más recomendable si usted quiere editar información existente.

---

## 8. Qué significa el campo ID

En algunas columnas va a ver un campo llamado `ID`.

Ese número es el identificador interno del sistema.

Piense en él como el documento de identidad de ese registro.

### Para qué sirve

Sirve para que el sistema sepa exactamente qué receta, qué ingrediente, qué bien o qué relación debe actualizar.

### Regla simple

- Si quiere **modificar algo que ya existe**, conviene dejar el `ID` tal como está.
- Si quiere **crear algo nuevo**, deje el `ID` vacío.

### Ejemplo

Si exportó una receta llamada `Budín de limón` con ID `15` y luego cambia su descripción, deje el ID `15` en esa fila.

Así el sistema entiende: "esta es la misma receta, solo que actualizada".

Si agrega una receta nueva llamada `Tarta de manzana`, deje el ID vacío.

Así el sistema entiende: "esto es una receta nueva".

---

## 9. Cómo completar la hoja Recetas

La hoja `Recetas` tiene estas columnas:

1. `ID`
2. `Nombre`
3. `Descripción`
4. `Categoría`
5. `Porciones`
6. `Rentabilidad %`
7. `IVA %`
8. `Comentarios`

Ahora explicamos cada una.

### 9.1 ID

- Puede quedar vacío si la receta es nueva.
- Si la receta ya existe, conviene no tocarlo.

### 9.2 Nombre

Es el nombre de la receta.

Ejemplos:

- Torta de chocolate
- Pan casero
- Alfajores de maicena

Este campo es obligatorio.

Eso quiere decir que no puede quedar vacío.

### 9.3 Descripción

Es una breve explicación de la receta.

Ejemplos:

- Torta húmeda con relleno de dulce de leche
- Pan suave para sandwiches
- Alfajor relleno con dulce de leche

También es obligatoria.

### 9.4 Categoría

Sirve para ordenar las recetas.

Ejemplos:

- Tortas
- Panificados
- Galletitas
- Postres

Si la categoría no existe, el sistema la crea automáticamente.

Además, el sistema intenta ordenarla para evitar duplicados por error.

Por ejemplo, si usted escribe:

- ` tortas`
- `TORTAS`
- `tortas`

el sistema intentará normalizarlo para que quede más uniforme.

### 9.5 Porciones

Es la cantidad de porciones que rinde la receta.

Debe ser un número mayor que 0.

Ejemplos válidos:

- `1`
- `8`
- `12`
- `24`

Ejemplos incorrectos:

- `0`
- `-3`
- texto como `muchas`

### 9.6 Rentabilidad %

Es el porcentaje de ganancia o margen que se aplica a la receta.

Debe ser un número entre `0` y `99.99`.

Ejemplos válidos:

- `0`
- `25`
- `50`
- `80`

Ejemplos incorrectos:

- `100`
- `-5`
- `abc`

### 9.7 IVA %

Es el porcentaje de IVA de la receta.

Debe ser un número igual o mayor que 0.

Ejemplos:

- `0`
- `10.5`
- `21`

### 9.8 Comentarios

Es un campo opcional.

Puede usarlo para escribir observaciones internas.

Ejemplo:

- Lleva cobertura aparte
- Receta de temporada
- Revisar decoración

---

## 10. Cómo completar la hoja Recetas-Productos

Esta hoja relaciona cada receta con sus ingredientes.

Sus columnas son:

1. `ID`
2. `Receta ID`
3. `Receta Nombre`
4. `Producto ID`
5. `Producto Nombre`
6. `Cantidad`
7. `Medida de uso`

### Idea simple para entender esta hoja

Cada fila representa un ingrediente usado dentro de una receta.

Por ejemplo:

- receta: Torta de chocolate
- producto: Harina
- cantidad: 500
- medida: Gramos

Eso sería una fila.

---

## 11. Cómo indicar a qué receta pertenece cada ingrediente

Para indicar la receta, puede usar una de estas dos opciones:

1. `Receta ID`
2. `Receta Nombre`

No hace falta usar las dos al mismo tiempo, aunque puede hacerlo si quiere.

### Opción más segura

La opción más segura es usar `Receta ID`, porque el ID no se repite.

### Si usa el nombre

Si usa `Receta Nombre`, escríbalo exactamente como corresponde.

Si hay dos recetas con el mismo nombre, el sistema puede pedirle que use ID para evitar confusiones.

---

## 12. Cómo indicar qué producto se usa como ingrediente

Para indicar el producto, también puede usar una de estas dos opciones:

1. `Producto ID`
2. `Producto Nombre`

La hoja `Productos` está justamente para ayudarlo a encontrar estos datos.

### Recomendación práctica

Si no está seguro, use la hoja `Productos` para copiar exactamente el nombre o el ID.

Eso reduce errores de escritura.

---

## 13. Cómo completar Cantidad y Medida de uso

### Cantidad

La cantidad debe ser un número mayor que 0.

Ejemplos:

- `1`
- `0.5`
- `250`

### Medida de uso

La medida debe ser compatible con la unidad del producto.

Por ejemplo:

- si el producto está en kilos, se puede usar kilos o gramos,
- si el producto está en litros, se puede usar litros o mililitros,
- si el producto está en unidades, se usa unidades.

Si la medida no coincide con el tipo de producto, el sistema lo va a marcar como error en la previsualización.

---

## 14. Cómo completar la hoja Bienes

La hoja `Bienes` tiene estas columnas:

1. `ID`
2. `Nombre`
3. `Descripción`
4. `Costo de compra`
5. `Vida útil cantidad`
6. `Vida útil unidad`
7. `Potencia watts`
8. `Factor de uso %`
9. `Activo`

### Idea simple para entender esta hoja

Cada fila representa un equipo o bien productivo.

Por ejemplo:

- un horno,
- una batidora,
- una amasadora.

### Cosas importantes

- `Nombre` es obligatorio.
- `Costo de compra` debe ser 0 o mayor.
- `Vida útil cantidad` debe ser mayor que 0.
- `Vida útil unidad` debe ser una unidad válida, por ejemplo `Horas`, `Dias` o `Meses`.
- `Potencia watts` puede ser 0 si no quiere costear electricidad.
- `Factor de uso %` debe estar entre `0` y `100`.
- `Activo` acepta valores simples como `Si` o `No`.

---

## 15. Cómo completar la hoja Recetas-Bienes

La hoja `Recetas-Bienes` relaciona una receta con un bien.

Sus columnas son:

1. `ID`
2. `Receta ID`
3. `Receta Nombre`
4. `Bien ID`
5. `Bien Nombre`
6. `Tiempo de uso cantidad`
7. `Tiempo de uso unidad`
8. `Incluir depreciación`
9. `Incluir electricidad`
10. `Observaciones`

### Idea simple para entender esta hoja

Cada fila representa un bien usado dentro de una receta.

Por ejemplo:

- receta: Tarta de chocolate
- bien: Horno convector
- tiempo: 40
- unidad: Minutos

Eso sería una fila.

### Cosas importantes

- puede indicar la receta por `Receta ID` o por `Receta Nombre`,
- puede indicar el bien por `Bien ID` o por `Bien Nombre`,
- `Tiempo de uso cantidad` debe ser mayor que 0,
- `Tiempo de uso unidad` debe ser una unidad válida,
- `Incluir depreciación` e `Incluir electricidad` aceptan `Si` o `No`.

---

## 16. Cómo completar la hoja Configuracion

La hoja `Configuracion` tiene una sola columna:

1. `Precio kWh`

### Qué significa

Es el costo de la electricidad por kilowatt hora.

Ese número se usa para calcular el costo eléctrico de los bienes asociados a las recetas.

### Importante

- debe ser un número mayor o igual a 0,
- solo debe haber una fila con datos,
- si cambia ese valor, el sistema lo toma en la importación.

---

## 17. Qué no conviene hacer en Excel

Para evitar errores, trate de no hacer estas cosas:

1. No cambie los nombres de las hojas.
2. No borre los encabezados de la primera fila.
3. No cambie el orden de las columnas.
4. No use formatos extraños o colores pensando que eso carga información.
5. No escriba texto donde debería haber números.
6. No modifique la hoja `Productos` esperando que se importe.
7. No cambie `Si` y `No` por textos raros en las columnas booleanas.
8. No borre la hoja `Configuracion` si quiere mantener el costo kWh dentro del archivo.

Si quiere trabajar tranquilo, lo mejor es partir de la plantilla o de un archivo exportado por el propio sistema.

---

## 18. Cómo importar el archivo, paso por paso

Ahora vamos al proceso completo de subida.

### Paso 1

Abra la pantalla **Importar / Exportar Recetas**.

### Paso 2

En el bloque **Importar desde Excel**, haga clic sobre el área donde dice que puede seleccionar o arrastrar un archivo.

### Paso 3

Busque en su computadora el archivo `.xlsx` que quiere subir.

### Paso 4

Haga doble clic sobre el archivo, o selecciónelo y luego pulse **Abrir**.

### Paso 5

Revise que el nombre del archivo aparezca en pantalla.

Esto le confirma que eligió el archivo correcto.

### Paso 6

Presione el botón **Analizar archivo**.

Muy importante:

En este paso, el sistema todavía **no guarda cambios definitivos**.

Solo revisa el archivo y prepara un resumen.

---

## 19. Qué hace el sistema cuando usted pulsa "Analizar archivo"

El sistema revisa varias cosas:

1. Que el archivo sea `.xlsx`.
2. Que existan las 6 hojas necesarias.
3. Que las columnas tengan los nombres esperados.
4. Que los valores obligatorios estén completos.
5. Que los números sean válidos.
6. Que las recetas existan si se intenta actualizarlas.
7. Que los productos existan si se usan como ingredientes.
8. Que los bienes existan si se usan en una receta.
9. Que las unidades sean compatibles.
10. Que el `Precio kWh` tenga un valor válido.

Después de revisar todo eso, muestra una **previsualización**.

---

## 20. Qué es la previsualización

La previsualización es una pantalla de control antes de guardar.

Es como una instancia de revisión.

Sirve para que usted vea:

- cuántas recetas se van a crear,
- cuántas recetas se van a actualizar,
- cuántos ingredientes se van a crear,
- cuántos ingredientes se van a actualizar,
- cuántos bienes se van a crear,
- cuántos bienes se van a actualizar,
- cuántas relaciones receta-bien se van a crear,
- cuántas relaciones receta-bien se van a actualizar,
- si se va a crear o actualizar la configuración de `Precio kWh`,
- si hay advertencias,
- si hay errores.

Esto es muy importante porque le permite frenar antes de cometer un cambio equivocado.

---

## 21. Diferencia entre advertencia y error

### Advertencia

Una advertencia es un mensaje que avisa algo, pero no siempre impide seguir.

Ejemplo:

- se va a crear una categoría nueva.

### Error

Un error es un problema que sí impide confirmar la importación.

Ejemplos:

- falta el nombre de una receta,
- la cantidad es 0,
- el producto no existe,
- el bien no existe,
- la medida no es compatible,
- el tiempo de uso es 0,
- falta una hoja del archivo.

Si hay errores, primero hay que corregir el Excel y luego volver a analizarlo.

---

## 22. Qué hacer si la previsualización muestra errores

Si aparecen errores:

1. Lea el mensaje con calma.
2. Fíjese en qué hoja ocurrió el error.
3. Fíjese en qué fila ocurrió.
4. Abra nuevamente el archivo Excel.
5. Corrija esa información.
6. Guarde el archivo.
7. Vuelva al sistema.
8. Súbalo otra vez.
9. Presione nuevamente **Analizar archivo**.

No se preocupe: mientras haya errores, el sistema no debería confirmar los cambios.

---

## 23. Qué hacer si la previsualización no muestra errores

Si el archivo está bien, aparecerá el botón:

**Confirmar importación**

En ese momento:

1. revise el resumen final,
2. verifique que las cantidades tengan sentido,
3. compruebe que el archivo sea el correcto,
4. recién entonces pulse **Confirmar importación**.

---

## 24. Qué pasa cuando usted confirma

Cuando presiona **Confirmar importación**, el sistema vuelve a revisar el archivo por seguridad.

Luego:

1. guarda primero las recetas,
2. guarda después los cambios de configuración,
3. guarda los bienes,
4. guarda los ingredientes,
5. guarda las relaciones entre recetas y bienes,
6. y al final muestra un mensaje con el resultado.

Ese mensaje suele indicar cuántos registros fueron:

- creados,
- actualizados.

---

## 25. Qué pasa si el archivo es muy grande

Si el archivo tiene muchísimas filas, el sistema puede mostrar una advertencia de volumen alto.

Por ejemplo, si se trata de cientos de recetas, miles de ingredientes o muchas relaciones con bienes.

Esto no significa necesariamente que esté mal.

Significa que:

- puede tardar más,
- y en sistemas muy grandes conviene usar procesos especiales.

Para el uso normal, alcanza con revisar esa advertencia y actuar con cuidado.

---

## 26. Ejemplo simple de uso completo

Supongamos que quiere cargar una receta nueva llamada `Tarta de coco`.

### En la hoja Recetas

- `ID`: vacío
- `Nombre`: Tarta de coco
- `Descripción`: Tarta dulce con coco rallado
- `Categoría`: Tartas
- `Porciones`: 10
- `Rentabilidad %`: 40
- `IVA %`: 21
- `Comentarios`: Receta nueva

### En la hoja Recetas-Productos

Fila 1:

- `ID`: vacío
- `Receta Nombre`: Tarta de coco
- `Producto Nombre`: Harina
- `Cantidad`: 300
- `Medida de uso`: Gramos

Fila 2:

- `ID`: vacío
- `Receta Nombre`: Tarta de coco
- `Producto Nombre`: Azúcar
- `Cantidad`: 200
- `Medida de uso`: Gramos

Fila 3:

- `ID`: vacío
- `Receta Nombre`: Tarta de coco
- `Producto Nombre`: Coco rallado
- `Cantidad`: 150
- `Medida de uso`: Gramos

### En la hoja Bienes

Fila 1:

- `ID`: vacío
- `Nombre`: Horno convector
- `Descripción`: Horno principal de producción
- `Costo de compra`: 850000
- `Vida útil cantidad`: 5
- `Vida útil unidad`: Años
- `Potencia watts`: 2500
- `Factor de uso %`: 100
- `Activo`: Si

### En la hoja Recetas-Bienes

Fila 1:

- `ID`: vacío
- `Receta Nombre`: Tarta de coco
- `Bien Nombre`: Horno convector
- `Tiempo de uso cantidad`: 35
- `Tiempo de uso unidad`: Minutos
- `Incluir depreciación`: Si
- `Incluir electricidad`: Si
- `Observaciones`: Horneado principal

### En la hoja Configuracion

Fila 1:

- `Precio kWh`: 135.5

Después:

1. guarda el Excel,
2. lo sube,
3. lo analiza,
4. revisa el preview,
5. confirma.

---

## 27. Consejos prácticos para trabajar más tranquilo

1. Siempre guarde una copia del archivo antes de hacer cambios grandes.
2. Si va a modificar recetas existentes, primero expórtelas desde el sistema.
3. No escriba nombres de productos “de memoria” si puede copiarlos desde la hoja `Productos`.
4. Si va a usar bienes, exporte antes para copiar exactamente nombres, unidades y relaciones.
5. Revise con atención las columnas de unidades y tiempos de uso.
6. Si algo falla, corrija el Excel y vuelva a analizar. No hace falta rehacer todo desde cero.
7. Si tiene miedo de equivocarse, pruebe primero con 1 o 2 recetas.

---

## 28. Problemas frecuentes y su explicación

### "Solo se aceptan archivos .xlsx"

El archivo no es del tipo correcto.

Solución:

- guarde el archivo como Excel `.xlsx`,
- o use una plantilla descargada desde el sistema.

### "Faltan hojas obligatorias"

Alguna hoja fue borrada o renombrada.

Solución:

- use nuevamente la plantilla,
- o no cambie el nombre de las hojas.

### "Nombre es obligatorio"

Hay una receta sin nombre.

Solución:

- complete el nombre en esa fila.

### "Descripción es obligatoria"

La receta no tiene descripción.

Solución:

- escriba una descripción breve.

### "No se encontró un producto"

El producto escrito no existe o no coincide exactamente.

Solución:

- revise la hoja `Productos`,
- copie el nombre correcto,
- o use el ID.

### "No se encontró un bien"

El bien escrito no existe o no coincide exactamente.

Solución:

- revise la hoja `Bienes`,
- copie el nombre correcto,
- o use el ID.

### "Medida de uso inválida" o "no compatible"

La unidad elegida no corresponde al producto.

Solución:

- revise cómo está cargado ese producto,
- use una unidad compatible.

### "Tiempo de uso inválido"

El tiempo del bien es 0, negativo o no tiene una unidad válida.

Solución:

- complete un número mayor que 0,
- use una unidad de tiempo válida como `Minutos`, `Horas`, `Dias`, `Meses` o `Años`.

### "Precio kWh inválido"

El valor de `Precio kWh` no es numérico o es negativo.

Solución:

- escriba un número válido,
- deje solo una fila con ese dato en la hoja `Configuracion`.

---

## 29. Resumen corto del proceso completo

Si quiere una versión resumida, el trabajo completo es así:

1. Descargar plantilla o exportar recetas actuales.
2. Abrir el Excel.
3. Completar o corregir datos en `Recetas`.
4. Completar o corregir ingredientes en `Recetas-Productos`.
5. Completar o corregir datos en `Bienes` si hace falta.
6. Completar o corregir relaciones en `Recetas-Bienes` si la receta usa equipos o bienes.
7. Revisar el valor de `Precio kWh` en `Configuracion`.
8. Usar `Productos` solo como referencia.
9. Guardar el archivo como `.xlsx`.
10. Subirlo en la pantalla de importación.
11. Pulsar **Analizar archivo**.
12. Revisar advertencias y errores.
13. Si todo está bien, pulsar **Confirmar importación**.

---

## 30. Recomendación final

Si es la primera vez que usa esta herramienta, no empiece con 100 recetas.

Lo más recomendable es hacer una prueba pequeña:

1. exporte una receta existente,
2. cambie un dato simple,
3. analice el archivo,
4. confirme,
5. y vea el resultado.

Cuando ya se sienta cómodo, puede trabajar con archivos más grandes.

---

## 31. En una frase simple

La lógica de esta herramienta es:

**descargar, editar, analizar, revisar y recién después confirmar.**

Ese orden ayuda a trabajar con seguridad y a cometer menos errores.

---

## 32. Atribución

Este proyecto es traído por **EXCEL-ENTE** en colaboración con **ADEMA Sistemas**.
