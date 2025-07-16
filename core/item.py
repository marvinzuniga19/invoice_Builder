
class Item:
  def __init__(self, description: str, quantity: int, price: float):
    self.description = description
    self.quantity = quantity
    self.price = price

  def total(self) -> float:
    return self.quantity * self.price
  