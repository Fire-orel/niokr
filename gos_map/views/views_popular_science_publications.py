from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,PopularSciencePublications,FullNameАuthor
from datetime import datetime

class addPopularSciencePublications(View):
    def post(self, request, *args, **kwargs):
        full_name_author = request.POST.getlist("full_name_author")
        name_publication_popular_science_publications = request.POST.get("name_publication_popular_science_publications")
        place_publication_popular_science_publications = request.POST.get("place_publication_popular_science_publications")
        volume_popular_science_publications = request.POST.get("volume_popular_science_publications")
        note = request.POST.get("note")

        full_name_author_optim=""
        for i in full_name_author:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'






        if full_name_author!="" and name_publication_popular_science_publications!="" and place_publication_popular_science_publications!="" and volume_popular_science_publications!="" and note!="":
            status="Завершено"

        popular_science_publications=PopularSciencePublications.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                full_name_author=full_name_author_optim,
                name_publication_popular_science_publications=name_publication_popular_science_publications,
                place_publication_popular_science_publications=place_publication_popular_science_publications,
                volume_popular_science_publications=volume_popular_science_publications,
                note=note,
                status=status
            )
        popular_science_publications.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deletePopularSciencePublications(View):
    def post(self, request, pk):
        try:
            popular_science_publications = PopularSciencePublications.objects.get(pk=pk)
            popular_science_publications.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except PopularSciencePublications.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editPopularSciencePublications(View):
    def get(self, request,pk, *args, **kwargs):

        popular_science_publications=get_object_or_404(PopularSciencePublications, id=pk)



        serialized_data = serializers.serialize('json', [popular_science_publications])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        popular_science_publications = get_object_or_404(PopularSciencePublications,id=pk)
        full_name_author = request.POST.getlist("full_name_author")
        name_publication_popular_science_publications = request.POST.get("name_publication_popular_science_publications")
        place_publication_popular_science_publications = request.POST.get("place_publication_popular_science_publications")
        volume_popular_science_publications = request.POST.get("volume_popular_science_publications")
        note = request.POST.get("note")

        full_name_author_optim=""
        for i in full_name_author:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'




        if full_name_author!="" and name_publication_popular_science_publications!="" and place_publication_popular_science_publications!="" and volume_popular_science_publications!="" and note!="":
            status="Завершено"

        popular_science_publications.full_name_author=full_name_author_optim
        popular_science_publications.name_publication_popular_science_publications=name_publication_popular_science_publications
        popular_science_publications.place_publication_popular_science_publications=place_publication_popular_science_publications
        popular_science_publications.volume_popular_science_publications=volume_popular_science_publications
        popular_science_publications.note=note
        popular_science_publications.status=status

        popular_science_publications.save()



        return JsonResponse({'message': "Success"}, status=200)
