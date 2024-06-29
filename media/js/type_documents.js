$(document).ready(function() {
    $("TypeDocumentsModal").on('hidden.bs.modal',function() {
        $('#addTypeDocumentsForm').attr('id','TypeDocumentsForm');
        $('#editTypeDocumentsForm').attr('id','TypeDocumentsForm');
        $('#error-message-type-documents').hide().text('');
        $('#TypeDocumentsForm')[0].reset();

    });


    $(document).on('click', '#deleteTypeDocuments', function(){

        var typedocumentsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteTypeDocumentsBtn').data('id', typedocumentsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteTypeDocumentsBtn').click(function() {


        var typedocumentsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_type_documents/${typedocumentsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addtypedocuments', function(){

        $('#TypeDocumentsForm').attr('id','addTypeDocumentsForm');
        $('#addTypeDocumentsForm').attr('action',"/add_type_documents/");

    });

    $(document).on('submit','#addTypeDocumentsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeDocumentsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-type-documents').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#edittypedocuments', function(){
        var typedocumentsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_type_documents/${typedocumentsID}/`,
            data: typedocumentsID ,


            success: function(response) {
                $('#TypeDocumentsForm').attr('id','editTypeDocumentsForm');
                $('#editTypeDocumentsForm').attr('action',`/edit_type_documents/${typedocumentsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#id_name_type_documents').val(formData.name_type_documents);


                $('#TypeDocumentsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editTypeDocumentsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#TypeDocumentsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-type-documents').text("Ошибка").show();
            }
        });
    });




});
