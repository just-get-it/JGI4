from django.urls import path
from . import views

urlpatterns=[
	# path('dash/',views.dash,name='dash'),
	# path('dash/add_project',views.add_project,name='add_project'),
	# path('dash/p_add',views.p_add,name='p_add'),
	# path('dash/add_task',views.add_task,name='add_task'),
	# path('dash/task_page',views.task_page,name='task_page'),
	# path('dash/add_subtask',views.add_subtask,name='add_subtask'),
	# path('dash/add_activity',views.add_activity,name='add_activity'),
	# path('dash/activity_features',views.activity_features,name='activity_features'),
	# path('dash/assign_project',views.assign_project,name='assign_project'),
	# path('dash/show_specific_task',views.show_specific_task,name='show_specific_task'),
	# path('dash/delete_activity',views.delete_activity,name='delete_activity'),
	# path('dash/delete_project',views.delete_project,name='delete_project'),
	# path('dash/delete_task',views.delete_task,name='delete_task'),
	# path('dash/delete_subtask',views.delete_subtask,name='delete_subtask'),	
	# path('dash/task_page_assign',views.task_page_assign,name='task_page_assign'),	
	# path('dash/activity_feature_assign',views.activity_feature_assign,name='activity_feature_assign'),
	# path('dash/edit_project',views.edit_project,name='edit_project'),
	# path('dash/edit_task',views.edit_task,name='edit_task'),
	# path('dash/edit_subtask',views.edit_subtask,name='edit_subtask'),
	# path('dash/edit_activity',views.edit_activity,name='edit_activity'),
	# path('dash/assign_section',views.assign_section,name='assign_section'),
	# path('dash/show_specific_section',views.show_specific_section,name='show_specific_section'),
	# path('dash/assign_subtask',views.assign_subtask,name='assign_subtask'),
	# path('dash/show_specific_subtask',views.show_specific_subtask,name='show_specific_subtask'),
	# Planner App URLs
	path('planner/',views.planner_index,name='planner_home'),
	path('internships/', views.internships, name='internships'),
	path('internship/<int:internship_id>', views.singleInternship, name='single_internship'),
	path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
	path('staff/edit/<int:internship_id>', views.editInternship, name='edit_internship'),
	path('staff/add/', views.add_internship, name='add_internship'),
	path('staff/details', views.add_details, name='add_details'),
	path('apply/<int:internship_id>', views.apply, name='apply'),
	path('myapplications', views.my_applications, name='myapplications'),
	path('applicants/<int:internship_id>', views.view_applicants, name='applicants'),
	# Channels App Urls
	path('dashboard/', views.dashboard, name='dash'),
	path('project/<int:project_id>', views.project, name='project'),
	path('project_treeview/', views.project_treeview, name='project_treeview'),
	path('section/<int:section_id>', views.section, name='section'),
	path('task/<int:task_id>', views.task, name='task'),
	path('ajax_handler', views.ajax_request, name='ajax'),
	path('notifications/', views.notifications, name='notifications'),
	path('student-user-profile/', views.student_user_profile, name="student_user_profile"),
]