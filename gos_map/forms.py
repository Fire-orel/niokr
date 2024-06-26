
from django import forms
from .models import Map,Publications,SecurityDocuments,Monographs,Event,Grant,NIRS,PopularSciencePublications,ScientificDirections,FullNameАuthor,InternationalCooperation,Department
from datetime import datetime
from django_select2.forms import Select2TagWidget


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class MapForms(forms.ModelForm):
    department = forms.ModelMultipleChoiceField(
        label='Кафедра',
        queryset=Department.objects.none(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',



            }),
        required=False,
        to_field_name='name_department'
    )

    def __init__(self, *args, **kwargs):
        user=kwargs.pop("user",None)

        super().__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        current_quarter = (current_month - 1) // 3 + 1  # Вычисляем текущий квартал
        self.fields['year'].initial = current_year
        self.fields['quarter'].initial = current_quarter
        # self.fields['department'].choices=[(department.name_department, department.name_department) for department in Department.objects.all()]
        self.fields['department'].widget.attrs.update({
            'style': 'width: 100%'
        })
        if user.position=="НО":
            self.fields['department'].queryset=Department.objects.all()
        elif user.position=="ЗД":
            self.fields['department'].queryset=Department.objects.filter(faculty=user.faculty)
        elif user.position=="ЗК":
            self.fields['department'].queryset=Department.objects.filter(name_department=user.department)
        else:
            self.fields['department'].queryset=Department.objects.all()

    class Meta:
        model = Map
        fields = ['year', 'quarter','department',"comment"]

class PublicationForms(forms.ModelForm):
    full_name_author_publications = forms.ModelMultipleChoiceField(
        label='ФИО автора',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            'value': 'full_name'
            }),
        required=False,
        to_field_name='full_name'
    )

    class Meta:
        model=Publications
        fields = ['type_publication', 'full_name_author_publications','name_publication_publications',"exit_data",'year','place_publication_publications','volume_publication','eLIBRARY_ID','doi_publication']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        self.fields['year'].initial = current_year
        self.fields['full_name_author_publications'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })

class SecurityDocumentsForms(forms.ModelForm):
    full_name_author_security_documents = forms.ModelMultipleChoiceField(
        label='ФИО автора',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            'value': 'full_name'
            }),
        required=False,
        to_field_name='full_name'
    )

    class Meta:
        model = SecurityDocuments
        fields=['type_document','type_property','full_name_author_security_documents','name_publication_security_documents','application_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name_author_security_documents'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })


class MonographsForms(forms.ModelForm):
    full_name_author_monographs = forms.ModelMultipleChoiceField(
        label='Автор(ы) ФИО (полностью)',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',

            }),
        required=False,
        to_field_name='full_name'
    )

    class Meta:
        model=Monographs
        fields=['type_monographs','full_name_author_monographs','name_works','circulation','volume_monographs','publishing_house','type_publishing_house','year_of_publication_monographs']

    def __init__(self, *args, **kwargs):
        super(MonographsForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        current_year = now.year
        self.fields['year_of_publication_monographs'].initial = current_year
        self.fields['full_name_author_monographs'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })





class EventForms(forms.ModelForm):
    full_name_author_event = forms.ModelMultipleChoiceField(
        label='ФИО участников ЗабГУ',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',

            }),
        required=False,
        to_field_name='full_name'
    )
    def __init__(self, *args, **kwargs):
        super(EventForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        self.fields['date_event_event'].initial = now
        self.fields['full_name_author_event'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })

    class Meta:
        model=Event
        fields=['type_participation','full_name_author_event','name_event_event','level','type_event','title_report','date_event_event','place_event','number_participants','number_foreign_participants','number_exhibits','publication_collection','awards','link']
        widgets = {
            'date_event_event': forms.DateInput(attrs={'type': 'date'}),
        }



class GrantForms(forms.ModelForm):

    project_manager = forms.ModelMultipleChoiceField(
        label='Руководитель проекта (ФИО полностью)',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            }),
        required=False,
        to_field_name='full_name'
    )
    full_name_performer = forms.ModelMultipleChoiceField(
        label='ФИО (полностью) исполнителей',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            }),
        required=False,
        to_field_name='full_name'
    )


    class Meta:
        model=Grant
        fields=['type_grant','name_fund','name_competition','kod_competition','nomination','name_project_topic','project_manager','number_project_team','number_young_scientists','full_name_performer','winner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project_manager'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })
        self.fields['full_name_performer'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })


class NIRSForms(forms.ModelForm):
    full_name_students = forms.ModelMultipleChoiceField(
        label='ФИО студентов',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            }),
        required=False,
        to_field_name='full_name'
    )
    full_name_scientific_supervisor = forms.ModelMultipleChoiceField(
        label='ФИО научного руководителя',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            }),
        required=False,
        to_field_name='full_name'
    )
    def __init__(self, *args, **kwargs):
        super(NIRSForms, self).__init__(*args, **kwargs)
        now = datetime.now()
        self.fields['date_event_nirs'].initial = now
        self.fields['full_name_students'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })
        self.fields['full_name_scientific_supervisor'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })

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
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            'value': 'full_name'
            }),
        required=False,
        to_field_name='full_name'
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

    leading_scientists = forms.ModelMultipleChoiceField(
        label='Ведущие ученые в данной области (1-3 человека)',
        queryset=FullNameАuthor.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2',
            'multiple': 'multiple',
            'data-tags': 'true',
            'value': 'full_name'
            }),
        required=False,
        to_field_name='full_name'
    )
    class Meta:
        model=ScientificDirections
        fields=['name_scientific_direction','name_scientific_school','leading_scientists','number_defended_doctoral_dissertations','number_defended_PhD_theses','number_monographs','number_articles_WoS_Scopus','number_articles_VAK','number_articles_RIHC','number_applications_inventions','number_security_documents_received','number_organized','amount_funding']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leading_scientists'].widget.attrs.update({
            'data-tags': 'true',
            'data-placeholder': 'Выберите автора или введите нового',
            'style': 'width: 100%'  # Пример установки стиля для ширины поля
        })


class InternationalCooperationForms(forms.ModelForm):
    class Meta:
        model=InternationalCooperation
        fields=['name_scientific_research','name_scientific_centers','name_topics','name_research_topics','name_scientific_programs']
