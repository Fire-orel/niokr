$(document).ready(function() {
    $("#NIRSModal").on('hidden.bs.modal',function() {
        $('#addNIRSForm').attr('id','NIRSForm');
        $('#editNIRSForm').attr('id','NIRSForm');
        $('#error-message-nirs').hide().text('');
        $('#NIRSForm')[0].reset();
    });


    $(document).on('click', '#deleteNIRS', function(){

        var nirsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteNIRSBtn').data('id', nirsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteNIRSBtn').click(function() {


        var nirsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_nirs/${nirsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addnirs', function(){

        $('#NIRSForm').attr('id','addNIRSForm');
        $('#addNIRSForm').attr('action',"/add_nirs/");

    });

    $(document).on('submit','#addNIRSForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#NIRSModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-nirs').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editnirs', function(){
        var nirsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_nirs/${nirsID}/`,
            data: nirsID ,


            success: function(response) {
                $('#NIRSForm').attr('id','editNIRSForm');
                $('#editNIRSForm').attr('action',`/edit_nirs/${nirsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData)
                

                $('#id_number_students').val(formData.number_students);
                $('#id_full_name_students').val(formData.full_name_students);
                $('#id_form_participation').val(formData.form_participation);
                $('#id_name_event_nirs').val(formData.name_event_nirs);
                $('#id_full_name_scientific_supervisor').val(formData.full_name_scientific_supervisor);
                $('#id_awards_diplomas').val(formData.awards_diplomas);
                $('#id_date_event_nirs').val(formData.date_event_nirs);

                $('#NIRSModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editNIRSForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#NIRSModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-NIRS').text("Ошибка").show();
            }
        });
    });




});
