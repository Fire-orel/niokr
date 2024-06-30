$(document).ready(function() {
    $("#TypeParticipationModal").on('hidden.bs.modal',function() {
        $('#addTypeParticipationForm').attr('id','TypeParticipationForm');
        $('#editTypeParticipationForm').attr('id','TypeParticipationForm');
        $('#error-message-type-publications').hide().text('');
        $('#TypeParticipationForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeParticipation', function(){

        var typeparticipationID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeParticipationBtn').data('id', typeparticipationID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeParticipationBtn').click(function() {


        var typeparticipationID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_participation/${typeparticipationID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypeparticipation', function(){

        $('#TypeParticipationForm').attr('id','addTypeParticipationForm');
        $('#addTypeParticipationForm').attr('action',"/add_type_participation/");

    });

    $(document).on('submit','#addTypeParticipationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeParticipationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-participation').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypeparticipation', function(){
        var typeparticipationID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_participation/${typeparticipationID}/`,
            data: typeparticipationID ,


            success: function(response) {
                $('#TypeParticipationForm').attr('id','editTypeParticipationForm');
                $('#editTypeParticipationForm').attr('action',`/edit_type_participation/${typeparticipationID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_participation').val(formData.name_type_participation);


                $('#TypeParticipationModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeParticipationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeParticipationModal').modal('hide').on('hidden.bs.modal', function() {
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
