from django.shortcuts import render,redirect, HttpResponseRedirect, reverse,get_object_or_404
from .models import *
from .forms import *
from django.db.models import Max
from django.contrib import messages
# from .forms import *
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from userdetail.models import *
from userdetail.forms import *
from channels.models import *
from channels.forms import *
import json
from django.views.decorators.csrf import csrf_exempt
# import daily_report.models
from daily_report.models import Report
from datetime import datetime, timedelta,date
from django.utils import timezone
from django.db.models import Q
from django.contrib import auth
from django.forms import modelformset_factory
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from product.models import *

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        instance = detail.objects.filter(email=request.user.email).first()
        profile = []
        print("inside index")
        if not User.objects.filter(email=instance):
            email = instance
            name = instance.name
            profile = User(email=email, name=name)
            profile.save()

        profile = User.objects.get(email=instance)
        posts = Post.objects.filter(draft=False).order_by('-post_time')
        comments=PostComment.objects.all()
        postform = AddPostForm
        albumfrom = AlbumForm
        imageform = ImageForm
        adform = AdsForm
        pollform = CreatePollForm
        return render(request, 'just-connect/post.html', {'posts': posts,'pollForm':pollform,'profile': profile,'liked':True, 'comments':comments,'postform':postform,'formset':imageform, 'adform':adform, 'albumform':albumfrom })
    else:
        return redirect('/userdetail/login')

def ProductPricingList(product,points,user): #find or add new commercial product with >= minpoints
    newproduct = PostProductPricing.objects.filter(post=product)
    if not newproduct:
        newproduct = PostProductPricing(post=product,mrp=points.default_mrp)
        newproduct.save()
        ProductBooking(users=product.post_by,product=newproduct).save()
    else:
        return newproduct[0]
    return newproduct

def checkPoints(productpost,user): #add points with each like,share and comments
    try:
        points = CommercialProductPoints.objects.get(product_type=productpost.post_type)
    except Exception:
        return False
    if productpost.points >= points.min_booking_points:
        product = ProductPricingList(productpost,points,user)
        return product

def cProductOrdersIndex(request): #commercial product order index
    postform = AddPostForm
    albumfrom = AlbumForm
    adform = AdsForm
    profile = User.objects.get(email=detail.objects.filter(email=request.user.email).first())
    product = PostProductPricing.objects.filter(accepting_booking=True).filter(booking_last_till__gte=date.today()).order_by('-post')
    post=[]
    for i in product:
        post.append(i.post) 
    comments=PostComment.objects.all()
    return render(request,'just-connect/post.html', {'product':product,'posts':post,'profile': profile,'comments':comments,'postform':postform,'adform':adform, 'albumform':albumfrom})

def PostDetailView(request,pk):
    print('detailview',request.GET.get('fbclid'))
    instance = detail.objects.filter(email=request.user.email).first()
    print(instance)
    if instance:
        profile = User.objects.get(email=instance)
    else:
        profile = request.user
    post = Post.objects.filter(id=pk)
    comments = PostComment.objects.all()
    return render(request, 'just-connect/post_detail.html', 
        {'posts': post, 'profile': profile, 'comments':comments})

def PostEditView(request,pk):
    post = Post.objects.get(id=pk)
    postform = AddPostForm
    adform = AdsForm
    albumform = AlbumForm
    form = None
    postformdata = None
    formdata = None
    if post.post_type.category_name == 'Ad':
        form = AdsForm(instance=post.ad)
    elif post.post_type.category_name =='Post':
        form = AddPostForm(instance = post)
    elif post.post_type.category_name == 'Album':
        form = AlbumForm(instance = post.album)

    if request.method == "POST":
        if post.post_type.category_name == 'Ad':
            formdata = AdsForm(request.POST, request.FILES, instance = post.ad)
        elif post.post_type.category_name == 'Post':
            postformdata = AddPostForm(request.POST, request.FILES, instance = post)
        elif post.post_type.category_name == 'Album':
            formdata = AlbumForm(request.POST, request.FILES, instance = post.album)

        if postformdata is not None and postformdata.is_valid :
            epost = postformdata.save()
            post.description = epost.description
            post.post_title = epost.post_title
            post.save()     
       
        if formdata is not None and formdata.is_valid:
            epost = formdata.save()
            post.description = epost.description
            post.post_title = epost.title
            post.save()

        return redirect('postdetail',pk=pk)
        

    return render(request, 'just-connect/edit_post.html',
        {'form':form,'post':post,'postform':postform,'adform':adform, 'albumform':albumform})

def draftIndex(request):
    postform = AddPostForm
    albumfrom = AlbumForm
    adform = AdsForm
    profile = User.objects.get(email=detail.objects.filter(email=request.user.email).first())
    post = Post.objects.filter(draft=True).order_by('-post_time')
    comments=PostComment.objects.all()
    return render(request,'just-connect/post.html', {'posts':post,'profile': profile,'comments':comments,'postform':postform,'adform':adform, 'albumform':albumfrom})

def cProductIndex(request):
    postform = AddPostForm
    albumfrom = AlbumForm
    adform = AdsForm
    profile = User.objects.get(email=detail.objects.filter(email=request.user.email).first())
    post = Post.objects.filter(commercial_post=True).order_by('-post_time')
    comments=PostComment.objects.all()
    return render(request,'just-connect/post.html', {'posts':post,'profile': profile,'comments':comments,'postform':postform,'adform':adform, 'albumform':albumfrom})

def BookmarkIndex(request):
    postform = AddPostForm
    albumfrom = AlbumForm
    adform = AdsForm
    profile = User.objects.get(email=detail.objects.filter(email=request.user.email).first())
    bookmarks = Bookmark.objects.filter(user=profile)[0]
    post=bookmarks.posts.all()
    print(post)
    comments=PostComment.objects.all()
    return render(request,'just-connect/post.html', {'posts':post,'profile': profile,'comments':comments,'bookmarks':bookmarks,'postform':postform,'adform':adform, 'albumform':albumfrom})

def addBookmark(request,pk):
    user = User.objects.get(email=detail.objects.filter(email=request.user.email).first())
    post = Post.objects.filter(id=pk)[0]
    if not Bookmark.objects.filter(user=user):
        Bookmark(user=user).save()
    bookmarks = Bookmark.objects.filter(user=user)[0]
    print(bookmarks.posts.all())
    if post in bookmarks.posts.all():
        bookmarks.posts.remove(post.id)
    else:
        bookmarks.posts.add(post.id)
    return redirect(f'/connect/#post')

def createPost(request):
    if request.method=='POST':
        postform = AddPostForm(request.POST,request.FILES or None)
        pollform = CreatePollForm(request.POST or None)
        adform = AdsForm(request.POST,request.FILES or None)
        albumform = AlbumForm(request.POST,request.FILES or None)
        post_type = request.POST.get("postType")

        postype = PostType.objects.filter(category_name=post_type)
        if not postype:
            postype = PostType(category_name=post_type)
            postype.save()
        else:
            postype = postype[0]
        #formset = PostImageForm(request.POST, request.FILES)
        email = detail.objects.filter(email=request.user.email)[0]
        post_by =  User.objects.get(email=email)
        if post_type == "Ad" and adform.is_valid():
            cd = adform.cleaned_data
            if Ad.objects.filter(title = cd['title']):
                ad = Ad.objects.get(title = cd['title'])
            else:
                ad = adform.save(commit = False)
                ad.user = post_by
                ad.save()
            post = Post(user=email,post_by=post_by,post_title=ad.title,description=ad.description,post_type=postype,ad = ad)
            post.save()
            files = request.FILES.getlist('image')
            for image in files:
                try:
                    photo = Image(user = post_by, image = image, title= post.post_title)
                    photo.save()
                    post.image.add(photo)
                    ad.image.add(photo)
                except:
                    return redirect(f'/connect/#post')
        
        elif post_type =="Album" and albumform.is_valid():
            #for fetching data from django form cleaned_data function is used 
            cd = albumform.cleaned_data
            if Album.objects.filter(title=cd['title']):
                album = Album.objects.get(title=cd['title'])
            else:
                album = albumform.save(commit=False)
                album.user = post_by
                album.save()
            post = Post(user=email,post_by=post_by,post_title=album.title,description=album.description,post_type=postype,album=album)
            post.save()
            files = request.FILES.getlist('image')
            for image in files:
                try:
                    #print(image)
                    photo = Image(user=post_by,image=image,title=post.post_title)
                    photo.save()
                    post.image.add(photo)
                    album.images.add(photo)
                except Exception as e:
                    print(e)
                    break  

        elif post_type=="Post" and postform.is_valid() and pollform.is_valid():
            post = postform.save(commit=False)
            postPoll = pollform.save(commit=False)
            postPoll.save()
            post.user = email            
            post.post_by = post_by 
            post.post_type=postype
            post.post_pull = postPoll           
            post.save()
            files = request.FILES.getlist('image')
            if len(files) > 2:
                album=Album(user=post_by,title=post.post_title,description=post.description)
                album.save()
            #print('images',request.FILES.getlist('image'),request.FILES)
            for image in files:
                try:
                    #print(image)
                    photo = Image(user=post_by,image=image,title=post.post_title)
                    photo.save()
                    post.image.add(photo)
                    if len(files)>2:
                        album.images.add(photo)
                except Exception as e:
                    print(e)
                    break 
        else:
            messages.add_message(request, 'Form is not valid')
            redirect(f'/connect/#post')
                           
            #print(post)
        
    return redirect(f'/connect/#post')

def submit_poll(request):
    if request.method=="POST":
        #fetching the logged in user
        email = detail.objects.filter(email=request.user.email)[0]
        user = User.objects.filter(email=email).first()
        #fetching the values which were send form ajax
        poll_id = request.POST.get('poll_id')
        selected_option = request.POST.get('poll_answer')
        #fetching the poll for which option is submitted
        current_poll = PostPoll.objects.get(id = poll_id)
        #fetching the status is user already answered the poll or not
        poll_user = PostPollPoints.objects.filter(user = user , poll = current_poll).first()
        #if user is not present in postpollpoints table then run following
        if poll_user is None:
            poll = PostPoll.objects.filter(id = poll_id).first()
            poll_points = PostPollPoints(user = user, poll = poll, selected_option = selected_option)
            poll_points.save()
            print(poll)
            print(poll.option_one_count)
            print(selected_option)
            print(poll_id)
            if selected_option == 'option1':
                poll.option_one_count += 1
            elif selected_option == 'option2':
                poll.option_two_count += 1
            else:
                return JsonResponse({"message":"Wrong form information  !"})
            poll.user = user
            poll.save()
            print(poll.option_one_count)
            post_poll = PostPoll.objects.values()
            post_poll = list(post_poll)
            print(post_poll)
            return JsonResponse({"post_poll":post_poll,"message":"Thanku for Polling !"})
        #if user is present / already answered then run this
        else:
            return JsonResponse({"message":"You have already votes"})

def Draft(request):
    if request.method =='POST':
        postform = AddPostForm(request.POST,request.FILES or None)
        print(postform)
        cd = postform.cleaned_data
        print(cd)
        adform = AdsForm(request.POST,request.FILES or None)
        albumform = AlbumForm(request.POST)
        post_type = request.POST.get("postType")
        #formset = PostImageForm(request.POST, request.FILES)
        postype = PostType.objects.filter(category_name=post_type)
        if not postype:
            postype = PostType(category_name=post_type)
            postype.save()
        email = detail.objects.filter(email=request.user.email)[0]
        post_by =  User.objects.get(email=email)
        if post_type =="Ad" and adform.is_valid():
            ad = adform.save(commit=False)
            ad.user = post_by
            image = request.FILES.getlist('image')
            ad.image = image
            ad.save()
            post = Post(user=email,post_by=post_by,post_title=ad.title,description=ad.description,post_type=postype[0],ad=ad)
            post.draft=True
            post.save()
        
        elif post_type =="Album" and albumform.is_valid():
            album = albumform.save(commit=False)
            album.user = post_by
            album.save()
            post = Post(user=email,post_by=post_by,post_title=album.title,description=album.description,post_type=postype[0],album=album)
            post.draft=True
            post.save()
            files = request.FILES.getlist('image')
            for image in files:
                try:
                    #print(image)
                    photo = Image(user=post_by,image=image,title=post.post_title)
                    photo.save()
                    post.image.add(photo)
                    album.images.add(photo)
                except Exception as e:
                    print(e)
                    break  

        elif post_type=="Post" and postform.is_valid():
            post = postform.save(commit=False)
            post.user = email            
            post.post_by = post_by 
            post.post_type=postype[0]          
            post.draft=True
            post.save()
            files = request.FILES.getlist('image')
            if len(files) > 2:
                album=Album(user=post_by,title=post.post_title,description=post.description)
                album.save()
            #print('images',request.FILES.getlist('image'),request.FILES)
            for image in files:
                try:
                    #print(image)
                    photo = Image(user=post_by,image=image,title=post.post_title)
                    photo.save()
                    post.image.add(photo)
                    if len(files)>2:
                        album.images.add(photo)
                except Exception as e:
                    print(e)
                    break 
                           
            #print(post)
        
    return redirect(f'/connect/#post')

def postDraft(request,pk=None):
    post = Post.objects.get(id=pk)
    post.draft = False
    post.save()
    return redirect(f'/connect/#post')

def Booking(request):
    post = get_object_or_404(Post, id=request.POST.get('postid'))
    instance = detail.objects.filter(email=request.user.email)[0]
    user = User.objects.get(email=instance)
    product = PostProductPricing.objects.get(post=post)
    print(product)
    if product.bookings.filter(id=user.id).exists():
        message = 'Already Booked'
    elif product.total_booking >= product.max_bookings:
        message = "Out of stock"
    else:
        cost = product.mrp * len(product.bookings.all()) / 100
        cost = product.mrp if cost > product.mrp else cost
        update_total_booking = product.total_booking + 1
        ProductBooking(users=user,product=product,cost=cost).save()
        message = 'Successfull!'
    print('message',message)
    return JsonResponse({'message':message,'postid':request.POST.get('postid')})

def order_product(request):
    instance = detail.objects.filter(email=request.user.email)[0]
    user = User.objects.get(email=instance)
    products = ProductBooking.objects.filter(users= user)
    print(products)
    context={
        "products":products,
    }
    return render(request, template_name="just-connect/order.html",context=context ) 
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('postid'))
    instance = detail.objects.filter(email=request.user.email)[0]
    points = CommercialProductPoints.objects.filter(product_type=post.post_type).first()
    #print(post.liked_by.filter(id=User.objects.get(email=instance).id))
    liked=False
    if post.liked_by.filter(id=User.objects.get(email=instance).id).exists():
        post.liked_by.remove(User.objects.get(email=instance).id)
        liked=False
    else:
        post.liked_by.add(User.objects.get(email=instance).id)
        liked=True
    return JsonResponse({'liked':liked,'total_likes':post.total_like(),'postid':request.POST.get('postid'),})

def share_post(request):
    post = get_object_or_404(Post, id=request.POST.get('postid'))
    user = User.objects.get(email=detail.objects.filter(email=request.user.email)[0])
    points = CommercialProductPoints.objects.filter(product_type=post.post_type)
    if points:
        points=points[0]
        post.points+=points.share
        post.save()
        checkPoints(post,user)
        return JsonResponse({'message':'success'})
    return JsonResponse({'message':'Post type not listed'})

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = User.objects.get(email=detail.objects.filter(email=request.user.email)[0])
        postID = request.POST.get("postID")
        #print(postID)
        post = Post.objects.get(id=postID)
        points = CommercialProductPoints.objects.filter(product_type=post.post_type).first()
        parentID = request.POST.get("parentID")

        if parentID == "":
            comment = PostComment(
                comment=comment,
                user=user,
                post=post
            )
        else:
            print(post,parentID)
            parent = PostComment.objects.get(id=parentID)
            comment = PostComment(
                comment=comment,
                user=user,
                post=post,
                parent=parent
            )

        comment.save()
        if points:
            new_points = post.points + points.comments
            post.points = new_points 
            post.save()
            checkPoints(post,user)
        else:
            print('Post type/category has points.')

    return redirect(f'/connect/')

def deletePost(request,pk=None):
    post=Post.objects.get(id=pk)
    post.delete()
    return redirect(f'/connect/')



def member_profile(request):
    if request.user.is_authenticated:
        instance = detail.objects.filter(email=request.user.email).first()
        if request.POST.get('action') == 'gotoprofile':
            name = request.POST.get('p_name')
            print(name)
            member = detail.objects.get(name=name)
            profile = User.objects.get(name=name)
            print(member)
            member_id = member.id
            profile_id = profile.id
            return JsonResponse({'member': member_id, 'profile': profile_id})

        if request.GET.get('member'):
            member_id = request.GET.get('member')
            profile_id = request.GET.get('profile')
            member = detail.objects.get(id=member_id)
            follow = User.objects.get(email=instance.id)
            profile = User.objects.get(id=profile_id)
            friends = False
            f = []
            for friend in profile.friends.all():
                f.append(friend.email)
            if instance.email in f:
                friends = True
            post = Post.objects.filter(post_by=profile.id)
            return render(request, 'just-connect/member-profile.html', {'member': member, 'profile': profile, 'friends': friends, 'instance': instance, 'post': post})

        if request.POST.get('action') == 'visit_profile':
            instance_email = request.POST.get('instance')
            member = detail.objects.get(email=instance_email)
            profile = User.objects.get(email=member.id)
            member_id = member.id
            profile_id = profile.id
            follow = User.objects.get(email=instance.id)
            friends = False
            f = []
            for friend in profile.friends.all():
                f.append(friend.email)
            if instance.email in f:
                friends = True
            print(f)
            return JsonResponse({'member': member_id, 'profile': profile_id})
            return render(request, 'just-connect/member-profile.html', {'member': member, 'profile': profile, 'friends': friends, 'instance': instance})


def events(request):
    if request.user.is_authenticated:
        user = detail.objects.get(email=request.user.email)
        currentUser = User.objects.get(email=user)
        time_threshold = datetime.now() - timedelta(hours=5)
        Events = Events.objects.filter(Q(date=now.date(), time__gte=now.time()) | Q(
            date__gt=now.date())).order_by('-date')
    return render(request, 'just-connect/events.html')


def event_detail_view(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Events, slug=slug)
        hosted_by_some_other_user = False
        user = detail.objects.get(email=request.user.email)
        currentUser = User.objects.get(email=user)
        if instance.hosted_by != currentUser:
            hosted_by_some_other_user = True

        context_data = {'event': instance,
                        'intrested': hosted_by_some_other_user}
        return render(request, 'just-connect/event_detail.html', context_data)


def update_event(request, slug):
    instance = get_object_or_404(Events, slug=slug)
    form = EventForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context_data = {"data": "your event was changed"}
        return render(request, 'just-connect/event_info.html', context_data)
    return render(request, 'just-connect/event_create.html', {'form': form, 'slug': slug})


@csrf_exempt
def create_event_view(request):
    if request.user.is_authenticated:
        print("user is  auth")
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                user = detail.objects.get(email=request.user.email)
                currentUser = User.objects.get(email=user)
                event.hosted_by = currentUser  # if I need to do something before saving it
                event.save()
                context_data = {"data": "your event added"}
                return redirect('connect-upcoming-list')
            else:
                form = EventForm()
                context_data = {'form': form}
                return render(request, 'just-connect/news_form.html', context_data)

        else:
            form = EventForm()
            context_data = {'form': form}
            return render(request, 'just-connect/event_create.html', context_data)
    else:
        return redirect('/userdetail/login')


def event_detail_view(request, slug):
    if request.user.is_authenticated:
        instance = get_object_or_404(Events, slug=slug)
        hosted_by_some_other_user = False
        user = detail.objects.get(email=request.user.email)
        currentUser = User.objects.get(email=user)
        if instance.hosted_by != currentUser:
            hosted_by_some_other_user = True

        context_data = {'event': instance,
                        'intrested': hosted_by_some_other_user}
        return render(request, 'just-connect/event_detail.html', context_data)


def events_manage(request):
    context_data = {}
    if request.user.is_authenticated:
        user = detail.objects.get(email=request.user.email)
        currentUser = User.objects.get(email=user)
        event_hostedlist = Events.objects.filter(hosted_by=currentUser)
        event_not_hosted_by_user = Events.objects.filter(
            ~Q(hosted_by=currentUser))

        context_data = {"hosted_list": event_hostedlist,
                        "upcoming event": event_not_hosted_by_user}

        print(context_data)
    return render(request, 'just-connect/events_manage.html', context_data)


def get_profiles(request):
    if request.user.is_authenticated:
        if request.POST.get('action') == 'get_profiles':
            instance = detail.objects.filter(email=request.user.email).first()
            profiles = []
            profile = User.objects.all()
            for i in profile:
                if instance.name == i.name:
                    print('matched')
                else:
                    profiles.append(i.name)
            return JsonResponse({'profiles': profiles})


def my_profile(request):
    if request.user.is_authenticated:
        
        
        instance = detail.objects.filter(email=request.user.email).first()
        profile = User.objects.get(email=instance)
        public_projects = Portfolio_Project.objects.filter(user =profile)
        private_projects = Portfolio_Project.objects.filter(user = profile, visibility="PRIVATE")
        # edit_form = edit_profile(instance=profile, prefix=profile.id)
        postype =  PostType.objects.get(category_name = 'Post')
        post = Post.objects.filter(post_by=profile.id, post_type=postype.id)
        album = Album.objects.filter(user =profile)
        ad = Ad.objects.filter(user = profile )
        print(post)
        # if request.POST.get('submit'):
        #     instance_id = request.POST.get('submit')
        #     edit = User.objects.get(pk=instance_id)
        #     editedform = edit_profile(request.POST, instance=edit, prefix=instance_id)
        #     if editedform.is_valid():
        #         editedform.save()
        #     else:
        #         print('Profile edit form error: ', editedform.errors)
        # 'edit_form': edit_form,
        education = instance.education_details.all()
        education_form = Education_Form()
        education_edit = []
        education_check = False
        for edetail in education:
            education_check = True
            temp_form = Education_Form(instance=edetail, prefix=edetail.id)
            education_edit.append([edetail, temp_form])
        if request.POST.get('submit') == 'edu_form':
            edu_form = Education_Form(request.POST)
            if edu_form.is_valid():
                e_form = edu_form.save()
                e_form.created_by = instance
                e_form.save()
            else:
                print('ED FORM ERRORS ',edu_form.errors)
            return redirect('my_profile')
        if request.POST.get('edit_edu_profile'):
            instance_id = request.POST.get('edit_edu_profile')
            instance = Education_Qualification.objects.get(pk=instance_id)
            editedFormEdu = Education_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormEdu.is_valid():
                editedFormEdu.save()
            else:
                print('EDIT EDUCATION FORM ERRORS', editedFormEdu.errors)
            return redirect('my_profile')
        
        job = instance.job_details.all()
        job_form = Job_Profile_Form()
        job_edit = []
        job_check = False
        for jdetail in job:
            job_check = True
            temp_form = Job_Profile_Form(instance=jdetail, prefix=jdetail.id)
            job_edit.append([jdetail, temp_form])
        if request.POST.get('submit') == 'job_form':
            job_form1 = Job_Profile_Form(request.POST)
            if job_form1.is_valid():
                j_form = job_form1.save()
                j_form.created_by = instance
                j_form.save()
            else:
                print('Job FORM ERRORS ',job_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_job_profile'):
            instance_id = request.POST.get('edit_job_profile')
            instance = Profile_Jobs.objects.get(pk=instance_id)
            editedFormJob = Job_Profile_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormJob.is_valid():
                editedFormJob.save()
            else:
                print('EDIT EDUCATION FORM ERRORS', editedFormJob.errors)
            return redirect('my_profile')
        
        internship = instance.intern_details.all()
        intern_form = Internship_Profile_Form()
        intern_edit = []
        internship_check = False
        for idetail in internship:
            internship_check = True
            temp_form = Internship_Profile_Form(instance=idetail, prefix=idetail.id)
            intern_edit.append([idetail, temp_form])
        if request.POST.get('submit') == 'internship_form':
            internship_form1 = Internship_Profile_Form(request.POST)
            if internship_form1.is_valid():
                i_form = internship_form1.save()
                i_form.created_by = instance
                i_form.save()
            else:
                print('Internship FORM ERRORS ',internship_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_internship_profile'):
            instance_id = request.POST.get('edit_internship_profile')
            instance = Profile_Internship.objects.get(pk=instance_id)
            editedFormInternship = Internship_Profile_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormInternship.is_valid():
                editedFormInternship.save()
            else:
                print('EDIT Internship FORM ERRORS', editedFormInternship.errors)
            return redirect('my_profile')
        
        training = instance.training_details.all()
        training_form = Profile_Training_Form()
        training_edit = []
        training_check = False
        for tdetail in training:
            training_check = True
            temp_form = Profile_Training_Form(instance=tdetail, prefix=tdetail.id)
            training_edit.append([tdetail, temp_form])
        if request.POST.get('submit') == 'training_form':
            training_form1 = Profile_Training_Form(request.POST)
            if training_form1.is_valid():
                t_form = training_form1.save()
                t_form.created_by = instance
                t_form.save()
            else:
                print('Training FORM ERRORS ',training_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_training_profile'):
            instance_id = request.POST.get('edit_training_profile')
            instance = Profile_Training.objects.get(pk=instance_id)
            editedFormTraining = Profile_Training_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormTraining.is_valid():
                editedFormTraining.save()
            else:
                print('EDIT Training FORM ERRORS', editedFormTraining.errors)
            return redirect('my_profile')
        
        project = instance.project_details.all()
        project_form = Project_Form()
        project_edit = []
        project_check = False
        for pdetail in project:
            project_check = True
            temp_form = Project_Form(instance=pdetail, prefix=pdetail.id)
            project_edit.append([pdetail, temp_form])
        if request.POST.get('submit') == 'project_form':
            project_form1 = Project_Form(request.POST)
            if project_form1.is_valid():
                p_form = project_form1.save()
                p_form.created_by = instance
                p_form.save()
            else:
                print('Project FORM ERRORS ',project_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_project_profile'):
            instance_id = request.POST.get('edit_project_profile')
            instance = Profile_Project.objects.get(pk=instance_id)
            editedFormProject = Project_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormProject.is_valid():
                editedFormProject.save()
            else:
                print('EDIT Project FORM ERRORS', editedFormProject.errors)
            return redirect('my_profile')
        
        skill = instance.skill_details.all()
        skill_form = Profile_Skills_Form()
        skill_edit = []
        skill_check = False
        for sdetail in skill:
            skill_check = True
            temp_form = Profile_Skills_Form(instance=sdetail, prefix=sdetail.id)
            skill_edit.append([sdetail, temp_form])
        if request.POST.get('submit') == 'skill_form':
            skill_form1 = Profile_Skills_Form(request.POST)
            if skill_form1.is_valid():
                s_form = skill_form1.save()
                s_form.created_by = instance
                s_form.save()
            else:
                print('Skill FORM ERRORS ',skill_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_skill_profile'):
            instance_id = request.POST.get('edit_skill_profile')
            instance = Profile_Skills.objects.get(pk=instance_id)
            editedFormSkill = Profile_Skills_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormSkill.is_valid():
                editedFormSkill.save()
            else:
                print('EDIT Skill FORM ERRORS', editedFormSkill.errors)
            return redirect('my_profile')
        
        worksample = instance.work_sample_details.all()
        worksample_form = Work_Sample_Form()
        worksample_edit = []
        worksample_check = False
        for wdetail in worksample:
            worksample_check = True
            temp_form = Work_Sample_Form(instance=wdetail, prefix=wdetail.id)
            worksample_edit.append([wdetail, temp_form])
        if request.POST.get('submit') == 'worksample_form':
            worksample_form1 = Work_Sample_Form(request.POST)
            if worksample_form1.is_valid():
                w_form = worksample_form1.save()
                w_form.created_by = instance
                w_form.save()
            else:
                print('Work Sample FORM ERRORS ',worksample_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_worksample_profile'):
            instance_id = request.POST.get('edit_worksample_profile')
            instance = Profile_WorkSamples.objects.get(pk=instance_id)
            editedFormWorksample = Work_Sample_Form(request.POST, instance=instance, prefix=instance_id)
            if editedFormWorksample.is_valid():
                editedFormWorksample.save()
            else:
                print('EDIT Work Sample FORM ERRORS', editedFormWorksample.errors)
            return redirect('my_profile')
        
        social = instance.profile_social.all()
        social_form = SocialForm()
        social_edit = []
        social_check = False
        for sdetail in social:
            social_check = True
            temp_form = SocialForm(instance=sdetail, prefix=sdetail.id)
            social_edit.append([sdetail, temp_form])
        if request.POST.get('submit') == 'social_form':
            social_form1 = SocialForm(request.POST)
            if social_form1.is_valid():
                s_form = social_form1.save()
                s_form.created_by = instance
                s_form.save()
            else:
                print('Social FORM ERRORS ',social_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_social_profile'):
            instance_id = request.POST.get('edit_social_profile')
            instance = Social_Profile.objects.get(pk=instance_id)
            editedFormSocial = SocialForm(request.POST, instance=instance, prefix=instance_id)
            if editedFormSocial.is_valid():
                editedFormSocial.save()
            else:
                print('EDIT Social FORM ERRORS', editedFormSocial.errors)
            return redirect('my_profile')

        medical = instance.profile_medical.all()
        medical_form = MedForm()
        medical_edit = []
        medical_check = False
        for mdetail in medical:
            medical_check = True
            temp_form = MedForm(instance=mdetail, prefix=mdetail.id)
            medical_edit.append([mdetail, temp_form])
        if request.POST.get('submit') == 'medical_form':
            medical_form1 = MedForm(request.POST)
            if medical_form1.is_valid():
                m_form = medical_form1.save()
                m_form.created_by = instance
                m_form.save()
            else:
                print('Medical FORM ERRORS ',medical_form1.errors)
            return redirect('my_profile')
        if request.POST.get('edit_medical_profile'):
            instance_id = request.POST.get('edit_medical_profile')
            instance = Medical_Profile.objects.get(pk=instance_id)
            editedFormMedical = MedForm(request.POST, instance=instance, prefix=instance_id)
            if editedFormMedical.is_valid():
                editedFormMedical.save()
            else:
                print('EDIT Medical FORM ERRORS', editedFormMedical.errors)
            return redirect('my_profile')

        print(intern_edit)
        data = {'education': education, 'job': job, 'internship': internship, 'training': training, 'project': project, 'skills': skill, 'worksmaple': worksample, 'social': social, 'medical': medical}
        return render(request, 'just-connect/my-profile.html', {'profile': profile, 'instance': instance, 'posts': post, 'data': data,'albums':album, 'ads':ad, 'education_check': education_check, 'education_form': education_form, 'education_edit': education_edit, 'job_check': job_check, 'job_form': job_form, 'job_edit': job_edit, 'internship_check': internship_check, 'internship_form': intern_form, 'internship_edit': intern_edit, 'training_check': training_check, 'training_form': training_form, 'training_edit': training_edit, 'project_check': project_check, 'project_form': project_form, 'project_edit': project_edit, 'skill_check': skill_check, 'skill_form': skill_form, 'skill_edit': skill_edit, 'worksample_check': worksample_check, 'worksample_form': worksample_form, 'worksample_edit': worksample_edit, 'social_check': social_check, 'social_form': social_form, 'social_edit': social_edit, 'medical_check': medical_check, 'medical_form': medical_form, 'medical_edit': medical_edit,'public_projects':public_projects,'private_project':private_projects})


def my_profile_edit(request):
    instance = detail.objects.filter(email=request.user.email).first()
    profile = User.objects.get(email=instance)
    if request.method == 'POST':
        form = detailForm(request.POST, request.FILES, instance=instance, prefix=instance.id)
        if form.is_valid():
            form.save()
            return render(request, 'just-connect/my-profile-edit.html', {'instance':instance, 'profile':profile,})
    else:
        form = detailForm(request.POST, request.FILES, instance=instance, prefix=instance.id)

    return render(request, 'just-connect/my-profile-edit.html', {'instance':instance, 'profile':profile, 'form':form})

def upcomming_events_view(request):
    today = datetime.today()
    upcoming_events = Events.objects.filter(
        Q(start_time__gte=today)).order_by('-start_time')
    print(upcoming_events)
    context_data = {"hosted_list": upcoming_events}
    return render(request, 'just-connect/events_upcomming.html', context_data)


def news_list_view(request):
    news_list = News.objects.all()
    context_data = {'news_list': news_list}
    return render(request, 'just-connect/news_list.html', context_data)


def news_detail_view(request, slug):
    if request.user.is_authenticated:
        news = get_object_or_404(News, slug=slug)
        newsallcomment = NewsComment.objects.filter(news=news)
        user = detail.objects.get(email=request.user.email)
        currentUser = User.objects.get(email=user)
        context_data = {}
        if request.method == 'POST':
            form = NewsCommentForm(request.POST)
            if form.is_valid():
                newsComment = form.save(commit=False)
                user = detail.objects.get(email=request.user.email)
                currentUser = User.objects.get(email=user)
                newsComment.author = currentUser
                newsComment.news = news
                newsComment.save()
                return redirect('connect-news-detail', slug=news.slug)
        else:
            form = NewsCommentForm()
        context_data = {'news': news, 'form': form,
                        'allcomment': newsallcomment}
        return render(request, 'just-connect/news_detail.html', context_data)


@csrf_exempt
def news_create_view(request):
    if request.user.is_authenticated:
        print("user is  auth")
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                news = form.save(commit=False)
                user = detail.objects.get(email=request.user.email)
                currentUser = User.objects.get(email=user)
                news.user = currentUser
                print(request.FILES)
                news.save()
                context_data = {"data": "your event added"}
                return render(request, 'just-connect/news_form.html', context_data)
        else:
            form = NewsForm()
        context_data = {'form': form}
        return render(request, 'just-connect/news_form.html', context_data)


def news_update_view(request, slug):
    instance = get_object_or_404(News, slug=slug)
    form = NewsForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context_data = {"data": "your event was changed"}
        return render(request, 'just-connect/event_info.html', context_data)
    return render(request, 'just-connect/event_create.html', {'form': form, 'slug': slug})



def follow(request):
    if request.POST.get('action') == 'follow':
        instance_id = request.POST.get('instance_id')
        profile_id = request.POST.get('profile_id')
        profile = User.objects.get(id=profile_id)
        profile.friends.add(instance_id)
        profile.save()
        return JsonResponse({'response': 'done', })

def page_create_view(request):
    if request.user.is_authenticated:
        print("user is  auth")
        if request.method == 'POST':
            form = PageForm(request.POST, request.FILES)
            if form.is_valid():
                page = form.save(commit=False)
                user = detail.objects.get(email=request.user.email)
                currentUser = User.objects.get(email=user)
                page.admin = currentUser  # if I need to do something before saving it
                page.save()

                return redirect('connect-upcoming-list')
            else:
                form = PageForm(request.POST, request.FILES)
                context_data = {'form': form}
                return render(request, 'just-connect/page_create.html', context_data)

        else:
            form = PageForm()
            context_data = {'form': form}
            return render(request, 'just-connect/page_create.html', context_data)
    else:
        return redirect('/userdetail/login')

def page_edit_view(request, slug):
    instance = get_object_or_404(Page, slug=slug)
    form = PageForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context_data = {"data": "your event was changed"}
        return render(request, 'just-connect/event_info.html', context_data)
    return render(request, 'just-connect/page_create.html', {'form': form})

def page_home_view(request,slug):
    if request.user.is_authenticated:
        url = request.resolver_match.url_name
        print(url)
        page = get_object_or_404(Page, slug=slug)
        user = detail.objects.get(email=request.user.email)
        print(page.name)
        currentUser = User.objects.get(email=user)
        context_data = {'page': page}
        return render(request, 'just-connect/pages/about.html', context_data)

def page_detail_view(request, slug):
    if request.user.is_authenticated:
        page = get_object_or_404(Page, slug=slug)
        user = detail.objects.get(email=request.user.email)
        print(page.name)
        currentUser = User.objects.get(email=user)
        context_data = {'page': page, "currentUser": currentUser}
        return render(request, 'just-connect/page_detail.html', context_data)


#view for showing project
def project_view(request,slug):
    project = Portfolio_Project.objects.filter(slug = slug).first()
    data = {
        'project':project,
    }
    return render(request, template_name="just-connect/project_view.html",context=data)

#view for showing all public project on one page
def discoverProject(request):
    categories = ProjectCategory.objects.all()
    cat_value= request.GET.get('value');
    print(cat_value)
    if cat_value is None:
        projects = Portfolio_Project.objects.filter(visibility = "PUBLIC")
        data = {
        'projects':projects,
        'categories':categories,
        }
        return render(request, template_name="just-connect/discover.html",context=data)  
    else:
        if cat_value == "all":
            projects = Portfolio_Project.objects.values()
            cat_projects = list(projects)
            return JsonResponse({'projects':cat_projects})
        else:
            projects = Portfolio_Project.objects.values().filter(category__icontains = cat_value)
            cat_projects = list(projects)
            return JsonResponse({'projects':cat_projects})

def project_feed(request):
    query = request.GET.get('search')
    if query is not None and query != '':
        #fetching all those tags which contains query
        tags_match = ProjectTags.objects.filter(Q(title__icontains = query))
        #fetching all those projects which contain query 
        allProjects = Portfolio_Project.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(
        user__name__icontains=query) | Q(category__icontains=query) | Q(tools__icontains=query)).exclude(visibility = "PRIVATE")
        for tags in tags_match:
            project =  tags.project
            project = Portfolio_Project.objects.filter(slug = project.slug)
            allProjects = allProjects | project
        print(allProjects)
        return render(request, template_name="just-connect/project_feed.html", context = {'projects':allProjects})
    else:
        allProjects = Portfolio_Project.objects.filter(visibility = "PUBLIC")
        return render(request, template_name="just-connect/project_feed.html", context = {'projects':allProjects})

#view for creating a project
def create_project(request):
    categories = ProjectCategory.objects.all()
    data={
        'categories':categories
    }
    if request.method == 'POST':
        #fetching value from ajax call
        user = detail.objects.get(email=request.user.email)
        project_user = User.objects.get(email = user)
        project_name = request.POST.get('project_name')
        project_content = request.POST.get('project_content')
        project_tools = request.POST.get('project_tools')
        project_visibility = request.POST.get('project_visibility')
        project_tags = request.POST.getlist('project_tags[]')
        project_category = request.POST.get('project_category')
        project_cover_image = request.POST.get('project_cover_image')
        
        #creating a object of Project model class
        project = Portfolio_Project()
        project.user = project_user
        project.title = project_name
        project.content = project_content
        project.tools = project_tools
        project.visibility = project_visibility
        project.category = project_category
        project.cover_image = project_cover_image
        project.save() #saving project object
        print(project)
        print("hello")

        project = Portfolio_Project.objects.filter(id = project.id).first()
        #iterating over project_tags array
        for tags_title in project_tags:
            try:
                print(tags_title)
                tags = ProjectTags()
                tags.project = project 
                tags.title = tags_title
                tags.save() #saving projectTags in the database
            except Exception as e:
                print(e)
                break  

        return redirect('my_profile')
    return render(request, template_name='just-connect/project_editor.html',context=data)

#view for user portfolio
def project_delete(request,slug):
    project = Portfolio_Project.objects.filter(slug = slug).first()
    project.delete()
    return redirect('my_profile')

def project_edit(request,slug):
    project = Portfolio_Project.objects.filter(slug = slug).first()
    tags = ProjectTags.objects.filter(project = project)
    categories = ProjectCategory.objects.all()
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_content = request.POST.get('project_content')
        project_tools = request.POST.get('project_tools')
        project_visibility = request.POST.get('project_visibility')
        project_tags = request.POST.getlist('project_tags[]')
        project_category = request.POST.get('project_category')
        project_cover_image = request.POST.get('project_cover_image')

        #saving the project data after edit
        project.title = project_name
        project.content = project_content
        project.tools = project_tools
        project.visibility = project_visibility
        project.category = project_category
        project.cover_image = project_cover_image
        project.save() #saving project object
        print(project)
        print("hello")

        project = Portfolio_Project.objects.filter(id = project.id).first()
        #deleting previous tags of the project
        for tag in tags:
            tag.delete()
        
        #inserting new tags in the array
        for tags_title in project_tags:
            try:
                print(tags_title)
                tags = ProjectTags()
                tags.project = project 
                tags.title = tags_title
                tags.save() #saving projectTags in the database
            except Exception as e:
                print(e)
                break  
        return redirect('my_profile')
    data = {
        'project':project,
        'tags':tags,
        'categories':categories,
        
    }
    return render(request, template_name = "just-connect/edit_project.html",context = data)

