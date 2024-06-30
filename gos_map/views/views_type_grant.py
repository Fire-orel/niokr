from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,TypeGrant
from datetime import datetime

class addTypeGrant(View):
    def post(self, request, *args, **kwargs):

        name_type_grant = request.POST.get("name_type_grant")

        type_grant=TypeGrant.objects.create(
                name_type_grant = name_type_grant
            )
        type_grant.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteTypeGrant(View):
    def post(self, request, pk):
        try:
            type_grant = TypeGrant.objects.get(pk=pk)
            type_grant.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except TypeGrant.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editTypeGrant(View):
    def get(self, request,pk, *args, **kwargs):

        type_grant=get_object_or_404(TypeGrant, id=pk)
        print(type_grant)

        serialized_data = serializers.serialize('json', [type_grant])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        type_grant = get_object_or_404(TypeGrant,id=pk)
        name_type_grant = request.POST.get("name_type_grant")

        type_grant.name_type_grant=name_type_grant

        type_grant.save()



        return JsonResponse({'message': "Success"}, status=200)
