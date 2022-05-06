from django.db import models
from userdetail.models import detail
import random
import os

# Create your models here.
# class project(models.Model):
# 	name=models.CharField(max_length=30)
# 	permission=models.CharField(default="guest",max_length=200)
# 	def __str__(self):
# 		return self.name
# class permit(models.Model):
# 	project_id= models.ForeignKey(project,on_delete=models.CASCADE)
# 	project_name=models.CharField(max_length=200,blank=True)
# 	assigned_to=models.CharField(max_length=300)
# 	assigned_by=models.CharField(max_length=300)

# class task(models.Model):
#     project_id= models.ForeignKey(project,on_delete=models.CASCADE)
#     task_name=models.CharField(max_length=200)

#     def __str__(self):
#     	return "{}".format(self.task_name)

# class sub_task(models.Model):
# 	task_name=models.ForeignKey(task,on_delete=models.CASCADE)
# 	sub_task_name=models.CharField(max_length=200)
# 	project_id=models.CharField(max_length=200,blank=True)

# 	def __str__(self):
# 		return self.sub_task_name
	
		 
# class activity(models.Model):
# 	activity_map=models.ForeignKey(sub_task,on_delete=models.CASCADE)
# 	activity_name=models.CharField(max_length=200)
# 	project_id=models.CharField(max_length=200,blank=True)
# 	status=models.CharField(max_length=200,default='Not_Completed')

# 	def __str__(self):
# 		return self.activity_name

# class act_feature(models.Model):
# 	feat=models.ForeignKey(activity,on_delete=models.CASCADE)
# 	assigned_to=models.CharField(max_length=200)
# 	check_list=models.CharField(max_length=200,null=True,blank=True)
# 	attachments=models.FileField(upload_to='files',null=True,blank=True)
# 	status=models.CharField(max_length=200,default='Not_Completed')
# 	comment=models.TextField(max_length=300,null=True,blank=True)
# 	project_id=models.CharField(max_length=200,blank=True)

# 	def __str__(self):
# 		return str(self.feat)

# class assigned_task(models.Model):
# 	activity_id=models.CharField(max_length=100)
# 	activity_name=models.CharField(max_length=200)
# 	project_name=models.CharField(max_length=200)
# 	assigned_to=models.CharField(max_length=300)
# 	assigned_by=models.CharField(max_length=300)
# 	status=models.CharField(max_length=200,default='Not_Completed')
# 	project_id=models.CharField(max_length=200,blank=True)

# 	def __str__(self):
# 		return self.assigned_to 

# class assigned_section(models.Model):
# 	task_id=models.IntegerField()
# 	project_id=models.IntegerField()
# 	assigned_to=models.CharField(max_length=200)
# 	assigned_by=models.CharField(max_length=200)
# 	project_name=models.CharField(max_length=200,blank=True)

# class assigned_subtask(models.Model):
# 	sub_task_id=models.IntegerField()
# 	task_id=models.IntegerField()
# 	project_id=models.IntegerField()
# 	assigned_to=models.CharField(max_length=200)
# 	assigned_by=models.CharField(max_length=200)
# 	project_name=models.CharField(max_length=200,blank=True)


### PLANNER APP INTEGRATION MODELS
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "local/channels/companylogo/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_file_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=name, ext=ext)
    return "local/channels/files/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class OrganizationDetails(models.Model):
	owner = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=200)
	desc = models.TextField()
	logo = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	def __str__(self):
		return self.name

class PersonalDetails(models.Model):
	owner = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	fname = models.CharField(max_length=200)
	lname = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	mobile = models.CharField(max_length=200)
	whatsapp_mobile = models.CharField(max_length=200)
	def __str__(self):
		return self.fname + self.lname

class JobProfiles(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name 

class InternshipType(models.Model):
	type = models.CharField(max_length=200)
	def __str__(self):
		return self.type

class Cities(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class StipendType(models.Model):
	type = models.CharField(max_length=200)
	def __str__(self):
		return self.type

class Perks(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Skills(models.Model):
	skill = models.CharField(max_length=200)
	def __str__(self):
		return self.skill



class Internship(models.Model):
	poster = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	pdetails = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, null=True)
	organization = models.ForeignKey(OrganizationDetails, on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=200)
	profile = models.ForeignKey(JobProfiles, on_delete=models.SET_NULL, null=True)
	type = models.ForeignKey(InternshipType, on_delete=models.SET_NULL, null=True)
	cities = models.ManyToManyField(Cities)
	no_of_openings = models.IntegerField()
	start_date_from = models.DateField(null=True)
	start_date_to = models.DateField(null=True)
	apply_by = models.DateField()
	duration = models.CharField(max_length=200)
	daily_responsiblilities = models.TextField(null=True)
	stipend_type = models.ForeignKey(StipendType, on_delete=models.SET_NULL, null=True)
	perks = models.ManyToManyField(Perks, blank=True)
	skills = models.ManyToManyField(Skills)
	stipend = models.CharField(max_length=200)
	detail_of_internship = models.TextField(null=True)
	q1 = models.CharField(max_length=400, null=True)
	q2 = models.CharField(max_length=400, null=True)
	q3 = models.CharField(max_length=400, null=True, blank=True)
	q4 = models.CharField(max_length=400, null=True, blank=True)
	is_filled = models.NullBooleanField(default=False)
	is_draft = models.NullBooleanField(default=None, null=True)
	def __str__(self):
		return self.title

class ApplicationForm(models.Model):
	applied_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True)
	applied_on = models.ForeignKey(Internship, on_delete=models.CASCADE, null=True)
	applied_date = models.DateTimeField(auto_now_add=True, blank=True)
	question1 = models.CharField(max_length=400, null=True, blank=True)
	answer1 = models.TextField(null=True, blank=True)
	question2 = models.CharField(max_length=400, null=True, blank=True)
	answer2 = models.TextField(null=True, blank=True)
	question3 = models.CharField(max_length=400, null=True, blank=True)
	answer3 = models.TextField(null=True, blank=True)
	question4 = models.CharField(max_length=400, null=True, blank=True)
	answer4 = models.TextField(null=True, blank=True)

#### TASK APP MODELS
class Project(models.Model):
	creator = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, related_name='created_projects')
	assigned_to = models.ManyToManyField(detail, related_name='assigned_projects')
	name = models.CharField(max_length=200)
	description = models.TextField(null=True)
	def __str__(self):
		return self.name

class Section(models.Model):
	index = models.IntegerField(null=True)
	creator = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, related_name='created_sections')
	assigned_to = models.ManyToManyField(detail, related_name='assigned_sections')
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True)
	def __str__(self):
		return self.name

class Task(models.Model):
	index = models.IntegerField(null=True)
	creator = models.ForeignKey(detail, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
	date_created = models.DateTimeField(auto_now_add=True)
	section = models.ForeignKey(Section, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	assigned_to = models.ManyToManyField(detail, related_name='assigned_tasks')
	description = models.TextField(null=True)
	due_date = models.DateTimeField(null=True)
	date_completed = models.DateTimeField(null=True)
	is_complete = models.BooleanField(default=False)
	def __str__(self):
		return self.name

class CheckListItem(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	is_checked = models.BooleanField(default=False)
	def __str__(self):
		return self.title

class Attachment(models.Model):
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	file = models.FileField(upload_to=upload_file_path)


class Comment(models.Model):
	commentor = models.ForeignKey(detail, on_delete=models.CASCADE, related_name='task_comments', null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	def __str__(self):
		return self.text



class Notification(models.Model):
	to = models.ForeignKey(detail, on_delete=models.CASCADE, related_name='all_notifications')
	type = models.CharField(max_length=200)
	text = models.CharField(max_length=200) 
	link_id = models.IntegerField(null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	viewed = models.BooleanField(default=False)
	task = models.BooleanField(default=False)
	project = models.BooleanField(default=False)
	section = models.BooleanField(default=False)
	report = models.BooleanField(default=False)
	internship = models.BooleanField(default=False)
	def __str__(self):
		return self.text

#student profile models

class Education_Qualification(models.Model):
	"""docstring for Education_Qualification"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name='education_details')
	college_name = models.CharField(max_length=500, null=True,blank=True)
	stream = models.CharField(max_length=200,null=True,blank=True)
	degree = models.CharField(max_length=500,null=True,blank=True)
	admission_year = models.DateField(null=True)
	passout_year = models.DateField(null=True)
	result = models.CharField(max_length=25)
	def __str__(self):
		return self.college_name

class Profile_Jobs(models.Model):
	"""docstring for Jobs"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="job_details")
	job_title = models.CharField(max_length=200)
	company_name = models.CharField(max_length=200)
	join_date = models.DateField(null=True, blank=True)
	leave_date = models.DateField(null=True, blank=True)
	location = models.CharField(max_length=200, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	# def __init__(self, arg):
	# 	super(Jobs, self).__init__()
	# 	self.arg = arg

class Profile_Internship(models.Model):
	"""docstring for Jobs"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="intern_details")
	internship_title = models.CharField(max_length=200)
	company_name = models.CharField(max_length=200)
	join_date = models.DateField(null=True, blank=True)
	leave_date = models.DateField(null=True, blank=True)
	location = models.CharField(max_length=200, null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	# def __init__(self, arg):
	# 	super(Jobs, self).__init__()
	# 	self.arg = arg

class Profile_Responsibility(models.Model):
	"""docstring for Profile_Responsibility"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="responsibility_details")
	responsibility = models.TextField(null=True,blank=True)
	# def __init__(self, arg):
	# 	super(ClassName, self).__init__()
	# 	self.arg = arg
		
class Profile_Training(models.Model):
	"""docstring for Profile_Training"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="training_details")
	program = models.CharField(max_length=200)
	organisation_name = models.CharField(max_length=200)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	location = models.CharField(max_length=200,null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	# def __init__(self, arg):
	# 	super(Jobs, self).__init__()
	# 	self.arg = arg		

class Profile_Project(models.Model):
	"""docstring for Profile_Project"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="project_details")
	project_name = models.CharField(max_length=200)
	start_date = models.DateField(null=True, blank=True)
	end_date = models.DateField(null=True, blank=True)
	project_link = models.CharField(max_length=200,null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	# def __init__(self, arg):
	# 	super(Jobs, self).__init__()
	# 	self.arg = arg	

class Profile_Skills(models.Model):
	"""docstring for Profile_Skills"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="skill_details")
	profile_skills = models.CharField(max_length=100, null=True,blank=True)
	proficiency_level = models.CharField(max_length=100, null=True,blank=True)
	# def __init__(self, arg):
	# 	super(Profile_Skills, self).__init__()
	# 	self.arg = arg

class Profile_WorkSamples(models.Model):
	"""docstring for Profile_WorkSamples"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="work_sample_details")
	blog_link = models.CharField(max_length=200,null=True,blank=True)
	github_link = models.CharField(max_length=200,null=True,blank=True)
	playstore_link = models.CharField(max_length=200,null=True,blank=True)
	behance_link = models.CharField(max_length=200,null=True,blank=True)
	other_link = models.CharField(max_length=200,null=True,blank=True)
	# def __init__(self, arg):
	# 	super(Profile_WorkSamples, self).__init__()
	# 	self.arg = arg

class Profile_AdditionDetails(models.Model):
	"""docstring for Profile_AdditionDetails"""
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="additional_details")
	additional_details = models.TextField(blank=True,null=True)
	# def __init__(self, arg):
	# 	super(Profile_AdditionDetails, self).__init__()
	# 	self.arg = arg

class Student_Profile(models.Model):
	created_by = models.ForeignKey(detail, on_delete=models.CASCADE, null=True, related_name="student_details")
	report_to = models.ManyToManyField(detail, related_name='reporters')
	username = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	mobile = models.BigIntegerField(null=True,blank=True)
	fname = models.CharField(max_length=200)
	mname = models.CharField(max_length=200,null=True,blank=True)
	lname = models.CharField(max_length=200)
	address = models.TextField(null=True,blank=True)
	profile = models.ManyToManyField(JobProfiles)
	cities = models.ManyToManyField(Cities, max_length=200,blank=True)
	country = models.CharField(max_length=200)
	postal = models.BigIntegerField(blank=True, null=True)
	image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
	info_update=models.BooleanField(default=False)
	profession = models.CharField(max_length=200, null=True, blank=True)
	# def __str__(self):
	# 	return self.title