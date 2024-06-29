$(document).ready(function() {
    $("#TypePropertyModal").on('hidden.bs.modal',function() {
        $('#addTypePropertyForm').attr('id','TypePropertyForm');
        $('#editTypePropertyForm').attr('id','TypePropertyForm');
        $('#error-message-type-publications').hide().text('');
        $('#TypePropertyForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeProperty', function(){

        var typepropertyID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypePropertyBtn').data('id', typepropertyID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypePropertyBtn').click(function() {


        var typepropertyID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_property/${typepropertyID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypeproperty', function(){

        $('#TypePropertyForm').attr('id','addTypePropertyForm');
        $('#addTypePropertyForm').attr('action',"/add_type_property/");

    });

    $(document).on('submit','#addTypePropertyForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypePropertyModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-property').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypeproperty', function(){
        var typepropertyID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_property/${typepropertyID}/`,
            data: typepropertyID ,


            success: function(response) {
                $('#TypePropertyForm').attr('id','editTypePropertyForm');
                $('#editTypePropertyForm').attr('action',`/edit_type_property/${typepropertyID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_property').val(formData.name_type_property);


                $('#TypePropertyModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypePropertyForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypePropertyModal').modal('hide').on('hidden.bs.modal', function() {
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
