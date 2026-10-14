"""Interfaz gráfica de Winter Store.

La ventana principal administra el pedido y el catálogo se abre por separado.
Las reglas de negocio permanecen en logic.py y los datos en models.py.
"""

from pathlib import Path
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox

import logic
from models import AppState, Product


class WinterStoreApp(ttk.Frame):
    """Interfaz visual; las reglas del negocio se delegan a logic.py."""

    def __init__(self, master) -> None:
        super().__init__(master, padding=16)
        self.pack(fill="both", expand=True)
        self._state = AppState()
        self._code_var = tk.StringVar(value="")
        self._subtotal_var = tk.StringVar(value="$0.00")
        self._discount_amount_var = tk.StringVar(value="$0.00")
        self._total_var = tk.StringVar(value="$0.00")
        self._discount_label_var = tk.StringVar(value="Descuento")
        self._applied_code_var = tk.StringVar(value="Sin código aplicado")
        self._catalog_window = None
        self._catalog_images = []  # Evita que Tkinter libere las imágenes.
        self._catalog_status = None
        self._brand_image = None  # Mantiene viva la imagen del logotipo.
        self._window_icon_image = None  # Mantiene viva la imagen del icono.
        self._configure_window_branding()

        self._build_header()
        self._build_body()
        self._build_status_bar()
        self._refresh()

    def _configure_window_branding(self) -> None:
        """Configura el título y el icono de la ventana principal si existen los archivos."""
        window = self.winfo_toplevel()
        window.title("Winter Store")
        assets = Path(__file__).resolve().parent / "assets"

        # El archivo ICO se recomienda para Windows; PNG funciona en varias plataformas.
        ico_path = assets / "winter_store.ico"
        if ico_path.is_file():
            try:
                window.iconbitmap(str(ico_path))
            except tk.TclError as error:
                print(f"No se pudo cargar el icono ICO: {error}")

        png_path = assets / "winter_store_icon.png"
        if png_path.is_file():
            try:
                self._window_icon_image = tk.PhotoImage(file=str(png_path))
                window.iconphoto(True, self._window_icon_image)
            except tk.TclError as error:
                print(f"No se pudo cargar el icono PNG: {error}")

    def _load_brand_image(self):
        """Carga el logotipo que aparece junto al nombre de la tienda."""
        logo_path = Path(__file__).resolve().parent / "assets" / "logo_winter_store.png"
        if not logo_path.is_file():
            return None
        try:
            try:
                from PIL import Image, ImageTk

                image = Image.open(logo_path).convert("RGBA")
                image.thumbnail((120, 120))
                return ImageTk.PhotoImage(image)
            except ImportError:
                image = tk.PhotoImage(file=str(logo_path))
                factor = max(
                    1, (image.width() + 119) // 120, (image.height() + 119) // 120
                )
                return image.subsample(factor, factor)
        except (tk.TclError, OSError) as error:
            print(f"No se pudo cargar el logotipo: {error}")
            return None

    def _build_header(self) -> None:
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 4))

        brand_row = ttk.Frame(header)
        brand_row.pack(anchor="w")
        self._brand_image = self._load_brand_image()
        if self._brand_image is not None:
            ttk.Label(brand_row, image=self._brand_image).pack(
                side="left", padx=(0, 10)
            )
        ttk.Label(
            brand_row,
            text="Winter Store",
            font=("Segoe UI", 40, "bold"),
            bootstyle="primary",
        ).pack(side="left", anchor="center")

        ttk.Label(
            header,
            text="❄ Tecnología que congela tus sentidos ❄",
            font=("Segoe UI", 12, "bold"),
            bootstyle="primary",
        ).pack(anchor="w", pady=(5, 0))
        ttk.Button(
            header,
            text="EXPLORAR CATÁLOGO",
            bootstyle="success",
            command=self._open_catalog,
            padding=(18, 10),
        ).pack(anchor="e", pady=(10, 0))

    def _build_body(self) -> None:
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, pady=(5, 0))
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)
        self._build_order_table(body).grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        right = ttk.Frame(body)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        self._build_promotions(right).pack(fill="x", pady=(0, 10))
        self._build_summary(right).pack(fill="x")

    def _build_order_table(self, parent) -> ttk.Labelframe:
        box = ttk.Labelframe(parent, text="Tu pedido", padding=12)
        columns = ("product", "quantity", "price", "amount")
        self._table = ttk.Treeview(
            box, columns=columns, show="headings", height=12, selectmode="browse"
        )
        headings = (
            ("product", "Producto", 190, "w"),
            ("quantity", "Cant.", 55, "center"),
            ("price", "Precio", 85, "e"),
            ("amount", "Importe", 90, "e"),
        )
        for key, title, width, anchor in headings:
            self._table.heading(key, text=title)
            self._table.column(key, width=width, anchor=anchor)
        self._table.pack(fill="both", expand=True)
        buttons = ttk.Frame(box)
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(
            buttons,
            text="− 1 unidad",
            bootstyle="warning-outline",
            command=self._on_decrease,
        ).pack(side="left")
        ttk.Button(
            buttons,
            text="Eliminar Producto",
            bootstyle="danger-outline",
            command=self._on_remove,
        ).pack(side="left", padx=(8, 0))
        ttk.Button(
            buttons,
            text="Vaciar pedido",
            bootstyle="secondary-outline",
            command=self._on_clear,
        ).pack(side="left", padx=(8, 0))
        return box

    def _build_promotions(self, parent) -> ttk.Labelframe:
        box = ttk.Labelframe(parent, text="Promociones", padding=12)
        ttk.Label(box, text="Código de descuento").pack(anchor="w")
        ttk.Entry(box, textvariable=self._code_var).pack(fill="x", pady=(4, 8))
        buttons = ttk.Frame(box)
        buttons.pack(fill="x")
        ttk.Button(
            buttons,
            text="Aplicar código",
            bootstyle="primary",
            command=self._on_apply_code,
        ).pack(side="left")
        ttk.Button(
            buttons,
            text="Quitar código",
            bootstyle="secondary-outline",
            command=self._on_remove_code,
        ).pack(side="left", padx=(8, 0))
        ttk.Label(
            box,
            textvariable=self._applied_code_var,
            bootstyle="success",
            wraplength=300,
        ).pack(anchor="w", pady=(10, 0))
        ttk.Label(
            box,
            text="Disponibles: BIENVENIDO5 (5 %) y WINTER10 (10 %).",
            wraplength=300,
        ).pack(anchor="w", pady=(8, 0))
        return box

    def _build_summary(self, parent) -> ttk.Labelframe:
        box = ttk.Labelframe(parent, text="Resumen del pedido", padding=12)
        box.columnconfigure(1, weight=1)
        ttk.Label(box, text="Subtotal").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Label(box, textvariable=self._subtotal_var).grid(
            row=0, column=1, sticky="e"
        )
        ttk.Label(box, textvariable=self._discount_label_var).grid(
            row=1, column=0, sticky="w", pady=5
        )
        ttk.Label(
            box, textvariable=self._discount_amount_var, bootstyle="success"
        ).grid(row=1, column=1, sticky="e")
        ttk.Separator(box).grid(row=2, column=0, columnspan=2, sticky="we", pady=8)
        ttk.Label(box, text="TOTAL", font=("Segoe UI", 11, "bold")).grid(
            row=3, column=0, sticky="w"
        )
        ttk.Label(
            box,
            textvariable=self._total_var,
            bootstyle="primary",
            font=("Segoe UI", 18, "bold"),
        ).grid(row=3, column=1, sticky="e")
        ttk.Button(
            box, text="Finalizar pedido", bootstyle="success", command=self._on_finalize
        ).grid(row=4, column=0, columnspan=2, sticky="we", pady=(16, 0))
        return box

    def _build_status_bar(self) -> None:
        self._status = ttk.Label(
            self,
            text="Listo. Abre el catálogo para agregar productos.",
            bootstyle="secondary",
        )
        self._status.pack(fill="x", pady=(10, 0))

    def _open_catalog(self) -> None:
        if self._catalog_window is not None and self._catalog_window.winfo_exists():
            self._catalog_window.deiconify()
            self._catalog_window.lift()
            return

        window = ttk.Toplevel(self)
        self._catalog_window = window
        window.title("Winter Store · Catálogo")
        # Reutiliza el icono de la ventana principal si está configurado.
        icon_path = Path(__file__).resolve().parent / "assets" / "winter_store_icon.png"
        if icon_path.is_file():
            try:
                window_icon = tk.PhotoImage(file=str(icon_path))
                window.iconphoto(True, window_icon)
                window._winter_store_icon = window_icon  # conserva la referencia
            except tk.TclError:
                pass
        ico_path = Path(__file__).resolve().parent / "assets" / "winter_store.ico"
        if ico_path.is_file():
            try:
                window.iconbitmap(str(ico_path))
            except tk.TclError:
                pass
        window.geometry("900x680")
        window.minsize(700, 500)
        window.transient(self.winfo_toplevel())
        window.columnconfigure(0, weight=1)
        window.rowconfigure(1, weight=1)

        header = ttk.Frame(window, padding=(16, 14, 16, 8))
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(
            header,
            text="Catálogo de productos",
            font=("Segoe UI", 20, "bold"),
            bootstyle="primary",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="Elige un producto, indica la cantidad y agrégalo al pedido.",
            bootstyle="secondary",
        ).pack(anchor="w", pady=(3, 0))
        self._catalog_status = ttk.Label(
            header, text="Listo para agregar productos.", bootstyle="secondary"
        )
        self._catalog_status.pack(anchor="w", pady=(8, 0))

        canvas = tk.Canvas(window, highlightthickness=0)
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=1, column=0, sticky="nsew", padx=(12, 0), pady=(0, 12))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 12), padx=(0, 8))
        cards = ttk.Frame(canvas, padding=8)
        canvas_window = canvas.create_window((0, 0), window=cards, anchor="nw")
        cards.bind(
            "<Configure>",
            lambda _event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(canvas_window, width=event.width),
        )

        # La rueda funciona en Windows/macOS y Linux, solo al pasar por el catálogo.
        def scroll_catalog(event):
            if getattr(event, "delta", 0):
                canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
            elif getattr(event, "num", None) == 4:  # Linux: rueda arriba
                canvas.yview_scroll(-1, "units")
            elif getattr(event, "num", None) == 5:  # Linux: rueda abajo
                canvas.yview_scroll(1, "units")
            return "break"

        def bind_wheel(widget):
            widget.bind("<MouseWheel>", scroll_catalog)
            widget.bind("<Button-4>", scroll_catalog)
            widget.bind("<Button-5>", scroll_catalog)

        bind_wheel(canvas)
        bind_wheel(cards)
        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        self._catalog_images = []

        
        # Aplicamos una promoción del 10 % al catálogo.
        self._catalog_products = logic.apply_price_transform(
            logic.CATALOG,
            lambda price: price * 0.90,
        )

        for index, product in enumerate(self._catalog_products):
            self._build_product_card(cards, product, index)


        def bind_wheel_to_children(widget):
            for child in widget.winfo_children():
                bind_wheel(child)
                bind_wheel_to_children(child)

        bind_wheel_to_children(cards)

        def close_catalog():
            window.destroy()
            self._catalog_window = None
            self._catalog_images = []

        window.protocol("WM_DELETE_WINDOW", close_catalog)
        # Menú contextual copiar/pegar en campos de texto editables del catálogo.
        self._attach_text_context_menu(window)

    def _attach_text_context_menu(self, parent, extra_widget=None) -> None:
        """Agrega menú de clic derecho a Entry, Spinbox y Text editables."""
        menu = tk.Menu(parent, tearoff=0)

        def focused_widget():
            try:
                widget = parent.focus_get()
                if widget is not None and widget.winfo_class() in (
                    "Entry",
                    "TEntry",
                    "Text",
                    "TSpinbox",
                    "Spinbox",
                ):
                    return widget
            except tk.TclError:
                pass
            return None

        def copy_text():
            widget = focused_widget()
            if widget is None:
                return
            try:
                selected = widget.selection_get()
            except tk.TclError:
                return
            parent.clipboard_clear()
            parent.clipboard_append(selected)

        def cut_text():
            widget = focused_widget()
            if widget is None:
                return
            try:
                selected = widget.selection_get()
                parent.clipboard_clear()
                parent.clipboard_append(selected)
                widget.delete("sel.first", "sel.last")
            except (tk.TclError, AttributeError):
                pass

        def paste_text():
            widget = focused_widget()
            if widget is None:
                return
            try:
                value = parent.clipboard_get()
                if widget.winfo_class() == "Text":
                    widget.insert("insert", value)
                else:
                    widget.insert("insert", value)
            except tk.TclError:
                pass

        menu.add_command(label="Copiar", command=copy_text)
        menu.add_command(label="Cortar", command=cut_text)
        menu.add_command(label="Pegar", command=paste_text)
        menu.add_separator()
        menu.add_command(
            label="Seleccionar todo", command=lambda: self._select_all_focused(parent)
        )

        def show_menu(event):
            event.widget.focus_set()
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
            return "break"

        def bind_widget(widget):
            widget.bind("<Button-3>", show_menu, add="+")
            widget.bind(
                "<Control-a>", lambda _event: self._select_all_widget(widget), add="+"
            )
            widget.bind(
                "<Control-A>", lambda _event: self._select_all_widget(widget), add="+"
            )

        def bind_descendants(container):
            for widget in container.winfo_children():
                if widget.winfo_class() in (
                    "Entry",
                    "TEntry",
                    "Text",
                    "TSpinbox",
                    "Spinbox",
                ):
                    bind_widget(widget)
                bind_descendants(widget)

        bind_descendants(parent)
        if extra_widget is not None:
            bind_widget(extra_widget)

    @staticmethod
    def _select_all_widget(widget):
        try:
            if widget.winfo_class() == "Text":
                widget.tag_add("sel", "1.0", "end-1c")
            else:
                widget.selection_range(0, "end")
            return "break"
        except (tk.TclError, AttributeError):
            return "break"

    def _select_all_focused(self, parent):
        widget = parent.focus_get()
        if widget is not None:
            self._select_all_widget(widget)

    def _load_product_image(self, product: Product):
        """Carga una imagen local y la reduce para mostrarla en la tarjeta."""
        image_path = Path(__file__).resolve().parent / product.image
        if not image_path.is_file():
            return None
        try:
            # Pillow mejora el redimensionamiento; si no está instalado se usa Tkinter.
            try:
                from PIL import Image, ImageTk

                image = Image.open(image_path).convert("RGBA")
                image.thumbnail((170, 120))
                return ImageTk.PhotoImage(image)
            except ImportError:
                image = tk.PhotoImage(file=str(image_path))
                factor = max(
                    1, (image.width() + 169) // 170, (image.height() + 119) // 120
                )
                return image.subsample(factor, factor)
        except (tk.TclError, OSError) as error:
            print(f"No se pudo cargar la imagen de {product.name}: {error}")
            return None

    def _build_product_card(self, parent, product: Product, index: int) -> None:
        card = ttk.Labelframe(parent, text=product.name, padding=12)
        card.grid(row=index // 2, column=index % 2, sticky="nsew", padx=7, pady=7)

        image = self._load_product_image(product)
        if image is not None:
            self._catalog_images.append(image)
            ttk.Label(card, image=image).pack(pady=(0, 8))
        else:
            ttk.Label(
                card,
                text="Imagen no disponible",
                bootstyle="secondary",
                width=24,
                anchor="center",
            ).pack(pady=(12, 20))

        ttk.Label(card, text=product.name, font=("Segoe UI", 12, "bold")).pack(
            anchor="w"
        )
        ttk.Label(card, text=product.description, wraplength=330, justify="left").pack(
            anchor="w", pady=(4, 6)
        )
        ttk.Label(
            card,
            text=logic.format_money(product.price),
            font=("Segoe UI", 14, "bold"),
            bootstyle="success",
        ).pack(anchor="w", pady=(0, 8))

        controls = ttk.Frame(card)
        controls.pack(fill="x", side="bottom")
        quantity_var = tk.StringVar(value="1")
        ttk.Label(controls, text="Cantidad:").pack(side="left", padx=(0, 6))
        ttk.Spinbox(controls, from_=1, to=999, width=5, textvariable=quantity_var).pack(
            side="left"
        )
        ttk.Button(
            controls,
            text="Agregar",
            bootstyle="primary",
            command=lambda p=product, q=quantity_var: self._add_from_catalog(
                p, q.get()
            ),
        ).pack(side="right")

    def _add_from_catalog(self, product: Product, raw_quantity: object) -> None:
        try:
            quantity = logic.parse_quantity(raw_quantity)
        except ValueError as error:
            self._set_catalog_status(str(error), "danger")
            Messagebox.show_error(
                str(error),
                title="Cantidad no válida",
                parent=self._catalog_window or self,
            )
            return
        if self._apply_action("add", product=product, quantity=quantity):
            message = f"{quantity} x {product.name} agregado al pedido."
            # La confirmación se muestra únicamente en el catálogo.
            self._set_catalog_status(message, "success")

    def _selected_order_item(self):
        selection = self._table.selection()
        if not selection:
            self._set_status("Selecciona un producto del pedido primero.", "warning")
            return None
        product_id = int(selection[0])
        return next(
            (item for item in self._state.order if item.product.id == product_id), None
        )


    def _on_decrease(self) -> None:
        item = self._selected_order_item()
        if item is None:
            return

        remaining = item.quantity - 1

        if self._apply_action("decrease", product_id=item.product.id):
            self._set_status(
                f"Se redujo {item.product.name} a {remaining} unidad(es).",
                "success",
            )

    def _on_remove(self) -> None:
        selection = self._table.selection()
        product_id = int(selection[0]) if selection else None
        if self._apply_action("remove", product_id=product_id):
            self._set_status("Producto eliminado del pedido.", "success")

    def _on_clear(self) -> None:
        if self._apply_action("clear"):
            self._set_status("Pedido y descuento vaciados.", "secondary")

    def _on_apply_code(self) -> None:
        if self._apply_action("apply_code", code=self._code_var.get()):
            self._set_status("Código aplicado correctamente.", "success")

    def _on_remove_code(self) -> None:
        if self._apply_action("remove_code"):
            self._set_status("Código de descuento retirado.", "secondary")

    def _on_finalize(self) -> None:
        if not logic.can_finalize(self._state.order):
            self._set_status("No se puede finalizar un pedido vacío.", "danger")
            return
        summary = logic.summarize_state(self._state)
        receipt = logic.build_receipt(
            self._state.order, summary, self._state.applied_code
        )
        self._show_receipt(receipt)
        if self._apply_action("finalize"):
            self._set_status("Pedido finalizado correctamente.", "success")

    def _show_receipt(self, receipt: str) -> None:
        """Muestra el comprobante en un cuadro de texto seleccionable y copiable."""
        window = ttk.Toplevel(self)
        window.title("Comprobante · Winter Store")
        window.geometry("520x460")
        window.minsize(420, 350)
        window.transient(self.winfo_toplevel())
        frame = ttk.Frame(window, padding=14)
        frame.pack(fill="both", expand=True)
        ttk.Label(
            frame,
            text="Comprobante del pedido",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary",
        ).pack(anchor="w", pady=(0, 10))
        text_box = tk.Text(frame, wrap="word", height=15, undo=True)
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", receipt)
        self._attach_text_context_menu(window)
        text_box.focus_set()
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(
            buttons,
            text="Seleccionar todo",
            command=lambda: (
                text_box.tag_add("sel", "1.0", "end-1c"),
                text_box.focus_set(),
            ),
        ).pack(side="left")
        ttk.Button(
            buttons,
            text="Copiar comprobante",
            bootstyle="primary",
            command=lambda: self._copy_receipt(text_box.get("1.0", "end-1c"), window),
        ).pack(side="left", padx=8)
        ttk.Button(buttons, text="Cerrar", command=window.destroy).pack(side="right")
        text_box.bind(
            "<Control-a>",
            lambda _event: (text_box.tag_add("sel", "1.0", "end-1c"), "break"),
        )
        text_box.bind(
            "<Control-A>",
            lambda _event: (text_box.tag_add("sel", "1.0", "end-1c"), "break"),
        )

    @staticmethod
    def _copy_receipt(text: str, parent) -> None:
        parent.clipboard_clear()
        parent.clipboard_append(text)
        parent.update()

    def _apply_action(self, action: str, **kwargs) -> bool:
        """Actualiza el estado con el nuevo valor calculado por la capa lógica."""
        try:
            new_state = logic.process_action(self._state, action, **kwargs)
        except ValueError as error:
            self._set_status(str(error), "danger")
            return False
        self._state = new_state
        self._refresh()
        return True

    def _refresh(self) -> None:
        self._table.delete(*self._table.get_children())
        for row in logic.order_rows(self._state.order):
            product_id, name, quantity, price, amount = row
            self._table.insert(
                "", "end", iid=str(product_id), values=(name, quantity, price, amount)
            )
        summary = logic.summarize_state(self._state)
        self._subtotal_var.set(logic.format_money(summary.subtotal))
        self._discount_label_var.set(
            logic.describe_discount_label(self._state.applied_code)
        )
        self._discount_amount_var.set(logic.format_money(summary.discount))
        self._total_var.set(logic.format_money(summary.total))
        self._applied_code_var.set(
            logic.describe_applied_code(self._state.applied_code)
        )

    def _set_status(self, message: str, style: str) -> None:
        self._status.configure(text=message, bootstyle=style)

    def _set_catalog_status(self, message: str, style: str) -> None:
        """Muestra el resultado de agregar dentro de la ventana del catálogo."""
        if self._catalog_status is not None:
            try:
                if self._catalog_status.winfo_exists():
                    self._catalog_status.configure(text=message, bootstyle=style)
                    return
            except tk.TclError:
                pass
        self._set_status(message, style)
