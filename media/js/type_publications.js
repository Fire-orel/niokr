$(document).ready(function() {
    $("#TypePublicationsModal").on('hidden.bs.modal',function() {
        $('#addTypePublicationsForm').attr('id','TypePublicationsForm');
        $('#editTypePublicationsForm').attr('id','TypePublicationsForm');
        $('#error-message-type-publications').hide().text('');
        $('#TypePublicationsForm')[0].reset();

    });


    $(document).on('click', '#deleteTypePublications', function(){

        var typepublicationsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypePublicationsBtn').data('id', typepublicationsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypePublicationsBtn').click(function() {


        var typepublicationsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_publications/${typepublicationsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypepublications', function(){

        $('#TypePublicationsForm').attr('id','addTypePublicationsForm');
        $('#addTypePublicationsForm').attr('action',"/add_type_publications/");

    });

    $(document).on('submit','#addTypePublicationsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypePublicationsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-publications').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypepublications', function(){
        var typepublicationsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_publications/${typepublicationsID}/`,
            data: typepublicationsID ,


            success: function(response) {
                $('#TypePublicationsForm').attr('id','editTypePublicationsForm');
                $('#editTypePublicationsForm').attr('action',`/edit_type_publications/${typepublicationsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_publications').val(formData.name_type_publications);


                $('#TypePublicationsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypePublicationsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypePublicationsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-type-publications').text("Ошибка").show();
            }
        });
    });




});
