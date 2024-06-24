from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,FormParticipation,InternationalCooperation
from datetime import datetime

class addInternationalCooperation(View):
    def post(self, request, *args, **kwargs):
        name_scientific_research = request.POST.get("name_scientific_research")
        name_scientific_centers = request.POST.get("name_scientific_centers")
        name_topics = request.POST.get("name_topics")
        name_research_topics = request.POST.get("name_research_topics")
        name_scientific_programs = request.POST.get("name_scientific_programs")

        status='Редактируется'



        if name_scientific_research!="" and name_scientific_centers!="" and name_topics!="" and name_research_topics!="" and name_scientific_programs!="":
            status="Завершено"

        internationalcooperation=InternationalCooperation.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                name_scientific_research=name_scientific_research,
                name_scientific_centers=name_scientific_centers,
                name_topics=name_topics,
                name_research_topics=name_research_topics,
                name_scientific_programs=name_scientific_programs,
                status=status
            )
        internationalcooperation.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteInternationalCooperation(View):
    def post(self, request, pk):
        try:
            internationalcooperation = InternationalCooperation.objects.get(pk=pk)
            internationalcooperation.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except InternationalCooperation.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editInternationalCooperation(View):
    def get(self, request,pk, *args, **kwargs):

        internationalcooperation=get_object_or_404(InternationalCooperation, id=pk)

        serialized_data = serializers.serialize('json', [internationalcooperation])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        internationalcooperation=get_object_or_404(InternationalCooperation, id=pk)
        name_scientific_research = request.POST.get("name_scientific_research")
        name_scientific_centers = request.POST.get("name_scientific_centers")
        name_topics = request.POST.get("name_topics")
        name_research_topics = request.POST.get("name_research_topics")
        name_scientific_programs = request.POST.get("name_scientific_programs")

        status='Редактируется'





        if name_scientific_research!="" and name_scientific_centers!="" and name_topics!="" and name_research_topics!="" and name_scientific_programs!="":
            status="Завершено"

        internationalcooperation.name_scientific_research=name_scientific_research
        internationalcooperation.name_scientific_centers=name_scientific_centers
        internationalcooperation.name_topics=name_topics
        internationalcooperation.name_research_topics=name_research_topics
        internationalcooperation.name_scientific_programs=name_scientific_programs
        internationalcooperation.status=status

        internationalcooperation.save()



        return JsonResponse({'message': "Success"}, status=200)
