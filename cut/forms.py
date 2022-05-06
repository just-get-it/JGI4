from django import forms
from django.forms import ModelForm

from .models import CutLoadPlan, IssueDetails, TableCapacityLeft, AvailCapacity
from .admin import *

class availcapa(forms.ModelForm):

    class Meta:
        model = AvailCapacity
        fields = '__all__'
        fields_order = ['tableno', 'tabletype','modeofspread','modeofcut', 'availcapaforspreadandcut', 'capacityleft', 'datefield']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class capacleft(forms.ModelForm):

    class Meta:
        model = TableCapacityLeft
        fields = '__all__'
        fields_order = ['orderno', 'tableno', 'availcapaforspreadandcut', 'capacityleft', 'datefield']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class loadplanform(forms.ModelForm):

    class Meta:
        model = CutLoadPlan
        fields = '__all__'
        fields_order = ['orderno','styleno','totalorderquantity', 'markerprep', 'tabletype', 'markerno', 'laylength', 'noofplies', 'noofpieces', 'sprsmvmanual', 'sprsmvautospreader', 'crmanual', 'crautospreader', 'cutsmvstraight', 'cutsmvband', 'cutsmvcnc', 'crstraightband', 'crcnc', 'totmm', 'totma', 'totam', 'totaa', 'matinhousefabric', 'matinhousefusing', 'issuetable']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class issuedets(forms.ModelForm):

    class Meta:
        model = IssueDetails
        fields = '__all__'
        fields_order = ['orderno','styleno','markerno', 'noofplies', 'issuetable', 'availcapaforspreadandcut', 'cutpaneldelivery', 'requiredcapacity', 'requiredday', 'requiredtime', 'leadtime', 'issuedate']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)