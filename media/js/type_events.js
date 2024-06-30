$(document).ready(function() {
    $("#TypeEventModal").on('hidden.bs.modal',function() {
        $('#addTypeEventForm').attr('id','TypeEventForm');
        $('#editTypeEventForm').attr('id','TypeEventForm');
        $('#error-message-type-events').hide().text('');
        $('#TypeEventForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeEvent', function(){

        var typeeventsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeEventBtn').data('id', typeeventsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeEventBtn').click(function() {


        var typeeventsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_events/${typeeventsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypeevent', function(){

        $('#TypeEventForm').attr('id','addTypeEventForm');
        $('#addTypeEventForm').attr('action',"/add_type_events/");

    });

    $(document).on('submit','#addTypeEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeEventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-events').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypeevent', function(){
        var typeeventsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_events/${typeeventsID}/`,
            data: typeeventsID ,


            success: function(response) {
                $('#TypeEventForm').attr('id','editTypeEventForm');
                $('#editTypeEventForm').attr('action',`/edit_type_events/${typeeventsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_events').val(formData.name_type_events);


                $('#TypeEventModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeEventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-type-participation').text("Ошибка").show();
            }
        });
    });




});
