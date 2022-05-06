from django.db import models

# Create your models here.

YESNO_CSV = (
	('Yes', 'Yes'),
	('No', 'No'),
	)
class Fabric(models.Model):
	id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
	Fabric_Required = models.FloatField()  # Comes from form 4

	def __str__(self):
		return str("Fabric_Required : " + str(self.Fabric_Required))

class RollOrder(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    Roll_No = models.IntegerField()
    Roll_Length = models.FloatField()
    Fabric_Width = models.FloatField()
    CSV = models.CharField(max_length=3, choices=YESNO_CSV)
    Shade_Grade = models.CharField(max_length=1)
    Shrinkage = models.FloatField()
    Lay_Length = models.FloatField()
    Roll_Lay_Height = models.IntegerField(null=True, blank=True, default=None)
    Utilised_Fabric = models.FloatField(null=True, blank=True, default=None)       #RESULT
    End_Bits = models.FloatField(null=True, blank=True, default=None)              #RESULT
    Lay_No = models.IntegerField(null=True, blank=True, default=None)            #RESULT
    Roll_Lay_Seq = models.IntegerField(null=True, blank=True, default=None)   #RESULT

    def __str__(self):
        return str("Roll Length : "+str(self.Roll_Length))



YESNO = (
	('yes', 'Yes'),
	('no', 'No'),
	)


TableType = (
	('pintable', 'Pin Table'),
	('airfloation', 'Air Floation'),
	('normal', 'Normal'), 
	)

ModeOfSpreading = (
	('manual', 'Manual'),
	('autospreader', 'Auto Spreader'),
	)


ModeOfCutting = (
	('manual', 'Manual'),
	('cnc', 'CNC'),
	)

class CutLoadPlan(models.Model):
	orderno = models.CharField(max_length=100)
	styleno = models.CharField(max_length=100)
	totalorderquantity = models.IntegerField()
	markerprep = models.CharField(max_length=100, choices = YESNO)
	tabletype =  models.CharField(max_length=100, choices = TableType)
	markerno = models.IntegerField()
	laylength = models.DecimalField(max_digits=6, decimal_places=2)
	noofplies = models.IntegerField()
	noofpieces = models.IntegerField()
	sprsmvmanual = models.IntegerField()
	sprsmvautospreader = models.IntegerField()
	crmanual = models.IntegerField()
	crautospreader =  models.IntegerField()
	cutsmvstraight = models.IntegerField()
	cutsmvband = models.IntegerField()
	cutsmvcnc = models.IntegerField()
	crstraightband = models.IntegerField()
	crcnc =  models.IntegerField()
	totmm = models.IntegerField()
	totma =  models.IntegerField()
	totam =  models.IntegerField()
	totaa =  models.IntegerField()
	matinhousefabric =  models.CharField(max_length=100, choices = YESNO)
	matinhousefusing = models.CharField(max_length=100, choices = YESNO)
	issuetable =  models.IntegerField()


	def __str__(self):
		return str("Order No." + self.orderno +" -> Marker No: "+ str(self.markerno))

	class Meta:
		unique_together = (("orderno", "markerno"),)	
	

class IssueDetails(models.Model):
	
	orderno = models.CharField(max_length=100)
	styleno = models.CharField(max_length=100)
	markerno = models.IntegerField()
	noofplies = models.IntegerField()
	issuetable =  models.IntegerField()
	availcapaforspreadandcut = models.IntegerField()
	cutpaneldelivery =  models.DateField()
	requiredcapacity = models.IntegerField()
	requiredday =  models.DecimalField(max_digits=6, decimal_places=5)
	requiredtime =  models.DecimalField(max_digits=6, decimal_places=5)
	leadtime =  models.IntegerField()
	issuedate =  models.DateField()

	def __str__(self):
		return str("Order No." + self.orderno +" -> Marker No: "+ str(self.markerno))

	class Meta:
		unique_together = (("orderno", "markerno"),)
	
class AvailCapacity(models.Model):
	tableno = models.IntegerField()
	tabletype =  models.CharField(max_length=100, choices = TableType)
	modeofspread = models.CharField(max_length=100, choices = ModeOfSpreading)
	modeofcut = models.CharField(max_length=100, choices = ModeOfCutting)
	availcapaforspreadandcut = models.IntegerField()
	capacityleft = models.IntegerField()
	datefield = models.DateField()

	def __str__(self):
		return str("Table No." + str(self.tableno) +" -> Table Type: "+ self.tabletype)

	class Meta:
		unique_together = (("tableno", "tabletype"),)

class TableCapacityLeft(models.Model):
	orderno = models.CharField(max_length=100)
	tableno = models.IntegerField()
	tabletype =  models.CharField(max_length=100, choices = TableType)
	availcapaforspreadandcut = models.IntegerField()
	capacityleft = models.IntegerField()
	datefield = models.DateField()

	def __str__(self):
		return str(self.tableno)

	# class Meta:
	# 	unique_together = (("orderno", "tabletype"),)
