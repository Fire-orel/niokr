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

    position = models.CharField(max_length=100,choices=[("НО","Научный отдел"),("ЗД","Заместитель декана по научной работе"),("ЗК","Заведующий кафедрой")],verbose_name="Должность",blank = True)

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

class Faculty(models.Model):
    name_faculty=models.CharField(max_length=500,verbose_name="Факультет",blank=True,null=True)

    def __str__(self):
            return self.name_faculty



class Department(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.SET_NULL,verbose_name="Факультет",null=True)
    name_department=models.CharField(max_length=500,verbose_name="Кафедра",blank=True,null=True)

    def __str__(self):
            return self.name_department


class FullNameАuthor(models.Model):
    full_name=models.CharField(max_length=500,verbose_name="Ф.И.О.",blank=True,null=True)

    def __str__(self):
            return self.full_name


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

    comment = models.TextField(verbose_name="Комментарий",blank=True)

    responsible = models.ForeignKey(UserManager,on_delete=models.SET_NULL,verbose_name="Ответсвенный",null=True)

    status = models.CharField(max_length=20,choices=[("Редактируется","Редактируется"),("Завершено","Завершено")],default="Редактируется",verbose_name="Статус")

    def check_data(year,quarter, department):
        try:
            return Map.objects.get(year=year,quarter=quarter,department=department)
        except:
            return False

    def __str__(self):
            return F"{self.year} год, {self.quarter} квартал, {self.department}"

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

    full_name_author_publications = models.CharField(max_length=200,verbose_name="ФИО автора",blank=True)

    name_publication_publications = models.CharField(max_length=1000,verbose_name="Наименование публикации",blank=True)

    exit_data = models.TextField(verbose_name="Выходные данные публикации (Название журнала, Номер, Том, страницы)",blank=True)

    year = models.IntegerField(verbose_name="Год",blank=True)

    place_publication_publications = models.TextField(verbose_name="Место опубликования",blank=True)

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
    name_type_property=models.CharField(max_length=100,verbose_name="Вид интеллектуальной собственности")

    def __str__(self):
            return self.name_type_property

    class Meta:
        verbose_name="Вид интеллектуальной собственности"
        verbose_name_plural='Вид интеллектуальной собственности'




class SecurityDocuments(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    type_document=models.ForeignKey(TypeDocuments,on_delete=models.SET_NULL,verbose_name='Тип документа',null=True)

    type_property=models.ForeignKey(TypeProperty,on_delete=models.SET_NULL,verbose_name='Вид интеллектуальной собственности',null=True)

    full_name_author_security_documents = models.CharField(max_length=200,verbose_name="ФИО автора",blank=True,null=True)

    name_publication_security_documents = models.TextField(verbose_name="Наименование публикации",blank=True,null=True)

    application_number=models.CharField(max_length=50,verbose_name="Номер заявки / патента",blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")

    def __str__(self):
        return f'{self.name_publication_security_documents} {self.full_name_author_security_documents}'

    class Meta:
        verbose_name="Охранные документы"
        verbose_name_plural='Охранные документы'


class TypeMonographs(models.Model):
    name_type_monographs=models.CharField(max_length=100,verbose_name="Тип монографии")

    def __str__(self):
        return f'{self.name_type_monographs}'

    class Meta:
        verbose_name="Тип монографии"
        verbose_name_plural='Тип монографии'



class Monographs(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    type_monographs=models.ForeignKey(TypeMonographs,on_delete=models.SET_NULL,verbose_name='Тип монографии',null=True)

    full_name_author_monographs = models.TextField(verbose_name="Автор(ы) ФИО (полностью)",blank=True,null=True)

    name_works = models.TextField(verbose_name="Название работы",blank=True,null=True)


    circulation=models.IntegerField(verbose_name="Тираж",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    volume_monographs=models.IntegerField(verbose_name="Объем",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    publishing_house=models.CharField(max_length=1000,verbose_name="Издательство (наименование)",blank=True,null=True)

    type_publishing_house=models.CharField(max_length=400,verbose_name="Вид издательство",blank=True,null=True)

    year_of_publication_monographs=models.IntegerField(verbose_name="Год издание",blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")


    def __str__(self):
            return f"{self.name_works} {self.full_name_author_monographs}"


    class Meta:
        verbose_name="Монографии"
        verbose_name_plural='Монографии'


class TypeParticipation(models.Model):
    name_type_participation=models.CharField(max_length=100,verbose_name="Тип участия")
    def __str__(self):
        return f'{self.name_type_participation}'

    class Meta:
        verbose_name="Тип участия"
        verbose_name_plural='Тип участия'

class TypeEvent(models.Model):
    name_type_events=models.CharField(max_length=100,verbose_name="Тип мероприятия")
    def __str__(self):
        return f'{self.name_type_events}, {self.pk}'

    class Meta:
        verbose_name="Тип мероприятия"
        verbose_name_plural='Тип мероприятия'


class TypeLevel(models.Model):
    name_type_level=models.CharField(max_length=100,verbose_name="Уровень")
    def __str__(self):
        return f'{self.name_type_level}'

    class Meta:
        verbose_name="Уровень"
        verbose_name_plural='Уровень'

class Event (models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    type_participation=models.ForeignKey(TypeParticipation,on_delete=models.SET_NULL,verbose_name="Тип участия",null=True)

    full_name_author_event = models.TextField(verbose_name="ФИО (полностью) участников ЗабГУ",blank=True,null=True)

    name_event_event=models.TextField(verbose_name="Название мероприятия",blank=True,null=True)

    level=models.ForeignKey(TypeLevel,on_delete=models.CASCADE,verbose_name="Уровень",null=True)

    type_event=models.ForeignKey(TypeEvent,on_delete=models.SET_NULL,verbose_name="Тип мероприятия",null=True)

    title_report=models.TextField(verbose_name="Наименование Доклада на мероприятия (для конференций)",blank=True,null=True)

    date_event_event=models.DateField(verbose_name='Дата проведения',blank=True,null=True)

    place_event=models.TextField(verbose_name="Место проведения",blank=True,null=True)

    number_participants=models.IntegerField(verbose_name="Общее кол-во участников мероприятия",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_foreign_participants=models.IntegerField(verbose_name="Кол-во зарубежных участников мероприятия",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_exhibits=models.IntegerField(verbose_name="Кол-во экспонатов (для выставки)",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    publication_collection=models.CharField(max_length=100,choices=[("Yes","Да"),("No","Нет")],verbose_name="С изданием сборника (для конференций)",blank=True,null=True,default="No")

    awards=models.TextField(verbose_name="Полученные награды НПР и студентами ЗабГУ (медали, дипломы, грамоты)",blank=True,null=True)

    link=models.CharField(max_length=500,verbose_name="Ссылка на программу мероприятия",blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("E","Редактируется"),("с","Завершено")],default="Редактируется",verbose_name="Статус")

    def __str__(self):
        return f'{self.name_event_event}'

    class Meta:
        verbose_name="Мероприятия"
        verbose_name_plural='Мероприятия'


class TypeGrant(models.Model):
    name_type_grant=models.CharField(max_length=100,verbose_name="Тип гранта")
    def __str__(self):
        return f'{self.name_type_grant}'

    class Meta:
        verbose_name="Тип гранта"
        verbose_name_plural='Тип гранта'


class Grant(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    type_grant=models.ForeignKey(TypeGrant,on_delete=models.SET_NULL,verbose_name="Тип гранта",null=True)

    name_fund=models.CharField(max_length=500,verbose_name="Наименование фонда",blank=True,null=True)

    name_competition=models.CharField(max_length=500,verbose_name="Наименование конкурса",blank=True,null=True)

    kod_competition=models.CharField(max_length=50,verbose_name="Код конкурса",blank=True,null=True)

    nomination=models.CharField(max_length=500,verbose_name="Номинация (при наличии)",blank=True,null=True)

    name_project_topic=models.CharField(max_length=500,verbose_name="Наименование темы проекта (без кавычек)",blank=True,null=True)

    project_manager = models.CharField(max_length=200,verbose_name="Руководитель проекта (ФИО полностью)",blank=True,null=True)

    number_project_team=models.IntegerField(verbose_name="Численность проектного коллектива",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_young_scientists=models.IntegerField(verbose_name="Численность молодых ученых",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    full_name_performer = models.CharField(max_length=200,verbose_name="ФИО (полностью) исполнителей",blank=True,null=True)

    winner=models.CharField(max_length=3,choices=[("Д","Да"),("Н","Нет")],default="Н",verbose_name="Выиграно (Да, Нет)")

    status = models.CharField(max_length=20,choices=[("Р","Редактируется"),("З","Завершено")],default="Р",verbose_name="Статус")


    def __str__(self):
        return f'{self.name_project_topic}'

    class Meta:
        verbose_name="Грант"
        verbose_name_plural='Грант'

class FormParticipation(models.Model):
    name_form_participation=models.CharField(max_length=500,verbose_name="Форма участия")
    def __str__(self):
        return f'{self.name_form_participation}'

    class Meta:
        verbose_name="Форма участия"
        verbose_name_plural='Форма участия'

class NIRS (models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    number_students=models.IntegerField(verbose_name="Численность студентов",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    full_name_students= models.TextField(verbose_name="ФИО студентов",blank=True,null=True)

    form_participation = models.ForeignKey(FormParticipation,on_delete=models.SET_NULL,verbose_name="Карта",null=True)

    name_event_nirs = models.CharField(max_length=500,verbose_name="Наименование мероприятия",blank=True,null=True)

    full_name_scientific_supervisor=models.TextField(verbose_name="ФИО научного руководителя",blank=True,null=True)

    awards_diplomas = models.TextField(verbose_name="Награды/Дипломы",blank=True,null=True)

    date_event_nirs=models.DateField(verbose_name='Дата мероприятия',blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("Р","Редактируется"),("З","Завершено")],default="Р",verbose_name="Статус")

    def __str__(self):
        return f'{self.name_event_nirs}'

    class Meta:
        verbose_name="НИРС"
        verbose_name_plural='НИРС'


class PopularSciencePublications(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    full_name_author= models.CharField(max_length=500,verbose_name="Ф.И.О. автора (полностью)",blank=True,null=True)

    name_publication_popular_science_publications = models.CharField(max_length=1000,verbose_name="Название публикации",blank=True)

    place_publication_popular_science_publications = models.TextField(verbose_name="Место опубликования, издательство, год, № выпуска",blank=True,null=True)

    volume_popular_science_publications=models.IntegerField(verbose_name="Объем публикации",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    note = models.TextField(verbose_name="Примечание",blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("Р","Редактируется"),("З","Завершено")],default="Р",verbose_name="Статус")

    def __str__(self):
        return f'{self.name_publication_popular_science_publications} {self.full_name_author}'

    class Meta:
        verbose_name="Научно-популярные издания"
        verbose_name_plural='Научно-популярные издания'



class ScientificDirections (models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    name_scientific_direction = models.CharField(max_length=700,verbose_name="Научное направление",blank=True)

    name_scientific_school=models.CharField(max_length=700,verbose_name="Название научной школы",blank=True)

    leading_scientists=models.TextField(verbose_name="Ведущие ученые в данной области (1-3 человека)",blank=True,null=True)

    number_defended_doctoral_dissertations=models.IntegerField(verbose_name="Кол-во защищенных докторских диссертаций",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_defended_PhD_theses=models.IntegerField(verbose_name="Кол-во защищенных кандидатских диссертаций",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_monographs=models.IntegerField(verbose_name="Кол-во монографий",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_articles_WoS_Scopus=models.IntegerField(verbose_name="Кол-во статей WoS/Scopus",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_articles_VAK=models.IntegerField(verbose_name="Кол-во статей ВАК",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_articles_RIHC=models.IntegerField(verbose_name="Кол-во статей РИНЦ",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_applications_inventions=models.IntegerField(verbose_name="Кол-во заявок на изобретения",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_security_documents_received=models.IntegerField(verbose_name="Кол-во полученных охранных документов",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    number_organized=models.IntegerField(verbose_name="Кол-во организованных международных и (или) всероссийских научных и (или) научно-практических мероприятий",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    amount_funding=models.IntegerField(verbose_name="Объем финансирования",blank=True,null=True,default=1,validators=[MinValueValidator(0)])

    status = models.CharField(max_length=20,choices=[("Р","Редактируется"),("З","Завершено")],default="Р",verbose_name="Статус")


    def __str__(self):
        return f'{self.name_scientific_direction} {self.name_scientific_school}'

    class Meta:
        verbose_name="Научные направления"
        verbose_name_plural='Научные направления'



class InternationalCooperation(models.Model):
    id_map = models.ForeignKey(Map,on_delete=models.CASCADE,verbose_name="Карта")

    name_scientific_research=models.TextField(verbose_name="Наименование научно-исследовательских  и научно-технических проектов ",blank=True,null=True)

    name_scientific_centers=models.TextField(verbose_name="Наименование научных центров, лабораторий, других подразделений, созданнх с участвием международных или иностранных организаций",blank=True,null=True)

    name_topics=models.TextField(verbose_name="Наименование тем, проводимых совместных научных исследований",blank=True,null=True)

    name_research_topics=models.TextField(verbose_name="Наименование тем научных исследований, опытно-конструкторских работ, проводимых по заказам международных и иностранных организаций",blank=True,null=True)

    name_scientific_programs=models.TextField(verbose_name="Наименование научных программ, разработка и реализация которых осуществляется  совместно с международными или иностранными организациями",blank=True,null=True)

    status = models.CharField(max_length=20,choices=[("Р","Редактируется"),("З","Завершено")],default="Р",verbose_name="Статус")

    def __str__(self):
        return f'{self.name_scientific_research} '

    class Meta:
        verbose_name="Международное сотрудничество"
        verbose_name_plural='Международное сотрудничество'
