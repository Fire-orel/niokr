
from django import forms
from .models import Map,Publications,SecurityDocuments,Monographs,Event,Grant,NIRS,PopularSciencePublications,ScientificDirections,FullNameАuthor,InternationalCooperation
from datetime import datetime
from django_select2.forms import Select2TagWidget


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
        fields = ['type_publication', 'full_name_author_publications','name_publication_publications',"exit_data",'year','place_publication_publications','volume_publication','eLIBRARY_ID','doi_publication']

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
        fields=['type_monographs','full_name_author_monographs','name_works','circulation','volume_monographs','publishing_house','type_publishing_house','year_of_publication_monographs']


class EventForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        self.fields['date_event_event'].initial = now

    class Meta:
        model=Event
        fields=['type_participation','full_name_author_event','name_event_event','level','type_event','title_report','date_event_event','place_event','number_participants','number_foreign_participants','number_exhibits','publication_collection','awards','link']
        widgets = {
            'date_event_event': forms.DateInput(attrs={'type': 'date'}),
        }


class GrantForms(forms.ModelForm):
    class Meta:
        model=Grant
        fields=['type_grant','name_fund','name_competition','kod_competition','nomination','name_project_topic','project_manager','number_project_team','number_young_scientists','full_name_performer','winner']


class NIRSForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NIRSForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        self.fields['date_event_nirs'].initial = now

    class Meta:
        model=NIRS
        fields=['number_students','full_name_students','form_participation','name_event_nirs','full_name_scientific_supervisor','awards_diplomas','date_event_nirs']
        widgets = {
            'date_event_nirs': forms.DateInput(attrs={'type': 'date'}),
        }


class PopularSciencePublicationsForms(forms.ModelForm):

    full_name_author = forms.ModelMultipleChoiceField(
        label='Ф.И.О. автора (полностью)',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'multiple': 'multiple'}),
        required=False
    )

    class Meta:
        model=PopularSciencePublications
        fields=['full_name_author','name_publication_popular_science_publications','place_publication_popular_science_publications','volume_popular_science_publications','note',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name_author'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })





class ScientificDirectionsForms(forms.ModelForm):
    class Meta:
        model=ScientificDirections
        fields=['name_scientific_direction','name_scientific_school','leading_scientists','number_defended_doctoral_dissertations','number_defended_PhD_theses','number_monographs','number_articles_WoS_Scopus','number_articles_VAK','number_articles_RIHC','number_applications_inventions','number_security_documents_received','number_organized','amount_funding']


class InternationalCooperationForms(forms.ModelForm):
    class Meta:
        model=InternationalCooperation
        fields=['name_scientific_research','name_scientific_centers','name_topics','name_research_topics','name_scientific_programs']
