from core.invoice import Invoice
from data.invoice_repository import InvoiceRepository

def save_invoice(invoice: Invoice, repository: InvoiceRepository):
    repository.save(invoice)