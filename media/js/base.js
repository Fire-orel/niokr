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

    if (window.location.pathname === '/home/') {
        localStorage.removeItem('activeTab');
    }
    $(document).on('submit','#addMapForm', function(event) {

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
            error: function(response) {
                if (response.responseJSON.message === 'Invalid request method'){
                    $('#error-message').text("Ошибка проверьте введённые данные").show();
                }
                else{
                    $('#error-message').text("Запись с такими данными уже существует").show();
                }


            }
        });
    });

    $('button[data-toggle="tab"]').on('shown.bs.tab', function (e) {

        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    // Восстановление активной вкладки из локального хранилища
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab button[href="' + activeTab + '"]').tab('show');
    } else {
        $('#myTab button[data-toggle="tab"]:first').tab('show'); // Установка первой вкладки активной по умолчанию
    }



    $(document).on('click', '#deleteMap', function(){

        var mapID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteMapBtn').data('id', mapID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteMapBtn').click(function() {


        var mapID = $(this).data('id');// Получаем ID публикации
        console.log(eventID)

        // Отправляем запрос на удаление публикации
        $.ajax({
            url: `/delete_map/${mapID}/`, // Путь к представлению для удаления публикации
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






    $('#quarter').select2();
    $('#faculty').select2();
    $('#id_department').select2({
        allowClear: true,
        minimumResultsForSearch: Infinity
    });
    $('#department').select2();
    $('#quarter').select2();
    $('#table').select2();
    $('#table_type').select2();
    $('#year').select2();

    $('#table').on('change', function() {
        // Получаем выбранное значение
        var selectedValue = $(this).val();
        // Если выбрано значение 1, показываем второй select, иначе скрываем

        // if($('#table').val()== 'publication') {
        //     $('#table_type_div').show();
        // } else {
        //     $('#table_type_div').hide();
        // }
    });




});
