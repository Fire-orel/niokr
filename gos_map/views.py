# views.py

from django.contrib.auth import login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from ldap3 import Server, Connection, ALL, NTLM
from .forms import LoginForm,MapForms,PublicationForms,SecurityDocumentsForms
from .models import UserManager,Map,Publications,TypePublications,SecurityDocuments,TypeDocuments,TypeProperty
from django.views.generic import ListView,DetailView,UpdateView
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from openpyxl import Workbook
import zipfile
import io
from django.core import serializers


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
                return redirect('home')

            # Если аутентификация не удалась, выводим сообщение об ошибке
            return render(request, self.template_name, {'form': form, 'error': 'Логин или пароль неверны'})

        return render(request, self.template_name, {'form': form})

    def ldap_authenticate(self, username, password):
        LDAP_SERVER = "ldap://192.168.0.33"
        LDAP_USER = f'FIREOREL\\{username}'
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
            'type_publications':TypePublications.objects.all()

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
        department = request.POST.get("department")
        check=Map.check_data(year,quarter,department)
        # Обработка данных
        print(request.session.get("user_id"))
        print(request.POST)
        if not check:  # Замените на ваше условие
            map=Map.objects.create(
                year=year,
                quarter=quarter,
                department=department,
                comment=request.POST.get("comment"),
                responsible=UserManager.get_user_id(request.session.get("user_id"))
            )
            map.save()
            return JsonResponse({'message': 'Success'}, status=200)
        else:
            return JsonResponse({'message': 'Error'}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class MapDetails(View):
    def get(self,request,pk):

        user_full_name = request.session.get('user_full_name')

        data = get_object_or_404(Map, pk=pk)
        request.session['map_id']=pk
        # print(request.session['map_id'])
        publications=Publications.objects.filter(id_map=Map.get_map_id(pk))
        securitydocuments = SecurityDocuments.objects.filter(id_map=Map.get_map_id(pk))

        context = {
            'user_full_name': user_full_name,
            'map':data,

            'publications':publications,
            'publicationsforms':PublicationForms(),


            'securitydocuments':securitydocuments,
            'securitydocumentsforms':SecurityDocumentsForms()


        }
        return render(request, 'map_details.html',context)

    def post(self, request,**kwargs):

        if request.POST.get('logout'):
            request.session.flush()
            return redirect('login')



class addPublication(View):
    def post(self, request, *args, **kwargs):
        type_publication = request.POST.get("type_publication")
        full_name_author = request.POST.get("full_name_author")
        name_publication = request.POST.get("name_publication")
        exit_data = request.POST.get("exit_data")
        year = request.POST.get("year")
        place_publication = request.POST.get("place_publication")
        volume_publication = request.POST.get("volume_publication")
        eLIBRARY_ID = request.POST.get("eLIBRARY_ID")
        doi_publication = request.POST.get("doi_publication")
        print(exit_data)
        status='Редактируется'


        if type_publication!="" and full_name_author!="" and name_publication!="" and exit_data!="" and place_publication!="" and eLIBRARY_ID!="" and doi_publication!="":
            status="Завершено"
        publication=Publications.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_publication=TypePublications.get_type_publications_id(type_publication),
                full_name_author=full_name_author,
                name_publication=name_publication,
                exit_data=exit_data,
                year=year,
                place_publication=place_publication,
                volume_publication=volume_publication,
                eLIBRARY_ID=eLIBRARY_ID,
                doi_publication=doi_publication,
                status=status
            )
        publication.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)

class editPublication(View):
    def get(self, request,pk, *args, **kwargs):

        #print(Publications.objects.filter(pk=pk))
        publications=get_object_or_404(Publications, id=pk)

        # form=PublicationFormsEdit(instance=publications)
        serialized_data = serializers.serialize('json', [publications])
        response_data={
            'type_publication': publications.type_publication,
            'full_name_author':publications.full_name_author,
            'name_publication':publications.name_publication,
            'exit_data':publications.exit_data,
            'year':publications.year,
            'place_publication':publications.place_publication,
            'volume_publication':publications.volume_publication,
            'eLIBRARY_ID':publications.eLIBRARY_ID,
            'doi_publication':publications.doi_publication
        }
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        publications = get_object_or_404(Publications,id=pk)
        type_publication = request.POST.get("type_publication")
        full_name_author = request.POST.get("full_name_author")
        name_publication = request.POST.get("name_publication")
        exit_data = request.POST.get("exit_data")
        year = request.POST.get("year")
        place_publication = request.POST.get("place_publication")
        volume_publication = request.POST.get("volume_publication")
        eLIBRARY_ID = request.POST.get("eLIBRARY_ID")
        doi_publication = request.POST.get("doi_publication")

        status='Редактируется'


        if type_publication!="" and full_name_author!="" and name_publication!="" and exit_data!="" and place_publication!="" and eLIBRARY_ID!="" and doi_publication!="":
            status="Завершено"

        print(type_publication)
        publications.type_publication=TypePublications.objects.get(pk=type_publication)
        publications.full_name_author=full_name_author
        publications.name_publication=name_publication
        publications.exit_data=exit_data
        publications.year=year
        publications.place_publication=place_publication
        publications.volume_publication=volume_publication
        publications.eLIBRARY_ID=eLIBRARY_ID
        publications.doi_publication=doi_publication
        publications.status=status

        publications.save()



        return JsonResponse({'message': "Success"}, status=200)



class deletePublication(View):
    def post(self, request, pk):
        try:
            publication = Publications.objects.get(pk=pk)
            publication.delete()
            return JsonResponse({'message': 'Publication deleted successfully'}, status=200)
        except Publications.DoesNotExist:
            return JsonResponse({'error': 'Publication not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



class otchet(View):
    def post(self,request):
        faculty = request.POST.getlist('faculty')
        department = request.POST.getlist('department')
        quarter = request.POST.getlist('quarter')
        tables=request.POST.getlist('table')
        year = request.POST.get('year')
        type_table_publication=request.POST.getlist('table_type')
        # print(quarter,table,type_table_publication)
        # print(UserManager.get_user_id(request.session.get("user_id")))
        user_id=UserManager.get_user_id(request.session.get("user_id"))



class addSecurityDocuments(View):
    def post(self, request, *args, **kwargs):
        type_document = request.POST.get("type_document")
        type_property = request.POST.get("type_property")
        full_name_author = request.POST.get("full_name_author")
        name_publication = request.POST.get("name_publication")
        application_number = request.POST.get("application_number")

        status='Редактируется'


        if type_document!="" and type_property!="" and name_publication!="" and full_name_author!="" and name_publication!="" and application_number!="":
            status="Завершено"
        securitydocuments=SecurityDocuments.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_document=TypeDocuments.objects.get(pk=type_document),
                type_property=TypeProperty.objects.get(pk=type_property),
                full_name_author=full_name_author,
                name_publication=name_publication,
                application_number=application_number,
                status=status
            )
        securitydocuments.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteSecurityDocuments(View):
    def post(self, request, pk):
        try:
            securitydocuments = SecurityDocuments.objects.get(pk=pk)
            securitydocuments.delete()
            return JsonResponse({'message': 'Security Documents deleted successfully'}, status=200)
        except Publications.DoesNotExist:
            return JsonResponse({'error': 'Security Documents not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
