from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import Map,Grant,TypeGrant,FullNameАuthor
from datetime import datetime

class addGrant(View):
    def post(self, request, *args, **kwargs):
        type_grant = request.POST.get("type_grant")
        name_fund = request.POST.get("name_fund")
        name_competition = request.POST.get("name_competition")
        kod_competition = request.POST.get("kod_competition")
        nomination = request.POST.get("nomination")
        name_project_topic = request.POST.get("name_project_topic")
        project_manager = request.POST.getlist("project_manager")
        number_project_team = request.POST.get("number_project_team")
        number_young_scientists = request.POST.get("number_young_scientists")
        full_name_performer = request.POST.getlist("full_name_performer")
        winner = request.POST.get("winner")

        project_manager_optim=""
        for i in project_manager:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                project_manager_optim=project_manager_optim+name+','
            else:
                project_manager_optim=project_manager_optim+i+','

        full_name_performer_optim=""
        for i in full_name_performer:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_performer_optim=full_name_performer_optim+name+','
            else:
                full_name_performer_optim=full_name_performer_optim+i+','


        status='Редактируется'



        if type_grant!="" and name_fund!="" and name_competition!="" and kod_competition!="" and nomination!="" and name_project_topic!="" and len(project_manager)!=0 and number_project_team!="" and number_young_scientists!="" and len(full_name_performer)!=0 and winner!="":
            status="Завершено"

        grant=Grant.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_grant=TypeGrant.objects.get(pk=type_grant),
                name_fund=name_fund,
                name_competition=name_competition,
                kod_competition=kod_competition,
                nomination=nomination,
                name_project_topic=name_project_topic,
                project_manager=project_manager_optim,
                number_project_team=number_project_team,
                number_young_scientists=number_young_scientists,
                full_name_performer=full_name_performer_optim,
                winner=winner,
                status=status
            )
        grant.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteGrant(View):
    def post(self, request, pk):
        try:
            event = Grant.objects.get(pk=pk)
            event.delete()
            return JsonResponse({'message': 'Event deleted successfully'}, status=200)
        except Grant.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editGrant(View):
    def get(self, request,pk, *args, **kwargs):

        grant=get_object_or_404(Grant, id=pk)

        serialized_data = serializers.serialize('json', [grant])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        grant = get_object_or_404(Grant,id=pk)
        type_grant = request.POST.get("type_grant")
        name_fund = request.POST.get("name_fund")
        name_competition = request.POST.get("name_competition")
        kod_competition = request.POST.get("kod_competition")
        nomination = request.POST.get("nomination")
        name_project_topic = request.POST.get("name_project_topic")
        project_manager = request.POST.getlist("project_manager")
        number_project_team = request.POST.get("number_project_team")
        number_young_scientists = request.POST.get("number_young_scientists")
        full_name_performer = request.POST.getlist("full_name_performer")
        winner = request.POST.get("winner")

        project_manager_optim=""
        for i in project_manager:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                project_manager_optim=project_manager_optim+name+','
            else:
                project_manager_optim=project_manager_optim+i+','

        full_name_performer_optim=""
        for i in full_name_performer:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_performer_optim=full_name_performer_optim+name+','
            else:
                full_name_performer_optim=full_name_performer_optim+i+','


        status='Редактируется'



        if type_grant!="" and name_fund!="" and name_competition!="" and kod_competition!="" and nomination!="" and name_project_topic!="" and project_manager!="" and number_project_team!="" and number_young_scientists!="" and full_name_performer!="" and winner!="":
            status="Завершено"

        grant.type_grant=TypeGrant.objects.get(pk=type_grant)
        grant.name_fund=name_fund
        grant.name_competition=name_competition
        grant.kod_competition=kod_competition
        grant.nomination=nomination
        grant.name_project_topic=name_project_topic
        grant.project_manager=project_manager_optim
        grant.number_project_team=number_project_team
        grant.number_young_scientists=number_young_scientists
        grant.full_name_performer=full_name_performer_optim
        grant.winner=winner
        grant.status=status

        grant.save()



        return JsonResponse({'message': "Success"}, status=200)
