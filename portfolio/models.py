


# # portfolio/models.py
# from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    purchase_price = models.FloatField()
    price = models.FloatField(null=True, blank=True)  # Make this field optional if needed
   
    added_on = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f'{self.name} ({self.ticker})'





