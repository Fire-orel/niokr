$(document).ready(function() {
    $("#SecurityDocumentsModal").on('hidden.bs.modal',function() {
        $('#addSecurityDocumentsForm').attr('id','SecurityDocumentsForm');
        $('#editSecurityDocumentsForm').attr('id','SecurityDocumentsForm');
        $('#error-message-security-documents').hide().text('');
        $('#SecurityDocumentsForm')[0].reset();
        $('#id_full_name_author_security_documents').val(null).trigger('change');
    });





    $(document).on('click', '#deleteSecurityDocuments', function(){

        var securitydocuments = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteSecurityDocumentsBtn').data('id', securitydocuments); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteSecurityDocumentsBtn').click(function() {


        var securitydocuments = $(this).data('id');// Получаем ID публикации
        console.log(securitydocuments)

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_security_documents/${securitydocuments}/`, // Путь к представлению для удаления публикации
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                // Обновляем страницу или делаем что-то еще при успешном удалении
                location.reload();
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    });

     //Добавления и редактирование таблицы SecurityDocuments
    $(document).on('click', '#addsecuritydocument', function(){

        $('#SecurityDocumentsForm').attr('id','addSecurityDocumentsForm');
        $('#addSecurityDocumentsForm').attr('action',"/add_security_documents/");

    });

    $(document).on('submit','#addSecurityDocumentsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#SecurityDocumentsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-security-documents').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editsecuritydocuments', function(){
        var securitydocumentId = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_security_documents/${securitydocumentId}/`,
            data: securitydocumentId ,


            success: function(response) {
                $('#SecurityDocumentsForm').attr('id','editSecurityDocumentsForm');
                $('#editSecurityDocumentsForm').attr('action',`/edit_security_documents/${securitydocumentId}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                var full_name_author_security_documentss=formData.full_name_author_security_documents.split(',')

                var filtered_full_name_author_security_documents = full_name_author_security_documentss.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_author_security_documents.forEach(function(full_name_author) {
                    // Создаем новую опцию, если её нет в списке
                    var optionExists = $("#id_full_name_author_security_documents option").filter(function() {
                        return $(this).text() === full_name_author;
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author, full_name_author, true, true);
                        $('#id_full_name_author_security_documents').append(newOption).trigger('change');
                    }
                });

                var full_name_author_security_documents_check = full_name_author_security_documentss.map(function(full_name_author) {

                    return full_name_author;
                });



                $('#id_type_document').val(formData.type_document);
                $('#id_type_property').val(formData.type_property);
                $('#id_full_name_author_security_documents').val(full_name_author_security_documents_check).trigger('change');
                $('#id_name_publication_security_documents').val(formData.name_publication_security_documents);
                $('#id_application_number').val(formData.application_number);
                $('#SecurityDocumentsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editSecurityDocumentsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#SecurityDocumentsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-security-documents').text("Ошибка").show();
            }
        });
    });

    $('#id_full_name_author_security_documents').select2({
        multiple: true,
        tags: true,
        tokenSeparators: [','],  // Разделители для тегов
        placeholder: 'Выберите или введите авторов',
        createTag: function (params) {
            var term = $.trim(params.term);
            if (term === '') {
                return null;
            }
            return {
                id: term,
                text: term,
                newTag: true // add additional parameters
            };
        },
        ajax: {
            url: '/path/to/select2-data/', // Убедитесь, что URL правильный
            dataType: 'json',

            data: function(params) {
                return {
                    q: params.term // Передача введенного текста на сервер
                };
            },
            processResults: function(data) {
                return {
                    results: data.results.map(function(item) {
                        return {
                            id: item.id,
                            text: item.name
                        };
                    })
                };
            },
            cache: true
        }


    });





});
