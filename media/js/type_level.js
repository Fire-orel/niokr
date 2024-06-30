$(document).ready(function() {
    $("#TypeLevelModal").on('hidden.bs.modal',function() {
        $('#addTypeLevelForm').attr('id','TypeLevelForm');
        $('#editTypeLevelForm').attr('id','TypeLevelForm');
        $('#error-message-type-level').hide().text('');
        $('#TypeLevelForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeLevel', function(){

        var typelevelID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeLevelBtn').data('id', typelevelID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeLevelBtn').click(function() {


        var typelevelID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_level/${typelevelID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypelevel', function(){

        $('#TypeLevelForm').attr('id','addTypeLevelForm');
        $('#addTypeLevelForm').attr('action',"/add_type_level/");

    });

    $(document).on('submit','#addTypeLevelForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeLevelModal').modal('hide').on('hidden.bs.modal', function() {
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
    $(document).on('click', '#edittypelevel', function(){
        var typelevelID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_level/${typelevelID}/`,
            data: typelevelID ,


            success: function(response) {
                $('#TypeLevelForm').attr('id','editTypeLevelForm');
                $('#editTypeLevelForm').attr('action',`/edit_type_level/${typelevelID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_level').val(formData.name_type_level);


                $('#TypeLevelModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeLevelForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeLevelModal').modal('hide').on('hidden.bs.modal', function() {
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
