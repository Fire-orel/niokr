# zip_buffer = io.BytesIO()
# if len(quarter)!=0:
#     for i in quarter:

#         map_dates=Map.objects.filter(quarter=i,responsible=user_id)
#         with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
#             for map_date in map_dates:

#                 workbook = Workbook()
#                 workbook.remove(workbook.active)
#                 for table in tables:

#                     if table == 'publication':
#                         count=2
#                         sheet = workbook.create_sheet('Публикации')
#                         sheet['A1']="Тип публикации"
#                         sheet['B1']="ФИО автора"
#                         sheet['C1']="Наименование публикации"
#                         sheet['D1']="Выходные данные публикации (Название журнала, Номер, Том, страницы)"
#                         sheet['E1']="Год"
#                         sheet['F1']="Место опубликования"
#                         sheet['G1']="Объем публикации (п.л.)"
#                         sheet['H1']="eLIBRARY ID"
#                         sheet['I1']="DOI публикации"
#                         if len(type_table_publication)== 0:
#                             publications=Publications.objects. filter(id_map=map_date)
#                             for u in publications:
#                                 print(u.full_name_author,map_date)
#                                 sheet[f"A{count}"]=u.type_publication.name_type_publications
#                                 sheet[f"B{count}"]=u.full_name_author
#                                 sheet[f"C{count}"]=u.name_publication
#                                 sheet[f"D{count}"]=u.exit_data
#                                 sheet[f"E{count}"]=u.year
#                                 sheet[f"F{count}"]=u.place_publication
#                                 sheet[f"G{count}"]=u.volume_publication
#                                 sheet[f"H{count}"]=u.eLIBRARY_ID
#                                 sheet[f"I{count}"]=u.doi_publication
#                                 count+=1
#                         else:
#                             for type in type_table_publication:
#                                 publications=Publications.objects.filter(id_map=type,type_publication=type)
#                                 for w in publications:
#                                     print(2)
#                                     sheet[f"A{count}"]=w.type_publication.name_type_publications
#                                     sheet[f"B{count}"]=w.full_name_author
#                                     sheet[f"C{count}"]=w.name_publication
#                                     sheet[f"D{count}"]=w.exit_data
#                                     sheet[f"E{count}"]=w.year
#                                     sheet[f"F{count}"]=w.place_publication
#                                     sheet[f"G{count}"]=w.volume_publication
#                                     sheet[f"H{count}"]=w.eLIBRARY_ID
#                                     sheet[f"I{count}"]=w.doi_publication
#                                     count+=1



#                 file_buffer = io.BytesIO()
#                 workbook.save(file_buffer)
#                 file_buffer.seek(0)

#                 # Добавляем файл в ZIP-архив

#                 zip_file.writestr(f'{map_date.__str__()}.xlsx', file_buffer.read())
# else:
#     map_dates=Map.objects.filter()
#     with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
#         for map_date in map_dates:

#             workbook = Workbook()
#             workbook.remove(workbook.active)
#             for table in tables:

#                 if table == 'publication':
#                     count=2
#                     sheet = workbook.create_sheet('Публикации')
#                     sheet['A1']="Тип публикации"
#                     sheet['B1']="ФИО автора"
#                     sheet['C1']="Наименование публикации"
#                     sheet['D1']="Выходные данные публикации (Название журнала, Номер, Том, страницы)"
#                     sheet['E1']="Год"
#                     sheet['F1']="Место опубликования"
#                     sheet['G1']="Объем публикации (п.л.)"
#                     sheet['H1']="eLIBRARY ID"
#                     sheet['I1']="DOI публикации"
#                     if len(type_table_publication)== 0:
#                         publications=Publications.objects. filter(id_map=map_date)
#                         for u in publications:

#                             sheet[f"A{count}"]=u.type_publication.name_type_publications
#                             sheet[f"B{count}"]=u.full_name_author
#                             sheet[f"C{count}"]=u.name_publication
#                             sheet[f"D{count}"]=u.exit_data
#                             sheet[f"E{count}"]=u.year
#                             sheet[f"F{count}"]=u.place_publication
#                             sheet[f"G{count}"]=u.volume_publication
#                             sheet[f"H{count}"]=u.eLIBRARY_ID
#                             sheet[f"I{count}"]=u.doi_publication
#                             count+=1
#                     else:
#                         for type in type_table_publication:
#                             publications=Publications.objects.filter(id_map=type,type_publication=type)
#                             for w in publications:
#                                 print(2)
#                                 sheet[f"A{count}"]=w.type_publication.name_type_publications
#                                 sheet[f"B{count}"]=w.full_name_author
#                                 sheet[f"C{count}"]=w.name_publication
#                                 sheet[f"D{count}"]=w.exit_data
#                                 sheet[f"E{count}"]=w.year
#                                 sheet[f"F{count}"]=w.place_publication
#                                 sheet[f"G{count}"]=w.volume_publication
#                                 sheet[f"H{count}"]=w.eLIBRARY_ID
#                                 sheet[f"I{count}"]=w.doi_publication
#                                 count+=1



#             file_buffer = io.BytesIO()
#             workbook.save(file_buffer)
#             file_buffer.seek(0)

#             # Добавляем файл в ZIP-архив

#             zip_file.writestr(f'{map_date.__str__()}.xlsx', file_buffer.read())

# # Настраиваем ответ для передачи ZIP-архива
# response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
# response['Content-Disposition'] = 'attachment; filename=tables.zip'

# return response
