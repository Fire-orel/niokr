from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeDocuments
from datetime import datetime

class addTypeDocuments(View):
    def post(self, request, *args, **kwargs):

        name_type_documents = request.POST.get("name_type_documents")

        type_documents=TypeDocuments.objects.create(
                name_type_documents = name_type_documents
            )
        type_documents.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeDocuments(View):
    def post(self, request, pk):
        try:
            type_documents = TypeDocuments.objects.get(pk=pk)
            type_documents.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeDocuments.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeDocuments(View):
    def get(self, request,pk, *args, **kwargs):

        type_documents=get_object_or_404(TypeDocuments, id=pk)

        serialized_data = serializers.serialize('json', [type_documents])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_documents = get_object_or_404(TypeDocuments,id=pk)
        name_type_documents = request.POST.get("name_type_documents")

        type_documents.name_type_documents=name_type_documents

        type_documents.save()



        return JsonResponse({'message': "Success"}, status=200)
