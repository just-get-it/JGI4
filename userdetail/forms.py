from django import forms
from .models import *
from b2b.models import company_Order

# currwork
# class pom_form(forms.ModelForm):
#     class Meta():
#         model = company_Order
#         fields =  ('poms_keys',)
#         widgets = {'poms_keys': forms.widgets.CheckboxSelectMultiple(),}
    

# class pom_form_new(forms.Form):


class FileForm(forms.Form):
    doc=forms.FileField(label="upload")

class CartonForm(forms.Form):
    capacity= forms.IntegerField(label="Enter carton capacity")


class StudentForm(forms.Form):  
    file      = forms.FileField(label="upload") # for creating file input 

class AcadForm(forms.ModelForm):
    
    class Meta:
        model = academic
        fields = '__all__'

class SocialForm(forms.ModelForm):
    
    class Meta:
        model = Social_Profile
        fields = ('age','gender','marital','hometown','hobbies','mobile_number','linkedin_profile','facebook_profile')

class ProfessionalForm(forms.ModelForm):
    
    class Meta:
        model = professional_pro
        fields = '__all__'

class MedForm(forms.ModelForm):
    
    class Meta:
        model = Medical_Profile
        fields = ('height','weight','blood_group','disability','medical_issues','diseases')

class SkillForm(forms.ModelForm):
    
    class Meta:
        model = add_skill
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    
    class Meta:
        model = add_project
        fields = '__all__'

class CertForm(forms.ModelForm):
    
    class Meta:
        model = add_certifications
        fields = '__all__'


class detailForm(forms.ModelForm):
    
    class Meta:
        model = detail
        fields = ("name", "contact", "coverimage", "image",)