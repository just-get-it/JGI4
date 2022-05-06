from django import forms
from .models import interest_users,post


class interest_form(forms.ModelForm):
    class Meta():
        model = post
        fields = ('related_interests',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_interests'].widget.attrs.update({'class': 'chosen-select'})


privacy_choices = (
    ('private', 'Private'),
    ('public', 'Public'),
    ('friends_only', 'Friends Only'),
)
class post_form(forms.ModelForm):
    image = forms.ImageField(label=('Primary Image'),required=True, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image1 = forms.ImageField(label=('Other Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image2 = forms.ImageField(label=('Other Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image3 = forms.ImageField(label=('Other Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    image4 = forms.ImageField(label=('Other Image'),required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta():
        model = post
        fields = ('title','description','actual_price','image','image1','image2','image3','image4', 'post_privacy','related_interests')
        widgets = {
            'post_privacy': forms.Select(choices=privacy_choices)
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_interests'].widget.attrs.update({'class': 'chosen-select'})
        self.fields['image'].widget.attrs.update({'onchange': 'ImgDisplay("id_image","disp_image");'})
        self.fields['image1'].widget.attrs.update({'onchange': 'ImgDisplay("id_image1","disp_image1");'})
        self.fields['image2'].widget.attrs.update({'onchange': 'ImgDisplay("id_image2","disp_image2");'})
        self.fields['image3'].widget.attrs.update({'onchange': 'ImgDisplay("id_image3","disp_image3");'})
        self.fields['image4'].widget.attrs.update({'onchange': 'ImgDisplay("id_image4","disp_image4");'})