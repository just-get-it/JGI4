from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.
class UserProfileInfo(models.Model):
    operator_name = models.CharField(max_length=50,default='')
    operator_id = models.CharField(primary_key=True,max_length=5,default='',unique=True)
    line_no=models.CharField(max_length=5,default='')
    address=models.CharField(max_length=100,default='')
    product_category=models.CharField(max_length=100,default='')
    product_sub_category=models.CharField(max_length=100,default='')
    operation=models.CharField(max_length=100,default='')
    operation_complexity=models.CharField(max_length=100,default='')
    no_of_operation=models.CharField(max_length=100,default='')
    skill_percentage=models.CharField(max_length=100,default='')
    grade=models.CharField(max_length=1,default='')
    password = models.CharField(max_length=10,default='')

    def __str__(self):
        return self.operator_name

class OperatorWindow(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    operation=models.CharField(max_length=100,default='')
    date=models.CharField(max_length=50,default='')
    ticket_no_start=models.IntegerField(default=0)
    ticket_no_end=models.IntegerField(default=0)
    total_pieces=models.IntegerField(default=0)
    wip=models.IntegerField(default=0)
    daily_target=models.IntegerField(default=0)
    daily_achieved=models.IntegerField(default=0)
    efficiency=models.IntegerField(default=0)
    performance=models.IntegerField(default=0)
    next_operation=models.IntegerField(default=0)
    rework_ticket_no=models.CharField(max_length=50,default='')
    repair_tkt_no=models.IntegerField(default=0)
    finishreturn_tkt_no=models.IntegerField(default=0)
    cutdefect_no=models.IntegerField(default=0)
    cutmiss_tkt_no=models.CharField(max_length=50,default='')
    rework_pieces=models.IntegerField(default=0)
    daily_cutting_miss=models.IntegerField(default=0)
    maintenance_start_time=models.CharField(max_length=50,default='')
    maintenance_stop_time=models.CharField(max_length=50,default='')
    maintenance_time=models.IntegerField(default=0)
    maintenance_name=models.CharField(max_length=50,default='')
    maintenance_value=models.CharField(max_length=50,default='')
    smed_start_time=models.CharField(max_length=50,default='')
    smed_stop_time=models.CharField(max_length=50,default='')
    smed_name=models.CharField(max_length=50,default='')
    smed_value=models.IntegerField(default=0)

    def __str__(self):
        return self.operator_name

class operator_skill_matrix(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    line_no=models.CharField(max_length=5,default='')
    product_category=models.CharField(max_length=100,default='')
    grade=models.CharField(max_length=1,default='')
    skill_percentage=models.CharField(max_length=3,default='')
    operation=models.CharField(max_length=100,default='')

    def __str__(self):
        return self.skill_percentage

class line1attendence(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    product = models.CharField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    attendence=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.operator_name

class line2attendence(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    product = models.CharField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    attendence=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.operator_name

class line3attendence(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    product = models.CharField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    attendence=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.operator_name

class line4attendence(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    product = models.CharField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    attendence=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.operator_name

class line5attendence(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    operator_name = models.CharField(max_length=50,default='')
    product = models.CharField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    attendence=models.CharField(max_length=50,default='')
    def __str__(self):
        return self.operator_name

class leaveCalender(models.Model):
    operator_id = models.CharField(max_length=5,default='')
    leave_start=models.DateField(max_length=50,default='')
    leave_end=models.DateField(max_length=50,default='')
    date= models.DateField(default=datetime.date.today)
    days=models.IntegerField(default=0)
    def __str__(self):
        return self.operator_id