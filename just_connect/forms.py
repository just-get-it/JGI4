from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from product.models import *

class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = NewsComment
        fields = ["comment"]

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", 'short_news', 'news', 'video', 'image']


class EventForm(forms.ModelForm):  # extending ModelForm, not Form as before
    class Meta:
        model = Events
        fields = ["pic", "event_name", "Agenda", "guest",
                  "event_type", "location", "event_description", "start_time", "durations", "end_time", "view_to_all", "any_one_can_joint", "longitude", "latitude", "no_of_spot"]
        

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        print(kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['start_time'] = 'datetime'

# class edit_profile(forms.ModelForm):
#     class Meta():
#         model = User
#         fields = ('name', 'mobile', 'dob', 'address', 'city', 'state', 'pincode','bio',)

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_title','commercial_post','description')
        widgets = {
            'post_title' : forms.TextInput(attrs={'class':'form-control'}),
            #'post_type' : forms.Select(choices=choices,attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control','style': 'width: 99% !important;','required':True}),
            # 'thumbnail' : forms.FileInput(attrs={'class': 'input-image-control','required':'False'}),
        }
    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['post_title'].label = "Title *"


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('title', 'description' )
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
        }

class PostImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', )
        widgets = {'image':forms.FileInput(
        attrs={'multiple':True,'class':'form-control', 'required': False,'id':'id_postimage' })}

class ImageForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True,'placeholder': 'Drag images or click to choose images'}))
    class Meta:
        model = Image
        fields = ('image', )
        

class AdsForm(forms.ModelForm):
    link = forms.URLField(max_length=400,widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Ad
        fields = ('link','title','description','image')
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
   
     }


class CreatePollForm(forms.ModelForm):
    class Meta:
        model = PostPoll
        fields = ['question', 'option_one', 'option_two']
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = product
#         fields = ('product_Category', 'product_Subcategory', 'product_Supercategory')
#         # widgets ={
#         #     'product_Category' : forms.TextInput(attrs={'class':'form-control'}),
#         #     'product_Subcategory': forms.TextInput(attrs={'class':'form-control'}),
#         #     'product_Supercategory': forms.TextInput(attrs={'class':'form-control'}),
#         # }

#     def __init__(self,*args, **kwargs):
#         super().__init__(*args,**kwargs)
#         self.fields['product_Subcategory'].widget.attrs['disabled']='disabled'
#         self.fields['product_Supercategory'].widget.attrs['disabled']='disabled'
#         # print(self.data)
#         # if 'product_Category' in self.data:
#         #     try:
#         #         category_id = int(self.data.get('product_Category'))
#         #         self.fields['product_Subcategory'].queryset = sub_category.objects.filter(product_Category=category_id).order_by('name')
#         #     except Exception as e:
#         #         print(e)
#         #         pass
        