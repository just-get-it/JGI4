from django import forms
from .models import trimcard_sections, manual_documents

class trim_form(forms.ModelForm):
    class Meta():
        model = trimcard_sections
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(trim_form, self).__init__(*args, **kwargs)
        # self.fields['seller'].widget.attrs['readonly'] = True
        self.fields['seller'].disabled = True

class manual_docs_form(forms.ModelForm):
    class Meta():
        model = manual_documents
        fields = ('seller', 'name', 'product_Category', 'product_Subcategory', 'product_Supercategory', 'folding_doc', 'packing_doc', 'packing_manual', 'all_in_one')
    def __init__(self, *args, **kwargs):
        super(manual_docs_form, self).__init__(*args, **kwargs)
        # self.fields['seller'].widget.attrs['readonly'] = True
        self.fields['seller'].disabled = True