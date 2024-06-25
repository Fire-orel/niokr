

$(document).ready(function() {

    $("#MonographModal").on('hidden.bs.modal',function() {
        $('#addMonographForm').attr('id','MonographForm');
        $('#editMonographForm').attr('id','MonographForm');
        $('#error-message-monograph').hide().text('');
        $('#MonographForm')[0].reset();
        $('#id_full_name_author_monographs').val(null).trigger('change');
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

                var full_name_author_monographss=formData.full_name_author_monographs.split(',')

                var filtered_full_name_author_monographs = full_name_author_monographss.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_author_monographs.forEach(function(full_name_author) {
                    // Создаем новую опцию, если её нет в списке
                    var optionExists = $("#id_full_name_author_monographs").filter(function() {
                        return $(this).text() === full_name_author;
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author, full_name_author, true, true);
                        $('#id_full_name_author').append(newOption).trigger('change');
                    }
                });

                var full_name_author_monographs_check = filtered_full_name_author_monographs.map(function(full_name_author) {

                    return full_name_author;
                });

                $('#MonographModal').modal('show');
                $('#id_type_monographs').val(formData.type_monographs);
                $('#id_full_name_author_monographs').val(full_name_author_monographs_check).trigger('change');
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

    $('#id_full_name_author_monographs').select2({
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
