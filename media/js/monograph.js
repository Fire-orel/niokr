

$(document).ready(function() {

    $("#MonographModal").on('hidden.bs.modal',function() {
        $('#addMonographForm').attr('id','MonographForm');
        $('#editMonographForm').attr('id','MonographForm');
        $('#error-message-publication').hide().text('');
        $('#MonographForm')[0].reset();
    });

    $(document).on('submit','#addMonographForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PublicationModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-monograph').text("Ошибка").show();
            }
        });
    });

    $(document).on('click', '#deleteMonograph', function(){

        var MonographId = $(this).data('id'); // Получаем ID публикации
        $('#confirmDeleteMonographBtn').data('id', MonographId); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteMonographBtn').click(function() {

        var MonographId = $(this).data('id'); // Получаем ID публикации

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_monographs/${MonographId}/`, // Путь к представлению для удаления публикации
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

    //Добавления и редактирование таблицы Publication
    $(document).on('click', '#addmonographs', function(){

        $('#MonographForm').attr('id','addMonographForm');
        $('#addMonographForm').attr('action',"/add_monographs/");

    });


    $(document).on('click', '#editmonographs', function(){
        var monographsId = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_monographs/${monographsId}/`,
            data: monographsId ,


            success: function(response) {
                $('#MonographForm').attr('id','editMonographForm');
                $('#editMonographForm').attr('action',`/edit_monographs/${monographsId}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                $('#MonographModal').modal('show');
                $('#id_type_monographs').val(formData.type_monographs);
                $('#id_full_name_author_Monographs').val(formData. full_name_author_Monographs);
                $('#id_name_works').val(formData.name_works);
                $('#id_circulation').val(formData.circulation);
                $('#id_volume_monographs').val(formData.volume_monographs);
                $('#id_publishing_house').val(formData.publishing_house);
                $('#id_type_publishing_house').val(formData.type_publishing_house);
                $('#id_year_of_publication_monographs').val(formData.year_of_publication_monographs);


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });



    $(document).on('submit','#editMonographForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#MonographModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-monograph').text("Ошибка").show();
            }
        });
    });








});
