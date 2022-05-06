from django.db import models


# Create your models here.
class enquiry_port(models.Model):
    fullname =  models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    number = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    subject = models.TextField()
    disp = models.TextField()
    en_title = models.TextField(max_length=25)

