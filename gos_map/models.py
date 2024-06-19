from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

def validate_year(value):
    if value < 1900 or value > 2100:  # Здесь можно задать нужный диапазон
        raise ValidationError('%(value)s is not a valid year', params={'value': value})

class YearField(models.IntegerField):
    default_validators = [validate_year]

    def __init__(self, *args, **kwargs):
        kwargs['validators'] = kwargs.get('validators', []) + self.default_validators
        super().__init__(*args, **kwargs)

class UserManager(models.Model):
    login=models.CharField(max_length=100,verbose_name="Логин")
    password = models.CharField(max_length=100,verbose_name='Пароль')
    full_name = models.CharField(max_length=100,verbose_name="ФИО",blank = True)
    position = models.CharField(max_length=100,choices=[("НО","Научный отдел"),("ЗДпоНР","Заместитель декана по научной работе"),("ЗК","Заведующий кафедрой")],verbose_name="Должность",blank = True)
    faculty = models.CharField(max_length=100,verbose_name="Факультет",blank = True)
    department = models.CharField(max_length=100,verbose_name="Кафедра",blank = True)
    last_login = models.DateTimeField(auto_now=True)

    def get_user_by_login(login):
        try:
            return UserManager.objects.get(login=login)
        except:
            return False
    def get_department_by_id(login):
        try:
            return UserManager.objects.get(login=login).dep
        except:
            return False
    def get_user_by_login_password(login,password):
        try:
            return UserManager.objects.get(login=login,password=password)
        except:
            return False
    def get_user_id(id):
        try:
            return UserManager.objects.get(pk=id)
        except:
            return False
    def get_position_id(id):
        try:
            return UserManager.objects.get(pk=id).position
        except:
            return False

    def __str__(self):
            return self.login

class TypePublications(models.Model):
    name_type_publications=models.CharField(max_length=100,verbose_name="Тип публикации")

    class Meta:
        verbose_name="Тип публикации"
        verbose_name_plural='Тип публикации'

    def get_type_publications_id(id):
        try:
            return TypePublications.objects.get(pk=id)
        except:
            return False

    def __str__(self):
            return self.name_type_publications

class Map(models.Model):
    year = models.IntegerField(verbose_name="Год")
    quarter = models.CharField(max_length=1,choices=[("1","1"),("2","2"),("3","3"),("4","4")],verbose_name="Квартал")
    department = models.CharField(max_length=100,verbose_name="Кафедра")
    comment = models.TextField(verbose_name="Комментарий")
    responsible = models.ForeignKey(UserManager,on_delete=models.SET_NULL,verbose_name="Ответсвенный",null=True)
    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")

    def check_data(year,quarter, department):
        try:
            return Map.objects.get(year=year,quarter=quarter,department=department)
        except:
            return False

    def __str__(self):
            return F"{self.year} год, {self.quarter} квартал, {self.department} кафедра"

    def get_map_id(id):
        try:
            return Map.objects.get(pk=id)
        except:
            return False

    class Meta:
        verbose_name="Карты"
        verbose_name_plural='Карты'


class Publications(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")
    type_publication = models.ForeignKey(TypePublications, on_delete=models.SET_NULL,verbose_name="Тип публикации",null=True)
    full_name_author = models.CharField(max_length=200,verbose_name="ФИО автора",blank=True)
    name_publication = models.CharField(max_length=1000,verbose_name="Наименование публикации",blank=True)
    exit_data = models.TextField(verbose_name="Выходные данные публикации (Название журнала, Номер, Том, страницы)",blank=True)
    year = models.IntegerField(verbose_name="Год",blank=True)
    place_publication = models.TextField(verbose_name="Место опубликования",blank=True)

    volume_publication=models.IntegerField(verbose_name="Объем публикации (п.л.)",blank=True,null=True,default=1,validators=[MinValueValidator(0)])
    eLIBRARY_ID=models.CharField(max_length=50,verbose_name="eLIBRARY ID",blank=True,null=True)
    doi_publication= models.CharField(max_length=50,verbose_name="DOI публикации",blank=True,null=True)
    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")

    class Meta:
        verbose_name="Публикации"
        verbose_name_plural='Публикации'



class TypeDocuments(models.Model):
    name_type_documents=models.CharField(max_length=100,verbose_name="Тип документа")

    class Meta:
        verbose_name="Тип документа"
        verbose_name_plural='Тип документа'

    def __str__(self):
            return self.name_type_documents



class TypeProperty(models.Model):
    name_type_Property=models.CharField(max_length=100,verbose_name="Вид интеллектуальной собственности")
    def __str__(self):
            return self.name_type_Property

    class Meta:
        verbose_name="Вид интеллектуальной собственности"
        verbose_name_plural='Вид интеллектуальной собственности'




class SecurityDocuments(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")
    type_document=models.ForeignKey(TypeDocuments,on_delete=models.SET_NULL,verbose_name='Тип документа',null=True)
    type_property=models.ForeignKey(TypeProperty,on_delete=models.SET_NULL,verbose_name='Вид интеллектуальной собственности',null=True)
    full_name_author = models.CharField(max_length=200,verbose_name="ФИО автора",blank=True)
    name_publication = models.CharField(max_length=1000,verbose_name="Наименование публикации",blank=True)

    application_number=models.CharField(max_length=50,verbose_name="Номер заявки / патента",blank=True,null=True)
    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")

    class Meta:
        verbose_name="Охранные документы"
        verbose_name_plural='Охранные документы'
