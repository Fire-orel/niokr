from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypePublications
from datetime import datetime

class addTypePublications(View):
    def post(self, request, *args, **kwargs):

        name_type_publications = request.POST.get("name_type_publications")
        print(name_type_publications)
        type_publications=TypePublications.objects.create(
                name_type_publications = name_type_publications
            )
        type_publications.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypePublications(View):
    def post(self, request, pk):
        try:
            type_publications = TypePublications.objects.get(pk=pk)
            type_publications.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypePublications.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypePublications(View):
    def get(self, request,pk, *args, **kwargs):

        type_publications=get_object_or_404(TypePublications, id=pk)

        serialized_data = serializers.serialize('json', [type_publications])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_publications = get_object_or_404(TypePublications,id=pk)
        name_type_publications = request.POST.get("name_type_publications")

        type_publications.name_type_publications=name_type_publications

        type_publications.save()



        return JsonResponse({'message': "Success"}, status=200)
