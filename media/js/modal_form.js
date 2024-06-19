function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


$(document).ready(function() {

    $('button[data-toggle="tab"]').on('shown.bs.tab', function (e) {

        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    // Восстановление активной вкладки из локального хранилища
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab button[href="' + activeTab + '"]').tab('show');
    } else {
        $('#myTab button[data-toggle="tab"]:first').tab('show'); // Установка первой вкладки активной по умолчанию
    }





    // Обработчик клика по кнопке удаления


    $('#addMapForm').on('submit', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                // Обрабатываем успешный ответ
                $('#addMapModal').modal('hide').on('hidden.bs.modal', function() {
                    // Здесь можно выполнить обновление данных на странице
                    location.reload(); // Пример: перезагрузить страницу
                });
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message').text("Запись с такими данными уже существует").show();
            }
        });
    });



    $('#quarter').select2();
    $('#faculty').select2();
    $('#department').select2();
    $('#quarter').select2();
    $('#table').select2();
    $('#table_type').select2();


    $('#table').on('change', function() {
        // Получаем выбранное значение
        var selectedValue = $(this).val();
        // Если выбрано значение 1, показываем второй select, иначе скрываем

        if($('#table').val()== 'publication') {
            $('#table_type_div').show();
        } else {
            $('#table_type_div').hide();
        }
    });



    //Добавления и редактирование таблицы Publication
    $(document).on('click', '#addpublication', function(){

        $('#PublicationForm').attr('id','addPublicationForm');
        $('#addPublicationForm').attr('action',"/add_publication/");

    });

    $(document).on('submit','#addPublicationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PublicationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-publication').text("Ошибка").show();
            }
        });
    });

    $(document).on('click', '#editpublication', function(){
        var publicationId = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_publication/${publicationId}/`,
            data: publicationId ,


            success: function(response) {
                $('#PublicationForm').attr('id','editPublicationForm');
                $('#editPublicationForm').attr('action',`/edit_publication/${publicationId}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData.full_name_author)
                $('#PublicationModal').modal('show');
                $('#id_type_publication').val(formData.type_publication);
                $('#id_full_name_author').val(formData.full_name_author);
                $('#id_name_publication').val(formData.name_publication);
                $('#id_exit_data').val(formData.exit_data);
                $('#id_year').val(formData.year);
                $('#id_place_publication').val(formData.place_publication);
                $('#id_volume_publication').val(formData.volume_publication);
                $('#id_eLIBRARY_ID').val(formData.eLIBRARY_ID);
                $('#id_doi_publication').val(formData.doi_publication);


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });



    $(document).on('submit','#editPublicationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PublicationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message').text("Ошибка").show();
            }
        });
    });



    $("#PublicationModal").on('hidden.bs.modal',function() {
        $('#addPublicationForm').attr('id','PublicationForm');
        $('#editPublicationForm').attr('id','PublicationForm');
        $('#error-message').hide().text('');
        $('#PublicationForm')[0].reset();
    });

    $(document).on('click', '#deletePublication', function(){

        var publicationId = $(this).data('id'); // Получаем ID публикации
        $('#confirmDeletePublicationBtn').data('id', publicationId); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeletePublicationBtn').click(function() {


        var publicationId = $(this).data('id'); // Получаем ID публикации

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_publication/${publicationId}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#SecurityDocumentsModal', function(){

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

    $(document).on('click', '#', function(){
        var publicationId = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_publication/${publicationId}/`,
            data: publicationId ,


            success: function(response) {
                $('#PublicationForm').attr('id','editPublicationForm');
                $('#editPublicationForm').attr('action',`/edit_publication/${publicationId}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData.full_name_author)
                $('#PublicationModal').modal('show');
                $('#id_type_publication').val(formData.type_publication);
                $('#id_full_name_author').val(formData.full_name_author);
                $('#id_name_publication').val(formData.name_publication);
                $('#id_exit_data').val(formData.exit_data);
                $('#id_year').val(formData.year);
                $('#id_place_publication').val(formData.place_publication);
                $('#id_volume_publication').val(formData.volume_publication);
                $('#id_eLIBRARY_ID').val(formData.eLIBRARY_ID);
                $('#id_doi_publication').val(formData.doi_publication);


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });

    $(document).on('submit','#', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PublicationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message').text("Запись с такими данными уже существует").show();
            }
        });
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



    $("#").on('hidden.bs.modal',function() {
        $('#addPublicationForm').attr('id','PublicationForm');
        $('#editPublicationForm').attr('id','PublicationForm');
        $('#error-message').hide().text('');
        $('#PublicationForm')[0].reset();
    });

});
