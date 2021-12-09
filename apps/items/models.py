from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    description = models.CharField(max_length=150)

    class Meta:
        db_table = "item"

    def __str__(self):
        return '{}'.format(self.name)
