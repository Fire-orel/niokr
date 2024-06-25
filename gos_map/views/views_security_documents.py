from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from gos_map.models import SecurityDocuments,Map,TypeDocuments,TypeProperty,Publications,FullNameАuthor

class addSecurityDocuments(View):
    def post(self, request, *args, **kwargs):
        type_document = request.POST.get("type_document")
        type_property = request.POST.get("type_property")
        full_name_author_security_documents = request.POST.getlist("full_name_author_security_documents")
        name_publication_security_documents = request.POST.get("name_publication_security_documents")
        application_number = request.POST.get("application_number")

        full_name_author_optim=""
        for i in full_name_author_security_documents:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'


        if type_document!="" and type_property!="" and full_name_author_security_documents!="" and name_publication_security_documents!="" and application_number!="":
            status="Завершено"
        securitydocuments=SecurityDocuments.objects.create(
                id_map = Map.get_map_id(request.session.get('map_id')),
                type_document=TypeDocuments.objects.get(pk=type_document),
                type_property=TypeProperty.objects.get(pk=type_property),
                full_name_author_security_documents=full_name_author_optim,
                name_publication_security_documents=name_publication_security_documents,
                application_number=application_number,
                status=status
            )
        securitydocuments.save()
        return JsonResponse({'message': 'Success'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class deleteSecurityDocuments(View):
    def post(self, request, pk):
        try:
            securitydocuments = SecurityDocuments.objects.get(pk=pk)
            securitydocuments.delete()
            return JsonResponse({'message': 'Security Documents deleted successfully'}, status=200)
        except SecurityDocuments.DoesNotExist:
            return JsonResponse({'error': 'Security Documents not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class editSecurityDocuments(View):
    def get(self, request,pk, *args, **kwargs):

        securitydocuments=get_object_or_404(SecurityDocuments, id=pk)

        serialized_data = serializers.serialize('json', [securitydocuments])
        return JsonResponse({'form_data': serialized_data}, status=200)

    def post(self, request,pk, *args, **kwargs):
        securitydocuments = get_object_or_404(SecurityDocuments,id=pk)
        type_document = request.POST.get("type_document")
        type_property = request.POST.get("type_property")
        full_name_author_security_documents = request.POST.getlist("full_name_author_security_documents")
        name_publication_security_documents = request.POST.get("name_publication_security_documents")
        application_number = request.POST.get("application_number")

        full_name_author_optim=""
        for i in full_name_author_security_documents:
            if i.isdigit():
                name=FullNameАuthor.objects.get(pk=i).full_name
                full_name_author_optim=full_name_author_optim+name+','
            else:
                full_name_author_optim=full_name_author_optim+i+','

        status='Редактируется'


        if type_document!="" and type_property!="" and full_name_author_security_documents!="" and name_publication_security_documents!="" and application_number!="":
            status="Завершено"

        securitydocuments.type_document=TypeDocuments.objects.get(pk=type_document)
        securitydocuments.type_property=TypeProperty.objects.get(pk=type_property)
        securitydocuments.full_name_author_security_documents=full_name_author_optim
        securitydocuments.name_publication_security_documents=name_publication_security_documents
        securitydocuments.application_number=application_number
        securitydocuments.status=status

        securitydocuments.save()



        return JsonResponse({'message': "Success"}, status=200)
