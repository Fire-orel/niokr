$(document).ready(function() {
    $("#ScientificDirectionsModal").on('hidden.bs.modal',function() {
        $('#addScientificDirectionsForm').attr('id','ScientificDirectionsForm');
        $('#editScientificDirectionsForm').attr('id','ScientificDirectionsForm');
        $('#error-message-scientific_directions').hide().text('');
        $('#ScientificDirectionsForm')[0].reset();
        $('#id_leading_scientists').val(null).trigger('change');
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


                var leading_scientistss = formData.leading_scientists.split(',');

                var filtered_leading_scientists = leading_scientistss.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_leading_scientists.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_leading_scientists").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_leading_scientists').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var leading_scientists_check = filtered_leading_scientists.map(function(full_name_author) {
                    return full_name_author.trim();
                });

                $('#id_name_scientific_direction').val(formData.name_scientific_direction);
                $('#id_name_scientific_school').val(formData.name_scientific_school);
                $('#id_leading_scientists').val(leading_scientists_check).trigger('change');
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


    $('#id_leading_scientists').select2({
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
        },
        minimumInputLength: 2,
        ajax: {
            url: '/path/to/select2-data/', // Убедитесь, что URL правильный
            dataType: 'json',

            data: function(params) {
                return {
                    q: params.term // Передача введенного текста на сервер
                };
            },
            processResults: function(data) {
                return {
                    results: data.results.map(function(item) {
                        return {
                            id: item.id,
                            text: item.name
                        };
                    })
                };
            },
            cache: true
        }

    });






});
