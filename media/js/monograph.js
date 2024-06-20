

$(document).ready(function() {
    $(document).on('submit','#addMonographForm', function(event) {

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
                $('#error-message-monograph').text("Ошибка").show();
            }
        });
    });

    $(document).on('click', '#deleteMonograph', function(){

        var publicationId = $(this).data('id'); // Получаем ID публикации
        $('#confirmDeleteMonographBtn').data('id', publicationId); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteMonographBtn').click(function() {


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

    //Добавления и редактирование таблицы Publication
    $(document).on('click', '#addmonographs', function(){

        $('#MonographForm').attr('id','addMonographForm');
        $('#addMonographForm').attr('action',"/add_monographs/");

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

                $('#PublicationModal').modal('show');
                $('#id_type_publication').val(formData.type_publication);
                $('#id_full_name_author_publications').val(formData.full_name_author_publications);
                $('#id_name_publication_publications').val(formData.name_publication_publications);
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
                $('#error-message-publication').text("Ошибка").show();
            }
        });
    });



    $("#MonographModal").on('hidden.bs.modal',function() {
        $('#addMonographModal').attr('id','MonographModal');
        $('#editMonographModal').attr('id','MonographModal');
        $('#error-message-publication').hide().text('');
        $('#MonographForm')[0].reset();
    });




});
