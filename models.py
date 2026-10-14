"""Modelos inmutables de Winter Store."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """Producto del catálogo."""
    id: int
    name: str
    price: float
    description: str = ""
    image: str = ""


@dataclass(frozen=True)
class OrderItem:
    """Línea del pedido: producto y cantidad."""
    product: Product
    quantity: int

    @property
    def amount(self) -> float:
        return round(self.product.price * self.quantity, 2)


@dataclass(frozen=True)
class DiscountCode:
    """Código de descuento; rate=0.10 equivale al 10 %."""
    code: str
    rate: float


@dataclass(frozen=True)
class OrderSummary:
    """Resumen de los importes del pedido."""
    subtotal: float
    discount: float
    total: float


@dataclass(frozen=True)
class AppState:
    """Estado completo e inmutable de la aplicación."""
    order: tuple[OrderItem, ...] = ()
    applied_code: DiscountCode | None = None
    used_codes: tuple[str, ...] = ()
