$(document).ready(function() {
    $("#FormParticipationModal").on('hidden.bs.modal',function() {
        $('#addFormParticipationForm').attr('id','FormParticipationForm');
        $('#editFormParticipationForm').attr('id','FormParticipationForm');
        $('#error-message-type-level').hide().text('');
        $('#FormParticipationForm')[0].reset();

    });


    $(document).on('click', '#deleteFormParticipation', function(){

        var formparticipationID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteFormParticipationBtn').data('id', formparticipationID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteFormParticipationBtn').click(function() {


        var formparticipationID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_form_participation/${formparticipationID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addformparticipation', function(){

        $('#FormParticipationForm').attr('id','addFormParticipationForm');
        $('#addFormParticipationForm').attr('action',"/add_form_participation/");

    });

    $(document).on('submit','#addFormParticipationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#FormParticipationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-form-participation').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editformparticipation', function(){
        var formparticipationID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_form_participation/${formparticipationID}/`,
            data: formparticipationID ,


            success: function(response) {
                $('#FormParticipationForm').attr('id','editFormParticipationForm');
                $('#editFormParticipationForm').attr('action',`/edit_form_participation/${formparticipationID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_form_participation').val(formData.name_form_participation);


                $('#FormParticipationModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editFormParticipationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#FormParticipationModal').modal('hide').on('hidden.bs.modal', function() {
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
