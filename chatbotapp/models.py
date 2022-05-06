from django.db import models

# Create your models here.

    
    
class Complaint(models.Model) :
    number = models.IntegerField(default=12)
    desc = models.TextField(default="Not Applicable") 
    status = models.CharField(max_length=10, default="NA")
    reply = models.TextField(max_length=100,default="NA")
    def __str__(self):
        return self.desc


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    suggestions = models.TextField(max_length=100, default="NA")


