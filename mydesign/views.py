

from django.shortcuts import render,redirect
from userdetail.models import detail
# Create your views here.
from django.http import HttpResponse
import json
# from mydesign.models import interests,interest_users,followers,post,friend
from .models import *
from .forms import *
from b2b.models import notifications,chats_head,messages_head

from userdetail.models import staff_Categories,seller_Categories
import datetime
from movintrendz.views import label_home_page
import random

def mydesign_home(request):
    '''if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        return label_home_page(request, label_tag="My Design")
        if details:
            if not(details.info_update):
                return redirect('/mydesign/profile')
            data={
                "page":"design"
            }
            return render(request,"mydesign/mydesign_home.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login?next=mydesign')'''
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details:
            if not(details.info_update):
                return redirect('/mydesign/profile')
            data={
                "page":"design"
            }
            return render(request,"mydesign/mydesign_home.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login_page?next=mydesign')


def mydesign_profile(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details:
            interest=interests.objects.all().order_by('-priority')
            interes_obj=interest_users.objects.filter(user=details).first()
            interested_in=[]
            if interes_obj:
                interested_in=interes_obj.interest_user.all()
            interest=interest.exclude(id__in=interested_in)[:18]
            a=followers.objects.filter(user=details).first()
            follower=[]
            if a:
                for ik in a.followers_users.all():
                    follower.append(ik)
            a=followers.objects.filter(followers_users=details)
            following=[]
            for ik in a:
                following.append(ik.user)
            print(follower)
            posts=post.objects.filter(user=details)
            friends=friend.objects.filter(user1=details,request_accepted=True)
            friends1=friend.objects.filter(user2=details,request_accepted=True)
            friends=friends | friends1
            data={
                "user":details,
                "page":"profile",
                "interest":interest,
                "follower":follower,
                "following":following,
                "posts":posts,
                "friends":friends
            }
            if request.FILES.get('design_profile_input'):
                details.image=request.FILES.get('design_profile_input')
                details.info_update=True
                details.save()
                img=details.image.url
                return HttpResponse(json.dumps({'img':img}), content_type="application/json")
            if request.POST.get('tagline_ajax'):
                details.mission=request.POST.get('tagline_ajax')
                details.save()
                return HttpResponse(json.dumps({'img':True}), content_type="application/json")
            if request.POST.get('about_ajax'):
                details.description=request.POST.get('about_ajax')
                details.save()
                return HttpResponse(json.dumps({'img':True}), content_type="application/json")
            if request.POST.get('id_interest_ajax'):
                interest_obj=interests.objects.filter(id=int(request.POST.get('id_interest_ajax'))).first()
                interes_new_obj=interest_users.objects.filter(user=details).first()
                if not(interes_new_obj):
                    interes_new_obj=interest_users()
                    interes_new_obj.user=details
                    interes_new_obj.save()
                interes_new_obj.interest_user.add(interest_obj)
                interes_new_obj.save()
                interest_obj.priority+=1
                interest_obj.save()
                interest=interests.objects.all().order_by('-priority')
                interes_obj=interest_users.objects.filter(user=details).first()
                interested_in=[]
                if interes_obj:
                    interested_in=interes_obj.interest_user.all()
                interest=interest.exclude(id__in=interested_in)[:18]
                interest=list(interest.values())
                return HttpResponse(json.dumps({'interest':interest}), content_type="application/json")
            return render(request,"mydesign/mydesign_profile.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')

def mydesign_interest(request, interest_name):
    if request.user.is_authenticated:
        print(f'IntersetName : {interest_name}')
        thisInterest = interests.objects.filter(name=interest_name).first()
        posts = thisInterest.posts.all()
        return render(request, 'mydesign/mydesign_interest.html', {'posts':posts, 'interest':thisInterest})
    else:
        return redirect('login_page')
    return render(request, 'mydesign/mydesign_interest.html')


def mydesign_post(request, post_id):
    print(f'THIS IS POST {request.POST}')
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        thisPost = post.objects.filter(pk = post_id).first()
        related_posts = []
        if request.POST.get('new_comment'):
            text = request.POST.get('text')
            parent_id = request.POST.get('parent_id')
            comm = Comment(post=thisPost, user=details, text=text)
            if parent_id:
                comm.parent_id = parent_id
            comm.save()
            return redirect('mydesign_post', post_id=thisPost.id)
        if len(thisPost.related_interests.all()) >= 2:
            interests = random.sample(list(thisPost.related_interests.all()),2)
            for interest in interests:
                temp = interest.posts.all().exclude(id=thisPost.id)
                related_posts += list(temp)
            if len(list(set(related_posts))) >= 2:
                related_posts = random.sample(list(set(related_posts)),2)
        if thisPost:
            comments = thisPost.comments.all()
            return render(request, 'mydesign/mydesign_single_post.html', {'post': thisPost, 'related_posts':related_posts, 'comments': comments})
        else:
            return redirect('mydesign_profile')
    else:
        return redirect('login_page')



def mydesign_other_profile(request,email):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details:
            user_to_view=detail.objects.filter(email=email).first()
            if user_to_view:
                interest=interests.objects.all().order_by('-priority')
                interes_obj=interest_users.objects.filter(user=user_to_view).first()
                interested_in=[]
                if interes_obj:
                    interested_in=interes_obj.interest_user.all()
                interest=interest.exclude(id__in=interested_in)[:18]
                a=followers.objects.filter(user=user_to_view).first()
                follower=[]
                if a:
                    for ik in a.followers_users.all():
                        follower.append(ik)
                a=followers.objects.filter(followers_users=user_to_view)
                following=[]
                for ik in a:
                    following.append(ik.user)
                print(follower)
                posts=post.objects.filter(user=user_to_view)
                friends=friend.objects.filter(user1=user_to_view,request_accepted=True)
                friends1=friend.objects.filter(user2=user_to_view,request_accepted=True)
                friends=friends | friends1
                interest=interest_users.objects.filter(user=user_to_view).first()
                if interest:
                    interest=interest.interest_user.all()
                fo=followers.objects.filter(user=user_to_view).first()
                follow=False
                if fo:
                    if details in fo.followers_users.all():
                        follow=True
                fr=friend.objects.filter(user1=details,user2=user_to_view)
                if fr:
                    fr=fr | friend.objects.filter(user2=details,user1=user_to_view)
                friends_jk=False
                request_jk=False
                if fr.first():
                    aj=fr
                    if aj.first().request_accepted:
                        friends_jk=True
                    else:
                        request_jk=True
                data={
                    "user":user_to_view,
                    "interest":interest,
                    "follower":follower,
                    "following":following,
                    "posts":posts,
                    "friends":friends,
                    "follow":follow,
                    "friend_jk":friends_jk,
                    "request_jk":request_jk
                }
                if request.POST.get('follow'):
                    a=followers.objects.filter(user=user_to_view).first()
                    if not(a):
                        a=followers(user=user_to_view)
                        a.save()
                    a.followers_users.add(details)
                    a.save()
                    return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
                if request.POST.get('unfollow'):
                    a=followers.objects.filter(user=user_to_view).first()
                    if a:
                        if details in a.followers_users.all():
                            a.followers_users.remove(details)
                        a.save()
                    return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
                if request.POST.get('cancelrequest'):
                    friends_having=friend.objects.filter(user1=details,user2=user_to_view)
                    friends_having=friends_having | friend.objects.filter(user2=details,user1=user_to_view)
                    if friends_having.first():
                        friends_having.first().delete()
                    return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
                if request.POST.get('unfriend'):
                    friends_having=friend.objects.filter(user1=details,user2=user_to_view)
                    friends_having=friends_having | friend.objects.filter(user2=details,user1=user_to_view)
                    if friends_having.first():
                        friends_having.first().delete()
                    return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
                if request.POST.get('addfriend'):
                    obj=friend(user1=details,user2=user_to_view)
                    obj.save()
                    return HttpResponse(json.dumps({'bol':True}), content_type="application/json")
                return render(request,"mydesign/mydesign_other_profile.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')







def mydesign_notifications(request):
	if request.GET.get('noti'):
		noti=int(request.GET.get('noti'))
		ogh=notifications.objects.filter(id=noti).first()
		if ogh:
			ogh.seen=True
			ogh.save()
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email).first()
		if details:
			noti=notifications.objects.filter(user=details).order_by('-created_on')
			no_count=notifications.objects.filter(seen=False,user=details).count()
			if request.GET.get('filter'):
				filter_noti=request.GET.get('filter')
				if filter_noti=='staff':
					pass
				elif filter_noti=='enquiry':
					noti=noti.filter(type_of_order='E')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='design':
					noti=noti.filter(type_of_order='D')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='sampling':
					noti=noti.filter(type_of_order='S')
					no_count=noti.filter(seen=False).count()
				elif filter_noti=='order':
					noti=noti.filter(type_of_order='O')
					no_count=noti.filter(seen=False).count()
			oty=notifications.objects.filter(user=details,type_of_order='E',seen=False).count()
			oty1=notifications.objects.filter(user=details,type_of_order='D',seen=False).count()
			oty2=notifications.objects.filter(user=details,type_of_order='S',seen=False).count()
			oty3=notifications.objects.filter(user=details,type_of_order='O',seen=False).count()
			oty4=oty1+oty2+oty3+oty
			data={
			"noti":noti,
			"no_count":no_count,
			"oty":oty,
			"oty1":oty1,
			"oty2":oty2,
			"oty3":oty3,
			"oty4":oty4,
            "page":"notification"
			}
			return render(request,"mydesign/mydesign_notifications.html",data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')




def mydesign_messages(request):
	if request.user.is_authenticated:
		details=detail.objects.filter(email=request.user.email)
		if details.count()>0:
			details=details.first()
		else:
			return redirect('/userdetail/logout')
		if details:
			chats=chats_head.objects.filter(user1=details)
			chats1=chats_head.objects.filter(user2=details)
			chats= chats | chats1
			chats.order_by('-last_message_time')
			# print(chats)
			staff_cate=staff_Categories.objects.all()
			data={
			"chats":chats,
			"staff_cate":staff_cate,
			"details":details,
			"chat_id":None,
			"cur":datetime.datetime.now(),
            "page":"message"
			}
			if request.GET.get('to') and request.GET.get('message'):
				to_open_chat=request.GET.get('to')
				to_open_chat=detail.objects.filter(email=to_open_chat).first()
				if to_open_chat:
					objyut=chats_head.objects.filter(user1=details,user2=to_open_chat).first()
					if not(objyut):
						objyut=chats_head.objects.filter(user1=to_open_chat,user2=details).first()
						if not(objyut):
							objyut=chats_head(user1=details,user2=to_open_chat,
							last_message=request.GET.get('message'),
							last_message_time=datetime.datetime.now())
							objyut.save()
					objyut.last_message=request.GET.get('message')
					objyut.last_message_time=datetime.datetime.now()
					objyut.save()
					sydty=messages_head(chat=objyut,
					message=request.GET.get('message'))
					if objyut.user1==to_open_chat:
						sydty.sent_by_user1=False
						sydty.sent_by_user2=True
					else:
						sydty.sent_by_user1=True
						sydty.sent_by_user2=False
					sydty.save()
					data["chat_id"]=objyut.id
			if request.POST.get('position_ajax_staff'):
				staff_ajax_cate=request.POST.get('staff_ajax_cate')
				position_ajax_staff=request.POST.get('position_ajax_staff')
				if staff_ajax_cate is None:
					obj1=detail.objects.filter(position=position_ajax_staff,staff=True)
				else:
					ort=staff_Categories.objects.filter(name=staff_ajax_cate).first()
					obj1=detail.objects.filter(staff_category=ort,position=position_ajax_staff,staff=True)

				if obj1.count()>0:
					bol=True
				else:
					bol=False
				obj1=list(obj1.values())
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")

			if request.POST.get('message_ajax'):
				chat_id=request.POST.get('chats_ajax');
				message=request.POST.get('message_ajax')
				chats=chats_head.objects.filter(id=chat_id).first()

				obj1=messages_head(
						chat=chats,
						message=message,
						sent_by_user1=False,
						sent_by_user2=False
					)
				chats.last_message=message
				chats.last_message_time=datetime.datetime.now()
				if chats.user1==details:
					obj1.sent_by_user1=True
				else:
					obj1.sent_by_user2=True
				obj1.save()
				bol=True
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")
			if request.POST.get('message') and request.POST.get('staff'):
				to_email=request.POST.get('staff')
				message=request.POST.get('message')
				to_email=detail.objects.filter(email=to_email).first()
				obj=chats_head(
						user1=details,
						user2=to_email,
						last_message=message,
						last_message_time=datetime.datetime.now()

					)
				obj.save()
				obj1=messages_head(
						chat=obj,
						message=message,
						sent_by_user1=True,
						sent_by_user2=False
					)
				obj1.save()
				return redirect('/userdetail/staff_profile/message')
			if request.POST.get('chats_ajax_id'):
				obj1=messages_head.objects.filter(chat=chats_head.objects.get(id=int(request.POST.get('chats_ajax_id')))).order_by('created_on')
				print(obj1.count())
				if obj1.count()>0:
					bol=True
				else:
					bol=False
				li1=[]
				for a in obj1:
					li={}
					li["message"]=a.message
					li["sent_by_user1"]=a.sent_by_user1
					li["sent_by_user2"]=a.sent_by_user2
					li["created_on"]=a.created_on
					li["user1"]=a.chat.user1.email
					li["user2"]=a.chat.user2.email
					li1.append(li)
				obj1=li1
				return HttpResponse(json.dumps({'data': obj1,'bol':bol},default=str), content_type="application/json")

			return render(request,'mydesign/mydesign_messages.html',data)
		else:
			return redirect('/userdetail/logout')
	else:
		return redirect('/userdetail/login')

def mydesign_editpost(request, post_id):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        thisPost = post.objects.filter(pk = post_id).first()
        if not thisPost:
            return redirect('mydesign_profile')
        if thisPost.user == details:
            if request.method == 'POST':
                if request.POST.get('delete_post'):
                    thisPost.delete()
                    return redirect('mydesign_profile')
                editedForm = post_form(request.POST, instance=thisPost)
                if editedForm.is_valid():
                    editedForm.save()
                    return redirect('mydesign_post', post_id=thisPost.id)
            pform = post_form(instance=thisPost)
            return render(request, 'mydesign/mydesign_editpost.html',{'form':pform}) 
        else:
            return redirect('mydesign_post', post_id=thisPost.id)
    else:
        return redirect('login_page')

def mydesign_newpost(request):
    if request.user.is_authenticated:
        details=detail.objects.filter(email=request.user.email).first()
        if details:
            int_form = interest_form()
            data={  
                'interest_form':int_form
            }
            if request.POST.get('title') and request.FILES.get('image'):
                # print("HERE for the POST")
                price=request.POST.get('price')
                print(f'THIS IS POST: {request.POST}')
                intrst = request.POST.getlist('related_interests')
                if price:
                    price=int(price)
                obj=post(
                title=request.POST.get('title'),
                description=request.POST.get('desc'),
                estimated_price=price,
                image=request.FILES.get('image'),
                image1=request.FILES.get('image2'),
                image2=request.FILES.get('image3'),
                image3=request.FILES.get('image4'),
                image4=request.FILES.get('image5'),
                post_privacy=request.POST.get('post_privacy'),
                user=details
                )
                obj.save()
                obj.related_interests.add(*intrst)
                if obj.post_privacy == "public":
                    des_mode=staff_Categories.objects.filter(name="Design Moderator").first()
                    to_staffs=detail.objects.filter(staff_category=des_mode)
                    for i in to_staffs:
                        noti_oj=notifications(
                        	title="New Product posted please Approve it !",
                        	description="New Product posted please Approve it !",
                        	user=i,
                        	link="/mydesign/post/"+str(obj.id))
                        noti_oj.save()
                        noti_oj.link=noti_oj.link+"?noti="+str(noti_oj.id)
                        noti_oj.save()
                else:
                    obj.approved=True
                    obj.save()
            return render(request,"mydesign/mydesign_newpost.html",data)
        else:
            return redirect('/userdetail/logout')
    else:
        return redirect('/userdetail/login')
