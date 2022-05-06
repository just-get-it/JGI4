
from django.db import models

# Register your models here.
class Resume(models.Model):
    name= models.CharField(max_length=50,default="")
    age = models.CharField(max_length=2,default="")
    phone =models.CharField(max_length=13,default="")
    email = models.CharField(max_length=50,default="")
    address = models.CharField(max_length=50,default="")
    language = models.CharField(max_length=50,default="")
    about =models.TextField()
    exp_tech_name= models.CharField(max_length=50,default="")
   
    image = models.ImageField(upload_to='uploads/products/',default="")
    contact_image = models.ImageField(upload_to='uploads/products/',default="")
    background_image = models.ImageField(upload_to='uploads/products/',default="")
    
    portfolio_image1= models.ImageField(upload_to='uploads/products/',default="")
    portfolio_image2= models.ImageField(upload_to='uploads/products/',default="")
    portfolio_image3= models.ImageField(upload_to='uploads/products/',default="")
    portfolio_image4= models.ImageField(upload_to='uploads/products/',default="")
    fb= models.CharField(max_length=500,default="")
    insta= models.CharField(max_length=500,default="")
    twiter= models.CharField(max_length=500,default="")
    google= models.CharField(max_length=500,default="")
    



    def __str__(self):
        return str(self.name )
