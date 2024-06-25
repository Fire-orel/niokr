

$(document).ready(function() {
    $(document).on('click', '#deletePublication', function(){

        var publicationId = $(this).data('id'); // Получаем ID публикации
        $('#confirmDeletePublicationBtn').data('id', publicationId); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeletePublicationBtn').click(function() {


        var publicationId = $(this).data('id'); // Получаем ID публикации

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_publication/${publicationId}/`, // Путь к представлению для удаления публикации
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
    $(document).on('click', '#addpublication', function(){

        $('#PublicationForm').attr('id','addPublicationForm');
        $('#addPublicationForm').attr('action',"/add_publication/");

    });

    $(document).on('submit','#addPublicationForm', function(event) {

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
                $('#error-message-publication').text("Ошибка").show();
            }
        });
    });

    $(document).on('click', '#editpublication', function(){
        var publicationId = $(this).data('id');
        $.ajax({
            type: 'GET',
            url: `/edit_publication/${publicationId}/`,
            data: publicationId ,


            success: function(response) {
                $('#PublicationForm').attr('id','editPublicationForm');
                $('#editPublicationForm').attr('action',`/edit_publication/${publicationId}/`);
                // Если успешный ответ от сервера, открываем модальное окно
                var formData = JSON.parse(response.form_data)[0].fields;

                var full_name_author_publicationss=formData.full_name_author_publications.split(',')

                var filtered_full_name_author_publications= full_name_author_publicationss.filter(function(author) {
                    return author.trim() !== ''; // Фильтруем пустые строки
                });

                filtered_full_name_author_publications.forEach(function(full_name_author) {
                    // Создаем новую опцию, если её нет в списке
                    var optionExists = $("#id_full_name_author_publications option").filter(function() {
                        return $(this).text() === full_name_author;
                    }).length > 0;

                    if (!optionExists) {
                        var newOption = new Option(full_name_author, full_name_author, true, true);
                        $('#id_full_name_author_publications').append(newOption).trigger('change');
                    }
                });

                var full_name_author_publications_check = full_name_author_publicationss.map(function(full_name_author) {
                    return full_name_author;
                });





                $('#PublicationModal').modal('show');
                $('#id_type_publication').val(formData.type_publication);
                $('#id_full_name_author_publications').val(full_name_author_publications_check).trigger('change');
                $('#id_name_publication_publications').val(formData.name_publication_publications);
                $('#id_exit_data').val(formData.exit_data);
                $('#id_year').val(formData.year);
                $('#id_place_publication_publications').val(formData.place_publication_publications);
                $('#id_volume_publication').val(formData.volume_publication);
                $('#id_eLIBRARY_ID').val(formData.eLIBRARY_ID);
                $('#id_doi_publication').val(formData.doi_publication);


            },
            // error: function(xhr, status, error) {
            //     // Обработка ошибок AJAX-запроса
            //     console.error('Произошла ошибка:', error);
            //     alert('Произошла ошибка при выполнении запроса.');
            // }
        });
    });



    $(document).on('submit','#editPublicationForm', function(event) {

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
                $('#error-message-publication').text("Ошибка").show();
            }
        });
    });



    $("#PublicationModal").on('hidden.bs.modal',function() {
        $('#addPublicationForm').attr('id','PublicationForm');
        $('#editPublicationForm').attr('id','PublicationForm');
        $('#error-message-publication').hide().text('');
        $('#PublicationForm')[0].reset();
        $('#id_full_name_author_publications').val(null).trigger('change');
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
        }

    });
    $('#id_full_name_author_publications').select2({
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
