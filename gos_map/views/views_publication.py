from django.views import View
from gos_map.models import Publications,TypePublications,Map,FullNameАuthor
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

class addPublication(View):
    def post(self, request, *args, **kwargs):
        type_publication = request.POST.get("type_publication")
        full_name_author_publications = request.POST.getlist("full_name_author_publications")
        name_publication_publications = request.POST.get("name_publication_publications")
        exit_data = request.POST.get("exit_data")
        year = request.POST.get("year")
        place_publication_publications = request.POST.get("place_publication_publications")
        volume_publication = request.POST.get("volume_publication")
        eLIBRARY_ID = request.POST.get("eLIBRARY_ID")
        doi_publication = request.POST.get("doi_publication")
        print(full_name_author_publications)


        full_name_author_optim=""
        for i in full_name_author_publications:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','
        status='Редактируется'


        if type_publication!="" and len(full_name_author_publications)!=0 and name_publication_publications!="" and exit_data!="" and place_publication_publications!="" and eLIBRARY_ID!="" and doi_publication!="":
            status="Завершено"

        publication=Publications.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_publication=TypePublications.get_type_publications_id(type_publication),
                full_name_author_publications=full_name_author_optim,
                name_publication_publications=name_publication_publications,
                exit_data=exit_data,
                year=year,
                place_publication_publications=place_publication_publications,
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

        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        publications = get_object_or_404(Publications,id=pk)
        type_publication = request.POST.get("type_publication")
        full_name_author_publications = request.POST.getlist("full_name_author_publications")
        name_publication_publications = request.POST.get("name_publication_publications")
        exit_data = request.POST.get("exit_data")
        year = request.POST.get("year")
        place_publication_publications = request.POST.get("place_publication_publications")
        volume_publication = request.POST.get("volume_publication")
        eLIBRARY_ID = request.POST.get("eLIBRARY_ID")
        doi_publication = request.POST.get("doi_publication")

        full_name_author_optim=""
        for i in full_name_author_publications:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'


        if type_publication!="" and len(full_name_author_publications)!=0 and name_publication_publications!="" and exit_data!="" and place_publication_publications!="" and eLIBRARY_ID!="" and doi_publication!="":
            status="Завершено"


        publications.type_publication=TypePublications.objects.get(pk=type_publication)
        publications.full_name_author_publications=full_name_author_optim
        publications.name_publication_publications=name_publication_publications
        publications.exit_data=exit_data
        publications.year=year
        publications.place_publication_publications=place_publication_publications
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
