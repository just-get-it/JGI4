from django.db import models
# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from userdetail.models import detail


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Report(models.Model):
    report_owner = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, related_name='owned_reports')
    report_submitter = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, related_name='submitted_reports')
    report_head = models.CharField(max_length=200, default = "No One")
    report_id = models.CharField(max_length=10 , default = 1)
    name = models.CharField(max_length=60)
    report = models.CharField(max_length=10)
    task = models.CharField(max_length=60)
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    no_of_hours = models.CharField(max_length=20)
    team_lead = models.CharField(max_length=30)
    today_progress = models.CharField(max_length=1000)
    todays_files_url = models.URLField(null=True)
    concern = models.CharField(max_length=1000)
    next_plan = models.CharField(max_length=1000)
    next_plan_files_url = models.URLField(null=True)
    report_rating = models.FloatField(null=True)


    def __str__(self):
        return self.name


class Fileupload(models.Model):
    fileid = models.CharField(max_length=10)
    filename = models.FileField(upload_to='documents/')
    owner = models.ForeignKey(Report,
                              on_delete=models.CASCADE,
                              db_constraint=False,
                              null=True,
                              blank=True)

    def __str__(self):
        return self.owner.name + " " + self.owner.report + " " + str(
            self.owner.date)


class Fileuploadnext(models.Model):
    fileid = models.CharField(max_length=10)
    filename = models.FileField(upload_to='next/')
    owner = models.ForeignKey(Report,
                              on_delete=models.CASCADE,
                              null=True,
                              db_constraint=False,
                              blank=True)

    def __str__(self):
        return self.owner.name + " " + self.owner.report + " " + str(
            self.owner.date)


@receiver(post_delete, sender=Fileupload)
def fileupload_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.filename.delete(False)


@receiver(post_delete, sender=Fileuploadnext)
def fileupload_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.filename.delete(False)
