# views.py

from django.contrib.auth import login,logout
from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from ldap3 import Server, Connection, ALL, NTLM
from .forms import LoginForm,MapForms,PublicationForms
from .models import UserManager,Map,Publications,TypePublications
from django.views.generic import ListView
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from openpyxl import Workbook
import zipfile
import io


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
        user_id = request.session.get('user_id')
        print(UserManager.get_user_id(request.session.get("user_id")).position)
        context = {
            'user_full_name': user_full_name,
            'user_id':UserManager.get_user_id(request.session.get("user_id")),
            'user_posistion':UserManager.get_user_id(request.session.get("user_id")).position,
            'maps': Map.objects.all (),
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
        context = {
            'user_full_name': user_full_name,
            'map':data,
            'publications':publications,
            'publicationsforms':PublicationForms(),
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
        # print(request.session.get('map_id'))
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
                doi_publication=doi_publication
            )
        publication.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)



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
        map_list=[]
        zip_buffer = io.BytesIO()
        if len(quarter)!=0:
            for i in quarter:

                map_dates=Map.objects.filter(quarter=i)
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for map_date in map_dates:

                        workbook = Workbook()
                        workbook.remove(workbook.active)
                        for table in tables:

                            if table == 'publication':
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
                                if len(type_table_publication)== 0:
                                    publications=Publications.objects. filter(id_map=map_date)
                                    for u in publications:
                                        print(u.full_name_author,map_date)
                                        sheet[f"A{count}"]=u.type_publication.name_type_publications
                                        sheet[f"B{count}"]=u.full_name_author
                                        sheet[f"C{count}"]=u.name_publication
                                        sheet[f"D{count}"]=u.exit_data
                                        sheet[f"E{count}"]=u.year
                                        sheet[f"F{count}"]=u.place_publication
                                        sheet[f"G{count}"]=u.volume_publication
                                        sheet[f"H{count}"]=u.eLIBRARY_ID
                                        sheet[f"I{count}"]=u.doi_publication
                                        count+=1
                                else:
                                    for type in type_table_publication:
                                        publications=Publications.objects.filter(id_map=type,type_publication=u)
                                        for w in publications:
                                            print(2)
                                            sheet[f"A{count}"]=w.type_publication.name_type_publications
                                            sheet[f"B{count}"]=w.full_name_author
                                            sheet[f"C{count}"]=w.name_publication
                                            sheet[f"D{count}"]=w.exit_data
                                            sheet[f"E{count}"]=w.year
                                            sheet[f"F{count}"]=w.place_publication
                                            sheet[f"G{count}"]=w.volume_publication
                                            sheet[f"H{count}"]=w.eLIBRARY_ID
                                            sheet[f"I{count}"]=w.doi_publication
                                            count+=1



                        file_buffer = io.BytesIO()
                        workbook.save(file_buffer)
                        file_buffer.seek(0)

                        # Добавляем файл в ZIP-архив

                        zip_file.writestr(f'{map_date.__str__()}.xlsx', file_buffer.read())
        else:
            map_dates=Map.objects.filter()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for map_date in map_dates:

                    workbook = Workbook()
                    workbook.remove(workbook.active)
                    for table in tables:

                        if table == 'publication':
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
                            if len(type_table_publication)== 0:
                                publications=Publications.objects. filter(id_map=map_date)
                                for u in publications:
                                    print(u.full_name_author,map_date)
                                    sheet[f"A{count}"]=u.type_publication.name_type_publications
                                    sheet[f"B{count}"]=u.full_name_author
                                    sheet[f"C{count}"]=u.name_publication
                                    sheet[f"D{count}"]=u.exit_data
                                    sheet[f"E{count}"]=u.year
                                    sheet[f"F{count}"]=u.place_publication
                                    sheet[f"G{count}"]=u.volume_publication
                                    sheet[f"H{count}"]=u.eLIBRARY_ID
                                    sheet[f"I{count}"]=u.doi_publication
                                    count+=1
                            else:
                                for type in type_table_publication:
                                    publications=Publications.objects.filter(id_map=type,type_publication=u)
                                    for w in publications:
                                        print(2)
                                        sheet[f"A{count}"]=w.type_publication.name_type_publications
                                        sheet[f"B{count}"]=w.full_name_author
                                        sheet[f"C{count}"]=w.name_publication
                                        sheet[f"D{count}"]=w.exit_data
                                        sheet[f"E{count}"]=w.year
                                        sheet[f"F{count}"]=w.place_publication
                                        sheet[f"G{count}"]=w.volume_publication
                                        sheet[f"H{count}"]=w.eLIBRARY_ID
                                        sheet[f"I{count}"]=w.doi_publication
                                        count+=1



                    file_buffer = io.BytesIO()
                    workbook.save(file_buffer)
                    file_buffer.seek(0)

                    # Добавляем файл в ZIP-архив

                    zip_file.writestr(f'{map_date.__str__()}.xlsx', file_buffer.read())

        # Настраиваем ответ для передачи ZIP-архива
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=tables.zip'

        return response
