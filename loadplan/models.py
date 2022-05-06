from django.db import models

# Create your models here.

class Ord(models.Model):
    orderno = models.IntegerField()
    styleno = models.IntegerField()
    orderqty = models.IntegerField()
    ordercd = models.DateField()
    plancd = models.DateField()
    ocd = models.DateField()
    ltf = models.IntegerField()
    ltb = models.IntegerField()

class Avc(models.Model):
    lineno = models.IntegerField()
    noo = models.FloatField()
    workdays = models.FloatField()
    dwh = models.FloatField()
    absent = models.FloatField()
    efficiency = models.FloatField()
    mac = models.FloatField()

class Cpr(models.Model):
    orderno = models.IntegerField()
    ltlc = models.IntegerField()
    orderqty = models.IntegerField()
    smv = models.IntegerField()
    crm = models.FloatField()
    capd = models.FloatField()
    crd = models.FloatField()

class Mat(models.Model):
    orderno = models.IntegerField()
    fin = models.CharField(max_length=2)
    threads = models.CharField(max_length=2)
    sewtrim = models.CharField(max_length=2)
    fintrim = models.CharField(max_length=2)
    packtrim = models.CharField(max_length=2)

class Lio(models.Model):
    orderno = models.IntegerField()
    ltlc = models.IntegerField()
