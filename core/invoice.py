from datetime import datetime
from typing import List
from .item import Item


class Invoice:
  def __init__(self, client:str, items:List[Item], date: datetime = None):
    self.client = client
    self.items = items
    self.date = date or datetime.now()

  def total(self) -> float:
    return sum(item.total() for item in self.items)
  