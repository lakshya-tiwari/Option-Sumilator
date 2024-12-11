from django.db import models

class OptionStrategy(models.Model):
    strategy_name = models.CharField(max_length=100)
    stock_price = models.FloatField()
    strike_price = models.FloatField()
    option_type = models.CharField(max_length=10, choices=[('call', 'Call'), ('put', 'Put')])
    premium = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.strategy_name
