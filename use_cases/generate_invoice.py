from core.invoice import Invoice
from core.item import Item

def generate_invoice(client: str, items_data: list) -> Invoice:
    items = [Item(desc, qty, price) for desc, qty, price in items_data]
    return Invoice(client=client, items=items)