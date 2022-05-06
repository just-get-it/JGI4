from django.shortcuts import render,redirect, HttpResponseRedirect, reverse
from .models import *
from django.db.models import Max
from .forms import *
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import default_storage
from userdetail.models  import detail 
import json
from django.views.decorators.csrf import csrf_exempt
# import daily_report.models
from daily_report.models import Report
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.

# def add_project(request):
# 	return render(request,'channels/project_add.html')

# def p_add(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		project_name=request.POST['p_name']
# 		pobj=project(name=project_name,permission=email)
# 		pobj.save()
# 		return redirect('dash')
	
# 	else:
# 		project_name=request.POST['p_name']
# 		pobj=project(name=project_name,permission='guest')
# 		pobj.save()
# 		return redirect('dash')
			
# def dash(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		pobj=project.objects.filter(permission=email).all()
# 		tobj=permit.objects.filter(assigned_to=email).all()
# 		assigned_task_obj=assigned_task.objects.filter(assigned_to=email).all()
# 		assign_section_obj=assigned_section.objects.filter(assigned_to=email).all()
# 		assign_subtask_obj=assigned_subtask.objects.filter(assigned_to=email).all()
# 		if permit.objects.filter(assigned_to=email).exists() or assigned_task.objects.filter(assigned_to=email).exists() or assigned_section.objects.filter(assigned_to=email).exists() or assigned_subtask.objects.filter(assigned_to=email).exists():
# 			project_assign=True
# 		else:
# 			project_assign=False
# 	else:
# 		pobj=project.objects.filter(permission='guest').all()
# 		tobj=permit.objects.filter(assigned_to='guest').all()
# 		assigned_task_obj=assigned_task.objects.filter(assigned_to='guest').all()
# 		assign_section_obj=assign_section.objects.filter(assigned_to='guest').all()
# 		assign_subtask_obj=assigned_subtask.objects.filter(assigned_to='guest').all()
# 		if permit.objects.filter(assigned_to='guest').exists() or assigned_task.objects.filter(assigned_to='guest').exists() or assigned_section.objects.filter(assigned_to='guest').exists() or assigned_subtask.objects.filter(assigned_to='guest').exists():
# 			project_assign=True
# 		else:
# 			project_assign=False	
# 	return render(request,'channels/dash.html',{'pobj':pobj,'task':task,'tobj':tobj
# 		,'assigned_task_obj':assigned_task_obj,'project_assign':project_assign,
# 		'assign_section_obj':assign_section_obj,'assign_subtask_obj':assign_subtask_obj})



# def add_task(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			#p_id=project.objects.filter(name=project_name).values('id')[0]['id'] 
# 			task_name=request.POST["task_name"]
# 			tobj=task(project_id_id=project_id,task_name=task_name)
# 			tobj.save()
# 			'''return render(request,'channels/back_project.html',{'project_name':project_name,
# 				'project_id':project_id})'''
# 			dobj=detail.objects.values('email').all()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
# 		else:
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/taskadd.html',{'project_name':project_name,
# 				'project_id':project_id})
# 	else:
# 		if request.method=='POST':
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			task_name=request.POST["task_name"]
# 			tobj=task(project_id_id=project_id,task_name=task_name)
# 			tobj.save()
# 			dobj=detail.objects.values('email').all()
# 			email='guest'
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# 		else:
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/taskadd.html',{'project_name':project_name,
# 				'project_id':project_id})
	


	# def ajax_request(request):
# 	pass
# def task_page(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			project_id=request.POST['project']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# 		else:
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			dobj=detail.objects.values('email').all()
	
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
			
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# 	else:
# 		if request.method=='POST':
# 			project_id=request.POST['project']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			pobj=project.objects.filter(permission='guest').all()
# 			tobj=permit.objects.filter(assigned_to='guest').all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
# 		else:
			
			
# 			dobj=detail.objects.values('email').all()
	
# 			pobj=project.objects.filter(permission='guest').all()
# 			tobj=permit.objects.filter(assigned_to='guest').all()

# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
			
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})


# def add_subtask(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			print('THIS IS POST DATA: ', request.POST)
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			#p_id=project.objects.filter(name=project_name).values('id')[0]['id'] 
# 			#t_id=task.objects.filter(task_name=task_name,project_id_id=p_id).values('id')[0]['id'] 
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			sub_task_name=request.POST['subtask_name']
# 			sobj=sub_task(task_name_id=task_id,sub_task_name=sub_task_name,project_id=project_id)
# 			sobj.save()
# 			dobj=detail.objects.values('email').all()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/subtaskadd.html',{'task_id':task_id,'project_id':project_id})

# 	else:
# 		if request.method=='POST':
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			#p_id=project.objects.filter(name=project_name).values('id')[0]['id'] 
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			#t_id=task.objects.filter(task_name=task_name,project_id_id=p_id).values('id')[0]['id'] 
# 			sub_task_name=request.POST['subtask_name']
# 			sobj=sub_task(task_name_id=task_id,sub_task_name=sub_task_name,project_id=project_id)
# 			sobj.save()
# 			dobj=detail.objects.values('email').all()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})		
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/subtaskadd.html',{'task_id':task_id,'project_id':project_id})








# def task_page_assign(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			project_id=request.POST['project']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtaskassign.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# 		else:
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			dobj=detail.objects.values('email').all()
	
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
			
# 			return render(request,'channels/newtaskassign.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
# 	else:
# 		if request.method=='POST':
# 			project_id=request.POST['project']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			email='guest'
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtaskassign.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# 		else:
# 			email='guest'
# 			dobj=detail.objects.values('email').all()
	
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
			
# 			return render(request,'channels/newtaskassign.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})

# def add_activity(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			sub_task_id=request.GET.get('sub_task_id')
# 			project_id=request.GET.get('project_id')
# 			activity_name=request.POST['activity_name']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			'''task_name=request.GET.get('task')
# 			p_id=project.objects.filter(name=project_name).values('id')[0]['id'] 
# 			t_id=task.objects.filter(project_id_id=p_id,task_name=task_name).values('id')[0]['id']
# 			a_id=sub_task.objects.filter(sub_task_name=sub_task_name,task_name_id=t_id).values('id')[0]['id']'''
# 			aobj=activity(activity_map_id=sub_task_id,activity_name=activity_name,
# 				project_id=project_id)
# 			aobj.save()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			dobj=detail.objects.values('email').all()
			


# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,'dobj':dobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'act_obj':act_obj})






# 	else:
# 		if request.method=='POST':
# 			sub_task_id=request.GET.get('sub_task_id')
# 			project_id=request.GET.get('project_id')
# 			activity_name=request.POST['activity_name']
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			'''task_name=request.GET.get('task')
# 			p_id=project.objects.filter(name=project_name).values('id')[0]['id'] 
# 			t_id=task.objects.filter(project_id_id=p_id,task_name=task_name).values('id')[0]['id']
# 			a_id=sub_task.objects.filter(sub_task_name=sub_task_name,task_name_id=t_id).values('id')[0]['id']'''
# 			aobj=activity(activity_map_id=sub_task_id,activity_name=activity_name,
# 				project_id=project_id)
# 			aobj.save()
# 			email='guest'
# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			dobj=detail.objects.values('email').all()
			


# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,'dobj':dobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'act_obj':act_obj})


# def activity_features(request):
# 	if request.user.is_authenticated:
# 		activity_id=request.GET.get('activity_id')
# 		project_id=request.GET.get('project_id')
# 		check_item=request.POST['check_item']
# 		assigned_to=request.POST['employee']
# 		attachments=request.POST['file']
# 		status=request.POST['status']
# 		comment=request.POST['comment']
# 		x=0
# 		if assigned_task.objects.filter(activity_id=activity_id).exists():
# 				email_already=assigned_task.objects.filter(activity_id=activity_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This activity is already assign to this email")
# 							break
# 							x=1
# 		if x!=1:
# 			aobj=act_feature(feat_id=activity_id,check_list=check_item,assigned_to=assigned_to,comment=comment,status=status,attachments=attachments,project_id=project_id)
# 			aobj.save()
# 			a=activity.objects.filter(id=activity_id)
# 			for a in a:
# 				a.status=status
# 				a.save()
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			activity_name=activity.objects.filter(id=activity_id).values('activity_name')[0]['activity_name']
# 			st=act_feature.objects.filter(feat_id=activity_id).values('status').last()['status']
			
# 			bobj=assigned_task(activity_id=activity_id,activity_name=activity_name,
# 				project_name=project_name,project_id=project_id,assigned_to=assigned_to,
# 				assigned_by=email,status=st)
# 			bobj.save()

# 			dobj=detail.objects.values('email').all()

# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

			

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()
# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 		'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 	,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
		

# 	else:
# 		activity_id=request.GET.get('activity_id')
# 		project_id=request.GET.get('project_id')
# 		check_item=request.POST['check_item']
# 		assigned_to=request.POST['employee']
# 		attachments=request.POST['file']
# 		status=request.POST['status']
# 		comment=request.POST['comment']
# 		x=0
# 		if assigned_task.objects.filter(activity_id=activity_id).exists():
# 				email_already=assigned_task.objects.filter(activity_id=activity_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This activity is already assign to this email")
# 							break
# 							x=1
# 		if x!=1:
# 			aobj=act_feature(feat_id=activity_id,check_list=check_item,assigned_to=assigned_to,comment=comment,status=status,attachments=attachments,project_id=project_id)
# 			aobj.save()
# 			a=activity.objects.filter(id=activity_id)
# 			for a in a:
# 				a.status=status
# 				a.save()

# 			email='guest'
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			dobj=detail.objects.values('email').all()
# 			activity_name=activity.objects.filter(id=activity_id).values('activity_name')[0]['activity_name']
# 			st=act_feature.objects.filter(feat_id=activity_id).values('status').last()['status']
			
# 			bobj=assigned_task(activity_id=activity_id,activity_name=activity_name,
# 				project_name=project_name,project_id=project_id,assigned_to=assigned_to,
# 				assigned_by=email,status=st)
# 			bobj.save()

# 			dobj=detail.objects.values('email').all()

# 			pobj=project.objects.filter(permission=email).all()
# 			tobj=permit.objects.filter(assigned_to=email).all()

			

# 			task_obj=task.objects.filter(project_id=project_id).all().order_by('id')

# 			sub_obj=sub_task.objects.filter(project_id=project_id).all()
# 			activity_obj=activity.objects.filter(project_id=project_id).all()
# 			act_obj=act_feature.objects.filter(project_id=project_id).all()

# 			return render(request,'channels/newtask.html',{'pobj':pobj,'tobj':tobj,
# 				'task_obj':task_obj,'sub_obj':sub_obj,'project_id':project_id
# 				,'project_name':project_name,'activity_obj':activity_obj,'dobj':dobj,'act_obj':act_obj})
			
	
# def assign_project(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			assigned_email=request.POST['email']
# 			x=0
# 			if permit.objects.filter(project_id=project_id).exists():
# 				email_already=permit.objects.filter(project_id=project_id).values('assigned_to').all()
# 				if assigned_email!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_email:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1

# 			if x!=1:				
# 				assigned_by=project.objects.filter(id=project_id).values('permission')[0]['permission']
# 				aobj=permit(project_id_id=project_id,assigned_to=assigned_email,assigned_by=assigned_by,
# 					project_name=project_name)
# 				aobj.save()
# 				return redirect('dash')
# 	else:
# 		if request.method=='POST':
# 			project_name=request.GET.get('project')
# 			project_id=request.GET.get('project_id')
# 			assigned_email=request.POST['email']
# 			x=0
# 			if permit.objects.filter(project_id=project_id).exists():
# 				email_already=permit.objects.filter(project_id=project_id).values('assigned_to').all()
# 				if assigned_email!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_email:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1

# 			if x!=1:
# 				assigned_by=project.objects.filter(id=project_id).values('permission')[0]['permission']
# 				aobj=permit(project_id_id=project_id,assigned_to=assigned_email,assigned_by=assigned_by,
# 					project_name=project_name)
# 				aobj.save()
# 				return redirect('dash')

# def show_specific_task(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		assign_id=request.GET.get('id')
# 		tobj=permit.objects.filter(assigned_to=email).all()
# 		assigned_task_obj=assigned_task.objects.filter(assigned_to=email).all()
# 		act_feat=assigned_task.objects.filter(id=assign_id).all()
# 		act_feat_id=assigned_task.objects.filter(id=assign_id).values('activity_id')[0]['activity_id']
# 		act_obj=act_feature.objects.filter(feat_id=act_feat_id).all()
# 		return render(request,'channels/specific_task.html',
# 			{'project_name':project_name,'project_id':project_id,
# 			'act_obj':act_obj,'act_feat':act_feat,
# 			'assigned_task_obj':assigned_task_obj,'tobj':tobj})
# 	else:
# 		email='guest'
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		assign_id=request.GET.get('id')
# 		tobj=permit.objects.filter(assigned_to=email).all()
# 		assigned_task_obj=assigned_task.objects.filter(assigned_to=email).all()
# 		act_feat=assigned_task.objects.filter(id=assign_id).all()
# 		act_feat_id=assigned_task.objects.filter(id=assign_id).values('activity_id')[0]['activity_id']
# 		act_obj=act_feature.objects.filter(feat_id=act_feat_id).all()
# 		return render(request,'channels/specific_task.html',
# 			{'project_name':project_name,'project_id':project_id,
# 			'act_obj':act_obj,'act_feat':act_feat,
# 			'assigned_task_obj':assigned_task_obj,'tobj':tobj})
	
		
# def delete_activity(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		activity_id=request.GET.get('activity_id')
# 		activity.objects.filter(id=activity_id).all().delete()
# 		return redirect('dash')
# 	else:
# 		email='guest'
# 		activity_id=request.GET.get('activity_id')
# 		activity.objects.filter(id=activity_id).all().delete()
# 		return redirect('dash')
	
			
# def delete_project(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		project_id=request.GET.get('project_id')
# 		project.objects.filter(id=project_id).all().delete()
# 		return redirect('dash')
# 	else:
# 		email='guest'
# 		project_id=request.GET.get('project_id')
# 		project.objects.filter(id=project_id).all().delete()
# 		return redirect('dash')
# def delete_task(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		task_id=request.GET.get('task_id')
# 		task.objects.filter(id=task_id).all().delete()
# 		return redirect('dash')
# 	else:
# 		email='guest'
# 		task_id=request.GET.get('task_id')
# 		task.objects.filter(id=task_id).all().delete()
# 		return redirect('dash')
# def delete_subtask(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		sub_task_id=request.GET.get('sub_task_id')
# 		sub_task.objects.filter(id=sub_task_id).all().delete()
# 		return redirect('dash')
# 	else:
# 		email='guest'
# 		sub_task_id=request.GET.get('sub_task_id')
# 		sub_task.objects.filter(id=sub_task_id).all().delete()
# 		return redirect('dash')
# def edit_task(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			task_id=request.GET.get('task_id')
# 			task_name=request.POST['task_name']
# 			tk=task.objects.filter(id=task_id)
# 			for t in tk:
# 				t.task_name=task_name
# 				t.save()
# 			return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			return render(request,'channels/task_edit.html',{'task_id':task_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			task_id=request.GET.get('task_id')
# 			task_name=request.POST['task_name']
# 			tk=task.objects.filter(id=task_id)
# 			for t in tk:
# 				t.task_name=task_name
# 				t.save()
# 			return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			return render(request,'channels/task_edit.html',{'task_id':task_id})
# def edit_subtask(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			sub_task_id=request.GET.get('sub_task_id')
# 			sub_task_name=request.POST['sub_task_name']
# 			sub=sub_task.objects.filter(id=sub_task_id)
# 			for t in sub:
# 				t.sub_task_name=sub_task_name
# 				t.save()
# 			return redirect('dash')
# 		else:
# 			sub_task_id=request.GET.get('sub_task_id')
# 			return render(request,'channels/subtaskedit.html',{'sub_task_id':sub_task_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			sub_task_id=request.GET.get('sub_task_id')
# 			sub_task_name=request.POST['sub_task_name']
# 			sub=sub_task.objects.filter(id=sub_task_id)
# 			for t in sub:
# 				t.sub_task_name=sub_task_name
# 				t.save()
# 			return redirect('dash')
# 		else:
# 			sub_task_id=request.GET.get('sub_task_id')
# 			return render(request,'channels/subtaskedit.html',{'sub_task_id':sub_task_id})
# def edit_project(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			project_id=request.GET.get('project_id')
# 			project_name=request.POST['project_name']

# 			pro=project.objects.filter(id=project_id)
# 			for p in pro:
# 				p.name=project_name
# 				p.save()
# 			return redirect('dash')
# 		else:
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/project_edit.html',{'project_id':project_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			project_id=request.GET.get('project_id')
# 			project_name=request.POST['project_name']

# 			pro=project.objects.filter(id=project_id)
# 			for p in pro:
# 				p.name=project_name
# 				p.save()
# 			return redirect('dash')
# 		else:
# 			project_id=request.GET.get('project_id')
# 			return render(request,'channels/project_edit.html',{'project_id':project_id})
# def edit_activity(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			activity_id=request.GET.get('activity_id')
# 			activity_name=request.POST['activity_name']
# 			act=activity.objects.filter(id=activity_id)
# 			for a in act:
# 				a.activity_name=activity_name
# 				a.save()
# 			return redirect('dash')
# 		else:
# 			activity_id=request.GET.get('activity_id')
# 			return render(request,'channels/activity_edit.html',{'activity_id':activity_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			activity_id=request.GET.get('activity_id')
# 			activity_name=request.POST['activity_name']
# 			act=activity.objects.filter(id=activity_id)
# 			for a in act:
# 				a.activity_name=activity_name
# 				a.save()
# 			return redirect('dash')
# 		else:
# 			activity_id=request.GET.get('activity_id')
# 			return render(request,'channels/activity_edit.html',{'activity_id':activity_id})
# def activity_feature_assign(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			project_id=request.GET.get('project_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			assign_id=request.GET.get('id')
# 			status=request.POST['status']


# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			assigned_task_obj=assigned_task.objects.filter(assigned_to=email).all()
# 			act_feat=assigned_task.objects.filter(id=assign_id).all()
# 			for a in act_feat:
# 				a.status=status
# 				a.save()
# 			act_feat_id=assigned_task.objects.filter(id=assign_id).values('activity_id')[0]['activity_id']
# 			act_obj=act_feature.objects.filter(feat_id=act_feat_id).all()
# 			return render(request,'channels/specific_task.html',
# 				{'project_name':project_name,'project_id':project_id,
# 				'act_obj':act_obj,'act_feat':act_feat,
# 				'assigned_task_obj':assigned_task_obj,'tobj':tobj})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			project_id=request.GET.get('project_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			assign_id=request.GET.get('id')
# 			status=request.POST['status']


# 			tobj=permit.objects.filter(assigned_to=email).all()
# 			assigned_task_obj=assigned_task.objects.filter(assigned_to=email).all()
# 			act_feat=assigned_task.objects.filter(id=assign_id).all()
# 			for a in act_feat:
# 				a.status=status
# 				a.save()
# 			act_feat_id=assigned_task.objects.filter(id=assign_id).values('activity_id')[0]['activity_id']
# 			act_obj=act_feature.objects.filter(feat_id=act_feat_id).all()
# 			return render(request,'channels/specific_task.html',
# 				{'project_name':project_name,'project_id':project_id,
# 				'act_obj':act_obj,'act_feat':act_feat,
# 				'assigned_task_obj':assigned_task_obj,'tobj':tobj})


# def assign_section(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			assigned_to=request.POST['assigned_to']
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			x=0
# 			if assigned_section.objects.filter(task_id=task_id).exists():
# 				email_already=assigned_section.objects.filter(task_id=task_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1
# 			if x!=1:
		
# 				a=assigned_section(task_id=task_id,assigned_to=assigned_to,assigned_by=email,
# 				project_id=project_id,project_name=project_name)
# 				a.save()
# 				return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			dobj=detail.objects.values('email').all()
# 			return render(request,'channels/assigned_sec.html',{'task_id':task_id,'dobj':dobj,
# 				'project_id':project_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			assigned_to=request.POST['assigned_to']
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			x=0
# 			if assigned_section.objects.filter(task_id=task_id).exists():
# 				email_already=assigned_section.objects.filter(task_id=task_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1
# 			if x!=1:
		
# 				a=assigned_section(task_id=task_id,assigned_to=assigned_to,assigned_by=email,
# 				project_id=project_id,project_name=project_name)
# 				a.save()
# 				return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			dobj=detail.objects.values('email').all()
# 			return render(request,'channels/assigned_sec.html',{'task_id':task_id,'dobj':dobj,
# 				'project_id':project_id})

# def show_specific_section(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		task_id=request.GET.get('task_id')
# 		task_name=task.objects.filter(id=task_id).values('task_name')[0]['task_name']
# 		sub_task_obj=sub_task.objects.filter(task_name_id=task_id).all()
# 		activity_obj=activity.objects.filter(project_id=project_id).all()
# 		act_obj=act_feature.objects.filter(project_id=project_id).all()
# 		return render(request,'channels/newsectionassign.html',{'project_name':project_name,
# 			'project_id':project_id,'task_name':task_name,'sub_task_obj':sub_task_obj,
# 			'activity_obj':activity_obj,'act_obj':act_obj,'task_id':task_id})
# 	else:
# 		email='guest'
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		task_id=request.GET.get('task_id')
# 		task_name=task.objects.filter(id=task_id).values('task_name')[0]['task_name']
# 		sub_task_obj=sub_task.objects.filter(task_name_id=task_id).all()
# 		activity_obj=activity.objects.filter(project_id=project_id).all()
# 		act_obj=act_feature.objects.filter(project_id=project_id).all()
# 		return render(request,'channels/newsectionassign.html',{'project_name':project_name,
# 			'project_id':project_id,'task_name':task_name,'sub_task_obj':sub_task_obj,
# 			'activity_obj':activity_obj,'act_obj':act_obj,'task_id':task_id})
		
# def assign_subtask(request):
# 	if request.user.is_authenticated:
# 		if request.method=='POST':
# 			email=detail.objects.filter(email=request.user.email)[0]
# 			assigned_to=request.POST['assigned_to']
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			sub_task_id=request.GET.get('sub_task_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			x=0
# 			if assigned_subtask.objects.filter(sub_task_id=sub_task_id).exists():
# 				email_already=assigned_subtask.objects.filter(sub_task_id=sub_task_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1
# 			if x!=1:	
# 				a=assigned_subtask(task_id=task_id,assigned_to=assigned_to,assigned_by=email,
# 				project_id=project_id,project_name=project_name,sub_task_id=sub_task_id)
# 				a.save()
# 				return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			sub_task_id=request.GET.get('sub_task_id')
# 			dobj=detail.objects.values('email').all()
# 			return render(request,'channels/assigned_subtask.html',{'task_id':task_id,'dobj':dobj,
# 				'project_id':project_id,'sub_task_id':sub_task_id})
# 	else:
# 		if request.method=='POST':
# 			email='guest'
# 			assigned_to=request.POST['assigned_to']
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			sub_task_id=request.GET.get('sub_task_id')
# 			project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 			x=0
# 			if assigned_subtask.objects.filter(sub_task_id=sub_task_id).exists():
# 				email_already=assigned_subtask.objects.filter(sub_task_id=sub_task_id).values('assigned_to').all()
# 				if assigned_to!='none':
# 					for i in email_already:
# 						if i['assigned_to']==assigned_to:
# 							return HttpResponse("This project is already assign to this email")
# 							break
# 							x=1
# 			if x!=1:	
# 				a=assigned_subtask(task_id=task_id,assigned_to=assigned_to,assigned_by=email,
# 				project_id=project_id,project_name=project_name,sub_task_id=sub_task_id)
# 				a.save()
# 				return redirect('dash')
# 		else:
# 			task_id=request.GET.get('task_id')
# 			project_id=request.GET.get('project_id')
# 			sub_task_id=request.GET.get('sub_task_id')
# 			dobj=detail.objects.values('email').all()
# 			return render(request,'channels/assigned_subtask.html',{'task_id':task_id,'dobj':dobj,
# 				'project_id':project_id,'sub_task_id':sub_task_id})

# def show_specific_subtask(request):
# 	if request.user.is_authenticated:
# 		email=detail.objects.filter(email=request.user.email)[0]
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		task_id=request.GET.get('task_id')
# 		sub_task_id=request.GET.get('sub_task_id')
# 		sub_task_name=sub_task.objects.filter(id=sub_task_id).values('sub_task_name')[0]['sub_task_name']
# 		task_name=task.objects.filter(id=task_id).values('task_name')[0]['task_name']
# 		sub_task_obj=sub_task.objects.filter(task_name_id=task_id).all()
# 		activity_obj=activity.objects.filter(project_id=project_id,activity_map_id=sub_task_id).all()
# 		act_obj=act_feature.objects.filter(project_id=project_id).all()
# 		return render(request,'channels/newsubtaskassign.html',{'project_name':project_name,
# 			'project_id':project_id,'task_name':task_name,'sub_task_obj':sub_task_obj,
# 			'activity_obj':activity_obj,'act_obj':act_obj,'task_id':task_id,'sub_task_id':sub_task_id,
# 			'sub_task_name':sub_task_name})
# 	else:
# 		email='guest'
# 		project_id=request.GET.get('project_id')
# 		project_name=project.objects.filter(id=project_id).values('name')[0]['name']
# 		task_id=request.GET.get('task_id')
# 		sub_task_id=request.GET.get('sub_task_id')
# 		sub_task_name=sub_task.objects.filter(id=sub_task_id).values('sub_task_name')[0]['sub_task_name']
# 		task_name=task.objects.filter(id=task_id).values('task_name')[0]['task_name']
# 		sub_task_obj=sub_task.objects.filter(task_name_id=task_id).all()
# 		activity_obj=activity.objects.filter(project_id=project_id,activity_map_id=sub_task_id).all()
# 		act_obj=act_feature.objects.filter(project_id=project_id).all()
# 		return render(request,'channels/newsubtaskassign.html',{'project_name':project_name,
# 			'project_id':project_id,'task_name':task_name,'sub_task_obj':sub_task_obj,
# 			'activity_obj':activity_obj,'act_obj':act_obj,'task_id':task_id,'sub_task_id':sub_task_id,
# 			'sub_task_name':sub_task_name})



#### PLANNER APP VIEWS #####
def planner_index(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			# LAST WEEKS RATINGS AVG
			today = datetime.today()
			prev_monday = today - timedelta(days=today.weekday())
			ratings = [0,0,0,0,0,0,0]
			no_of_ratings = [0,0,0,0,0,0,0]
			reports = Report.objects.filter(report_owner=details, date__gte=prev_monday, report_rating__isnull=False)
			for report in reports:
				print( f'Date: {report.date} Day: {report.date.weekday()}')
				if report.date.weekday() == 0:
					ratings[0] += report.report_rating
					no_of_ratings[0] += 1
				elif report.date.weekday() == 1:
					ratings[1] += report.report_rating
					no_of_ratings[1] += 1
				elif report.date.weekday() == 2:
					ratings[2] += report.report_rating
					no_of_ratings[2] += 1
				elif report.date.weekday() == 3:
					ratings[3] += report.report_rating
					no_of_ratings[3] += 1
				elif report.date.weekday() == 4:
					ratings[4] += report.report_rating
					no_of_ratings[4] += 1
				elif report.date.weekday() == 5:
					ratings[5] += report.report_rating
					no_of_ratings[5] += 1
				elif report.date.weekday() == 6:
					ratings[6] += report.report_rating
					no_of_ratings[6] += 1
			daily_percent_increase = 0
			for idx,rating in enumerate(ratings):
				print(f'idx: {idx} rating: {rating} no_of_rating[idx]: {no_of_ratings[idx]}')
				if no_of_ratings[idx]:
					print(f'..Calc Average of {rating}')
					rating = rating/no_of_ratings[idx]
					ratings[idx] = round(rating, 1)
					if ratings[idx-1]:
						print(f'calculating % {ratings[idx-1]} and {ratings[idx]}')
						daily_percent_increase = ((ratings[idx] - ratings[idx-1])/ratings[idx])*100
						daily_percent_increase = round(daily_percent_increase, 2)
						print(f'percent: {daily_percent_increase}%')
					print(f'Avg: {rating}')
			# LAST WEEKS COMPLETED TASKS
			today = datetime.today()
			prev_monday = today - timedelta(days=today.weekday())
			no_of_tasks = [0,0,0,0,0,0,0]
			tasks = Task.objects.filter(date_completed__gte=prev_monday)
			for task in tasks:
				if task.date_completed.weekday() == 0:
					no_of_tasks[0] += 1
				elif task.date_completed.weekday() == 1:
					no_of_tasks[1] += 1
				elif task.date_completed.weekday() == 2:
					no_of_tasks[2] += 1
				elif task.date_completed.weekday() == 3:
					no_of_tasks[3] += 1
				elif task.date_completed.weekday() == 4:
					no_of_tasks[4] += 1
				elif task.date_completed.weekday() == 5:
					no_of_tasks[5] += 1
				elif task.date_completed.weekday() == 6:
					no_of_tasks[6] += 1
			all_reports = len(details.owned_reports.all())
			rated_reports = len(details.owned_reports.filter(report_rating__isnull = False))
			ratingdt = [rated_reports, all_reports]
			total_internships = len(Internship.objects.all())
			total_applications = len(ApplicationForm.objects.all())
			total_incomplete_tasks = len(details.assigned_tasks.filter(is_complete=False))
			unassigned_tasks = len(details.created_tasks.filter(assigned_to = None))
			unassigned_projects = len(details.created_projects.filter(assigned_to = None))
			unassigned_sections = len(details.created_sections.filter(assigned_to = None))
			emp_data = []
			tasks = details.created_tasks.filter(is_complete = True, assigned_to__isnull=False)
			temp_data = {}
			for task in tasks:
				assigned = []
				for asgn in task.assigned_to.all():
					assigned.append(asgn)
				for person in assigned:
					if temp_data.get(person.name):
						temp_data[person.name] += 1
					else:
						temp_data[person.name] = 1
			for key,value in temp_data.items():
				emp_data.append([key,value])
			unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
			all_notifications = list(details.all_notifications.all().order_by('-date'))
			unseen_count = len(unseen_notifications)
			if len(all_notifications) > 5:
				while len(unseen_notifications) < 5:
					unseen_notifications.append(all_notifications.pop(0))
			else:
				unseen_notifications + all_notifications
			all_notifications = details.all_notifications.all()[:10]
			return render(request,"channels/planner/student_index.html",{'week_ratings': ratings,'all_notifications':all_notifications , 'week_today_percent':daily_percent_increase, 'no_of_tasks_completed':no_of_tasks, 'ratingdt': ratingdt, 'total_internships':total_internships,'total_applications':total_applications, 'incomplete_tasks':total_incomplete_tasks, 'unassigned_tasks': unassigned_tasks, 'unassigned_projects': unassigned_projects, 'unassigned_sections': unassigned_sections, 'emp_data':emp_data, 'notify':unseen_notifications, 'unseen_count': unseen_count})
		else:
			today = datetime.today()
			prev_monday = today - timedelta(days=today.weekday())
			ratings = [0,0,0,0,0,0,0]
			reports = Report.objects.filter(report_submitter=details, date__gte=prev_monday, report_rating__isnull=False)
			print(f'REPORTS: {reports}')
			for report in reports:
				if report.date.weekday() == 0:
					ratings[0] = report.report_rating
				elif report.date.weekday() == 1:
					ratings[1] = report.report_rating
				elif report.date.weekday() == 2:
					ratings[2] = report.report_rating
				elif report.date.weekday() == 3:
					ratings[3] = report.report_rating
				elif report.date.weekday() == 4:
					ratings[4] = report.report_rating
				elif report.date.weekday() == 5:
					ratings[5] = report.report_rating
				elif report.date.weekday() == 6:
					ratings[6] = report.report_rating
			print(f'RATINGS: {ratings}')
			daily_percent_increase = 0
			for idx,rating in enumerate(ratings):
				if ratings[idx-1] and ratings[idx]:
					print(f'calculating % {ratings[idx-1]} and {ratings[idx]}')
					daily_percent_increase = ((ratings[idx] - ratings[idx-1])/ratings[idx])*100
					daily_percent_increase = round(daily_percent_increase, 2)
					print(f'percent: {daily_percent_increase}%')
			# LAST WEEKS COMPLETED TASKS
			today = datetime.today()
			prev_monday = today - timedelta(days=today.weekday())
			no_of_tasks = [0,0,0,0,0,0,0]
			tasks = Task.objects.filter(assigned_to=details, date_completed__gte=prev_monday)
			for task in tasks:
				if task.date_completed.weekday() == 0:
					no_of_tasks[0] += 1
				elif task.date_completed.weekday() == 1:
					no_of_tasks[1] += 1
				elif task.date_completed.weekday() == 2:
					no_of_tasks[2] += 1
				elif task.date_completed.weekday() == 3:
					no_of_tasks[3] += 1
				elif task.date_completed.weekday() == 4:
					no_of_tasks[4] += 1
				elif task.date_completed.weekday() == 5:
					no_of_tasks[5] += 1
				elif task.date_completed.weekday() == 6:
					no_of_tasks[6] += 1
			all_reports = len(details.submitted_reports.all())
			rated_reports = len(details.submitted_reports.filter(report_rating__isnull = False))
			ratingdt = [rated_reports, all_reports]
			total_internships = len(Internship.objects.all())
			total_applications = len(ApplicationForm.objects.all())
			total_incomplete_tasks = len(details.assigned_tasks.filter(is_complete=False))
			unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
			all_notifications = list(details.all_notifications.all().order_by('-date'))
			unseen_count = len(unseen_notifications)
			if len(all_notifications) > 5:
				while len(unseen_notifications) < 5:
					unseen_notifications.append(all_notifications.pop(0))
			else:
				unseen_notifications + all_notifications
			return render(request,"channels/planner/student_index.html",{'week_ratings': ratings, 'week_today_percent':daily_percent_increase, 'no_of_tasks_completed':no_of_tasks, 'ratingdt': ratingdt, 'total_internships':total_internships,'total_applications':total_applications, 'incomplete_tasks':total_incomplete_tasks, 'notify':unseen_notifications, 'unseen_count': unseen_count})

def notifications(request):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		all_notifications = details.all_notifications.all().order_by('-date')
		return render(request, "channels/planner/notifications.html", {'notify': all_notifications})
	else:
		return redirect('login_page')

def internships(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			return redirect('staff_dashboard')
	active_internships = Internship.objects.filter(is_filled=False)
	unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
	all_notifications = list(details.all_notifications.all().order_by('-date'))
	unseen_count = len(unseen_notifications)
	if len(all_notifications) > 5:
		while len(unseen_notifications) < 5:
			unseen_notifications.append(all_notifications.pop(0))
	else:
		unseen_notifications + all_notifications
	return render(request, "channels/planner/internships.html",{'all_internships':active_internships, 'notify':unseen_notifications, 'unseen_count': unseen_count})

def singleInternship(request, internship_id):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if details.staff:
			# return redirect('edit_internship', { 'internship_id':internship_id })
			return HttpResponseRedirect(reverse("edit_internship", args=[internship_id]))
	intrn = Internship.objects.get(pk=internship_id)
	temp = ApplicationForm.objects.filter(applied_by=details, applied_on=intrn)
	if temp:
		applied = True
	else:
		applied = False
	unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
	all_notifications = list(details.all_notifications.all().order_by('-date'))
	unseen_count = len(unseen_notifications)
	if len(all_notifications) > 5:
		while len(unseen_notifications) < 5:
			unseen_notifications.append(all_notifications.pop(0))
	else:
		unseen_notifications + all_notifications
	return render(request, "channels/planner/single_internship.html", {'internship':intrn, 'applied': applied, 'notify':unseen_notifications, 'unseen_count': unseen_count})

def staff_dashboard(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if not details.staff:
			return redirect('internships')
		posted_internships = Internship.objects.filter(poster=details)
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		return render(request, "channels/planner/staff_dashboard.html", {'posted_internships': posted_internships, 'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		redirect('student_login')

def editInternship(request, internship_id):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if not details.staff:
			return redirect('internships')
		intrn = Internship.objects.get(pk=internship_id)
		if request.method == "POST":
			editedForm = internship_form(request.POST, instance=intrn)
			if editedForm.is_valid():
				editedForm.save()
			return redirect('staff_dashboard')
		editForm = internship_form(instance=intrn)
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		return render(request, "channels/planner/edit_internship.html", {'internship_form': editForm, 'notify':unseen_notifications, 'unseen_count': unseen_count})


def add_internship(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if not details.staff:
			return redirect('internships')
		pdetails = PersonalDetails.objects.filter(owner=details).first()
		odetails = OrganizationDetails.objects.filter(owner=details).first()
		if not pdetails or not odetails:
			return redirect('add_details')
		if request.method == "POST":
			print("THIS IS POST: ", request.POST)
			addNewForm = internship_form(request.POST)
			if addNewForm.is_valid():
				intrn = addNewForm.save()
				intrn.poster = details
				intrn.organization = odetails
				intrn.pdetails = pdetails
				intrn.save()
			else:
				print(addNewForm.errors)
			return redirect('staff_dashboard')
		addForm = internship_form()
		return render(request, "channels/planner/edit_internship.html", {'internship_form': addForm})
		
def add_details(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		if not details.staff:
			return redirect('internships')
		# Getting Old Details and Generating Form
		personal_details = PersonalDetails.objects.filter(owner=details).first()
		organisation_details = OrganizationDetails.objects.filter(owner=details).first()
		if personal_details:
			personal_form = personal_details_form(instance=personal_details)
		else:
			personal_form = personal_details_form()
		if organisation_details:
			organisation_form = organisation_details_form(instance=organisation_details)
		else:
			organisation_form = organisation_details_form()
		if request.method == "POST":
			# PERSONAL FORM HANDLING EDIT / ADD
			if personal_details:
				edited_personal_form = personal_details_form(request.POST, instance=personal_details)
			else:
				edited_personal_form = personal_details_form(request.POST)
			if edited_personal_form.is_valid():
				print('SAVING FORM')
				pf = edited_personal_form.save()
				pf.owner = details
				pf.save()
			else:
				print(edited_personal_form.errors)
			# ORGANISATIONAL FORM HANDLING EDIT / ADD
			if organisation_details:
				edited_organisation_form = organisation_details_form(request.POST, request.FILES, instance=organisation_details)
			else:
				edited_organisation_form = organisation_details_form(request.POST, request.FILES)
			if edited_organisation_form.is_valid():
				print('SAVING FORM')
				of = edited_organisation_form.save()
				of.owner = details
				of.save()
			else:
				print(edited_organisation_form.errors) 
			return redirect('add_internship')
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		context = {'personalform':personal_form, 
				   'organisationform': organisation_form, 'notify':unseen_notifications, 'unseen_count': unseen_count}
		return render(request, "channels/planner/add_details.html", context)
		
def apply(request, internship_id):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		intern = Internship.objects.get(pk = internship_id)
		temp = ApplicationForm.objects.filter(applied_by=details, applied_on=intern)
		if temp:
			applied = True
		else:
			applied = False
		if applied:
			return redirect('internships')
		if request.method == "POST":
			print("THIS IS POST DATTA", request.POST)
			edited_form = application_form(request.POST)
			edited = edited_form.save()
			edited.applied_by = details
			edited.applied_on = intern
			edited.question1 = intern.q1
			edited.question2 = intern.q2
			edited.question3 = intern.q3
			edited.question4 = intern.q4
			edited.save()
			text = edited.applied_by.name + " applied on internship " + intern.title
			notify = Notification(to=intern.poster, text=text, type='warning', link_id=intern.id, internship=True)
			notify.save()
			return redirect('myapplications')
		q1 = intern.q1
		q2 = intern.q2
		q3 = intern.q3
		totalQuest = 2
		if q3:
			totalQuest = 3
		q4 = intern.q4
		if q4:
			totalQuest = 4
		app_form = application_form()
		q_list = [q1,q2,q3,q4]
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications

		return render(request, "channels/planner/apply.html", {'app_form':app_form, 'questions_list': q_list, 'internship': intern, 'totalQuest':totalQuest, 'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		redirect('student_login')	

def my_applications(request):
	if request.user:
		details=detail.objects.filter(email=request.user.email).first()
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		if details.staff:
			internships = Internship.objects.filter(poster = details)
			return render(request, "channels/planner/staff_applications.html", {'internships': internships, 'notify':unseen_notifications, 'unseen_count': unseen_count})
		else:
			all_applications = ApplicationForm.objects.filter(applied_by = details)
			return render(request, "channels/planner/my_applications.html", {'applications': all_applications, 'notify':unseen_notifications, 'unseen_count': unseen_count})

def view_applicants(request, internship_id):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		intrn = Internship.objects.filter(pk = internship_id ).first()
		if details.staff:
			applications = ApplicationForm.objects.filter(applied_on=intrn)
			unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
			all_notifications = list(details.all_notifications.all().order_by('-date'))
			unseen_count = len(unseen_notifications)
			if len(all_notifications) > 5:
				while len(unseen_notifications) < 5:
					unseen_notifications.append(all_notifications.pop(0))
			else:
				unseen_notifications + all_notifications
			return render(request, "channels/planner/applicants.html", {'applications':applications, 'notify':unseen_notifications, 'unseen_count': unseen_count})
		else:
			return redirect('staff_dashboard')
	else:
		return redirect('login_page')
#Channel App Views
@csrf_exempt
def dashboard(request):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		staff = False
		if details.staff:
			staff=True
		if request.method == 'POST':
			action = request.POST.get('action')
			if action == 'add_project':
				pname = request.POST.get('project_name')
				new_proj = Project(creator=details, name=pname)
				new_proj.save()
				return JsonResponse({"project_id":new_proj.id, 'project_name': pname})
		projects = details.created_projects.all()
		assigned_projects = details.assigned_projects.all()
		assigned_sections = details.assigned_sections.all()
		assigned_tasks = details.assigned_tasks.all()
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		return render(request, "channels/tasks/dashboard.html", {'projects':projects, 'assigned_projects':assigned_projects,'assigned_sections':assigned_sections, 'assigned_tasks':assigned_tasks, 'notify':unseen_notifications, 'unseen_count': unseen_count, 'staff':staff})
	else:
		return redirect('login_page')

def section(request, section_id):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		section = Section.objects.get(pk = section_id)
		assigned_sections = details.assigned_sections.all()
		if section not in assigned_sections and section.creator != details:
			return redirect('dash')
		proj = section.project
		all_sections = proj.section_set.all().order_by('index')
		project_assigned_sections = []
		for section in all_sections:
			if section in assigned_sections:
				project_assigned_sections.append(section)
		section_dt = []
		passign_form = project_assign(prefix='project', instance=proj)
		for section in project_assigned_sections:
			tasks = section.task_set.all().order_by('index')
			prefix = str(section.id) + '-section'
			section_assign_form = section_assign(prefix=prefix, instance=section)
			taskdt = []
			for task in tasks:
				checklists = task.checklistitem_set.all()
				attachments = task.attachment_set.all()
				comments = task.comment_set.all()
				prefix = str(task.id) + '-task'
				task_assign_form = task_assign(prefix=prefix, instance=task)
				taskdt.append([task, checklists, attachments, comments, task_assign_form])
			section_dt.append([section,taskdt,section_assign_form])
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications

		return render(request, "channels/tasks/section.html", {'project': proj, 'section_dt': section_dt, 'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		return redirect('login_page')

def task(request, task_id):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		task = Task.objects.get(pk = task_id)
		assigned_tasks = details.assigned_tasks.all()
		if task not in assigned_tasks and task.creator != details:
			return redirect('dash')
		task_section = task.section
		proj = task_section.project
		sections = proj.section_set.all().order_by('index')
		section_dt = []
		relevant_sections = []
		for section in sections:
			tasks = section.task_set.all().order_by('index')
			skip = False
			for task in tasks:
				if task in assigned_tasks or task.creator == details:
					skip = True
					break
			if skip:
				relevant_sections.append(section)
		for section in relevant_sections:
			tasks = section.task_set.all().order_by('index')
			taskdt = []
			for task in tasks:
				if task in assigned_tasks or task.creator == details:
					checklists = task.checklistitem_set.all()
					attachments = task.attachment_set.all()
					comments = task.comment_set.all()
					prefix = str(task.id) + '-task'
					task_assign_form = task_assign(prefix=prefix, instance=task)
					taskdt.append([task, checklists, attachments, comments, task_assign_form])
			section_dt.append([section,taskdt])
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications

		return render(request, "channels/tasks/task.html", {'project': proj, 'section_dt': section_dt, 'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		return redirect('login_page')

@csrf_exempt
def ajax_request(request):
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		if request.POST.get('action') == 'get_details':
			profile = Student_Profile.objects.get(created_by=details)
			image = profile.image.url
			email = profile.email
			return JsonResponse({"image":image, "email": email})
		if request.POST.get('action') == 'add_project':
				pname = request.POST.get('project_name')
				new_proj = Project(creator=details, name=pname)
				new_proj.save()
				return JsonResponse({"project_id":new_proj.id, 'project_name': pname})
		if request.POST.get('action') == 'notifications_viewed':
			notify = details.all_notifications.filter(viewed=False)
			for n in notify:
				n.viewed = True
				n.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'assign_project':
			proj = Project.objects.get(pk = request.POST.get('project_id'))
			assign_to = request.POST.get('assign_to')
			assign_to = json.loads(assign_to)
			queryset = detail.objects.filter(id__in=assign_to)
			proj.assigned_to.clear()
			proj.save()
			proj.assigned_to.add(*queryset)
			for person in queryset:
				text = proj.name + " project assigned to you"
				notify = Notification(to=person, text=text, type='danger', link_id=proj.id, project=True)
				notify.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'edit_project':
			proj = Project.objects.get(pk = request.POST.get('project_id'))
			name = request.POST.get('name')
			description = request.POST.get('description')
			proj.name = name
			proj.description = description
			proj.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'update_taskname':
			task = Task.objects.get(pk = request.POST.get('task_id'))
			task.name = request.POST.get('name')
			task.save()
			text = details.name + " changed taskname to " + task.name
			comm = Comment(text=text, task = task)
			comm.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'delete_checklist':
			checklist = CheckListItem.objects.get(pk = request.POST.get('checklist_id'))
			task = checklist.task
			checklist.delete()
			text = details.name + " deleted checklist item"
			comm = Comment(text=text, task = task)
			comm.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'check_item':
			checklist = CheckListItem.objects.get(pk = request.POST.get('checklist_id'))
			value = request.POST.get("value")
			value = True if value =='true' else False
			checklist.is_checked = value
			checklist.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'add_checklist':
			title = request.POST.get('title')
			task_id = request.POST.get('task_id')
			newchecklist = CheckListItem(title=title, task_id=task_id)
			newchecklist.save()
			checklist_id = newchecklist.id
			text = details.name + " added checklist item"
			comm = Comment(text=text, task_id = task_id)
			comm.save()
			return JsonResponse({"success":True, 'checklist_id': checklist_id})
		if request.POST.get('action') == 'edit_checklist':
			print('done')
			checklist = CheckListItem.objects.get(pk=request.POST.get('checklist_id'))
			checklist_id = request.POST.get('checklist_id')
			checklist.title = request.POST.get('name')
			checklist.save()
			checklist_details = CheckListItem.objects.get(pk=checklist_id)
			return JsonResponse({"success":True, 'checklist': checklist.title})
		if request.POST.get('action') == 'complete_task':
			task = Task.objects.get(pk = request.POST.get('task_id'))
			value = request.POST.get("value")
			value = True if value =='true' else False
			task.is_complete = value
			if value:
				task.date_completed = datetime.now(tz=timezone.utc)
				text = task.name + " task has been completed"
				notify = Notification(to=task.creator, type='success', text=text, link_id=task.id, task=True)
				notify.save()
				text = details.name + " marked task complete"
				comm = Comment(text=text, task = task)
				comm.save()
			else:
				task.date_completed = None
				text = details.name + " un-marked task complete"
				comm = Comment(text=text, task = task)
				comm.save()
			task.save()
			
			return JsonResponse({"success":True, 'task_name': task.name})
		if request.POST.get('action') == 'update_due_date':
			task = Task.objects.get(pk = request.POST.get('task_id'))
			date = request.POST.get("date")
			task.due_date = date
			text = details.name + " updated due date"
			comm = Comment(text=text, task = task)
			comm.save()
			task.save()
			return JsonResponse({"success":True,})
		if request.POST.get('action') == 'update_task_desc':
			task = Task.objects.get(pk = request.POST.get('task_id'))
			description = request.POST.get("description")
			task.description = description
			task.save()
			return JsonResponse({"success":True,})
		if request.POST.get('action') == 'delete_attachment':
			attachment = Attachment.objects.get(pk = request.POST.get('attachment_id'))
			task = attachment.task
			attachment.delete()
			text = details.name + " deleted attachment"
			comm = Comment(text=text, task = task)
			comm.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'add_attachment':
			name = request.POST.get('name')
			task_id = request.POST.get('task_id')
			newattach = Attachment(name= name, task_id=task_id, file=request.FILES['file'])
			newattach.save()
			text = details.name + " added new attachment"
			comm = Comment(text=text, task_id = task_id)
			comm.save()
			return JsonResponse({"success":True, 'attachment_id': newattach.id, 'url': newattach.file.url})
		if request.POST.get('action') == 'add_comment':
			comment = request.POST.get('comment')
			task_id = request.POST.get('task_id')
			comm = Comment(text=comment, commentor=details, task_id = task_id)
			comm.save()
			return JsonResponse({"success":True, 'commentor': comm.commentor.email, 'date': comm.date_created})
		if request.POST.get('action') == 'edit_section':
			name = request.POST.get('name')
			section_id = request.POST.get('section_id')
			description = request.POST.get('description')
			sec = Section.objects.get(pk = section_id)
			sec.name = name
			sec.description = description
			sec.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'add_section':
			proj = Project.objects.get(pk = request.POST.get('project_id'))
			name = request.POST.get('name')
			description = request.POST.get('description')
			sec = Section(name=name, description=description, project=proj, creator=details)
			sec.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'add_task':
			name = request.POST.get('name')
			section_id = request.POST.get('section_id')
			section = Section.objects.get(pk  = section_id)
			max = section.task_set.all().aggregate(Max('index')).get('index__max')
			if max == 0 or max:
				index = max + 1
			else:
				index = 0
			print('Max: ', max)
			task = Task(name=name, section_id=section_id, creator=details, index=index)
			task.save()
			text = details.name + " created this task"
			comm = Comment(text=text, task = task)
			comm.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'delete_task':
			task_id = request.POST.get('task_id')
			task = Task.objects.get(pk = task_id)
			task.delete()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'delete_section':
			section_id = request.POST.get('section_id')
			section = Section.objects.get(pk = section_id)
			section.delete()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'delete_project':
			proj = Project.objects.get(pk = request.POST.get('project_id'))
			proj.delete()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'sort_task':
			task_index_change = Task.objects.get(pk = request.POST.get('task_id'))
			new_index = int(request.POST.get('index'))
			section = task_index_change.section
			section_tasks = section.task_set.all().order_by('index')
			reset = False
			for task in section_tasks:
				if task.index == None:
					reset = True
			if reset:
				i = 0
				for task in section_tasks:
					task.index = i
					task.save()
					i += 1
			old_index = task_index_change.index
			if old_index == new_index:
				return JsonResponse({"no_change":True})
			if old_index > new_index:
				for task in section_tasks:
					print('Task Index: {} Name: {}'.format(task.index, task.name))
					if task.index < new_index or task.index > old_index:
						continue
					if task.index >= new_index and task.index < old_index:
						task.index += 1
					task.save()
					print('Task Index: {} Name: {}'.format(task.index, task.name))
			if old_index < new_index:
				for task in section_tasks:
					if task.index < old_index or task.index > new_index:
						continue
					if task.index > old_index and task.index <= new_index:
						task.index -= 1
			task_index_change.index = new_index
			task_index_change.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'task_section_change':
			section_id = request.POST.get('section_id')
			task_id = request.POST.get('task_id')
			task_dropped = Task.objects.get(pk=task_id)
			old_section = task_dropped.section
			new_section = Section.objects.get(pk=section_id)
			if new_section.id == old_section.id:
				return JsonResponse({"success":True, "no_section_change": True})
			task_dropped.section = new_section
			max = new_section.task_set.all().aggregate(Max('index')).get('index__max')
			if max == 0 or max:
				index = max + 1
			else:
				index = 0
			task_dropped.index = index
			task_dropped.save()
			old_section_tasks = old_section.task_set.all().order_by('index')
			i = 0
			for task in old_section_tasks:
				task.index = i
				task.save()
				i += 1
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'sort_section':
			proj = Project.objects.get(pk = request.POST.get('project_id'))
			section_index_change = Section.objects.get(pk = request.POST.get('section_id'))
			new_index = int(request.POST.get('index'))
			project_sections = proj.section_set.all().order_by('index')
			reset = False
			for section in project_sections:
				if section.index == None:
					reset = True
					print('RESETTING')
			if reset:
				i = 0
				for section in project_sections:
					section.index = i
					section.save()
					i += 1
			section_index_change = Section.objects.get(pk = request.POST.get('section_id'))
			old_index = section_index_change.index
			if old_index == new_index:
				return JsonResponse({"no_change":True})
			if old_index > new_index:
				for section in project_sections:
					print('Section Index: {} Name: {}'.format(section.index, section.name))
					if section.index < new_index or section.index > old_index:
						continue
					if section.index >= new_index and section.index < old_index:
						section.index += 1
					section.save()
					print('Section Index: {} Name: {}'.format(section.index, section.name))
			if old_index < new_index:
				for section in project_sections:
					if section.index < old_index or section.index > new_index:
						continue
					if section.index > old_index and section.index <= new_index:
						section.index -= 1
			section_index_change.index = new_index
			section_index_change.save()
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'assign_task':
			assign_to = request.POST.get('assign_to')
			assign_to = json.loads(assign_to)
			task = Task.objects.get(pk=request.POST.get('task_id'))
			queryset = detail.objects.filter(id__in=assign_to)
			for person in queryset:
				text = task.name + " task assigned to you"
				notify = Notification(to=person, text=text, type='danger', link_id=task.id, task=True)
				notify.save()
			task.assigned_to.clear()
			task.assigned_to.add(*queryset)
			return JsonResponse({"success":True})
		if request.POST.get('action') == 'assign_section':
			assign_to = request.POST.get('assign_to')
			assign_to = json.loads(assign_to)
			section = Section.objects.get(pk=request.POST.get('section_id'))
			queryset = detail.objects.filter(id__in=assign_to)
			for person in queryset:
				text = section.name + " section assigned to you"
				notify = Notification(to=person, text=text, type='danger', link_id=section.id, section=True)
				notify.save()
			section.assigned_to.clear()
			section.assigned_to.add(*queryset)
			return JsonResponse({"success":True})
	else:
		return redirect('login_page')
		


def project(request, project_id):
	print('THIS IS POST DATA: ', request.POST)
	print('THESE ARE POST FILES ', request.FILES)
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		proj = Project.objects.get(pk = project_id)
		projects = details.created_projects.all()
		assigned_projects = details.assigned_projects.all()
		print('Proj: {}\nMy Proj: {}\nAss_Proj: {}'.format(proj, projects, assigned_projects))
		print('proj in projects: {} proj in assigned_projects: {}'.format(proj in projects,proj in assigned_projects))
		if not((proj in projects) or (proj in assigned_projects)):
			return redirect('dash')	
		sections = proj.section_set.all().order_by('index')
		section_dt = []
		passign_form = project_assign(prefix='project', instance=proj)
		for section in sections:
			tasks = section.task_set.all().order_by('index')
			prefix = str(section.id) + '-section'
			section_assign_form = section_assign(prefix=prefix, instance=section)
			taskdt = []
			for task in tasks:
				checklists = task.checklistitem_set.all()
				attachments = task.attachment_set.all()
				comments = task.comment_set.all()
				prefix = str(task.id) + '-task'
				task_assign_form = task_assign(prefix=prefix, instance=task)
				taskdt.append([task, checklists, attachments, comments, task_assign_form])
			section_dt.append([section,taskdt,section_assign_form])
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		return render(request, "channels/tasks/project.html", {'project': proj, 'section_dt': section_dt, 'passign_form':passign_form, 'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		return redirect('login_page')

def project_treeview(request):
	print('THIS IS POST DATA: ', request.POST)
	print('THESE ARE POST FILES ', request.FILES)
	if request.user.is_authenticated:
		details = detail.objects.filter(email=request.user.email).first()
		proj = details.created_projects.first()
		projects = details.created_projects.all()
		assigned_projects = details.assigned_projects.all()
		print('Proj: {}\nMy Proj: {}\nAss_Proj: {}'.format(proj, projects, assigned_projects))
		print('proj in projects: {} proj in assigned_projects: {}'.format(proj in projects,proj in assigned_projects))
		project_data = []
		if not((proj in projects) or (proj in assigned_projects)):
			return redirect('dash')	
		for proj in projects:
			sections = proj.section_set.all().order_by('index')
			section_dt = []
			prefix = 'project-' + str(proj.id)
			passign_form = project_assign(prefix=prefix, instance=proj)
			for section in sections:
				tasks = section.task_set.all().order_by('index')
				prefix = str(section.id) + '-section'
				section_assign_form = section_assign(prefix=prefix, instance=section)
				taskdt = []
				for task in tasks:
					checklists = task.checklistitem_set.all()
					attachments = task.attachment_set.all()
					comments = task.comment_set.all()
					prefix = str(task.id) + '-task'
					task_assign_form = task_assign(prefix=prefix, instance=task)
					taskdt.append([task, checklists, attachments, comments, task_assign_form])
				section_dt.append([section,taskdt,section_assign_form])
			project_data.append([proj, passign_form, section_dt])
		unseen_notifications = list(details.all_notifications.filter(viewed=False).order_by('-date'))
		all_notifications = list(details.all_notifications.all().order_by('-date'))
		unseen_count = len(unseen_notifications)
		if len(all_notifications) > 5:
			while len(unseen_notifications) < 5:
				unseen_notifications.append(all_notifications.pop(0))
		else:
			unseen_notifications + all_notifications
		return render(request, "channels/tasks/project_treeview.html", {'project_data': project_data,'notify':unseen_notifications, 'unseen_count': unseen_count})
	else:
		return redirect('login_page')

def student_user_profile(request):
	if request.user:
		details = detail.objects.filter(email=request.user.email).first()
		if not details.student:
			return redirect('planner_home')
		# if request.method=="POST":
		old_profile = Student_Profile.objects.filter(created_by=details).first()
		if request.POST.get('submit') == 'upload':
			student = Student_Profile.objects.filter(created_by=details).first()
			student.image = request.FILES.get('image')
			student.save()
			return redirect('student_user_profile')
		# else:
		# 	print('IMAGE ERRORS: ', student.errors)
		# 	return redirect('student_user_profile')
		
		if request.POST.get('submit') == 'add_form':
			print("THIS IS POST: ", request.POST)
			if old_profile:
				addNewForm = Student_User_Profile_Form(request.POST, instance=old_profile)
			else:
				addNewForm = Student_User_Profile_Form(request.POST)			
			if addNewForm.is_valid():
				stdnt_profile = addNewForm.save()
				stdnt_profile.created_by = details
				stdnt_profile.save()
			else:
				print('ADD NEW FORM: ',addNewForm.errors)
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'edu_form':
			edu_form = Education_Form(request.POST)
			if edu_form.is_valid():
				e_form = edu_form.save()
				e_form.created_by = details
				e_form.save()
			else:
				print('ED FORM ERRORS ',edu_form.errors)
			return redirect('student_user_profile')	
		if request.POST.get('edit_edu_profile'):
			instance_id = request.POST.get('edit_edu_profile')
			instance = Education_Qualification.objects.get(pk=instance_id)
			editedFormEdu = Education_Form(request.POST, instance=instance, prefix=instance_id)
			if editedFormEdu.is_valid():
				editedFormEdu.save()	
			else:
				print('EDIT EDUCATION FORM ERRORS')
		if request.POST.get('delete_education'):
			instance_id = request.POST.get('delete_education')
			instance = Education_Qualification.objects.get(pk=instance_id)
			instance.delete()
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'job_pro':
			job_profile_form = Job_Profile_Form(request.POST)
			if job_profile_form.is_valid():
				job_form = job_profile_form.save()
				job_form.created_by = details
				job_form.save()
			else:
				print('JOB PROFILE FORM ERRORS ',job_profile_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_job'):
			instance_id = request.POST.get('edit_job')
			instance = Profile_Jobs.objects.get(pk=instance_id)
			editedFormJob = Job_Profile_Form(request.POST, instance=instance, prefix=instance_id)
			if editedFormJob.is_valid():
				editedFormJob.save()
			else:
				print('JOB EDIT FORMS ERRORS', editedFormJob.errors)
		if request.POST.get('delete_job'):
			instance_id = request.POST.get('delete_job')
			instance = Profile_Jobs.objects.get(pk=instance_id)
			instance.delete()
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'int_pro':
			intern_profile_form = Internship_Profile_Form(request.POST)
			if intern_profile_form.is_valid():
				intern_form = intern_profile_form.save()
				intern_form.created_by = details
				intern_form.save()
			else:
				print('Internship PROFILE FORM ERRORS ',intern_profile_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_intern_profile'):
			instance_id = request.POST.get('edit_intern_profile')
			instance = Profile_Internship.objects.get(pk = instance_id)
			editedForm = Internship_Profile_Form(request.POST, instance=instance, prefix=instance_id)
			if editedForm.is_valid():
				editedForm.save()

		if request.POST.get('delete_internship'):
			instance_id = request.POST.get('delete_internship')
			instance = Profile_Internship.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'res_pro':
			responsibility_form = Responsibility_Form(request.POST)
			if responsibility_form.is_valid():
				res_form = responsibility_form.save()
				res_form.created_by = details
				res_form.save()
			else:
				print('Responsibility FORM ERRORS ', responsibility_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_responsibility'):
			instance_id = request.POST.get('edit_responsibility')
			instance = Profile_Responsibility.objects.get(pk=instance_id)
			responsibilityEditedForm = Responsibility_Form(request.POST, instance=instance, prefix=instance_id)
			if responsibilityEditedForm.is_valid():
				responsibilityEditedForm.save()
			else:
				print('EDIT RESPONSIBILITY FORM ERRORS ', responsibilityEditedForm.errors)
		if request.POST.get('delete_responsibility'):
			instance_id = request.POST.get('delete_responsibility')
			instance = Profile_Responsibility.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'train_pro':
			training_form = Profile_Training_Form(request.POST)
			if training_form.is_valid():
				train_form = training_form.save()
				train_form.created_by = details
				train_form.save()
			else:
				print('Training FORM ERRORS ', training_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_training'):
			instance_id = request.POST.get('edit_training')
			instance = Profile_Training.objects.get(pk=instance_id)
			trainingEditedForm = Profile_Training_Form(request.POST, instance=instance, prefix=instance_id)
			if trainingEditedForm.is_valid():
				trainingEditedForm.save()
			else:
				print('EDITED TRAINING FORM ERRORS ', trainingEditedForm.errors)
		if request.POST.get('delete_training'):
			instance_id = request.POST.get('delete_training')
			instance = Profile_Training.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'pro_pro':
			project_form = Project_Form(request.POST)
			if project_form.is_valid():
				pro_form = project_form.save()
				pro_form.created_by = details
				pro_form.save()
			else:
				print('PROJECT FORM ERRORS ', project_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_project'):
			instance_id = request.POST.get('edit_project')
			instance = Profile_Project.objects.get(pk=instance_id)
			projectEditedForm = Project_Form(request.POST, instance=instance, prefix=instance_id)
			if projectEditedForm.is_valid():
				projectEditedForm.save()
			else:
				print('EDITED PROJECT FORM ERRORS ', projectEditedForm.errors)
		if request.POST.get('delete_project'):
			instance_id = request.POST.get('delete_project')
			instance = Profile_Project.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'skill_pro':
			skill_form = Profile_Skills_Form(request.POST)
			if skill_form.is_valid():
				sk_form = skill_form.save()
				sk_form.created_by = details
				sk_form.save()
			else:
				print('SKILL FORM ERRORS ', skill_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_skills'):
			instance_id = request.POST.get('edit_skills')
			instance = Profile_Skills.objects.get(pk=instance_id)
			skillEditedForm = Profile_Skills_Form(request.POST, instance=instance, prefix=instance_id)
			if skillEditedForm.is_valid():
				skillEditedForm.save()
			else:
				print('EDITED SKILL FORM ERRORS ', skillEditedForm.errors)
		if request.POST.get('delete_skill'):
			instance_id = request.POST.get('delete_skill')
			instance = Profile_Skills.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'ws_pro':
			work_sample_form = Work_Sample_Form(request.POST)
			if work_sample_form.is_valid():
				ws_form = work_sample_form.save()
				ws_form.created_by = details
				ws_form.save()
			else:
				print('WORK SAMPLE FORM ERRORS ', work_sample_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_ws'):
			instance_id = request.POST.get('edit_ws')
			instance = Profile_WorkSamples.objects.get(pk=instance_id)
			workSampleEditedForm = Work_Sample_Form(request.POST, instance=instance, prefix=instance_id)
			if workSampleEditedForm.is_valid():
				workSampleEditedForm.save()
			else:
				print('EDITED WORK SAMPLE FORM ERRORS ', workSampleEditedForm.errors)
		if request.POST.get('delete_ws'):
			instance_id = request.POST.get('delete_ws')
			instance = Profile_WorkSamples.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		if request.POST.get('submit') == 'add_pro':
			add_details_form = Additional_Details_Form(request.POST)
			if add_details_form.is_valid():
				add_form = add_details_form.save()
				add_form.created_by = details
				add_form.save()
			else:
				print('ADDITIONAL DETAILS FORM ERRORS ', add_details_form.errors)
			return redirect('student_user_profile')
		if request.POST.get('edit_add'):
			instance_id = request.POST.get('edit_add')
			instance = Profile_AdditionDetails.objects.get(pk=instance_id)
			additionalEditedForm = Additional_Details_Form(request.POST, instance=instance, prefix=instance_id)
			if additionalEditedForm.is_valid():
				additionalEditedForm.save()
			else:
				print('ADDITIONAL DETAILS EDITED FORM ERRORS ', additionalEditedForm.errors)
		if request.POST.get('delete_add'):
			instance_id = request.POST.get('delete_add')
			instance = Profile_AdditionDetails.objects.get(pk=instance_id)
			instance.delete()			
			return redirect('student_user_profile')
		
		if old_profile:
			addForm = Student_User_Profile_Form(instance=old_profile)
			first_time = False
		else:
			addForm = Student_User_Profile_Form()
			first_time = True			
		student_profile_details = details.student_details.all()

		edu_form = Education_Form()
		education_profile_details = details.education_details.all()
		education_details = []
		for edetail in education_profile_details:
			temp_form = Education_Form(instance=edetail, prefix=edetail.id)
			education_details.append([edetail, temp_form])

		job_profile_form = Job_Profile_Form()
		job_profile_details = details.job_details.all()
		job_profile_data = []
		for jdetail in job_profile_details:
			temp_form = Job_Profile_Form(instance=jdetail, prefix=jdetail.id)
			job_profile_data.append([jdetail, temp_form])

		intern_profile_form = Internship_Profile_Form()
		intern_profile_details = details.intern_details.all()
		intern_profile_data = []
		for pdetail in intern_profile_details:
			temp_form = Internship_Profile_Form(instance=pdetail, prefix=pdetail.id)
			intern_profile_data.append([pdetail, temp_form])

		responsibility_form = Responsibility_Form()
		responsibility_form_details = details.responsibility_details.all()
		responsibility_data = []
		for rdetail in responsibility_form_details:
			temp_form = Responsibility_Form(instance=rdetail, prefix=rdetail.id)
			responsibility_data.append([rdetail, temp_form])

		training_form = Profile_Training_Form()
		training_details = details.training_details.all()
		training_data = []
		for tdetail in training_details:
			temp_form = Profile_Training_Form(instance=tdetail, prefix=tdetail.id)
			training_data.append([tdetail, temp_form])

		project_form = Project_Form()
		project_details = details.project_details.all()
		project_data = []
		for pdetail in project_details:
			temp_form = Project_Form(instance=pdetail, prefix=pdetail.id)
			project_data.append([pdetail, temp_form])

		skill_form = Profile_Skills_Form()
		skill_details = details.skill_details.all()
		skill_data = []
		for sdetail in skill_details:
			temp_form = Profile_Skills_Form(instance=sdetail, prefix=sdetail.id)
			skill_data.append([sdetail, temp_form])

		work_sample_form = Work_Sample_Form()
		work_sample_details = details.work_sample_details.all()
		work_sample_data = []
		for wdetail in work_sample_details:
			temp_form = Work_Sample_Form(instance=wdetail, prefix=wdetail.id)
			work_sample_data.append([wdetail, temp_form])

		add_details_form = Additional_Details_Form()
		addition_details = details.additional_details.all()
		addition_data = []
		for adetail in addition_details:
			temp_form = Additional_Details_Form(instance=adetail, prefix=adetail.id)
			addition_data.append([adetail, temp_form])
		return render(request, 'channels/planner/student-user-profile.html', {'student_user_profile_form':addForm,
		 'student_details':student_profile_details, 'first-time':first_time, 'education_form':edu_form, 'education_details':education_details, 'job_profile_form':job_profile_form,
		 'job_profile_details':job_profile_data, 'intern_profile_form':intern_profile_form,
		 'intern_profile_data':intern_profile_data, 'responsibility_form': responsibility_form,
		 'responsibility_form_details':responsibility_data, 'training_form':training_form,
		 'training_details':training_data, 'project_form':project_form, 'project_details':project_data,
		 'skill_form':skill_form, 'skill_details': skill_data, 'work_sample_form':work_sample_form,
		 'work_sample_details':work_sample_data, 'add_details_form':add_details_form, 
		 'addition_details':addition_data})

# return JsonResponse({"data":cols})