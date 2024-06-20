
from django import forms
from .models import Map,Publications,SecurityDocuments,Monographs
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
        fields = ['type_publication', 'full_name_author_publications','name_publication_publications',"exit_data",'year','place_publication','volume_publication','eLIBRARY_ID','doi_publication']

class SecurityDocumentsForms(forms.ModelForm):

    class Meta:
        model = SecurityDocuments
        fields=['type_document','type_property','full_name_author_security_documents','name_publication_security_documents','application_number']

class MonographsForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MonographsForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        self.fields['year_of_publication_monographs'].initial = current_year


    class Meta:
        model=Monographs
        fields=['type_monographs','full_name_author_Monographs','name_works','circulation','volume_monographs','publishing_house','type_publishing_house','year_of_publication_monographs']
