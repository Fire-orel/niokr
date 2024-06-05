
from django import forms
from .models import Map,Publications
from datetime import datetime


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class MapForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MapForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_quarter = (current_month - 1) // 3 + 1  # Вычисляем текущий квартал
        self.fields['year'].initial = current_year
        self.fields['quarter'].initial = current_quarter

    class Meta:
        model = Map
        fields = ['year', 'quarter','department',"comment"]

class PublicationForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PublicationForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        self.fields['year'].initial = current_year

    class Meta:
        model=Publications
        fields = ['type_publication', 'full_name_author','name_publication',"exit_data",'year','place_publication','volume_publication','eLIBRARY_ID','doi_publication']
