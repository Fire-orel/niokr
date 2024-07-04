$(document).ready(function() {
    $("#EventModal").on('hidden.bs.modal',function() {
        $('#addEventForm').attr('id','EventForm');
        $('#editEventForm').attr('id','EventForm');
        $('#error-message-event').hide().text('');
        $('#EventForm')[0].reset();
        $('#id_full_name_author_event').val(null).trigger('change');
    });


    $(document).on('click', '#deleteEvent', function(){

        var eventID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteEventBtn').data('id', eventID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteEventBtn').click(function() {


        var eventID = $(this).data('id');// Получаем ID публикации
        console.log(eventID)

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_event/${eventID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addevent', function(){

        $('#EventForm').attr('id','addEventForm');
        $('#addEventForm').attr('action',"/add_event/");

    });

    $(document).on('submit','#addEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#EventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-event').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editevent', function(){
        var eventID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_event/${eventID}/`,
            data: eventID ,


            success: function(response) {
                $('#EventForm').attr('id','editEventForm');
                $('#editEventForm').attr('action',`/edit_event/${eventID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;
                var full_name_author_events = formData.full_name_author_event.split(',');

                var filtered_full_name_author_event = full_name_author_events.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_author_event.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_full_name_author_event option").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_full_name_author_event').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var full_name_author_event_check = filtered_full_name_author_event.map(function(full_name_author) {
                    return full_name_author.trim();
                });

                $('#id_type_participation').val(formData.type_participation);
                $('#id_full_name_author_event').val(full_name_author_event_check).trigger('change');
                $('#id_name_event_event').val(formData.name_event_event);
                $('#id_level').val(formData.level);
                $('#id_type_event').val(formData.type_event);
                $('#id_title_report').val(formData.title_report);
                $('#id_date_event_event').val(formData.date_event_event);
                $('#id_place_event').val(formData.place_event);
                $('#id_number_participants').val(formData.number_participants);
                $('#id_number_foreign_participants').val(formData.number_foreign_participants);
                $('#id_number_exhibits').val(formData.number_exhibits);
                $('#id_publication_collection').val(formData.publication_collection);
                $('#id_awards').val(formData.awards);
                $('#id_link').val(formData.link);


                $('#EventModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editEventForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#EventModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-event').text("Ошибка").show();
            }
        });
    });

    $('#id_full_name_author_event').select2({
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
            url: '/full_name_authorList', // Убедитесь, что URL правильный
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
