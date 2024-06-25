$(document).ready(function() {
    $("#GrantModal").on('hidden.bs.modal',function() {
        $('#addGrantForm').attr('id','GrantForm');
        $('#editGrantForm').attr('id','GrantForm');
        $('#error-message-grant').hide().text('');
        $('#GrantForm')[0].reset();
        $('#id_project_manager').val(null).trigger('change');
        $('#id_full_name_performer').val(null).trigger('change');
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

                var project_managers = formData.project_manager.split(',');

                var filtered_project_manager = project_managers.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_project_manager.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_project_manager").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_project_manager').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var project_manager_check = filtered_project_manager.map(function(full_name_author) {
                    return full_name_author.trim();
                });



                var full_name_performers = formData.full_name_performer.split(',');

                var filtered_full_name_performer = full_name_performers.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_performer.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_full_name_performer").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_full_name_performer').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var full_name_performer_check = filtered_full_name_performer.map(function(full_name_author) {
                    return full_name_author.trim();
                });


                $('#id_type_grant').val(formData.type_grant);
                $('#id_name_fund').val(formData.name_fund);
                $('#id_name_competition').val(formData.name_competition);
                $('#id_kod_competition').val(formData.kod_competition);
                $('#id_nomination').val(formData.nomination);
                $('#id_name_project_topic').val(formData.name_project_topic);
                $('#id_project_manager').val(project_manager_check).trigger('change');
                $('#id_number_project_team').val(formData.number_project_team);
                $('#id_number_young_scientists').val(formData.number_young_scientists);
                $('#id_full_name_performer').val(full_name_performer_check).trigger('change');
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

    $('#id_project_manager').select2({
        multiple: true,
        tags: true,
        tokenSeparators: [','],  // Разделители для тегов
        placeholder: 'Выберите или введите авторов',
        createTag: function (params) {
            var term = $.trim(params.term);
            if (term === '') {
                return null;
            }
            return {
                id: term,
                text: term,
                newTag: true // add additional parameters
            };
        }

    });

    $('#id_full_name_performer').select2({
        multiple: true,
        tags: true,
        tokenSeparators: [','],  // Разделители для тегов
        placeholder: 'Выберите или введите авторов',
        createTag: function (params) {
            var term = $.trim(params.term);
            if (term === '') {
                return null;
            }
            return {
                id: term,
                text: term,
                newTag: true // add additional parameters
            };
        }

    });



});
