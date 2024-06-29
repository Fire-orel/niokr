from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeMonographs
from datetime import datetime

class addTypeMonographs(View):
    def post(self, request, *args, **kwargs):
        
        name_type_monographs = request.POST.get("name_type_monographs")

        type_monographs=TypeMonographs.objects.create(
                name_type_monographs = name_type_monographs
            )
        type_monographs.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeMonographs(View):
    def post(self, request, pk):
        try:
            type_monographs = TypeMonographs.objects.get(pk=pk)
            type_monographs.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeMonographs.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeMonographs(View):
    def get(self, request,pk, *args, **kwargs):

        type_monographs=get_object_or_404(TypeMonographs, id=pk)

        serialized_data = serializers.serialize('json', [type_monographs])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_monographs = get_object_or_404(TypeMonographs,id=pk)
        name_type_monographs = request.POST.get("name_type_monographs")

        type_monographs.name_type_monographs=name_type_monographs

        type_monographs.save()



        return JsonResponse({'message': "Success"}, status=200)
