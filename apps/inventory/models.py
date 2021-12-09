from django.db import models
from apps.items.models import Item


class Inventory(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateField()

    class Meta:
        db_table = "inventory"

    def __str__(self):
        return '{}'.format(self.name)

class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField()

    class Meta:
        db_table = "inventory_item"
