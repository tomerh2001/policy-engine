from django.db import models

class PolicyRule(models.Model):
    uid = models.IntegerField(default=0, primary_key=True, unique=True)
    maxAmount = models.FloatField() # Maximum amount in stoshis
    destinations = models.TextField() # Destinations seperated by delimiter

class Transaction(models.Model):
    amount = models.FloatField() # Sent amount in stoshis
    destination = models.TextField() # Transaction destination address
    outgoing = models.BooleanField(default=False) # Outgoing indication status