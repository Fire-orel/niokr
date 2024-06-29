from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeProperty
from datetime import datetime

class addTypeProperty(View):
    def post(self, request, *args, **kwargs):

        name_type_property = request.POST.get("name_type_property")

        type_property=TypeProperty.objects.create(
                name_type_property = name_type_property
            )
        type_property.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeProperty(View):
    def post(self, request, pk):
        try:
            type_property = TypeProperty.objects.get(pk=pk)
            type_property.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeProperty.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeProperty(View):
    def get(self, request,pk, *args, **kwargs):

        type_property=get_object_or_404(TypeProperty, id=pk)

        serialized_data = serializers.serialize('json', [type_property])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_property = get_object_or_404(TypeProperty,id=pk)
        name_type_property = request.POST.get("name_type_property")

        type_property.name_type_property=name_type_property

        type_property.save()



        return JsonResponse({'message': "Success"}, status=200)
