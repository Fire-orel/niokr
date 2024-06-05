function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(document).ready(function() {

    $('#addPublicationForm').on('submit', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                // Обрабатываем успешный ответ
                $('#addPublicationModal').modal('hide').on('hidden.bs.modal', function() {
                    // Здесь можно выполнить обновление данных на странице
                    location.reload(); // Пример: перезагрузить страницу
                });
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message').text("Запись с такими данными уже существует").show();
            }
        });
    });
});


$(document).ready(function() {
    // Обработчик клика по кнопке удаления
    $('.open-delete-modal').click(function() {
        var publicationId = $(this).data('id'); // Получаем ID публикации
        $('#confirmDeleteBtn').data('id', publicationId); // Устанавливаем ID в кнопку подтверждения удаления
    });

    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteBtn').click(function() {
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
});


$(document).ready(function() {
    $('#quarter').select2();
    $('#faculty').select2();
    $('#department').select2();
    $('#quarter').select2();
    $('#table').select2();
    $('#table_type').select2();


    $('#table').on('change', function() {
        // Получаем выбранное значение
        var selectedValue = $(this).val();
        // Если выбрано значение 1, показываем второй select, иначе скрываем

        if($('#table').val()== 'publication') {
            console.log("test")

            $('#table_type_div').show();
        } else {
            $('#table_type_div').hide();
        }
    });
});



$(document).ready(function() {

    $('#addMapForm').on('submit', function(event) {

        event.preventDefault(); // Предотвращаем отправку формы
        $.ajax({
            url: $(this).attr('action'), // URL для отправки запроса
            type: 'POST',
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken},
            success: function(response) {
                // Обрабатываем успешный ответ
                $('#addMapModal').modal('hide').on('hidden.bs.modal', function() {
                    // Здесь можно выполнить обновление данных на странице
                    location.reload(); // Пример: перезагрузить страницу
                });
            },
            error: function(xhr) {
                // Обрабатываем ошибочный ответ
                $('#error-message').text("Запись с такими данными уже существует").show();
            }
        });
    });
});



