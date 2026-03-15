# 🧁 Calculadora de Costos de Recetas

**Gestiona, calcula y optimiza el costo de tus recetas de cocina.**  
Ideal para emprendedores gastronómicos, pasteleros y chefs.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/Base%20de%20datos-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Licencia](https://img.shields.io/badge/Licencia-Apache%202.0-blue)](LICENSE)
[![YouTube](https://img.shields.io/badge/YouTube-%40excel--ente-FF0000?logo=youtube&logoColor=white)](https://www.youtube.com/@excel-ente)

[📺 Tutoriales en YouTube](https://www.youtube.com/@excel-ente) · [🐛 Reportar un problema](../../issues) · [💡 Sugerir mejora](../../issues/new)


---

## 📋 Tabla de contenidos

1. [¿Qué es este proyecto?](#-qué-es-este-proyecto)
2. [Características](#-características)
3. [Cómo se calcula una receta](#-cómo-se-calcula-una-receta)
4. [Requisitos previos](#-requisitos-previos)
5. [Instalación rápida — Windows](#-instalación-rápida--windows)
6. [Instalación manual paso a paso](#-instalación-manual-paso-a-paso)
7. [Uso diario](#️-uso-diario)
8. [Documentación](#-documentación)
9. [Contribuir al proyecto](#-contribuir-al-proyecto)
10. [Autor y créditos](#-autor-y-créditos)

---

## 🧁 ¿Qué es este proyecto?

La **Calculadora de Costos de Recetas** es una aplicación web que corre localmente en tu computadora, hecha con Python y Django. Te permite llevar un control completo del costo de producción de tus recetas: ingredientes, gastos adicionales, IVA, bienes de producción, fabricaciones y reportes.

> 💡 Este proyecto es **100 % gratuito y de código abierto**. Fue creado para ser mejorado por la comunidad. Seguí las **sagas de video en YouTube** donde lo mejoramos en vivo usando agentes de IA.

---

## ✨ Características

| Módulo | Descripción |
|---|---|
| 🥩 **Productos** | Ingredientes con costos actualizables |
| 🍰 **Recetas** | Recetas con pasos, ingredientes, bienes asociados y cálculo automático de costos |
| 🏭 **Bienes** | Equipos como hornos, batidoras o heladeras con costo de uso, depreciación y electricidad |
| 💰 **Costo de producción** | Cálculo con IVA, gastos adicionales, depreciación y consumo eléctrico cuando corresponde |
| � **Segunda moneda** | Mostrá todos los precios y costos en dos monedas simultáneamente (ej. $ y USD) con tipo de cambio y redondeo configurables |
| �📂 **Categorías** | Organización de recetas y productos por categoría |
| 🏭 **Fabricaciones** | Registro de producción con historial y fechas |
| 📊 **Exportaciones** | Descarga de reportes en Excel y PDF |
| 📅 **Agenda** | Agenda integrada de tareas y recordatorios |
| 👥 **Usuarios** | Múltiples usuarios con roles y permisos |
| ⚙️ **Configuración** | Personalización con logo, datos del negocio y más |

---

## 🧮 Cómo se calcula una receta

Ahora una receta no solo suma ingredientes.

El sistema puede contemplar también los **bienes de producción** que usás para hacerla, por ejemplo:

- horno
- amasadora
- batidora
- licuadora
- heladera

### ¿Qué costo puede aportar un bien?

Cada bien puede aportar dos tipos de costo:

1. **Depreciación por uso**
   Si un equipo se usa para producir una receta, una parte de su valor se reparte según el tiempo de uso.

2. **Costo de electricidad**
   Si ese equipo consume energía, el sistema calcula cuánto costó usarlo según su potencia, el tiempo de uso y el valor del kWh configurado.

### En palabras simples

El costo final de una receta puede incluir:

- ingredientes
- subrecetas
- gastos adicionales
- IVA
- costo de uso de bienes

Esto permite que el costo total y el costo por porción sean más reales, sobre todo en recetas donde intervienen equipos eléctricos o maquinaria de trabajo.

### Ejemplo simple

Si una receta usa un horno durante 40 minutos, el sistema puede sumar:

- una parte del desgaste del horno
- el costo de la electricidad consumida en ese tiempo

De esa forma, la receta no queda calculada solo con la materia prima, sino también con el costo real de producirla.

### ¿Es obligatorio usar bienes en todas las recetas?

No. Solo se usan cuando corresponde.

Si una receta no necesita asociar bienes, puede seguir calculándose de forma normal como hasta ahora.

---

## 💻 Requisitos previos

| Requisito | Versión mínima | Descarga |
|---|---|---|
| **Python** | 3.12 o superior | [python.org/downloads](https://www.python.org/downloads/) |
| **Sistema operativo** | Windows 10 / 11 | — |
| **Git** *(solo si vas a clonar o actualizar manualmente)* | Cualquier versión | [git-scm.com](https://git-scm.com/downloads) |
| **winget / App Installer** *(recomendado)* | Incluido en Windows 10/11 moderno | Microsoft Store |

### ¿Cómo verificar si ya tenés Python instalado?

Abrí el **Símbolo del sistema** (`Win + R` → escribí `cmd` → `Enter`) y ejecutá:

```cmd
python --version
```

Si ves `Python 3.12.x` o superior, ya podés seguir.  
Si no lo tenés, el instalador `iniciar_windows.bat` ahora puede intentar instalarlo automáticamente con `winget`.

---

## 🚀 Instalación rápida — Windows

> Recomendado para la mayoría de los usuarios. El script `iniciar_windows.bat` ahora sirve tanto como lanzador del proyecto como bootstrap instalable por copia y pegado.

### Paso 1 — Elegí una carpeta fija

Creá una carpeta donde quieras dejar instalada la app, por ejemplo:

`C:\Proyectos\calculadora-costos\`

> Todo queda guardado ahi: base de datos, `.env`, `media/` y `venv/`.

### Paso 2 — Pegá el contenido de `iniciar_windows.bat`

1. Abrí el archivo `iniciar_windows.bat` desde GitHub.
2. Copiá todo su contenido.
3. Creá un archivo nuevo con ese mismo nombre dentro de tu carpeta fija.
4. Ejecutalo con clic derecho → **Ejecutar como administrador**.

Este camino evita el bloqueo frecuente que Windows aplica a los `.bat` descargados dentro de un ZIP.

### Paso 3 — Dejá que el script haga el trabajo

Si en esa ruta todavia no existe la carpeta del proyecto, el script:

- ✅ instala Python 3.12+ si falta
- ✅ instala Git si falta
- ✅ clona el repositorio oficial en esa misma ruta
- ✅ crea el entorno virtual
- ✅ instala dependencias
- ✅ crea `.env`
- ✅ aplica migraciones
- ✅ te guia para crear el usuario administrador
- ✅ puede crear un acceso directo

Si la carpeta del proyecto ya existe y tiene Git, el script intenta hacer `git pull --ff-only` antes de iniciar.

> 📌 **Importante:** todo queda guardado en esa misma carpeta (por ejemplo `db.sqlite3`, `.env`, `media/` y el entorno `venv`).
> Antes de ejecutar el `.bat`, colocá el proyecto en un lugar seguro y permanente (por ejemplo `Documentos\calculadora-costos\`).
> Evitá mover o borrar esa carpeta después, porque ahí queda toda tu información.

### Paso 4 — Ingresá a la aplicación

En el navegador, iniciá sesión con el **nombre de usuario y contraseña** que creaste en el paso anterior.

¡Listo! 🎉

---

## 📖 Instalación manual paso a paso

> Para quienes prefieren controlar cada paso del proceso.

### 1. Descargá o cloná el proyecto

**Opción A — Descargar ZIP:**

1. En la página del repositorio, hacé clic en **`<> Code`** → **`Download ZIP`**
2. Descomprimí el archivo en `C:\Proyectos\calculadora-costos\`

**Opción B — Clonar con Git:**

```cmd
git clone https://github.com/Excel-ente/calculadora-de-costos-de-recetas.git
cd calculadora-costos
```

---

### 2. Verificá la versión de Python

```cmd
python --version
```

Necesitás **Python 3.12 o superior**. Si no lo tenés:

1. Descargá desde [python.org/downloads](https://www.python.org/downloads/)
2. **⚠️ Importante:** marcá la casilla **"Add Python to PATH"** al instalar
3. Cerrá y volvé a abrir el `cmd`

> Si preferís evitar esta parte manual, usá el `iniciar_windows.bat` copiado a mano y dejá que instale Python con `winget`.

---

### 3. Abrí el Símbolo del Sistema en la carpeta del proyecto

Desde el Explorador de archivos, navegá hasta la carpeta del proyecto, hacé clic en la barra de direcciones, escribí **`cmd`** y presioná `Enter`.

O desde cualquier `cmd`:

```cmd
cd C:\Proyectos\calculadora-costos
```

---

### 4. Creá el entorno virtual

```cmd
python -m venv venv
```

Esto crea una carpeta `venv` con un Python aislado para este proyecto, sin afectar el resto de tu sistema.

---

### 5. Activá el entorno virtual

```cmd
venv\Scripts\activate
```

Deberías ver `(venv)` al inicio de la línea. **Recordá activarlo siempre antes de trabajar con el proyecto.**

---

### 6. Instalá las dependencias

```cmd
pip install -r requirements.txt
```

Este proceso puede tardar unos minutos la primera vez.

---

### 7. Creá el archivo de configuración

Copiá el archivo de ejemplo incluido:

```cmd
copy .env.example .env
```

O creá el archivo `.env` manualmente en la raíz del proyecto con este contenido mínimo:

```env
MODO_DESARROLLO=True
SECRET_KEY=cambia-esta-clave-por-una-cadena-aleatoria-larga
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

> 💡 En modo desarrollo local no es necesario cambiar la `SECRET_KEY`. Solo modificala si vas a poner el proyecto en un servidor público.

---

### 8. Aplicá las migraciones de la base de datos

```cmd
python manage.py migrate
```

Deberías ver una lista de migraciones aplicadas. Esto crea la base de datos SQLite con todas las tablas necesarias.

---

### 9. Creá tu usuario administrador

```cmd
python manage.py createsuperuser
```

El sistema te va a pedir:

- **Username**: nombre de usuario (ej: `admin`)
- **Email** *(opcional)*: podés dejarlo en blanco y presionar `Enter`
- **Password**: tu contraseña (no se muestra al escribir)
- **Password (again)**: confirmación de contraseña

---

### 10. Iniciá el servidor

```cmd
python manage.py runserver
```

---

### 11. Abrí el navegador

Ingresá a: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**

Iniciá sesión con el usuario del paso 9. ¡Ya podés usar la aplicación!

---

## 🖥️ Uso diario

Una vez instalado, para abrir la aplicación cada día:

**Opción A — Acceso directo** *(si lo creaste durante la instalación)*  
Hacé doble clic en **`Calculadora de Costos`** en el escritorio.

**Opción B — Script bootstrap o script desde la carpeta**  
Hacé doble clic en **`iniciar_windows.bat`**. Si está fuera del repo, actualiza o reinstala en esa ruta. Si está dentro del repo, simplemente actualiza e inicia.

**Opción C — Desde el Símbolo del Sistema**

```cmd
cd C:\Proyectos\calculadora-costos
venv\Scripts\activate
python manage.py runserver
```

Para **detener el servidor**, presioná `Ctrl + C` en la ventana del script.

### Crear el acceso directo al escritorio manualmente

Si saltaste esa opción durante la instalación:

1. Abrí la carpeta del proyecto
2. Hacé **clic derecho** en `iniciar_windows.bat`
3. Seleccioná **"Enviar a"** → **"Escritorio (crear acceso directo)"**

---

## 📚 Documentación

La documentación complementaria del proyecto está organizada en la carpeta [`docs/`](docs/README.md).

- [Índice de documentación](docs/README.md)
- [Tutorial de uso en Windows](docs/tutorial-uso-windows.md)
- [Importar y exportar productos](docs/import-export-productos.md)
- [Importar y exportar recetas](docs/import-export-recetas.md)
- [Dashboard](docs/dashboard.md)
- [Resumen del dashboard](docs/dashboard-resumen.md)
- [Especificación funcional de bienes](docs/funcionalidad-bienes.md)
- [Segunda moneda (doble divisa)](docs/segunda-moneda.md)

---

## 🤝 Contribuir al proyecto

¡Este proyecto es abierto a mejoras de la comunidad! Seguí las sagas de video en YouTube donde vemos cómo usar agentes de IA para mejorarlo paso a paso.

### ¿Cómo contribuir?

1. Hacé un **Fork** del repositorio (botón en la esquina superior derecha de GitHub)
2. Creá tu rama de mejora:
   ```
   git checkout -b feature/mi-mejora
   ```
3. Hacé tus cambios y commiteá:
   ```
   git commit -m "Descripcion clara de la mejora"
   ```
4. Subí tu rama:
   ```
   git push origin feature/mi-mejora
   ```
5. Abrí un **Pull Request** desde GitHub

### Ideas para el futuro

- [ ] Versión móvil / PWA
- [ ] Gráficos de costos y tendencias con Chart.js
- [ ] Integración con APIs de precios de supermercados
- [ ] Alertas de stock mínimo de ingredientes
- [ ] Comparador de costos entre recetas
- [ ] Modo oscuro

> 🎬 Seguí el canal de YouTube para ver cómo se implementan estas mejoras en vivo con agentes de IA.

---

## 👨‍💻 Autor y créditos

**Kevin Turkienich**  
Fundador de **Excel-ente** & **ADEMA Sistemas**

| Red social | Enlace |
|---|---|
| 📺 YouTube | [youtube.com/@excel-ente](https://www.youtube.com/@excel-ente) |
| 📸 Instagram | [instagram.com/excel.entes](https://www.instagram.com/excel.entes) |
| 🎵 TikTok | [tiktok.com/@excel.entes](https://www.tiktok.com/@excel.entes) |

---

## 📄 Licencia

Este proyecto está bajo la **Licencia Apache 2.0** — podés usarlo, modificarlo y distribuirlo libremente siempre que incluyas el aviso de licencia original.

Adicionalmente, toda distribución o instancia pública debe conservar la atribución:

**"Esta herramienta la trae EXCEL-ENTE en colaboración con ADEMA Sistemas."**

Ver el archivo [LICENSE](LICENSE) para más detalles.


Hecho con ❤️ por [Excel-ente](https://www.youtube.com/@excel-ente)

Si te ayudó, ¡dejale una ⭐ al repositorio!

Contacto

Correo electrónico por turkienich@gmail.com

---

## 📦 Historial de versiones

### v2.1.0 — Segunda moneda (doble divisa) con redondeo configurable

**Fecha:** Marzo 2026

```
feat: implementar segunda moneda con redondeo configurable

- Agrega campos habilitar_segunda_moneda, segunda_moneda, tipo_de_cambio
  y redondeo_segunda_moneda al modelo Configuracion
- Migraciones 0002, 0003 y 0004 en configuracion/
- Métodos costo_unitario_segunda_moneda() en Producto y
  costo_porcion_segunda_moneda(), precio_venta_porcion_segunda_moneda(),
  precio_venta_total_segunda_moneda() en Receta con round() dinámico
- Admin: columnas de segunda moneda en lista de Productos y Recetas;
  celdas de Costo, Costo unitario, Costo total y Precio venta muestran
  ambas monedas en la misma celda (formato <small> gris)
- Reporte PDF: fmt2() aplica tipo de cambio y redondeo configurados
- Dashboard: valores costo_total_2, costo_porcion_2 y precio_venta_2
  usan redondeo_segunda_moneda independiente del redondeo principal
- JS: deshabilita campos de segunda moneda cuando el toggle está apagado
- Tests: clase SegundaMonedaTests con 13 casos integradores (13/13 OK)
- Docs: docs/segunda-moneda.md documentación completa de la feature
```

**Archivos modificados:**  
`configuracion/models.py` · `configuracion/admin.py` · `configuracion/migrations/0002–0004` · `administracion/models.py` · `administracion/admin.py` · `administracion/Reporte.py` · `administracion/dashboard_views.py` · `administracion/tests.py` · `static/js/segunda_moneda_admin.js` · `docs/segunda-moneda.md`