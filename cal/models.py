from django.db import models
from django.utils.timezone import now

# Create your models here.

class Event(models.Model):
    user = models.CharField(max_length=200, default='consumer1@gmail.com')
    title = models.CharField(max_length=200)
    sub_transaction_id = models.CharField(max_length=200, default='1')
    start_time = models.DateField(default=now)
    end_time = models.DateField(default=now)
    isStopped = models.BooleanField(default=False)
    isPaidForEvent = models.BooleanField(default=False)
    def __str__(self):
        return self.title
