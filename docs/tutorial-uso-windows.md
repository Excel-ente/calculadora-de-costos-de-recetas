# Tutorial de Uso en Windows: Cómo sacarle el jugo a la Calculadora de Costos de Recetas

Este documento está pensado como una guía simple, práctica y bien explicada para aprender:

1. para qué sirve esta app,
2. cómo usarla en Windows,
3. cómo organizar mejor sus productos y recetas,
4. y cómo aprovechar las funciones más útiles en el trabajo diario.

La idea no es hablar como técnico, sino explicarlo de forma clara, como si se lo estuviéramos mostrando paso a paso a una persona que quiere usar la herramienta para trabajar mejor.

---

## 1. Qué es esta app y para qué sirve

La **Calculadora de Costos de Recetas** es una aplicación para ayudarle a calcular cuánto cuesta producir lo que vende.

Está pensada especialmente para:

- pasteleros,
- panaderos,
- cocineros,
- emprendedores gastronómicos,
- personas que venden comida por pedido,
- negocios que necesitan ordenar sus costos.

La app le permite responder preguntas muy importantes, por ejemplo:

- ¿Cuánto me cuesta realmente una receta?
- ¿Cuánto me cuesta cada porción?
- ¿Estoy cobrando bien o me estoy quedando corto?
- ¿Qué pasa si sube el precio de un ingrediente?
- ¿Cómo ordeno mis productos y recetas sin hacer todo a mano?

En resumen:

**la app sirve para transformar ingredientes y recetas en información útil para decidir precios y trabajar con más orden.**

---

## 2. Qué problemas resuelve en la práctica

Muchas veces un negocio gastronómico trabaja “más o menos de memoria”.

Eso suele traer problemas como estos:

- no saber el costo real de cada receta,
- usar productos con precios viejos,
- no tener en cuenta gastos adicionales,
- cobrar un precio que parece correcto, pero no deja ganancia,
- perder tiempo buscando datos en cuadernos, papeles o planillas sueltas.

Esta app ayuda a ordenar eso.

Le da un lugar central para guardar:

- productos,
- costos,
- categorías,
- recetas,
- ingredientes,
- gastos extra,
- cálculos automáticos.

---

## 3. Cómo funciona la app en Windows

Esta aplicación funciona en su computadora con Windows y se abre en el navegador.

Eso significa que:

- no es un programa clásico que se instala como Word,
- pero tampoco necesita conocimientos avanzados para usarla,
- porque el propio proyecto trae un archivo que ayuda a iniciarla.

La forma más simple de usarla en Windows es con el archivo:

`iniciar_windows.bat`

Ese archivo prepara el entorno y abre la aplicación en el navegador.

---

## 4. Qué necesita tener en Windows

Para usar la app en Windows, lo ideal es tener:

- **Windows 10 u 11**
- **winget / App Installer** disponible
- conexión a internet en el primer arranque

Python y Git pueden instalarse solos desde el propio `iniciar_windows.bat` si todavía no están en la PC.

Si `winget` no está disponible, entonces sí conviene instalar Python manualmente desde su sitio oficial y Git desde git-scm.com.

---

## 5. La forma más fácil de arrancar la app en Windows

La forma recomendada es usar el archivo:

`iniciar_windows.bat`

### Paso a paso

1. Abra la carpeta del proyecto.
2. Busque el archivo `iniciar_windows.bat`.
3. Si usted mismo lo creó pegando el texto, haga clic derecho y elija **Ejecutar como administrador**.
4. Si ya está dentro de la carpeta del proyecto, también puede hacer doble clic normal.
5. Espere unos segundos.
6. Se abrirá una ventana negra o azul de comandos.
7. Luego se abrirá el navegador con la dirección de la app.

### Qué hace ese archivo por usted

Ese archivo se encarga de varias tareas automáticamente:

- verificar si falta Python y tratar de instalarlo,
- verificar si falta Git y tratar de instalarlo,
- descargar el proyecto si la carpeta todavia no existe,
- actualizarlo con Git si ya existe,
- preparar el entorno interno,
- instalar dependencias si hace falta,
- revisar la base de datos,
- y levantar el servidor local.

Dicho de forma simple:

**ese archivo es el botón de arranque práctico de la aplicación en Windows.**

---

## 6. Qué pasa la primera vez que la usa

La primera vez puede tardar un poco más.

Eso es normal.

Porque el sistema puede necesitar:

- instalar Python,
- instalar Git,
- descargar o actualizar el proyecto,
- preparar archivos internos,
- instalar paquetes,
- crear la base de datos,
- pedirle que cree un usuario administrador.

Esa primera preparación se hace una sola vez.

Después, el uso diario suele ser mucho más rápido.

---

## 7. Cómo entrar a la aplicación

Cuando la app se inicia correctamente, se abre en el navegador.

Normalmente se abre en una dirección como esta:

`http://127.0.0.1:8000/admin/`

Esa dirección significa que la aplicación está funcionando en su propia computadora.

No hace falta memorizarla si el script la abre automáticamente.

Para ingresar, use el nombre de usuario y la contraseña que creó al configurar el sistema.

---

## 8. Muy importante: no cierre la ventana del servidor si está usando la app

Cuando la app está abierta, también queda abierta la ventana del script o del servidor.

Esa ventana es la que mantiene funcionando la aplicación.

Si la cierra, la app deja de responder.

Por eso:

- si está trabajando, deje esa ventana abierta,
- cuando quiera terminar, ahí sí puede cerrarla.

---

## 9. Cómo cerrar la app correctamente

Cuando ya no va a usar la aplicación, puede detenerla.

La forma más común es esta:

1. vaya a la ventana del servidor,
2. presione `CTRL + C`,
3. confirme si Windows se lo pide,
4. cierre la ventana.

Eso detiene la app de forma normal.

---

## 10. Dónde queda guardada su información

Esto es muy importante de entender.

La información del sistema queda guardada dentro de la carpeta del proyecto.

Por ejemplo, en elementos como:

- la base de datos,
- archivos de configuración,
- imágenes,
- y otros datos internos.

En términos simples:

**si mueve, borra o rompe la carpeta del proyecto, puede perder información.**

Por eso conviene que la carpeta esté en un lugar fijo y seguro.

---

## 11. Qué conviene hacer antes de cargar datos reales

Antes de empezar a trabajar en serio, lo más recomendable es hacer estas cosas:

1. iniciar la app correctamente,
2. ingresar al panel,
3. revisar la sección de configuración,
4. hacer una pequeña prueba con pocos productos y pocas recetas.

No hace falta empezar con todo el negocio de una vez.

Es mejor tomarle la mano primero.

---

## 12. La lógica general para sacarle el jugo a la app

Si tuviéramos que resumir la mejor forma de usar esta herramienta, sería esta:

1. configurar el negocio,
2. cargar productos,
3. cargar recetas,
4. asociar ingredientes a cada receta,
5. agregar gastos adicionales si corresponde,
6. revisar costo por receta y costo por porción,
7. ajustar rentabilidad e IVA,
8. exportar o importar información cuando haga falta.

Esa es la lógica central del sistema.

---

## 13. Primer módulo clave: Productos

Los productos son la base de todo.

Un producto es cualquier insumo que usted compra y luego usa en una receta.

Por ejemplo:

- harina,
- azúcar,
- manteca,
- huevos,
- chocolate,
- envases,
- papel manteca,
- crema.

Cada producto guarda datos importantes como:

- nombre,
- categoría,
- marca,
- unidad de medida,
- cantidad,
- costo.

### Por qué este módulo es tan importante

Porque si el costo del producto está mal, el costo de la receta también estará mal.

En otras palabras:

**si quiere buenos números en recetas, primero necesita buenos datos en productos.**

---

## 14. Cómo aprovechar mejor el módulo de productos

Para sacarle más jugo al sistema en productos, conviene seguir estas ideas:

1. usar nombres claros,
2. mantener categorías ordenadas,
3. actualizar precios cuando cambian,
4. usar la unidad correcta,
5. evitar duplicados del mismo producto con nombres parecidos.

Ejemplo de uso correcto:

- `Harina 000`, no `harina`, `Harina`, `Harinaaaa`, todas mezcladas.

Mientras más ordenado esté el catálogo, más fácil será trabajar con recetas.

---

## 15. Segundo módulo clave: Recetas

Una receta es el producto final que usted vende o produce.

Por ejemplo:

- torta de chocolate,
- budín de limón,
- pan casero,
- alfajores,
- pizza,
- brownie.

Cada receta puede tener:

- nombre,
- descripción,
- categoría,
- porciones,
- rentabilidad,
- IVA,
- comentarios.

Pero la receta sola no alcanza.

La parte realmente importante es cuando se la vincula con sus ingredientes.

---

## 16. Tercer módulo clave: Ingredientes dentro de la receta

La app usa una relación entre productos y recetas.

Dicho simple:

- usted tiene productos cargados,
- después arma una receta,
- y luego le dice al sistema qué productos usa esa receta y en qué cantidad.

Eso permite calcular el costo real de preparación.

Ejemplo:

Si una receta usa:

- 500 gramos de harina,
- 200 gramos de azúcar,
- 4 huevos,
- 100 gramos de manteca,

el sistema puede calcular cuánto cuesta esa mezcla con base en los precios de sus productos.

---

## 17. Cuarto módulo útil: Gastos adicionales

Hay recetas cuyo costo no depende solamente de los ingredientes.

También puede haber gastos como:

- gas,
- electricidad,
- packaging,
- decoración,
- traslado,
- otros extras.

La app permite agregar gastos adicionales a una receta.

Eso es muy útil porque muchas personas calculan solo harina, azúcar y huevos, pero se olvidan del resto.

Y ese “resto” muchas veces hace la diferencia entre ganar y perder dinero.

---

## 18. Qué cálculos le devuelve la app

Cuando los datos están bien cargados, la app puede mostrarle cosas como:

- costo total de la receta,
- costo por porción,
- precio de venta por porción,
- impacto del IVA,
- impacto de la rentabilidad,
- cambios al subir o bajar el precio de un producto.

Eso le da una visión mucho más profesional para definir precios.

---

## 19. Cómo sacarle el mayor provecho en el día a día

Una forma muy útil de trabajar con esta app es convertirla en su base de referencia.

Por ejemplo:

### Cada vez que compra mercadería

Revise si cambió el precio de algún producto importante.

Si cambió:

1. entre al módulo de productos,
2. actualice el costo,
3. guarde.

Con eso, las recetas que usan ese producto ya quedan mejor calculadas.

### Cada vez que crea una receta nueva

1. cargue la receta,
2. agregue sus ingredientes,
3. revise el costo,
4. ajuste porciones, rentabilidad e IVA.

### Cada vez que quiera revisar un precio de venta

Abra la receta y vea los números actualizados.

Eso le evita calcular todo a mano otra vez.

---

## 20. Una manera recomendada de empezar a usar la app

Si recién empieza, un orden sano de trabajo sería este:

### Día 1

1. entrar a la app,
2. revisar la configuración general,
3. cargar 10 o 15 productos importantes.

### Día 2

1. cargar 2 o 3 recetas,
2. asociar ingredientes,
3. revisar costos.

### Día 3

1. agregar gastos adicionales si hace falta,
2. revisar porciones,
3. ajustar rentabilidad,
4. revisar precios finales.

### Día 4 en adelante

1. mantener productos actualizados,
2. ir sumando nuevas recetas,
3. usar importación/exportación para trabajo masivo.

---

## 21. Cómo aprovechar la importación y exportación masiva

La app tiene funciones especiales para trabajar con Excel de manera masiva.

Eso sirve para ahorrar tiempo cuando quiere:

- cargar muchos productos,
- actualizar muchos productos,
- cargar recetas en lote,
- actualizar recetas e ingredientes desde Excel.

### En qué casos conviene usar esto

- cuando tiene muchos datos,
- cuando ya usa planillas,
- cuando necesita corregir precios o nombres en bloque,
- cuando prefiere trabajar primero en Excel y luego subir todo.

### En qué casos no hace falta

- cuando solo quiere editar uno o dos registros,
- cuando recién está aprendiendo a usar el sistema.

En esos casos, conviene empezar manualmente.

---

## 22. Cómo usar la app con más orden en Windows

En Windows, una rutina práctica puede ser esta:

### Al empezar el día

1. haga doble clic en `iniciar_windows.bat`,
2. espere a que abra la app,
3. ingrese con su usuario.

### Durante el trabajo

1. deje abierta la ventana del servidor,
2. deje abierta la app en el navegador,
3. cargue o revise la información que necesite.

### Al terminar

1. cierre la sesión si lo desea,
2. vaya a la ventana del servidor,
3. presione `CTRL + C`,
4. cierre la ventana.

---

## 23. Qué conviene guardar como respaldo

Si la app le empieza a resultar útil de verdad, conviene hacer copias de seguridad.

La forma más simple para un usuario no técnico suele ser:

1. cerrar la aplicación,
2. copiar toda la carpeta del proyecto,
3. pegarla en otro lugar seguro.

Por ejemplo:

- un pendrive,
- otra carpeta,
- un disco externo,
- una carpeta sincronizada en la nube.

Esto no reemplaza un sistema profesional de backup, pero para uso cotidiano puede ser una solución muy práctica.

---

## 24. Errores comunes al usarla en Windows

### Error 1: doble clic y no pasa nada

Puede ser que Windows haya bloqueado el archivo descargado, o que falte `winget` para hacer la instalacion automatica.

La forma mas robusta es crear usted mismo el archivo `iniciar_windows.bat`, pegando el texto dentro de una carpeta nueva, y ejecutarlo como administrador.

### Error 2: se abre la app pero luego deja de responder

Probablemente se cerró la ventana del servidor.

### Error 3: no encuentra mis datos

Puede haberse movido la carpeta del proyecto o cambiado archivos importantes.

### Error 4: quiero seguir trabajando en otra computadora

Esta app funciona localmente, así que si quiere usarla en otra máquina necesita llevar la carpeta y hacer la puesta en marcha correspondiente.

---

## 25. Cómo saber si realmente le está sacando provecho a la app

La app le está dando resultado si usted empieza a notar estas mejoras:

1. sabe cuánto cuesta cada receta,
2. deja de poner precios “a ojo”,
3. detecta rápido cuando sube un insumo,
4. puede ajustar precios con más seguridad,
5. tiene la información más ordenada,
6. pierde menos tiempo con cuentas manuales.

Ese es el verdadero valor de esta herramienta.

---

## 26. Una forma simple de sacarle el máximo jugo

Si hubiera que dar un consejo principal, sería este:

**no la use solo como una calculadora, úsela como su sistema de orden.**

Es decir:

- cargue bien los productos,
- mantenga actualizados los costos,
- arme sus recetas correctamente,
- use importación/exportación cuando tenga mucho volumen,
- y vuelva a mirar los números cada vez que cambien los precios.

Cuanto más actualizada esté la información, más útil le será la app.

---

## 27. Resumen corto del mejor recorrido para empezar

Si quiere una versión resumida del mejor camino para comenzar, sería esta:

1. iniciar la app en Windows con `iniciar_windows.bat`,
2. entrar al panel,
3. configurar los datos básicos del negocio,
4. cargar productos,
5. cargar recetas,
6. agregar ingredientes,
7. revisar costos,
8. usar importación/exportación cuando ya se sienta cómodo.

---

## 28. En una frase simple

La mejor manera de sacarle el jugo a esta app es:

**usar Windows solo como puerta de entrada, y usar la aplicación como centro de control de sus costos, productos y recetas.**

---

## 29. Atribución

Este proyecto es traído por **EXCEL-ENTE** en colaboración con **ADEMA Sistemas**.