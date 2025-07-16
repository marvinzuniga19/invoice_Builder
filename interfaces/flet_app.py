import flet as ft
from use_cases import generate_invoice, save_invoice, generate_pdf
from data import JsonInvoiceRepository

class InvoiceApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Invoice Builder"
        self.items_data = []

        # UI Elements
        self.client_input = ft.TextField(label="Client", expand=True)
        self.desc_input = ft.TextField(label="Description", expand=True)
        self.qty_input = ft.TextField(label="Quantity", keyboard_type=ft.KeyboardType.NUMBER, width=100)
        self.price_input = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER, width=100)

        self.items_list = ft.Column()
        self.total_label = ft.Text("Total: C$0.00", size=20)

        # Buttons
        add_item_btn = ft.FilledButton("Add Item", on_click=self.add_item)
        generate_btn = ft.FilledButton("Generate and Save", on_click=self.generate_invoice)
        pdf_btn = ft.FilledButton("Generate PDF", on_click=self.generate_pdf_invoice)

        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("Client:", weight="bold"),
                    self.client_input,
                    ft.Divider(),
                    ft.Row([
                        self.desc_input,
                        self.qty_input,
                        self.price_input,
                        add_item_btn
                    ]),
                    ft.Divider(),
                    ft.Text("items added:", weight="bold"),
                    self.items_list,
                    ft.Divider(),
                    self.total_label,
                    ft.Row([generate_btn, pdf_btn])
                ]),
                padding=ft.padding.all(20)
            )
        )

    def add_item(self, e):
        desc = self.desc_input.value
        try:
            qty = int(self.qty_input.value)
            price = float(self.price_input.value)
        except ValueError:
            self.page.snack_bar = ft.SnackBar(ft.Text("Quantity and price must be valid numbers."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        if desc and qty > 0 and price > 0:
            self.items_data.append((desc, qty, price))
            self.items_list.controls.append(
                ft.Text(f"{desc} x{qty} @ ${price:.2f}")
            )
            self.total_label.value = f"Total: ${sum(qty * price for _, qty, price in self.items_data):.2f}"
            self.page.update()
            # Limpiar campos
            self.desc_input.value = ""
            self.qty_input.value = ""
            self.price_input.value = ""
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Invalid Data."))
            self.page.snack_bar.open = True

        self.page.update()

    def generate_invoice(self, e):
        client = self.client_input.value
        if not client or not self.items_data:
            self.page.snack_bar = ft.SnackBar(ft.Text("Client and ítems are required."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        invoice = generate_invoice(client, self.items_data)
        repo = JsonInvoiceRepository("invoices/")
        save_invoice(invoice, repo)

        self.page.snack_bar = ft.SnackBar(ft.Text(f"Saved Invoice. Total: ${invoice.total():.2f}"))
        self.page.snack_bar.open = True
        
        # Limpiar campos
        self.client_input.value = ""
        self.items_data.clear()
        self.items_list.controls.clear()
        self.total_label.value = "Total: $0.00"
        
        self.page.update()

    def generate_pdf_invoice(self, e):
        client = self.client_input.value
        if not client or not self.items_data:
            self.page.snack_bar = ft.SnackBar(ft.Text("Client and items are required."))
            self.page.snack_bar.open = True
            self.page.update()
            return

        invoice = generate_invoice(client, self.items_data)
        pdf_path = f"invoices/{invoice.date.strftime('%Y%m%d_%H%M%S')}.pdf"
        generate_pdf(invoice, pdf_path)

        self.page.snack_bar = ft.SnackBar(ft.Text(f"Invoice PDF saved in {pdf_path}"))
        self.page.snack_bar.open = True
        self.page.update()