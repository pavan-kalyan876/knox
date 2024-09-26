from django.db import models

# Create your models here.
from django.db import models


class Trade(models.Model):
    utc_time = models.DateTimeField()
    operation = models.CharField(max_length=10)  # e.g., 'buy' or 'sell'
    base_coin = models.CharField(max_length=10)  # e.g., 'BTC'
    quote_coin = models.CharField(max_length=10)  # e.g., 'INR'
    amount = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.operation} {self.amount} {self.base_coin} at {self.price} {self.quote_coin}"
