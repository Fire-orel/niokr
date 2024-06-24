$(document).ready(function() {
    $("#GrantModal").on('hidden.bs.modal',function() {
        $('#addGrantForm').attr('id','GrantForm');
        $('#editGrantForm').attr('id','GrantForm');
        $('#error-message-grant').hide().text('');
        $('#GrantForm')[0].reset();
    });


    $(document).on('click', '#deleteGrant', function(){

        var grantID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteGrantBtn').data('id', grantID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteGrantBtn').click(function() {


        var grantID = $(this).data('id');// Получаем ID публикации


        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_grant/${grantID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addgrant', function(){

        $('#GrantForm').attr('id','addGrantForm');
        $('#addGrantForm').attr('action',"/add_grant/");

    });

    $(document).on('submit','#addGrantForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#GrantModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-grant').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editgrant', function(){
        var grantID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_grant/${grantID}/`,
            data: grantID ,


            success: function(response) {
                $('#GrantForm').attr('id','editGrantForm');
                $('#editGrantForm').attr('action',`/edit_grant/${grantID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                console.log(formData)

                $('#id_type_grant').val(formData.type_grant);
                $('#id_name_fund').val(formData.name_fund);
                $('#id_name_competition').val(formData.name_competition);
                $('#id_kod_competition').val(formData.kod_competition);
                $('#id_nomination').val(formData.nomination);
                $('#id_name_project_topic').val(formData.name_project_topic);
                $('#id_project_manager').val(formData.project_manager);
                $('#id_number_project_team').val(formData.number_project_team);
                $('#id_number_young_scientists').val(formData.number_young_scientists);
                $('#id_full_name_performer').val(formData.full_name_performer);
                $('#id_winner').val(formData.winner);

                $('#GrantModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editGrantForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#GrantModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-Grant').text("Ошибка").show();
            }
        });
    });




});
