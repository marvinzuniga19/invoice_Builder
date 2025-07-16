import os
import json
from datetime import date

from core.invoice import Invoice



class JsonInvoiceRepository:
  def __init__(self, base_path: str):
    self.base_path = base_path
    os.makedirs(self.base_path, exist_ok = True)

  
  def save(self,invoice: Invoice):
    filename = f'{invoice.date.strftime('%Y%m%d_%H%M%S')}.json'
    path = os.path.join(self.base_path, filename)
    data = {
      'Client': invoice.client,
      'date': invoice.date.isoformat(),
      'items': [{'description': i.description, 'quantity': i.quantity, 'price': i.price} for i in invoice.items],
      'total': invoice.total() 
      }

    with open(path, 'w') as f:
      json.dump(data, f, indent = 4)