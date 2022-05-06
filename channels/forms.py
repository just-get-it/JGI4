from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple

#### CHANNELS APP FORMS
class project_assign(forms.ModelForm):
    class Meta():
        model = Project
        fields = ('assigned_to',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].widget.attrs.update({'class': 'chosen-select'})

class task_assign(forms.ModelForm):
    class Meta():
        model = Task
        fields = ('assigned_to',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].widget.attrs.update({'class': 'chosen-select'})

class section_assign(forms.ModelForm):
    class Meta():
        model = Section
        fields = ('assigned_to',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].widget.attrs.update({'class': 'chosen-select'})

#### INTERNSHIP FORMS 
class internship_form(forms.ModelForm):
    class Meta():
        model = Internship
        fields = ('title', 'profile', 'type', 'cities', 'no_of_openings', 'start_date_from', 'start_date_to', 'apply_by', 'duration',
                  'daily_responsiblilities','stipend_type', 'stipend','perks','skills','detail_of_internship','q1','q2','q3','q4')
        widgets = {
            'profile': forms.RadioSelect(),
            'type': forms.RadioSelect(),
            'start_date_from' : forms.TextInput(attrs={'type': 'date'}),
            'start_date_to': forms.TextInput(attrs={'type': 'date'}),
            'apply_by': forms.TextInput(attrs={'type': 'date'}),
            'stipend_type': forms.RadioSelect(),
            'perks': forms.CheckboxSelectMultiple(),
        }
    



class personal_details_form(forms.ModelForm):
    class Meta():
        model = PersonalDetails
        fields = ('fname','lname','email','mobile','whatsapp_mobile',)
        

class organisation_details_form(forms.ModelForm):
    class Meta():
        model = OrganizationDetails
        fields = ('name', 'desc', 'logo',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].widget.attrs.update({'onchange': 'ImgDisplay(this);'})


class application_form(forms.ModelForm):
    class Meta():
        model = ApplicationForm
        fields = ('answer1','answer2','answer3','answer4')
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['question1'].widget.attrs.update({'disabled': 'true', 'maxlength':'500'})
    #     self.fields['question2'].widget.attrs.update({'disabled': 'true', 'maxlength':'500'})
    #     self.fields['question3'].widget.attrs.update({'disabled': 'true'})
    #     self.fields['question4'].widget.attrs.update({'disabled': 'true'})

# Student Profile Formw

class Student_User_Profile_Form(forms.ModelForm):
    """docstring for Studemt_User_Profile_Form"""
    class Meta():
        model = Student_Profile
        fields = ('report_to','username','email','mobile','fname','mname','lname','address','cities','country','postal','profile')
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['report_to'].widget.attrs.update({'class': 'chosen-select'})

    widgets = {
        'profile': forms.CheckboxSelectMultiple(),
    }

class Education_Form(forms.ModelForm):
    class Meta():
        model = Education_Qualification
        fields = ('college_name','stream','degree','admission_year','passout_year','result')
        widgets ={
            'admission_year': forms.DateInput(attrs={'class':'datepicker'}),
            'passout_year': forms.DateInput(attrs={'class':'datepicker'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['admission_year'].widget.attrs.update({'type': 'date', 'class':'test'})
    #     self.fields['passout_year'].widget.attrs.update({'type': 'date'})

class Job_Profile_Form(forms.ModelForm):
    class Meta():
        model = Profile_Jobs
        fields = ('job_title','company_name','join_date','leave_date','location','description')

        widgets = {
            'join_date': forms.DateInput(attrs={'class':'datepicker'}),
            'leave_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class Internship_Profile_Form(forms.ModelForm):
    class Meta():
        model = Profile_Internship
        fields = ('internship_title','company_name','join_date','leave_date','location','description')

        widgets = {
            'join_date': forms.DateInput(attrs={'class':'datepicker'}),
            'leave_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class Responsibility_Form(forms.ModelForm):
    class Meta():
        model = Profile_Responsibility
        fields = ('responsibility',)

class Profile_Training_Form(forms.ModelForm):
    class Meta():
        model = Profile_Training
        fields = ('program','organisation_name','start_date','end_date','location','description')

        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class Project_Form(forms.ModelForm):
    class Meta():
        model = Profile_Project
        fields = ('project_name','start_date','end_date','project_link','description')

        widgets = {
            'start_date': forms.DateInput(attrs={'class':'datepicker'}),
            'end_date': forms.DateInput(attrs={'class':'datepicker'}),
        }

class Profile_Skills_Form(forms.ModelForm):
    class Meta():
        model = Profile_Skills
        fields = ('profile_skills','proficiency_level')

class Work_Sample_Form(forms.ModelForm):
    class Meta():
        model = Profile_WorkSamples
        fields = ('blog_link','github_link','playstore_link','behance_link','other_link')

class Additional_Details_Form(forms.ModelForm):
    class Meta():
        model = Profile_AdditionDetails
        fields = ('additional_details',)