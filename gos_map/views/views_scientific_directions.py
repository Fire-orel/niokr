from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,ScientificDirections
from datetime import datetime

class addScientificDirections(View):
    def post(self, request, *args, **kwargs):
        name_scientific_direction = request.POST.get("name_scientific_direction")
        name_scientific_school = request.POST.get("name_scientific_school")
        leading_scientists = request.POST.get("leading_scientists")
        number_defended_doctoral_dissertations = request.POST.get("number_defended_doctoral_dissertations")
        number_defended_PhD_theses = request.POST.get("number_defended_PhD_theses")
        number_monographs = request.POST.get("number_monographs")
        number_articles_WoS_Scopus = request.POST.get("number_articles_WoS_Scopus")
        number_articles_VAK = request.POST.get("number_articles_VAK")
        number_articles_RIHC = request.POST.get("number_articles_RIHC")
        number_applications_inventions = request.POST.get("number_applications_inventions")
        number_security_documents_received = request.POST.get("number_security_documents_received")
        number_organized = request.POST.get("number_organized")
        amount_funding = request.POST.get("amount_funding")



        status='Редактируется'



        if name_scientific_direction!="" and name_scientific_school!="" and leading_scientists!="" and number_defended_doctoral_dissertations!="" and number_defended_PhD_theses!="" and number_monographs!="" and number_articles_WoS_Scopus!="" and number_articles_VAK!="" and number_articles_RIHC!="" and number_applications_inventions!="" and number_security_documents_received!="" and number_organized!="" and amount_funding!="":
            status="Завершено"

        scientificdirections=ScientificDirections.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                name_scientific_direction=name_scientific_direction,
                name_scientific_school=name_scientific_school,
                leading_scientists=leading_scientists,
                number_defended_doctoral_dissertations=number_defended_doctoral_dissertations,
                number_defended_PhD_theses=number_defended_PhD_theses,
                number_monographs=number_monographs,
                number_articles_WoS_Scopus=number_articles_WoS_Scopus,
                number_articles_VAK=number_articles_VAK,
                number_articles_RIHC=number_articles_RIHC,
                number_applications_inventions=number_applications_inventions,
                number_security_documents_received=number_security_documents_received,
                number_organized=number_organized,
                amount_funding=amount_funding,

                status=status
            )
        scientificdirections.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteScientificDirections(View):
    def post(self, request, pk):
        try:
            scientificdirections = ScientificDirections.objects.get(pk=pk)
            scientificdirections.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except ScientificDirections.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editScientificDirections(View):
    def get(self, request,pk, *args, **kwargs):

        scientificdirections=get_object_or_404(ScientificDirections, id=pk)

        serialized_data = serializers.serialize('json', [scientificdirections])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        scientificdirections = get_object_or_404(ScientificDirections,id=pk)

        name_scientific_direction = request.POST.get("name_scientific_direction")
        name_scientific_school = request.POST.get("name_scientific_school")
        leading_scientists = request.POST.get("leading_scientists")
        number_defended_doctoral_dissertations = request.POST.get("number_defended_doctoral_dissertations")
        number_defended_PhD_theses = request.POST.get("number_defended_PhD_theses")
        number_monographs = request.POST.get("number_monographs")
        number_articles_WoS_Scopus = request.POST.get("number_articles_WoS_Scopus")
        number_articles_VAK = request.POST.get("number_articles_VAK")
        number_articles_RIHC = request.POST.get("number_articles_RIHC")
        number_applications_inventions = request.POST.get("number_applications_inventions")
        number_security_documents_received = request.POST.get("number_security_documents_received")
        number_organized = request.POST.get("number_organized")
        amount_funding = request.POST.get("amount_funding")



        status='Редактируется'



        if name_scientific_direction!="" and name_scientific_school!="" and leading_scientists!="" and number_defended_doctoral_dissertations!="" and number_defended_PhD_theses!="" and number_monographs!="" and number_articles_WoS_Scopus!="" and number_articles_VAK!="" and number_articles_RIHC!="" and number_applications_inventions!="" and number_security_documents_received!="" and number_organized!="" and amount_funding!="":
            status="Завершено"


        scientificdirections.name_scientific_direction=name_scientific_direction
        scientificdirections.name_scientific_school=name_scientific_school
        scientificdirections.leading_scientists=leading_scientists
        scientificdirections.number_defended_doctoral_dissertations=number_defended_doctoral_dissertations
        scientificdirections.number_defended_PhD_theses=number_defended_PhD_theses
        scientificdirections.number_monographs=number_monographs
        scientificdirections.number_articles_WoS_Scopus=number_articles_WoS_Scopus
        scientificdirections.number_articles_VAK=number_articles_VAK
        scientificdirections.number_articles_RIHC=number_articles_RIHC
        scientificdirections.number_applications_inventions=number_applications_inventions
        scientificdirections.number_security_documents_received=number_security_documents_received
        scientificdirections.number_organized=number_organized
        scientificdirections.amount_funding=amount_funding
        scientificdirections.status=status

        scientificdirections.save()



        return JsonResponse({'message': "Success"}, status=200)
