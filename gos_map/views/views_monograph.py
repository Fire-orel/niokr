from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,Monographs,TypeMonographs,FullNameАuthor

class addMonographs(View):
    def post(self, request, *args, **kwargs):
        type_monographs = request.POST.get("type_monographs")
        full_name_author_Monographs = request.POST.getlist("full_name_author_monographs")
        name_works = request.POST.get("name_works")
        circulation = request.POST.get("circulation")
        volume_monographs = request.POST.get("volume_monographs")
        publishing_house = request.POST.get("publishing_house")
        type_publishing_house = request.POST.get("type_publishing_house")
        year_of_publication_monographs = request.POST.get("year_of_publication_monographs")



        full_name_author_optim=""
        for i in full_name_author_Monographs:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'

        print(full_name_author_optim)

        if type_monographs!="" and full_name_author_Monographs!="" and name_works!="" and circulation!="" and volume_monographs!="" and publishing_house!="" and type_publishing_house!="" and year_of_publication_monographs!="":
            status="Завершено"

        monographs=Monographs.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_monographs=TypeMonographs.objects.get(pk=type_monographs),
                full_name_author_monographs=full_name_author_optim,
                name_works=name_works,
                circulation=circulation,
                volume_monographs=volume_monographs,

                publishing_house=publishing_house,
                type_publishing_house=type_publishing_house,
                year_of_publication_monographs=year_of_publication_monographs,
                status=status
            )
        monographs.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteMonograph(View):
    def post(self, request, pk):
        try:
            monographs = Monographs.objects.get(pk=pk)
            monographs.delete()
            return JsonResponse({'message': 'Security Documents deleted successfully'}, status=200)
        except Monographs.DoesNotExist:
            return JsonResponse({'error': 'Security Documents not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editMonographs(View):
    def get(self, request,pk, *args, **kwargs):

        monographs=get_object_or_404(Monographs, id=pk)

        serialized_data = serializers.serialize('json', [monographs])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        monographs = get_object_or_404(Monographs,id=pk)
        type_monographs = request.POST.get("type_monographs")
        full_name_author_Monographs = request.POST.getlist("full_name_author_monographs")
        name_works = request.POST.get("name_works")
        circulation = request.POST.get("circulation")
        volume_monographs = request.POST.get("volume_monographs")
        publishing_house = request.POST.get("publishing_house")
        type_publishing_house = request.POST.get("type_publishing_house")
        year_of_publication_monographs = request.POST.get("year_of_publication_monographs")

        full_name_author_optim=""
        for i in full_name_author_Monographs:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'


        if type_monographs!="" and full_name_author_Monographs!="" and name_works!="" and circulation!="" and volume_monographs!="" and publishing_house!="" and type_publishing_house!="" and year_of_publication_monographs!="":
            status="Завершено"


        monographs.type_monographs=TypeMonographs.objects.get(pk=type_monographs)
        monographs.full_name_author_monographs=full_name_author_optim
        monographs.name_works=name_works
        monographs.circulation=circulation
        monographs.volume_monographs=volume_monographs
        monographs.publishing_house=publishing_house
        monographs.type_publishing_house=type_publishing_house
        monographs.year_of_publication_monographs=year_of_publication_monographs
        monographs.status=status

        monographs.save()



        return JsonResponse({'message': "Success"}, status=200)
