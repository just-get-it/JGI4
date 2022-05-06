from django.db import models
from datetime import datetime, timedelta
from django.core.validators import URLValidator
from mptt.models import MPTTModel, TreeForeignKey
from userdetail.models import detail
import os
import random
from django.db.models.signals import pre_save
from .utlis import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

# def upload_profile_image_path(instance, filename):
#     new_filename = random.randint(1, 13516546431654)
#     name, ext = get_filename_ext(filename)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     return "local/just_connect/profile_pic/{final_filename}".format(
#         new_filename=new_filename,
#         final_filename=final_filename
#     )

# def upload_image_path(instance, filename):
#     new_filename = random.randint(1, 13516546431654)
#     name, ext = get_filename_ext(filename)
#     final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
#     return "local/just_connect/images/{final_filename}".format(
#         new_filename=new_filename,
#         final_filename=final_filename
#     )

# class JobFuncion(models.Model):
#     name = models.CharField(max_length=400)

# class IndianState(models.Model):
#     name = models.CharField(max_length=400)

# class UrlType(models.Model):
#     name =  models.CharField(max_length=400)

# class Website(models.Model):
#     url = models.URLField(max_length=400)
#     type = models.ManyToManyField(UrlType)

# class HashTag(models.Model):
#     # hashtag_name = models.CharField(max_length=200,validators=[RegexValidator('#(\w+)', message="Invalid Hashtag")]))
#     hashtag_name = models.CharField(max_length=200)
#     def __str__(self):
#         return "#"+ self.hashtag_name

# class Image(models.Model):
#     caption = models.CharField(max_length=400)
#     image = models.FileField(upload_to=upload_image_path, default='local/just_connect/profile_pic/def-2883257233.jpeg')

# class Address(models.Model):
#     shipping_address = models.CharField(max_length=255)
#     city = models.CharField(max_length=200)
#     state = models.CharField(max_length=200)
#     pin_code = models.CharField(max_length=200)

# class Website(models.Model):
#     link = models.URLField(max_length=400, null=True, blank=True)


# class Page(models.Model):
#     admins = models.ManyToManyField(detail, related_name='administered_pages')
#     title = models.CharField(max_length=400)
#     followers = models.ManyToManyField(detail, related_name='followed_pages')
#     capabilities = models.TextField()
#     highlights = models.ForeignKey(Image, blank=True)
#     company_founded_in = models.DateField(null=True, blank=True)
#     company_size = models.CharField(max_length=400, null=True, blank=True)
#     min_order = models.CharField(max_length=400, null=True, blank=True)
#     turnover = models.CharField(max_length=200, null=True, blank=True)
#     addresses = models.ManyToManyField(Address, related_name='page')
#     website = models.ManyToManyField(Website, related_name='page')
#     products = models.ManyToManyField(Image, blank=True)
#     customers = models.ManyToManyField(Image, blank=True)
#     production_facilities = models.ManyToManyField(Image, blank=True)
#     certificates = models.ManyToManyField(Image, blank=True)

# class JAccount(models.Model):
#     user = models.ForeignKey(detail, on_delete=models.CASCADE)
#     username = models.CharField(max_length = 100, primary_key=True)
#     type = models.ForeignKey(profile_type, on_delete=models.SET_NULL, null=True)
#     profile_pic = models.FileField(upload_to=upload_profile_image_path, default='local/just_connect/profile_pic/def-2883257233.jpeg')
#     job_function = models.ManyToManyField(JobFuncion)
#     # company_name = models.CharField(max_length=400, null=True, blank=True)
#     company_page = models.ManyToManyField(Page)
#     business_location = models.ManyToManyField(IndianStates, on_delete=models.SET_NULL, null=True)
#     headline = models.CharField(max_length=400, null=True, blank=True)
#     about = models.CharField(max_length=400, null=True, blank=True)
#     connections = models.ManyToManyField(delail)
#     websites = models.ManyToManyField(Website)
#     followed_hashtags = models.ManyToManyField(HashTag, related_name='followed_by')

# DELETED_ACCOUNT_ID = 1
# class Post(models.Model):
#     author = models.ForeignKey(detail, on_delete=models.SET_DEFAULT, default=DELETED_ACCOUNT_ID, related_name='written_posts')
#     title = models.CharField(max_length=400)
#     content = models.TextField()
#     hashtags = models.ManyToManyField(HashTag)
#     img_url = models.TextField(validators=[URLValidator()]) # https://drive.google.com/uc?id=FILE_ID https://drive.google.com/file/d/<file_id_here>/view?usp=sharing
#     video_url = models.TextField(validators=[URLValidator()]) # https://drive.google.com/uc?id=FILE_ID https://drive.google.com/file/d/10J-Dg4a3pgDVqlgMK4HSJSgO5GblJxsB/view?usp=sharing
#     file_url = models.TextField(validators=[URLValidator()])
#     shares = models.ManyToManyField("self")
#     archived_by = models.ManyToManyField(detail, related_name='archived_posts')
#     liked_by = models.ManyToManyField(detail, related_name='liked_posts')

# class Comment(MPTTModel):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(detail, on_delete=models.CASCADE, related_name='comments')
#     date = models.DateTimeField(auto_now_add=True)
#     liked_by = models.ManyToManyField(detail, related_name='liked_comments')
#     parent = TreeForeignKey(
#         'self',
#         on_delete=models.CASCADE,
#         null=True,
#         related_name="children",
#     )
#     class MPTTMeta:
#         order_insertion_by = ['date']
#     def __str__(self):
#         return self.comment[:15] + "... by " + str(self.author.username)

# class Report(models.Model):
#     reported_by = models.ForeignKey(detail, related_name="reports")
#     comment = models.ForeignKey(Comment, null=True, blank=True, related_name="reports")
#     cause = models.TextField()
#     on_post = models.BooleanField(default=False)
#     on_comment = models.BooleanField(default=False)

# class Event(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     hosts = models.ManyToManyField(detail, related_name='hosted_events')
#     start = models.DateTimeField()
#     end = models.DateTimeField(null=True, blank=True)
#     location_latitude = models.DecimalField(max_digits=10, decimal_places=7)
#     location_longitude = models.DecimalField(max_digits=10, decimal_places=7)
#     privacy = models.CharField(max_length=200)
#     guests = models.ManyToManyField(detail, related_name='attending_events')

# class Group(models.Model):
#     private = models.BooleanField(default=True)
#     title = models.CharField(max_length=400)
#     description = models.TextField()
#     rules = models.TextField()
#     private = models.BooleanField(default=False)
#     admins = models.ManyToManyField(detail, related_name='administered_groups')
#     events = models.ManyToManyField(Event)
#     members = models.ManyToManyField(detail, related_name='groups')

def news_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "local/just_connect/news/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename,
    )

# cover image path for portfolio image
def project_cover_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "local/just_connect/portfolio/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename,
    )

def event_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "local/just_connect/event/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename,
    )

def ads_image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "local/just_connect/Ads/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename,
    )

def image_path(instance, filename):
    new_filename = random.randint(1, 13516546431654)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "local/just_connect/images/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename,
    )

class User(models.Model):
    email = models.ForeignKey(
        detail, on_delete=models.CASCADE, related_name="social_profile")
    name = models.CharField(max_length=200, null=True, blank=True)
    friends = models.ManyToManyField(detail, blank=True)
    # req_rec = models.ManyToManyField(detail, max_length=200, blank=True)
    # req_sent = models.ManyToManyField(detail, max_length=200, blank=True)

    def __str__(self):
        return self.name

from .validators import *

def user_image_folder(instance, filename):
    return 'image/user_{0}/images/{1}'.format(instance.user.id, filename)

def user_adimage_folder(instance,filename):
    return 'image/user_{0}/ads/{1}'.format(instance.user.id, filename)

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to=user_image_folder, blank=True, null=True,validators=[validate_image_extension])

    def __str__(self):
        return os.path.basename(self.image.name)
    

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    def __str__(self):
        return self.title

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=400, null=True, blank=True)
    image = models.FileField(upload_to=user_adimage_folder,null=True, blank=True)

    def __str__(self):
        return self.title

class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    short_news = models.CharField(max_length=1000, null=True, blank=True)
    title = models.CharField(max_length=255)
    news = models.TextField()
    viewed_by = models.ManyToManyField(User, related_name="News_read_by_user")
    video = models.FileField(upload_to=news_image_path, null=True, blank=True)
    image = models.ImageField(upload_to=news_image_path, null=True, blank=True)
    liked_by = models.ManyToManyField(
        User, related_name="news_like_by", blank=True)
    slug = models.SlugField(null=True, blank=True)
    subscribe = models.ManyToManyField(
        User, related_name="news_subscriber", blank=True)

    def __str__(self):
        return self.title

    @property
    def totalViewed(self):
        return self.viewed_by.count()

    @property
    def totalLikes(self):
        return self.liked_by.count()


class NewsComment(MPTTModel):
    news = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='news_for_comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='news_auther')

    comment = models.TextField()
    liked_by = models.ManyToManyField(
        detail, related_name='liked_new_comments', blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name="children", blank=True
    )

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.comment[:15] + "... by " + str(self.author.name)


class Group(models.Model):
    email = models.ForeignKey(
        detail, on_delete=models.CASCADE, related_name="social_group")
    group_members = models.ManyToManyField(User)
    group_admin = models.BooleanField(default=False)
    group_name = models.CharField(max_length=200)
    group_desc = models.TextField()
    group_logo = models.FilePathField()

    def __str__(self):
        return self.group_name


class Page(models.Model):
    email = models.ForeignKey(
        detail, on_delete=models.CASCADE, related_name="social_page")
    page_admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_page")
    page_name = models.CharField(max_length=200)
    followers = models.ManyToManyField(User)
    page_description = models.TextField()
    page_logo = models.FilePathField()

    def __str__(self):
        return self.page_name

class AgendaTimeStampInfo(models.Model):
    startingTime = models.TimeField()
    endingTime = models.TimeField()
    task = models.TextField()
    done = models.BooleanField(default=False)
    remark = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.startingTime + "  " + self.endingTime


class Agenda(models.Model):
    day = models.DateField()
    tasks = models.ManyToManyField(AgendaTimeStampInfo)

    def __str__(self):
        return self.day


class Events(models.Model):
    hosted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_invite")
    event_name = models.CharField(max_length=200)
    Agenda = models.ManyToManyField(Agenda, blank=True)
    guest = models.TextField(null=True, blank=True)
    event_type = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    event_sort_description = models.TextField(null=True, blank=True)
    event_description = models.TextField()
    start_time = models.DateTimeField(null=True, blank=True)
    durations = models.TimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    view_to_all = models.BooleanField(default=False, blank=True)
    any_one_can_joint = models.BooleanField(default=False)
    pic = models.ImageField(upload_to=event_image_path, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    no_of_spot = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.event_name

    @property
    def title(self):
        return self.event_name


class EventResgiter(models.Model):
    event = models.ForeignKey(
        to=Events, on_delete=models.CASCADE, related_name="user_event_resgiter")
    user = models.ForeignKey(
        to=Events, on_delete=models.CASCADE, related_name="mostly_comming_user")
    invited = models.BooleanField(default=False)
    interested_to_join = models.BooleanField(default=True)

    def __str__(self):
        return self.event_name

#reciver for slug 
def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Report(models.Model):
    email = models.ForeignKey(
        detail, on_delete=models.CASCADE, related_name="social_report")
    report_of = models.ManyToManyField(User)
    report_description = models.TextField()

    def __str__(self):
        return self.report_description
class PostType(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

#model for creating poll 
class PostPoll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)

    def __str__(self):
        return self.post.post_title

class PostPollPoints(models.Model) :
    selected_option = models.CharField(max_length = 30)
    poll= models.ForeignKey(PostPoll,on_delete=models.CASCADE,null = True)
    user= models.ForeignKey(User,on_delete=models.SET_NULL , null = True)

class Post(models.Model):
    user = models.ForeignKey(
        detail, on_delete=models.CASCADE, related_name="social_post")
    description = models.TextField(null=True, blank=True)
    post_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    liked_by = models.ManyToManyField(
        User, related_name="posts_like", blank=True)
    draft = models.BooleanField(default=False)
    commercial_post = models.BooleanField(default=False)
    points = models.FloatField(default=0)
    #publish = models.DateField(auto_now=False,auto_now_add=False)
    post_time = models.DateTimeField(auto_now_add=True)
    post_type = models.ForeignKey(PostType,on_delete=models.SET_NULL,null=True, blank=True)
    post_pull = models.OneToOneField(PostPoll, on_delete=models.CASCADE,null=True, blank = True)
    image = models.ManyToManyField(Image, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE,null=True, blank=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE,null=True, blank=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE,null=True, blank=True)
    #  = models.ForeignKey( , on_delete=models.CASCADE,null=True, blank=True)
    #  = models.ForeignKey( , on_delete=models.CASCADE,null=True, blank=True)
    #  = models.ForeignKey( , on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.post_title + ' (' + self.post_type.category_name + ')' + ' - ' + self.post_by.name

    def total_like(self):
        return self.liked_by.count()

    class Meta:
        ordering = ('-post_time',)

class CommercialProductPoints(models.Model):
    product_type = models.ManyToManyField(PostType)
    like = models.FloatField(default=10)
    share = models.FloatField(default=30)
    comments = models.FloatField(default=20)
    min_booking_points = models.IntegerField(default=100)
    default_mrp = models.FloatField(null=True, blank=True)

 
class PostProductPricing(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    mrp = models.FloatField(null=True, blank=True)
    cost_increment = models.FloatField(default=0.01)
    accepting_booking = models.BooleanField(default=False)
    total_booking = models.IntegerField(default=500)
    min_bookings = models.IntegerField(default=100)
    max_bookings = models.IntegerField(default=500)
    bookings = models.ManyToManyField(User,through='ProductBooking')
    booking_days = models.IntegerField(default=7)
    booking_last_till = models.DateTimeField(null=True, blank=True)

    def save(self):
        from datetime import datetime, timedelta
        d = timedelta(days=self.booking_days)

        self.booking_last_till = datetime.now() + d
        super(PostProductPricing, self).save()
        
    def __str__(self):
        return self.post.post_title

class ProductBooking(models.Model):
    users = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(PostProductPricing,on_delete=models.CASCADE)
    order_on = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField(null=True, blank=True)
   


class PostComment(MPTTModel):

    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        related_name="children",
    )
    liked_by = models.ManyToManyField(User, related_name="comment_like", blank=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def total_like(self):
        return self.liked_by.count()

    class MPTTMeta:
        order_insertion_by = ['posted_on']

    def __str__(self):
        return self.comment[:15] + "... by " + str(self.user.name)

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post, related_name="post_bookmark", blank=True)

    def __str__(self):
        return self.user.name
    
    def total(self):
        return self.posts.count()

pre_save.connect(slug_pre_save_receiver, sender='just_connect.News')
pre_save.connect(slug_pre_save_receiver, sender='just_connect.Events')


# Porfolio project model
class Portfolio_Project(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    content = models.TextField()
    tools = models.CharField(max_length = 200)
    visibility = models.CharField(max_length=30)
    cover_image = models.FileField(upload_to=project_cover_image_path, null=True, blank=True)
    category = models.CharField(max_length = 200)
    publish_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

pre_save.connect(slug_pre_save_receiver, sender='just_connect.Portfolio_Project')

#portfolio project tags model
class ProjectTags(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 100)
    project = models.ForeignKey(Portfolio_Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
pre_save.connect(slug_pre_save_receiver, sender='just_connect.ProjectTags')

#portfolio project category model
class ProjectCategory(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 100)

    def __str__(self):
        return self.title
pre_save.connect(slug_pre_save_receiver, sender='just_connect.ProjectCategory')
