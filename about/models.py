from django.db import models

# Create your models here.
class FileUpload(models.Model):
    file=models.FileField(upload_to='fileField',blank=True,null=True)
    name=models.CharField(default="Garment Details",max_length=100)
    slug=models.SlugField(default="tag01",unique=True)
    def __str__(self):
        return self.name