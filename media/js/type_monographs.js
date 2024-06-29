$(document).ready(function() {
    $("#TypeMonographsModal").on('hidden.bs.modal',function() {
        $('#addTypeMonographsForm').attr('id','TypeMonographsForm');
        $('#editTypeMonographsForm').attr('id','TypeMonographsForm');
        $('#error-message-type-monographs').hide().text('');
        $('#TypeMonographsForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeMonographs', function(){

        var typemonographsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeMonographsBtn').data('id', typemonographsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeMonographsBtn').click(function() {


        var typemonographsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_monographs/${typemonographsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypemonographs', function(){

        $('#TypeMonographsForm').attr('id','addTypeMonographsForm');
        $('#addTypeMonographsForm').attr('action',"/add_type_monographs/");

    });

    $(document).on('submit','#addTypeMonographsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeMonographsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-monographs').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypemonographs', function(){
        var typemonographsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_monographs/${typemonographsID}/`,
            data: typemonographsID ,


            success: function(response) {
                $('#TypeMonographsForm').attr('id','editTypeMonographsForm');
                $('#editTypeMonographsForm').attr('action',`/edit_type_monographs/${typemonographsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_monographs').val(formData.name_type_monographs);


                $('#TypeMonographsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeMonographsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeMonographsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-type-property').text("Ошибка").show();
            }
        });
    });




});
