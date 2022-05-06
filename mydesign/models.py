



from django.db import models

# Create your models here.
from userdetail.models import detail
import random,os
from mptt.models import MPTTModel, TreeForeignKey



def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name ,ext=os.path.splitext(base_name)
    return name ,ext

def upload_image_path(instance,filename):
    new_filename=random.randint(1,13516546431654)
    name ,ext=get_filename_ext(filename)
    final_filename='{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)
    return "local/b2b/logo/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
        )



class interests(models.Model):
    name=models.CharField(max_length=255)
    priority=models.IntegerField(null=True,blank=True)


    def __str__(self):
        return self.name


class interest_users(models.Model):
    user=models.ForeignKey(detail,on_delete=models.CASCADE, blank=True)
    interest_user=models.ManyToManyField(interests,blank=True)


    def __str__(self):
        return str(self.user)


class post(models.Model):
    user=models.ForeignKey(detail,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    description_moderator=models.TextField(null=True,blank=True)
    estimated_price=models.IntegerField(default=0)
    actual_price=models.IntegerField(default=0)
    share_count=models.IntegerField(default=0)
    orders_count=models.IntegerField(default=0)
    image=models.FileField(upload_to=upload_image_path,null=True,blank=True)
    image1=models.FileField(upload_to=upload_image_path,null=True,blank=True)
    image2=models.FileField(upload_to=upload_image_path,null=True,blank=True)
    image3=models.FileField(upload_to=upload_image_path,null=True,blank=True)
    image4=models.FileField(upload_to=upload_image_path,null=True,blank=True)
    post_privacy=models.CharField(max_length=255,null=True,blank=True)
    approved=models.BooleanField(default=False)
    post_time=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    related_interests=models.ManyToManyField(interests, blank=True, related_name='posts')
    def __str__(self):
        return self.title

class like(models.Model):
    post_on=models.ForeignKey(post,on_delete=models.CASCADE)
    user=models.ForeignKey(detail,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.post_on)

class Comment(MPTTModel):
    post = models.ForeignKey(post, related_name='comments',on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    user = models.ForeignKey(detail, related_name='Commenter',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length = 256)
    class MPTTMeta:
        order_insertion_by = ['date']
    def __str__(self):
        return str(self.text)

# class comment(models.Model):
#     post_on=models.ForeignKey(post,on_delete=models.CASCADE, related_name='comments')
#     description=models.TextField(null=True,blank=True)
#     user=models.ForeignKey(detail,on_delete=models.CASCADE)


#     def __str__(self):
#         return str(self.post_on)


# class comment_likes(models.Model):
#     post_on=models.ForeignKey(comment,on_delete=models.CASCADE)
#     user=models.ForeignKey(detail,on_delete=models.CASCADE)


#     def __str__(self):
#         return str(self.post_on)


# class comment_reply(models.Model):
#     post_on=models.ForeignKey(comment,on_delete=models.CASCADE)
#     description=models.TextField(null=True,blank=True)
#     user=models.ForeignKey(detail,on_delete=models.CASCADE)


#     def __str__(self):
#         return str(self.post_on)



# class comment_reply_likes(models.Model):
#     post_on=models.ForeignKey(comment_reply,on_delete=models.CASCADE)
#     user=models.ForeignKey(detail,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return str(self.post_on)




class followers(models.Model):
    user=models.ForeignKey(detail,on_delete=models.CASCADE)
    followers_users=models.ManyToManyField(detail,blank=True,related_name='follower')


    def __str__(self):
        return str(self.user)


class friend(models.Model):
    user1=models.ForeignKey(detail,on_delete=models.CASCADE,related_name='user1_1')
    user2=models.ForeignKey(detail,on_delete=models.CASCADE,related_name='user2_2')
    request_accepted=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user1)+" & "+str(self.user2)
