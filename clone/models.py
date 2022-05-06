from django.db import models

# Create your models here.
class account (models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone_number= models.CharField(max_length=10)
    studying= models.CharField(max_length=50)
    education_intrest= models.CharField(max_length=30)
    city= models.CharField(max_length=30)



class new_events(models.Model):
    upcoming_form = models.CharField(max_length=30)
    starting_date = models.DateField()
    ending_date= models.DateField()
    Eligibility= models.CharField(max_length=30)
    link =models.URLField(default='NULL')


class old_events(models.Model):
    Ended_form = models.CharField(max_length=30)
    starting_date = models.DateField()
    ending_date= models.DateField()
    Eligibility= models.CharField(max_length=30)
    link =models.URLField(default='NULL')

class current(models.Model):
    exxam_form = models.CharField(max_length=30)
    starting_date = models.DateField()
    ending_date= models.DateField()
    Eligibility= models.CharField(max_length=30)
    link =models.URLField(default='NULL')


class enquiry_port(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone_number= models.CharField(max_length=10)
    country= models.CharField(max_length=50)
    subject= models.CharField(max_length=100)
    disp= models.CharField(max_length=30)
    en_title= models.CharField(max_length=30)



