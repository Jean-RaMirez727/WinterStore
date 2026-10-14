# Análisis funcional de Winter Store

## 1. Introducción

Winter Store es un simulador de tienda desarrollado en Python con una interfaz gráfica realizada con Tkinter y ttkbootstrap. Permite consultar un catálogo, agregar varios productos a un pedido, modificar cantidades, aplicar descuentos, consultar los importes y generar un comprobante.

El proyecto también permite aplicar los conceptos de programación funcional y modelado de datos estudiados en las unidades de la asignatura.

## 2. Organización del proyecto

El código se divide en tres responsabilidades principales:

- `models.py`: contiene las clases que representan los productos, las líneas del pedido, los descuentos, el resumen de compra y el estado de la aplicación.
- `logic.py`: contiene las reglas de negocio, las validaciones, los cálculos y las transformaciones del pedido.
- `ui.py`: administra la interfaz gráfica, las ventanas, los botones y la actualización visual.

Esta separación facilita la comprensión y el mantenimiento del proyecto. La interfaz recibe las acciones del usuario y delega las operaciones del pedido a la capa lógica.

## 3. Modelado de datos con dataclass

En `models.py` se utiliza `@dataclass(frozen=True)` para definir `Product`, `OrderItem`, `DiscountCode`, `OrderSummary` y `AppState`.

El parámetro `frozen=True` impide reasignar los atributos de una instancia después de crearla. El proyecto también utiliza tuplas para almacenar las líneas del pedido y los códigos utilizados.

Por ejemplo, `AppState` representa el estado actual del pedido mediante una tupla de productos, el código aplicado y los códigos que ya se utilizaron. Esto permite devolver un nuevo estado en lugar de modificar directamente el anterior.

## 4. Funciones de orden superior

Una función de orden superior puede recibir otra función como argumento o devolver una función como resultado.

En `logic.py`, `apply_price_transform()` recibe el parámetro `transform`, que representa una función encargada de modificar un precio. Después aplica esa función a cada producto y construye una colección nueva.

Este diseño permite reutilizar la operación con distintas transformaciones de precio sin tener que reescribir toda la función.

## 5. Closures

Una closure es una función que conserva acceso a variables del entorno donde fue creada.

En `make_discount()`, la función interna `discount()` utiliza la variable `rate` definida en la función externa. Por eso puede calcular el descuento correspondiente después de que `make_discount()` termina.

También se utiliza una closure en `make_code_validator()`. La función interna `validate()` conserva acceso a la tabla de códigos creada a partir de los descuentos disponibles.

Estos ejemplos muestran cómo una función puede conservar información para utilizarla posteriormente sin recurrir a una variable global mutable.

## 6. Uso de lambda, map, filter y reduce

El proyecto utiliza varias herramientas de programación funcional:

- `reduce()` en `calculate_subtotal()` acumula los importes de las líneas del pedido.
- `map()` en `get_item_count()` obtiene las cantidades de las líneas.
- `reduce()` en `get_item_count()` suma esas cantidades para conocer el total de unidades.
- `filter()` en `remove_item()` conserva las líneas cuyo identificador no coincide con el producto que se desea eliminar.
- `filter()` en `products_by_price()` selecciona los productos cuyos precios están dentro del rango indicado.
- `map()` en `apply_price_transform()` aplica la transformación a los productos.

Las expresiones `lambda` permiten definir funciones pequeñas para estas operaciones. Se utilizan cuando la lógica es breve y se entiende mejor en el lugar donde aparece.

En cambio, `with_new_price()` es una función con nombre dentro de `apply_price_transform()`. Se prefiere esta alternativa porque la transformación completa de cada producto resulta más legible.

## 7. Pattern matching con match/case

La función `process_action()` utiliza `match/case` para identificar la operación solicitada.

Las acciones contempladas son:

- `add`: agrega un producto o incrementa su cantidad.
- `decrease`: reduce en una unidad la cantidad de un producto.
- `remove`: elimina una línea del pedido.
- `clear`: vacía el pedido y retira el descuento aplicado.
- `apply_code`: valida y aplica un código de descuento.
- `remove_code`: retira el código aplicado.
- `finalize`: valida y finaliza el pedido.

El caso final `case _` rechaza las acciones desconocidas mediante una excepción `ValueError`. Esto permite centralizar las reglas y evitar que cada botón tenga que implementar por separado la lógica de negocio.

## 8. Inmutabilidad y transformación del estado

El estado se representa mediante `AppState`, cuyos atributos no pueden reasignarse directamente. Para actualizarlo, el programa utiliza `dataclasses.replace()` y obtiene una instancia nueva con los cambios necesarios.

Por ejemplo, `add_item()` devuelve una tupla nueva. Si el producto ya existe, genera una nueva línea con la cantidad actualizada; de lo contrario, añade una línea nueva a la tupla.

La acción `decrease` sigue el mismo principio: construye una tupla nueva y reemplaza la línea seleccionada por otra con una unidad menos. La colección original no se modifica.

Esta estrategia hace más claro el flujo de cambios del pedido y facilita identificar el estado que devuelve cada operación.

## 9. Funciones puras y efectos secundarios

Una función pura devuelve un resultado a partir de sus argumentos sin modificar el estado externo ni producir efectos secundarios.

En el proyecto, `calculate_subtotal()`, `summarize_order()` y `format_money()` son ejemplos de funciones de cálculo y formato que no necesitan interactuar con la interfaz. `build_receipt()` también construye un texto a partir de los datos recibidos.

En cambio, los métodos de `ui.py` como `_refresh()`, `_set_status()` y `_show_receipt()` interactúan con widgets y ventanas. Por ese motivo tienen efectos secundarios y pertenecen a la capa de interfaz.

No todas las operaciones deben ser puras: mostrar una ventana o actualizar una tabla requiere interactuar con la interfaz gráfica. Lo importante es mantener esas acciones separadas de los cálculos y reglas del pedido.

## 10. Comparación de los enfoques funcional e imperativo

El enfoque funcional aparece cuando se transforman los datos y se devuelve una nueva colección o un nuevo estado. Algunos ejemplos son `add_item()`, `remove_item()` y `summarize_order()`.

El enfoque imperativo se aprecia en la interfaz, donde se ejecutan instrucciones para crear ventanas, actualizar etiquetas, insertar filas y responder a los eventos de los botones.

Ambos enfoques se utilizan de manera complementaria: la programación funcional ayuda a organizar los cálculos y las transformaciones, mientras que la programación imperativa permite controlar la interacción visual.

## 11. Conclusión

Winter Store aplica los contenidos principales de las unidades mediante funciones de orden superior, closures, expresiones lambda, `map`, `filter`, `reduce`, `match/case` y modelos inmutables con `dataclass`.

La separación entre modelos, lógica e interfaz permite que el código sea más comprensible y que las reglas del pedido no dependan directamente de los widgets. Estas decisiones también facilitan la explicación y demostración del funcionamiento del proyecto.
