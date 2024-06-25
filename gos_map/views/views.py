# views.py

from django.contrib.auth import login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from ldap3 import Server, Connection, ALL, NTLM
from ..forms import LoginForm,MapForms,PublicationForms,SecurityDocumentsForms,MonographsForms,EventForms,GrantForms,NIRSForms,PopularSciencePublicationsForms,ScientificDirectionsForms,InternationalCooperationForms
from ..models import UserManager,Map,Publications,TypePublications,SecurityDocuments,Monographs,Event,Grant,NIRS,PopularSciencePublications,ScientificDirections,InternationalCooperation,Faculty,Department
from django.views.generic import ListView,DetailView,UpdateView
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from openpyxl import Workbook
import zipfile
import io
import os
from dotenv import load_dotenv
load_dotenv()



class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Сначала проверяем пользователя в базе данных Django
            try:
                user = UserManager.get_user_by_login(login=username)
                if user !=False :
                    if UserManager.get_user_by_login_password(login=username,password=password):
                        request.session['user_id'] = user.id
                        request.session['user_full_name'] = user.full_name
                        return redirect('home')
                    else:
                        return render(request, self.template_name, {'form': form, 'error': 'Логин или пароль неверны'})
            except UserManager.DoesNotExist:
                user = None

            # Если пользователь не найден в базе данных Django, пробуем аутентификацию через LDAP
            ldap_user = self.ldap_authenticate(username, password)

            if ldap_user:
                # Создаем пользователя в базе данных Django
                first_name=ldap_user['first_name']
                last_name=ldap_user['last_name']
                if first_name is None:
                    first_name=""
                if last_name is None:
                    last_name=""
                user = UserManager.objects.create(
                    login=ldap_user['username'],
                    password=password,  # Здесь пароль лучше захэшировать

                    full_name=first_name+' '+ last_name

                )
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                request.session['user_id'] = user.pk
                request.session['user_full_name'] = user.full_name

                return redirect('home')

            # Если аутентификация не удалась, выводим сообщение об ошибке
            return render(request, self.template_name, {'form': form, 'error': 'Логин или пароль неверны'})

        return render(request, self.template_name, {'form': form})

    def ldap_authenticate(self, username, password):
        LDAP_SERVER = os.getenv("server_adress")
        LDAP_USER = f'{os.getenv('server_domen')}\\{username}'
        LDAP_PASSWORD = password
        LDAP_SEARCH_BASE = 'DC=FIREOREL,DC=ru'

        # NTLM поддержка через ldap3
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=NTLM)

        if not conn.bind():
            return None

        conn.search(LDAP_SEARCH_BASE, f'(sAMAccountName={username})', attributes=['sAMAccountName', 'givenName', 'sn'])
        if len(conn.entries) != 1:
            return None


        user_info = conn.entries[0]

        return {
            'username': user_info.sAMAccountName.value,
            'first_name': user_info.givenName.value,
            'last_name': user_info.sn.value,
        }


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        user_full_name = request.session.get('user_full_name')
        position = UserManager.get_position_id(request.session.get("user_id"))

        if  position =="НО":
            maps= Map.objects.all ()
        else:
            maps = Map.objects.filter(responsible=UserManager.get_user_id(request.session.get("user_id")))


        context = {
            'user_full_name': user_full_name,
            'user_id':UserManager.get_user_id(request.session.get("user_id")),
            'user_posistion':UserManager.get_user_id(request.session.get("user_id")).position,
            'maps': maps,
            'mapform':MapForms(),
            'type_publications':TypePublications.objects.all(),
            'facultys':Faculty.objects.all(),
            'departments':Department.objects.all()

        }
        return render(request, self.template_name, context)

    def post(self, request):
        # print(request.POST.get('logout'))
        if request.POST.get('logout'):
            request.session.flush()
            return redirect('login')


class CheckMap(View):
    def post(self, request, *args, **kwargs):
        year = request.POST.get("year")
        quarter = request.POST.get("quarter")
        department = request.POST.getlist("department")
        if len(department)>1:
            return JsonResponse({'message': 'Invalid request method'}, status=400)
        check=Map.check_data(year,quarter,department)
        # Обработка данных
        if not check:  # Замените на ваше условие
            map=Map.objects.create(
                year=year,
                quarter=quarter,
                department=department[0],
                comment=request.POST.get("comment"),
                responsible=UserManager.get_user_id(request.session.get("user_id"))
            )
            map.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Error'}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)

class deleteMap(View):
    def post(self, request, pk):
        try:
            map = Map.objects.get(pk=pk)
            map.delete()
            return JsonResponse({'message': 'Map deleted successfully'}, status=200)
        except Map.DoesNotExist:
            return JsonResponse({'error': 'Map not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




class MapDetails(View):
    def get(self,request,pk):
        status="False"

        user_full_name = request.session.get('user_full_name')



        data = get_object_or_404(Map, pk=pk)
        request.session['map_id']=pk
        # print(request.session['map_id'])

        publications=Publications.objects.filter(id_map=Map.get_map_id(pk))
        publications_count=publications.filter(status="Завершено").count()

        securitydocuments = SecurityDocuments.objects.filter(id_map=Map.get_map_id(pk))
        securitydocuments_count=securitydocuments.filter(status="Завершено").count()

        monographs=Monographs.objects.filter(id_map=Map.get_map_id(pk))
        monographs_count=monographs.filter(status="Завершено").count()

        events=Event.objects.filter(id_map=Map.get_map_id(pk))
        events_count=events.filter(status="Завершено").count()

        grant=Grant.objects.filter(id_map=Map.get_map_id(pk))
        grant_count=grant.filter(status="Завершено").count()

        nirs = NIRS.objects.filter(id_map=Map.get_map_id(pk))
        nirs_count=nirs.filter(status="Завершено").count()

        popularsciencepublications = PopularSciencePublications.objects.filter(id_map=Map.get_map_id(pk))
        popularsciencepublications_count=popularsciencepublications.filter(status="Завершено").count()

        scientificdirections=ScientificDirections.objects.filter(id_map=Map.get_map_id(pk))
        scientificdirections_count=scientificdirections.filter(status="Завершено").count()

        internationalcooperation=InternationalCooperation.objects.filter(id_map=Map.get_map_id(pk))
        internationalcooperation_count=internationalcooperation.filter(status="Завершено").count()



        if len(publications)==publications_count and len(securitydocuments)==securitydocuments_count and len(monographs)==monographs_count and len(events)==events_count and len(grant)==grant_count and len(nirs)==nirs_count and len(popularsciencepublications)==popularsciencepublications_count and len(scientificdirections)==scientificdirections_count and len(internationalcooperation)==internationalcooperation_count:

            status="True"



        context = {
            'status':status,

            'user_full_name': user_full_name,
            'map':data,

            'publications':publications,
            'publicationsforms':PublicationForms(),


            'securitydocuments':securitydocuments,
            'securitydocumentsforms':SecurityDocumentsForms(),

            'monographs':monographs,
            'monographsforms':MonographsForms(),

            'events':events,
            'eventforms':EventForms(),

            'grants':grant,
            'grantforms':GrantForms(),

            'nirss':nirs,
            'nirsforms':NIRSForms(),

            'popularsciencepublicationss':popularsciencepublications,
            'popularsciencepublicationsforms':PopularSciencePublicationsForms(),
            'scientificdirectionss':scientificdirections,
            'scientificdirectionsforms':ScientificDirectionsForms(),
            'internationalcooperations':internationalcooperation,
            "internationalcooperationforms":InternationalCooperationForms(),




        }
        return render(request, 'map_details.html',context)

    def post(self, request,**kwargs):

        if request.POST.get('logout'):
            request.session.flush()
            return redirect('login')

class mapСompleted(View):
    def get(self, request,pk, *args, **kwargs):
        map=get_object_or_404(Map,id=pk)
        map.status="Завершено"
        map.save()
        return redirect('home')




class otchet(View):
    def post(self,request):
        # faculty = request.POST.getlist('faculty')
        department = request.POST.getlist('department')
        quarter = request.POST.getlist('quarter')
        tables=request.POST.getlist('table')
        year = request.POST.getlist('year')
        print(year)
        type_table_publication=request.POST.getlist('table_type')
        # print(quarter,table,type_table_publication)
        # print(UserManager.get_user_id(request.session.get("user_id")))
        user_id=UserManager.get_user_id(request.session.get("user_id"))
        zip_buffer = io.BytesIO()

        map_2=Map.objects.none()
        map_1=Map.objects.none()
        map=Map.objects.none()

        if len(quarter)>0:
            for i in quarter:
                map=map|Map.objects.filter(quarter=i)
        else :
            map=Map.objects.all()

        if len(department)>0:
            for q in department:
                map_1=map_1|map.filter(department=Department.objects.get(pk=q).name_department)
        else:
            map_1=map

        if len(year)>0:
            for q in year:
                map_2=map_2|map_1.filter(year=year)
                print(map_1.filter(year=year))
            else:
                map_2=map_1
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for id_map in map_1:
                workbook = Workbook()
                workbook.remove(workbook.active)
                for table in tables:
                    if table=='Publications':
                        count=2
                        sheet = workbook.create_sheet('Публикации')
                        sheet['A1']="Тип публикации"
                        sheet['B1']="ФИО автора"
                        sheet['C1']="Наименование публикации"
                        sheet['D1']="Выходные данные публикации (Название журнала, Номер, Том, страницы)"
                        sheet['E1']="Год"
                        sheet['F1']="Место опубликования"
                        sheet['G1']="Объем публикации (п.л.)"
                        sheet['H1']="eLIBRARY ID"
                        sheet['I1']="DOI публикации"

                        publicationss=Publications.objects.filter(id_map=id_map)
                        for publications in publicationss:
                            sheet[f"A{count}"]=publications.type_publication.name_type_publications
                            sheet[f"B{count}"]=publications.full_name_author_publications
                            sheet[f"C{count}"]=publications.name_publication_publications
                            sheet[f"D{count}"]=publications.exit_data
                            sheet[f"E{count}"]=publications.year
                            sheet[f"F{count}"]=publications.place_publication_publications
                            sheet[f"G{count}"]=publications.volume_publication
                            sheet[f"H{count}"]=publications.eLIBRARY_ID
                            sheet[f"I{count}"]=publications.doi_publication
                            count+=1
                    if table=='SecurityDocuments':
                        count=2
                        sheet = workbook.create_sheet('Охранные документы')
                        sheet['A1']="Тип документа"
                        sheet['B1']="Вид интеллектуальной собственности"
                        sheet['C1']="ФИО автора (ов)"
                        sheet['D1']="Наименование"
                        sheet['E1']="Номер заявки / патента"

                        securitydocumentss=SecurityDocuments.objects.filter(id_map=id_map)
                        for securitydocuments in securitydocumentss:

                            sheet[f"A{count}"]=str(securitydocuments.type_document)
                            sheet[f"B{count}"]=str(securitydocuments.type_property)
                            sheet[f"C{count}"]=securitydocuments.full_name_author_security_documents
                            sheet[f"D{count}"]=securitydocuments.name_publication_security_documents
                            sheet[f"E{count}"]=securitydocuments.application_number

                            count+=1
                    if table=='Monographs':
                        count=2
                        sheet = workbook.create_sheet('Охранные документы')
                        sheet['A1']="Тип монографии (выпадающий список)"
                        sheet['B1']="Автор(ы) ФИО (полностью)"
                        sheet['C1']="Название работы"
                        sheet['D1']="Тираж"
                        sheet['E1']="Объем"
                        sheet['F1']="Издательство(наименование)"
                        sheet['G1']="Вид издательства"
                        sheet['H1']="Год издания"

                        monographss=Monographs.objects.filter(id_map=id_map)
                        for monographs in monographss:

                            sheet[f"A{count}"]=str(monographs.type_monographs)
                            sheet[f"B{count}"]=monographs.full_name_author_monographs
                            sheet[f"C{count}"]=monographs.name_works
                            sheet[f"D{count}"]=monographs.circulation
                            sheet[f"E{count}"]=monographs.volume_monographs
                            sheet[f"F{count}"]=monographs.publishing_house
                            sheet[f"G{count}"]=monographs.type_publishing_house
                            sheet[f"H{count}"]=monographs.year_of_publication_monographs

                            count+=1



                file_buffer = io.BytesIO()
                workbook.save(file_buffer)
                file_buffer.seek(0)

                # Добавляем файл в ZIP-архив
                map_date= str(id_map.year)+" "+str(id_map.quarter)+" "+str(id_map.department)

                zip_file.writestr(f'{map_date.__str__()}.xlsx', file_buffer.read())

        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=tables.zip'

        return response
