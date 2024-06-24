$(document).ready(function() {
    $("#InternationalCooperationModal").on('hidden.bs.modal',function() {
        $('#addInternationalCooperationForm').attr('id','InternationalCooperationForm');
        $('#editInternationalCooperationForm').attr('id','InternationalCooperationForm');
        $('#error-message-international-cooperation').hide().text('');
        $('#InternationalCooperationForm')[0].reset();
    });


    $(document).on('click', '#deleteInternationalCooperation', function(){

        var internationalcooperationID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteInternationalCooperationBtn').data('id', internationalcooperationID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteInternationalCooperationBtn').click(function() {


        var internationalcooperationID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_international_cooperation/${internationalcooperationID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addinternationalcooperation', function(){

        $('#InternationalCooperationForm').attr('id','addInternationalCooperationForm');
        $('#addInternationalCooperationForm').attr('action',"/add_international_cooperation/");

    });

    $(document).on('submit','#addInternationalCooperationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#InternationalCooperationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-international-cooperation').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editinternationalcooperation', function(){
        var internationalcooperationID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_international_cooperation/${internationalcooperationID}/`,
            data: internationalcooperationID ,


            success: function(response) {
                $('#InternationalCooperationForm').attr('id','editInternationalCooperationForm');
                $('#editInternationalCooperationForm').attr('action',`/edit_international_cooperation/${internationalcooperationID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData)


                $('#id_name_scientific_research').val(formData.name_scientific_research);
                $('#id_name_scientific_centers').val(formData.name_scientific_centers);
                $('#id_name_topics').val(formData.name_topics);
                $('#id_name_research_topics').val(formData.name_research_topics);
                $('#id_name_scientific_programs').val(formData.name_scientific_programs);


                $('#InternationalCooperationModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editInternationalCooperationForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#InternationalCooperationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-international-cooperation').text("Ошибка").show();
            }
        });
    });




});
