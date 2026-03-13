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
| 📂 **Categorías** | Organización de recetas y productos por categoría |
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
| **Git** *(solo si vas a clonar)* | Cualquier versión | [git-scm.com](https://git-scm.com/downloads) |

### ¿Cómo verificar si ya tenés Python instalado?

Abrí el **Símbolo del sistema** (`Win + R` → escribí `cmd` → `Enter`) y ejecutá:

```cmd
python --version
```

Si ves `Python 3.12.x` o superior, ¡estás listo!  
Si no, descargá Python desde [python.org](https://www.python.org/downloads/) y durante la instalación **marcá la casilla "Add Python to PATH"**.

---

## 🚀 Instalación rápida — Windows

> Recomendado para la mayoría de los usuarios. El script `iniciar_windows.bat` hace todo automáticamente.

### Paso 1 — Descargá el proyecto

En la página del repositorio de GitHub:

1. Hacé clic en el botón verde **`<> Code`**
2. Seleccioná **`Download ZIP`**
3. Descomprimí el ZIP en una carpeta de tu elección

   > Ejemplo: `C:\Proyectos\calculadora-costos\`

   > ⚠️ Evitá rutas con espacios o caracteres especiales, como `Mis Documentos`.

### Paso 2 — Ejecutá el script de instalación

1. Abrí la carpeta donde descomprimiste el proyecto
2. Hacé **doble clic** en el archivo **`iniciar_windows.bat`**

> 📌 **Importante:** todo queda guardado en esa misma carpeta (por ejemplo `db.sqlite3`, `.env`, `media/` y el entorno `venv`).
> Antes de ejecutar el `.bat`, colocá el proyecto en un lugar seguro y permanente (por ejemplo `Documentos\calculadora-costos\`).
> Evitá mover o borrar esa carpeta después, porque ahí queda toda tu información.

El script realiza todo automáticamente en el primer uso:

- ✅ Verifica que Python esté instalado
- ✅ Crea el entorno virtual de Python (`venv`)
- ✅ Instala todas las dependencias del proyecto
- ✅ Crea el archivo de configuración `.env`
- ✅ Aplica las migraciones de la base de datos
- ✅ Te guía para crear tu usuario administrador
- ✅ Te ofrece crear un acceso directo en el escritorio
- ✅ Abre el navegador automáticamente en `http://127.0.0.1:8000/admin/`

### Paso 3 — Ingresá a la aplicación

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

**Opción B — Script desde la carpeta**  
Hacé doble clic en **`iniciar_windows.bat`** en la carpeta del proyecto.

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
- [ ] Soporte para múltiples monedas

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