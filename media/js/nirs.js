$(document).ready(function() {
    $("#NIRSModal").on('hidden.bs.modal',function() {
        $('#addNIRSForm').attr('id','NIRSForm');
        $('#editNIRSForm').attr('id','NIRSForm');
        $('#error-message-nirs').hide().text('');
        $('#NIRSForm')[0].reset();
        $('#id_full_name_students').val(null).trigger('change');
        $('#id_full_name_scientific_supervisor').val(null).trigger('change');
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

                var full_name_studentss = formData.full_name_students.split(',');

                var filtered_full_name_students = full_name_studentss.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_students.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_full_name_students").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_full_name_students').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var full_name_students_check = filtered_full_name_students.map(function(full_name_author) {
                    return full_name_author.trim();
                });



                var full_name_scientific_supervisors = formData.full_name_scientific_supervisor.split(',');

                var filtered_full_name_scientific_supervisors = full_name_scientific_supervisors.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_scientific_supervisors.forEach(function(full_name_author) {
                    // Проверяем, есть ли уже такая опция в select2
                    var optionExists = $("#id_full_name_scientific_supervisor").filter(function() {
                        return $(this).text().trim() === full_name_author.trim();
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author.trim(), full_name_author.trim(), true, true);
                        $('#id_full_name_scientific_supervisor').append(newOption).trigger('change');
                    }
                });

                // Собираем список выбранных значений для проверки, если это необходимо
                var full_name_scientific_supervisor_check = filtered_full_name_scientific_supervisors.map(function(full_name_author) {
                    return full_name_author.trim();
                });


                $('#id_number_students').val(formData.number_students);
                $('#id_full_name_students').val(full_name_students_check).trigger('change');
                $('#id_form_participation').val(formData.form_participation);
                $('#id_name_event_nirs').val(formData.name_event_nirs);
                $('#id_full_name_scientific_supervisor').val(full_name_scientific_supervisor_check).trigger('change');
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

    $('#id_full_name_students').select2({
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

    $('#id_full_name_scientific_supervisor').select2({
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
