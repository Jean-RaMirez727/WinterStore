# ❄ Winter Store

**Winter Store** es una aplicación de escritorio desarrollada en Python para simular el proceso de compra en una tienda de productos tecnológicos. Cuenta con una interfaz gráfica que permite explorar un catálogo, agregar varios productos a un pedido, modificar cantidades, aplicar códigos de descuento y generar un comprobante de compra.

## Características principales

- Catálogo visual con imágenes, nombres, descripciones y precios de los productos.
- Gestión de pedidos con cantidades múltiples.
- Incremento y reducción de unidades, eliminación de productos y opción para vaciar el pedido.
- Aplicación de códigos de descuento: `BIENVENIDO5` (5 %) y `WINTER10` (10 %).
- Cálculo automático del subtotal, descuento y total.
- Generación de un comprobante de compra que puede seleccionarse y copiarse.
- Separación entre la interfaz gráfica, las reglas de negocio y los modelos de datos.

## Tecnologías utilizadas

- Python 3.13
- Tkinter
- ttkbootstrap
- Programación funcional y funciones de orden superior

## Estructura del proyecto

```text
Winter Store/
├── main.py
├── ui.py
├── logic.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
├── analisis-funcional.md
├── bitacora-ia.md
├── enlace-video.txt
└── assets/
    ├── teclado_usb.png
    ├── mouse_optico.png
    ├── audifonos.png
    ├── memoria_usb.png
    ├── base_laptop.png
    ├── cable_hdmi.png
    ├── logo_winter_store.png
    └── winter_store_icon.png
```

*Nota: la estructura muestra los archivos previstos para el proyecto. Los nombres y documentos deben coincidir con los que existan realmente en la carpeta.*

## Instalación y ejecución

### 1. Instalar Python

Instala Python 3.13 o una versión compatible y comprueba que esté disponible desde la terminal:

```bash
python --version
```

### 2. Crear un entorno virtual

Desde la carpeta principal del proyecto, ejecuta:

```bash
python -m venv .venv
```

Actívalo en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si utilizas el símbolo del sistema de Windows (CMD):

```bat
.venv\Scripts\activate.bat
```

### 3. Instalar las dependencias

Con el entorno virtual activado, ejecuta:

```bash
python -m pip install -r requirements.txt
```

### 4. Iniciar la aplicación

```bash
python main.py
```

## Conceptos de programación aplicados

El proyecto incorpora conceptos de programación funcional y modelado de datos:

- **Funciones de orden superior:** funciones que reciben otras funciones como argumentos o las devuelven como resultado.
- **Closures:** funciones internas que conservan acceso a variables del ámbito donde fueron creadas.
- **`lambda`, `map`, `filter` y `reduce`:** herramientas para realizar transformaciones, filtrados y cálculos.
- **`match/case`:** selección de acciones según la operación solicitada.
- **Modelado de datos:** uso de clases de datos y estructuras inmutables para representar productos, elementos del pedido y el estado de la aplicación.
- **Funciones puras y efectos secundarios:** separación entre los cálculos de negocio y las acciones de la interfaz gráfica.

## Documentación académica

El repositorio también incluye la documentación de la actividad:

- `analisis-funcional.md`: análisis de los conceptos de programación funcional aplicados.
- `bitacora-ia.md`: registro del uso de inteligencia artificial y las modificaciones realizadas.
- `enlace-video.txt`: enlace al video de presentación del proyecto.

## Autoría

Proyecto académico desarrollado como parte de una actividad de programación, con el objetivo de aplicar los contenidos de las unidades estudiadas mediante una aplicación funcional con interfaz gráfica.