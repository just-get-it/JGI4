from django.db import models

# Create your models here.






class Notification_Modes(models.Model):
	name=models.CharField(max_length=255,editable=False)
	turn_on=models.BooleanField(default=False)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Notifications Mode"




class Offset(models.Model):
	offset=models.IntegerField()


	def __str__(self):
		return str(self.offset)
		