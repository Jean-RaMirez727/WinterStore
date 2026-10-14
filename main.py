"""Punto de entrada de Winter Store."""

import ttkbootstrap as ttk
from ui import WinterStoreApp


def main() -> None:
    root = ttk.Window(themename="flatly")
    root.title("Winter Store · Simulador de pedidos")
    root.state("zoomed")
    root.minsize(1100, 800)

    WinterStoreApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
