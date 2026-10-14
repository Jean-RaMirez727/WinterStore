"""Reglas de negocio puras para Winter Store.

Las funciones reciben datos y devuelven resultados nuevos; no leen ni modifican
widgets, archivos o variables globales mutables.
"""

import operator
from dataclasses import replace
from functools import reduce
from typing import Callable

from models import AppState, DiscountCode, OrderItem, OrderSummary, Product

Order = tuple[OrderItem, ...]

CATALOG: tuple[Product, ...] = (
    Product(
        1,
        "Teclado USB",
        18.50,
        "Teclado de tamaño completo con teclas silenciosas y cable USB de 1,5 m.",
        "assets/teclado_usb.png",
    ),
    Product(
        2,
        "Mouse óptico",
        9.90,
        "Mouse óptico de 1200 DPI con diseño ergonómico para oficina y estudio.",
        "assets/mouse_optico.png",
    ),
    Product(
        3,
        "Audífonos",
        24.00,
        "Audífonos de diadema con micrófono y almohadillas acolchadas.",
        "assets/audifonos.png",
    ),
    Product(
        4,
        "Memoria USB",
        12.75,
        "Memoria USB 3.0 de 64 GB para transportar documentos y proyectos.",
        "assets/memoria_usb.png",
    ),
    Product(
        5,
        "Base para laptop",
        21.50,
        "Base plegable de aluminio con inclinación ajustable.",
        "assets/base_laptop.png",
    ),
    Product(
        6,
        "Cable HDMI",
        7.80,
        "Cable HDMI de 1,8 m compatible con resolución Full HD.",
        "assets/cable_hdmi.png",
    ),
)

DISCOUNT_CODES: tuple[DiscountCode, ...] = (
    DiscountCode("BIENVENIDO5", 0.05),
    DiscountCode("WINTER10", 0.10),
)

VALID_DISCOUNT_RATES: tuple[float, ...] = (0.0, 0.05, 0.10)


def calculate_subtotal(items: Order) -> float:
    """Suma los importes del pedido usando reduce."""
    return round(
        reduce(lambda acc, item: acc + item.amount, items, 0.0),
        2,
    )


def make_discount(rate: float) -> Callable[[float], float]:
    """Crea una función que conserva la tasa de descuento en un closure."""
    if rate not in VALID_DISCOUNT_RATES:
        raise ValueError("El descuento debe ser 0 %, 5 % o 10 %.")

    def discount(amount: float) -> float:
        return round(amount * rate, 2)

    return discount

def normalize_code(text: object) -> str:
    """Normaliza un código para facilitar su validación."""
    return str(text).strip().upper()


def make_code_validator(
    codes: tuple[DiscountCode, ...],
) -> Callable[[str], DiscountCode | None]:
    """Crea una función de validación que conserva la tabla de códigos."""
    table = {code.code: code for code in codes}

    def validate(text: str) -> DiscountCode | None:
        return table.get(normalize_code(text))

    return validate


def summarize_order(
    items: Order,
    applied_code: DiscountCode | None,
) -> OrderSummary:
    """Calcula subtotal, descuento y total del pedido."""
    subtotal = calculate_subtotal(items)
    rate = applied_code.rate if applied_code is not None else 0.0
    discount = make_discount(rate)(subtotal)

    return OrderSummary(
        subtotal,
        discount,
        round(subtotal - discount, 2),
    )


def summarize_state(state: AppState) -> OrderSummary:
    return summarize_order(state.order, state.applied_code)


def _validate_quantity(quantity: int) -> None:
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("La cantidad debe ser un entero positivo.")


def parse_quantity(raw: object) -> int:
    """Convierte una entrada en una cantidad entera positiva."""
    try:
        quantity = int(str(raw).strip())
    except (ValueError, TypeError):
        raise ValueError("La cantidad debe ser un número entero.") from None

    _validate_quantity(quantity)
    return quantity


def add_item(
    items: Order,
    product: Product,
    quantity: int,
) -> Order:
    """Agrega un producto o aumenta su cantidad sin mutar la tupla original."""
    _validate_quantity(quantity)

    if any(item.product.id == product.id for item in items):
        return tuple(
            (
                replace(item, quantity=item.quantity + quantity)
                if item.product.id == product.id
                else item
            )
            for item in items
        )

    return items + (OrderItem(product=product, quantity=quantity),)


def remove_item(items: Order, product_id: int) -> Order:
    """Elimina una línea del pedido usando filter."""
    return tuple(filter(lambda item: item.product.id != product_id, items))


def _remove_from_order(
    items: Order,
    product_id: int | None,
) -> Order:
    if product_id is None or not any(item.product.id == product_id for item in items):
        raise ValueError("Debe seleccionar una fila del pedido para quitar.")

    return remove_item(items, product_id)


def _decrease_item(
    items: Order,
    product_id: int | None,
) -> Order:
    """Reduce una unidad de una línea sin modificar el pedido original."""
    if isinstance(product_id, bool) or not isinstance(product_id, int):
        raise ValueError("Debe seleccionar un producto válido.")

    selected = next(
        (item for item in items if item.product.id == product_id),
        None,
    )

    if selected is None:
        raise ValueError("Debe seleccionar una fila del pedido para reducir.")

    if selected.quantity <= 1:
        raise ValueError(
            "Este producto tiene 1 unidad. " "Usa 'Eliminar Producto' para eliminarlo."
        )

    return tuple(
        (
            replace(item, quantity=item.quantity - 1)
            if item.product.id == product_id
            else item
        )
        for item in items
    )


def get_item_count(items: Order) -> int:
    """Cuenta las unidades del pedido usando map y reduce."""
    return reduce(
        operator.add,
        map(lambda item: item.quantity, items),
        0,
    )


def can_finalize(items: Order) -> bool:
    return bool(items)


def _resolve_code(
    codes: tuple[DiscountCode, ...],
    state: AppState,
    text: object,
) -> DiscountCode:
    clean = normalize_code(text)

    if not clean:
        raise ValueError("Ingrese un código de descuento.")

    found = make_code_validator(codes)(clean)

    if found is None:
        raise ValueError("El código ingresado no es válido.")

    if found.code in state.used_codes:
        raise ValueError("Este código ya fue utilizado y no puede usarse otra vez.")

    if state.applied_code == found:
        raise ValueError("Ese código ya está aplicado a este pedido.")

    return found


def _consume_code(state: AppState) -> tuple[str, ...]:
    if state.applied_code is None:
        return state.used_codes

    return state.used_codes + (state.applied_code.code,)


def process_action(
    state: AppState,
    action: str,
    *,
    codes: tuple[DiscountCode, ...] = DISCOUNT_CODES,
    **data: object,
) -> AppState:
    """Procesa una acción y devuelve un AppState nuevo e inmutable."""
    match action:
        case "add":
            product = data.get("product")

            if not isinstance(product, Product):
                raise ValueError("Debe seleccionar un producto.")

            quantity = parse_quantity(data.get("quantity", 1))

            return replace(
                state,
                order=add_item(state.order, product, quantity),
            )

        case "decrease":
            product_id = data.get("product_id")

            return replace(
                state,
                order=_decrease_item(state.order, product_id),
            )

        case "remove":
            product_id = data.get("product_id")

            if isinstance(product_id, bool) or (
                product_id is not None and not isinstance(product_id, int)
            ):
                raise ValueError("El producto seleccionado no es válido.")

            return replace(
                state,
                order=_remove_from_order(state.order, product_id),
            )

        case "clear":
            return replace(
                state,
                order=(),
                applied_code=None,
            )

        case "apply_code":
            return replace(
                state,
                applied_code=_resolve_code(
                    codes,
                    state,
                    data.get("code", ""),
                ),
            )

        case "remove_code":
            return replace(state, applied_code=None)

        case "finalize":
            if not can_finalize(state.order):
                raise ValueError("No se puede finalizar un pedido vacío.")

            return replace(
                state,
                order=(),
                applied_code=None,
                used_codes=_consume_code(state),
            )

        case _:
            raise ValueError(f"Acción desconocida: {action!r}")


def products_by_price(
    products: tuple[Product, ...],
    min_price: float,
    max_price: float,
) -> tuple[Product, ...]:
    """Filtra productos dentro de un rango de precios inclusive."""
    return tuple(
        filter(
            lambda product: min_price <= product.price <= max_price,
            products,
        )
    )


def apply_price_transform(
    products: tuple[Product, ...],
    transform: Callable[[float], float],
) -> tuple[Product, ...]:
    """Devuelve productos nuevos con los precios transformados."""
    return tuple(
        map(
            lambda product: replace(
                product,
                price=round(transform(product.price), 2),
            ),
            products,
        )
    )


def format_money(amount: float) -> str:
    return f"${amount:,.2f}"


def describe_product(product: Product) -> str:
    """Texto que se muestra en el selector del catálogo."""
    return f"{product.name} · {format_money(product.price)}"


def _percent(code: DiscountCode) -> str:
    return f"{round(code.rate * 100, 2):g} %"


def describe_applied_code(code: DiscountCode | None) -> str:
    if code is None:
        return "Sin código aplicado"

    return f"Código {code.code} · {_percent(code)}"


def describe_discount_label(code: DiscountCode | None) -> str:
    if code is None:
        return "Descuento"

    return f"Descuento ({_percent(code)})"


def describe_cart(state: AppState) -> str:
    units = get_item_count(state.order)
    noun = "unidad" if units == 1 else "unidades"

    return f"Pedido: {units} {noun} · " f"{format_money(summarize_state(state).total)}"


def order_rows(items: Order) -> tuple[tuple[object, ...], ...]:
    """Construye filas de tabla: id, producto, cantidad, precio e importe."""
    return tuple(
        (
            item.product.id,
            item.product.name,
            item.quantity,
            format_money(item.product.price),
            format_money(item.amount),
        )
        for item in items
    )


def build_receipt(
    items: Order,
    summary: OrderSummary,
    applied_code: DiscountCode | None,
) -> str:
    """Construye el texto legible del comprobante."""
    lines = [
        "========================================",
        "             WINTER STORE",
        "          COMPROBANTE DE COMPRA",
        "========================================",
        "",
        "PRODUCTOS",
        "----------------------------------------",
    ]

    for item in items:
        lines.append(f"{item.quantity} x {item.product.name}")
        lines.append(f"    Precio unitario: {format_money(item.product.price)}")
        lines.append(f"    Subtotal: {format_money(item.amount)}")
        lines.append("")

    lines.extend(
        [
            "----------------------------------------",
            f"Subtotal:          {format_money(summary.subtotal)}",
        ]
    )

    if applied_code is not None:
        lines.append(f"Código aplicado:   {applied_code.code}")

    lines.extend(
        [
            f"Descuento:         {format_money(summary.discount)}",
            "----------------------------------------",
            f"TOTAL A PAGAR:     {format_money(summary.total)}",
            "========================================",
            "",
            "       Gracias por comprar con nosotros.",
            "          ¡Vuelve pronto!",
        ]
    )

    return "\n".join(lines)
