$(document).ready(function() {
    $("#TypeGrantModal").on('hidden.bs.modal',function() {
        $('#addTypeGrantForm').attr('id','TypeGrantForm');
        $('#editTypeGrantForm').attr('id','TypeGrantForm');
        $('#error-message-type-level').hide().text('');
        $('#TypeGrantForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeGrant', function(){

        var typegrantID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeGrantBtn').data('id', typegrantID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeGrantBtn').click(function() {


        var typegrantID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_grant/${typegrantID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypegrant', function(){

        $('#TypeGrantForm').attr('id','addTypeGrantForm');
        $('#addTypeGrantForm').attr('action',"/add_type_grant/");

    });

    $(document).on('submit','#addTypeGrantForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeGrantModal').modal('hide').on('hidden.bs.modal', function() {
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
    $(document).on('click', '#edittypegrant', function(){
        var typegrantID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_grant/${typegrantID}/`,
            data: typegrantID ,


            success: function(response) {
                $('#TypeGrantForm').attr('id','editTypeGrantForm');
                $('#editTypeGrantForm').attr('action',`/edit_type_grant/${typegrantID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                
                $('#id_name_type_grant').val(formData.name_type_grant);


                $('#TypeGrantModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeGrantForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeGrantModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-type-grant').text("Ошибка").show();
            }
        });
    });




});
