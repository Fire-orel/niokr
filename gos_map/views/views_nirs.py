from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,FormParticipation,NIRS,FullNameАuthor
from datetime import datetime

class addNIRS(View):
    def post(self, request, *args, **kwargs):
        number_students = request.POST.get("number_students")
        full_name_students = request.POST.getlist("full_name_students")
        form_participation = request.POST.get("form_participation")
        name_event_nirs = request.POST.get("name_event_nirs")
        full_name_scientific_supervisor = request.POST.getlist("full_name_scientific_supervisor")
        awards_diplomas = request.POST.get("awards_diplomas")
        date_event_nirs = request.POST.get("date_event_nirs")

        status='Редактируется'

        full_name_students_optim=""
        for i in full_name_students:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_students_optim=full_name_students_optim+name+','
            else:
                full_name_students_optim=full_name_students_optim+i+','

        full_name_scientific_supervisor_optim=""
        for i in full_name_scientific_supervisor:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_scientific_supervisor_optim=full_name_scientific_supervisor_optim+name+','
            else:
                full_name_scientific_supervisor_optim=full_name_scientific_supervisor_optim+i+','





        if full_name_students!="" and form_participation!="" and name_event_nirs!="" and full_name_scientific_supervisor!="" and awards_diplomas!="" and date_event_nirs!="":
            status="Завершено"

        nirs=NIRS.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                number_students=number_students,
                full_name_students=full_name_students_optim,
                form_participation=FormParticipation.objects.get(pk=form_participation),
                name_event_nirs=name_event_nirs,
                full_name_scientific_supervisor=full_name_scientific_supervisor_optim,
                awards_diplomas=awards_diplomas,
                date_event_nirs=date_event_nirs,
                status=status
            )
        nirs.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteNIRS(View):
    def post(self, request, pk):
        try:
            nirs = NIRS.objects.get(pk=pk)
            nirs.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except NIRS.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editNIRS(View):
    def get(self, request,pk, *args, **kwargs):

        nirs=get_object_or_404(NIRS, id=pk)

        serialized_data = serializers.serialize('json', [nirs])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        nirs = get_object_or_404(NIRS,id=pk)
        number_students = request.POST.get("number_students")
        full_name_students =request.POST.getlist("full_name_students")
        form_participation = request.POST.get("form_participation")
        name_event_nirs = request.POST.get("name_event_nirs")
        full_name_scientific_supervisor = request.POST.getlist("full_name_scientific_supervisor")
        awards_diplomas = request.POST.get("awards_diplomas")
        date_event_nirs = request.POST.get("date_event_nirs")

        full_name_students_optim=""
        for i in full_name_students:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_students_optim=full_name_students_optim+name+','
            else:
                full_name_students_optim=full_name_students_optim+i+','

        full_name_scientific_supervisor_optim=""
        for i in full_name_scientific_supervisor:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_scientific_supervisor_optim=full_name_scientific_supervisor_optim+name+','
            else:
                full_name_scientific_supervisor_optim=full_name_scientific_supervisor_optim+i+','

        status='Редактируется'



        if full_name_students!="" and form_participation!="" and name_event_nirs!="" and full_name_scientific_supervisor!="" and awards_diplomas!="" and date_event_nirs!="":
            status="Завершено"


        nirs.number_students=number_students
        nirs.full_name_students=full_name_students_optim
        nirs.form_participation=FormParticipation.objects.get(pk=form_participation)
        nirs.name_event_nirs=name_event_nirs
        nirs.full_name_scientific_supervisor=full_name_scientific_supervisor_optim
        nirs.awards_diplomas=awards_diplomas
        nirs.date_event_nirs=date_event_nirs
        nirs.status=status

        nirs.save()



        return JsonResponse({'message': "Success"}, status=200)
