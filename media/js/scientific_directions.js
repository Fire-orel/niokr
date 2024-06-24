$(document).ready(function() {
    $("#ScientificDirectionsModal").on('hidden.bs.modal',function() {
        $('#addScientificDirectionsForm').attr('id','ScientificDirectionsForm');
        $('#editScientificDirectionsForm').attr('id','ScientificDirectionsForm');
        $('#error-message-scientific_directions').hide().text('');
        $('#ScientificDirectionsForm')[0].reset();
    });


    $(document).on('click', '#deleteScientificDirections', function(){

        var scientificdirectionsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteScientificDirectionsBtn').data('id', scientificdirectionsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteScientificDirectionsBtn').click(function() {


        var scientificdirectionsID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_scientific_directions/${scientificdirectionsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addscientificdirections', function(){

        $('#ScientificDirectionsForm').attr('id','addScientificDirectionsForm');
        $('#addScientificDirectionsForm').attr('action',"/add_scientific_directions/");

    });

    $(document).on('submit','#addScientificDirectionsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#ScientificDirectionsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-scientific-directions').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editscientificdirections', function(){
        var scientificdirectionsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_scientific_directions/${scientificdirectionsID}/`,
            data: scientificdirectionsID ,


            success: function(response) {
                $('#ScientificDirectionsForm').attr('id','editScientificDirectionsForm');
                $('#editScientificDirectionsForm').attr('action',`/edit_scientific_directions/${scientificdirectionsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData)

                $('#id_name_scientific_direction').val(formData.name_scientific_direction);
                $('#id_name_scientific_school').val(formData.name_scientific_school);
                $('#id_leading_scientists').val(formData.leading_scientists);
                $('#id_number_defended_doctoral_dissertations').val(formData.number_defended_doctoral_dissertations);
                $('#id_number_defended_PhD_theses').val(formData.number_defended_PhD_theses);
                $('#id_number_monographs').val(formData.number_monographs);
                $('#id_number_articles_WoS_Scopus').val(formData.number_articles_WoS_Scopus);
                $('#id_number_articles_VAK').val(formData.number_articles_VAK);
                $('#id_number_articles_RIHC').val(formData.number_articles_RIHC);
                $('#id_number_applications_inventions').val(formData.number_applications_inventions);
                $('#id_number_security_documents_received').val(formData.number_security_documents_received);
                $('#id_number_organized').val(formData.number_organized);
                $('#id_amount_funding').val(formData.amount_funding);



                $('#ScientificDirectionsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editScientificDirectionsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#ScientificDirectionsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-scientific-directions').text("Ошибка").show();
            }
        });
    });




});
