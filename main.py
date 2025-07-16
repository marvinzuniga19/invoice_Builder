import flet as ft
from interfaces import InvoiceApp

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_GREY)
    InvoiceApp(page)

if __name__ == "__main__":
    ft.app(target=main)