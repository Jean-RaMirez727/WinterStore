# Bitácora de uso de inteligencia artificial

## 1. Introducción

Durante el desarrollo de Winter Store utilicé la inteligencia artificial como apoyo para organizar el proyecto, revisar errores, mejorar la interfaz y comprender cómo aplicar los contenidos de programación funcional solicitados en la actividad.

La IA se utilizó como herramienta de consulta y revisión. Las propuestas se fueron adaptando a las necesidades del proyecto y a las decisiones tomadas durante el desarrollo.

## 2. Selección y organización del proyecto

El objetivo fue desarrollar un simulador funcional con interfaz gráfica que permitiera mostrar un catálogo de productos y administrar un pedido.

Para organizar el trabajo se separaron los modelos de datos, las reglas de negocio y la interfaz gráfica. Esta decisión permitió trabajar con archivos específicos para cada responsabilidad y comprender mejor el funcionamiento de la aplicación.

## 3. Corrección y mejora del código

Durante el desarrollo solicité ayuda para revisar los archivos de la interfaz y la lógica, corregir problemas y mejorar la presentación del catálogo.

Una de las solicitudes realizadas fue:

> ayudame corrigiendo entonces ui y demas codigos que esten mal por favor

A partir de la revisión se trabajó en la organización de las funciones, la validación de las cantidades, el cálculo de los importes, la aplicación de descuentos y la administración del estado del pedido.

También se mejoró la presentación del catálogo para mostrar imágenes, descripciones y precios, además de permitir agregar diferentes productos y cantidades.

## 4. Aplicación de los contenidos de la asignatura

La revisión del proyecto permitió identificar ejemplos concretos de los contenidos obligatorios:

- Funciones de orden superior mediante `apply_price_transform()`.
- Pattern matching mediante `process_action()` y sus casos.
- Modelado de datos con `dataclass(frozen=True)`.
- Funciones lambda y operaciones con `map`, `filter` y `reduce`.
- Closures en `make_discount()` y `make_code_validator()`.
- Transformaciones inmutables mediante tuplas y `dataclasses.replace()`.
- Separación entre las funciones de cálculo y las operaciones de la interfaz.

Estos contenidos se incorporaron en las partes donde resultaban útiles para el funcionamiento del simulador.

## 5. Decisiones y adaptaciones

Las sugerencias recibidas no se adoptaron automáticamente. Se revisaron según la estructura existente y las necesidades de la actividad.

Se mantuvo el catálogo de productos y los códigos de descuento como datos definidos en la capa lógica. Las operaciones del pedido se concentraron en `process_action()` para evitar duplicar las reglas entre los botones de la interfaz.

También se conservó una función con nombre para transformar el precio de cada producto, ya que resultaba más fácil de leer que una expresión lambda extensa.

La interfaz se mantuvo separada de los cálculos. Su responsabilidad es recoger las acciones del usuario, mostrar mensajes, actualizar las tablas y presentar el comprobante.

## 6. Comprobación del funcionamiento

Durante el desarrollo se realizaron comprobaciones manuales de las funciones principales de la aplicación. El alcance de las verificaciones debe registrarse según lo efectivamente ejecutado en la versión final.

Las funciones que deben comprobarse antes de la entrega incluyen:

- Inicio de la aplicación y visualización de la ventana principal.
- Apertura del catálogo y visualización de los productos.
- Selección de productos y cantidades.
- Agregar varias unidades del mismo producto.
- Reducir cantidades y eliminar productos.
- Actualización del subtotal, descuento y total.
- Aplicación y retirada de códigos de descuento.
- Rechazo de cantidades inválidas y códigos incorrectos.
- Rechazo de pedidos vacíos al intentar finalizarlos.
- Generación del comprobante al finalizar un pedido válido.

Estas comprobaciones permiten identificar errores de interacción y confirmar que las reglas principales se mantienen después de los cambios.

## 7. Aprendizajes

El desarrollo me ayudó a distinguir entre una función de orden superior y una closure. También me permitió comprender mejor cómo `map`, `filter` y `reduce` pueden utilizarse para transformar y acumular datos.

Otro aprendizaje fue que la inmutabilidad no consiste solamente en evitar modificar una variable. En este proyecto también significa construir nuevas tuplas y nuevas instancias del estado para representar los cambios del pedido.

Finalmente, comprendí la importancia de separar las reglas de negocio de la interfaz para que los cálculos y validaciones puedan revisarse sin depender directamente de las ventanas.

## 8. Conclusión

La inteligencia artificial sirvió como apoyo durante la organización, revisión y mejora del proyecto. El trabajo realizado permitió relacionar los conceptos de la asignatura con un simulador que tiene una finalidad concreta.

La revisión final del código y las comprobaciones de funcionamiento son necesarias para asegurar que la versión entregada corresponda con lo explicado en los documentos y en el video de demostración.
