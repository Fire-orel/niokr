$(document).ready(function() {
    $("#EventModal").on('hidden.bs.modal',function() {
        $('#addEventForm').attr('id','EventForm');
        $('#editEventForm').attr('id','EventForm');
        $('#error-message-event').hide().text('');
        $('#EventForm')[0].reset();
    });


    $(document).on('click', '#deleteEvent', function(){

        var eventID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteEventBtn').data('id', eventID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteEventBtn').click(function() {


        var eventID = $(this).data('id');// Получаем ID публикации
        console.log(eventID)

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_event/${eventID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addevent', function(){

        $('#EventForm').attr('id','addEventForm');
        $('#addEventForm').attr('action',"/add_event/");

    });

    $(document).on('submit','#addEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#EventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-event').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editevent', function(){
        var eventID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_event/${eventID}/`,
            data: eventID ,


            success: function(response) {
                $('#EventForm').attr('id','editEventForm');
                $('#editEventForm').attr('action',`/edit_event/${eventID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData)

                $('#id_type_participation').val(formData.type_participation);
                $('#id_full_name_author_event').val(formData.full_name_author_event);
                $('#id_name_event_event').val(formData.name_event_event);
                $('#id_level').val(formData.level);
                $('#id_type_event').val(formData.type_event);
                $('#id_title_report').val(formData.title_report);
                $('#id_date_event_event').val(formData.date_event_event);
                $('#id_place_event').val(formData.place_event);
                $('#id_number_participants').val(formData.number_participants);
                $('#id_number_foreign_participants').val(formData.number_foreign_participants);
                $('#id_number_exhibits').val(formData.number_exhibits);
                $('#id_publication_collection').val(formData.publication_collection);
                $('#id_awards').val(formData.awards);
                $('#id_link').val(formData.link);


                $('#EventModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#EventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-event').text("Ошибка").show();
            }
        });
    });




});
