
$(document).ready(function() {
    $("#PopularSciencePublicationsModal").on('hidden.bs.modal',function() {
        $('#addPopularSciencePublicationsForm').attr('id','PopularSciencePublicationsForm');
        $('#editPopularSciencePublicationsForm').attr('id','PopularSciencePublicationsForm');
        $('#error-message-PopularSciencePublications').hide().text('');
        $('#EventForm')[0].reset();
        $('#id_full_name_author').val(null).trigger('change');
    });


    $(document).on('click', '#deletePopularSciencePublications', function(){

        var popularsciencepublicationsID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeletePopularSciencePublicationsBtn').data('id', popularsciencepublicationsID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeletePopularSciencePublicationsBtn').click(function() {


        var popularsciencepublicationsID = $(this).data('id');// Получаем ID публикации
        console.log(popularsciencepublicationsID)

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_popular_science_publications/${popularsciencepublicationsID}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addpopularsciencepublications', function(){

        $('#PopularSciencePublicationsForm').attr('id','addPopularSciencePublicationsForm');
        $('#addPopularSciencePublicationsForm').attr('action',"/add_popular_science_publications/");

    });

    $(document).on('submit','#addPopularSciencePublicationsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PopularSciencePublicationsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('error-message-popularsciencepublications').text("Ошибка").show();
            }
        });
    });
    $(document).on('click', '#editpopularsciencepublications', function(){
        var popularsciencepublicationsID = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_popular_science_publications/${popularsciencepublicationsID}/`,
            data: popularsciencepublicationsID ,


            success: function(response) {
                $('#PopularSciencePublicationsForm').attr('id','editPopularSciencePublicationsForm');
                $('#editPopularSciencePublicationsForm').attr('action',`/edit_popular_science_publications/${popularsciencepublicationsID}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                var full_name_authors=formData.full_name_author.split(',')

                var filtered_full_name_authors = full_name_authors.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_authors.forEach(function(full_name_author) {
                    // Создаем новую опцию, если её нет в списке
                    var optionExists = $("#id_full_name_author option").filter(function() {
                        return $(this).text() === full_name_author;
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author, full_name_author, true, true);
                        $('#id_full_name_author').append(newOption).trigger('change');
                    }
                });

                var full_name_author_check = full_name_authors.map(function(full_name_author) {

                    return full_name_author;
                });




                $('#id_full_name_author').val(full_name_author_check).trigger('change');
                $('#id_name_publication_popular_science_publications').val(formData.name_publication_popular_science_publications);
                $('#id_place_publication_popular_science_publications').val(formData.place_publication_popular_science_publications);
                $('#id_volume_popular_science_publications').val(formData.volume_popular_science_publications);
                $('#id_note').val(formData.note);


                $('#PopularSciencePublicationsModal').modal('show');


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });


    $(document).on('submit','#editPopularSciencePublicationsForm', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                if (response.message === 'Success') {
                    // Обрабатываем успешный ответ
                    $('#PopularSciencePublicationsModal').modal('hide').on('hidden.bs.modal', function() {
                        location.reload();
                    });
                };
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message-popularsciencepublications').text("Ошибка").show();
            }
        });
    });

    $('#id_full_name_author').select2({
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
