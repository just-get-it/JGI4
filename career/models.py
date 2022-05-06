from django.db import models
from django.core.validators import RegexValidator
from django.core import validators
from django.core.validators import URLValidator
 
URL_VALIDATOR_MESSAGE = 'Not a valid URL.'
URL_VALIDATOR = RegexValidator(regex='/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/', message=URL_VALIDATOR_MESSAGE)
 
class OptionalSchemeURLValidator(URLValidator):
    def __call__(self, value):
        if '://' not in value:
            # Validate as if it were http://
            value = 'http://' + value
        super(OptionalSchemeURLValidator, self).__call__(value)
 
class Notification(models.Model):
    upcoming_form = models.CharField('Title', max_length=140)
    starts = models.DateTimeField('Starts')
    ends = models.DateTimeField('Ends')
    eligibility = models.CharField(max_length=150)
    reference_link = models.URLField(max_length=250,blank=False,null=False,validators=[OptionalSchemeURLValidator])
   
    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events" 
        ordering = ['-starts']
 
    def __str__(self):
        if self.starts.date() != self.ends.date():
            return u"%s, %s - %s" % (self.upcoming_form,
                            self.starts.strftime("%a %H:%M"),
                            self.ends.strftime("%a %H:%M"))
        else:
            return u"%s, %s - %s" % (self.upcoming_form,
                            self.starts.strftime("%H:%M"),
                            self.ends.strftime("%H:%M"))