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
    var urlPath = window.location.pathname;
    var mapDetailsPattern = /^\/map_details\/\d+$/;

    if (mapDetailsPattern.test(urlPath)) {
        localStorage.removeItem('activeTabGlav');
        localStorage.removeItem('activeTabType');
    }




    $('#myTabGlav button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {


        localStorage.setItem('activeTabGlav', $(e.target).attr('href'));
    });

    // Восстановление активной вкладки из локального хранилища
    var activeTabGlav = localStorage.getItem('activeTabGlav');
    if (activeTabGlav) {
        $('#myTabGlav button[href="' + activeTabGlav + '"]').tab('show');
    } else {
        $('#myTabGlav button[data-bs-toggle="tab"]:first').tab('show'); // Установка первой вкладки активной по умолчанию
    }



    $('#myTab button[data-toggle="tab"]').on('shown.bs.tab', function (e) {


        localStorage.setItem('activeTab', $(e.target).attr('href'));
    });

    // Восстановление активной вкладки из локального хранилища
    var activeTab = localStorage.getItem('activeTab');
    if (activeTab) {
        $('#myTab button[href="' + activeTab + '"]').tab('show');
    } else {
        $('#myTab button[data-toggle="tab"]:first').tab('show'); // Установка первой вкладки активной по умолчанию
    }


    $('#myTabType button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        localStorage.setItem('activeTabType', $(e.target).attr('href'));
    });

    // Восстановление активной вкладки из локального хранилища
    var activeTabType = localStorage.getItem('activeTabType');
    if (activeTabType) {
        $('#myTabType button[href="' + activeTabType + '"]').tab('show');
    } else {
        $('#myTabType button[data-bs-toggle="tab"]:first').tab('show'); // Установка первой вкладки активной по умолчанию
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







    $(document).on('click', '#deleteMap', function(){

        var mapID = $(this).data('id'); // Получаем ID публикации

        $('#confirmDeleteMapBtn').data('id', mapID); // Устанавливаем ID в кнопку подтверждения удаления
    });


    // Обработчик клика по кнопке подтверждения удаления
    $('#confirmDeleteMapBtn').click(function() {


        var mapID = $(this).data('id');// Получаем ID публикации


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
    $('#table_name').select2();
    $('#table_type').select2();
    $('#year').select2();
    $('#position').select2();


    $('#table_name').on('change', function() {
        // Получаем выбранное значение
        var selectedValue = $(this).val();
        // Если выбрано значение 1, показываем второй select, иначе скрываем


    });


    $('#position').on('change', function() {
        // Получаем выбранное значение
        var selectedValue = $(this).val();
        // Если выбрано значение 1, показываем второй select, иначе скрываем

        if($('#position').val()== 'НО') {
            $('#faculty_div').hide();
            $('#department_div').hide();
        } else if ($('#position').val()== 'ЗД'){
            $('#faculty_div').show();
            $('#department_div').hide();
        }else if ($('#position').val()== 'ЗК'){
            $('#faculty_div').hide();
            $('#department_div').show();
        }
    });



    // Слушатель событий select2
    $('#table_name').select2();

    // Функция для обновления скрытого поля
    function updateHiddenField() {
        var selectedValues = $('#table_name').val();
        $('#hidden_selected_value').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#table_name').on('select2:select', function(e) {
        var selectedElement = e.params.data;
        var selectedValue = selectedElement.id;

        // Если выбранный элемент удовлетворяет условию, блокируем остальные
        if (selectedValue === 'All') { // Замените SPECIFIC_VALUE на ваше значение
            $('#table_name option').each(function() {
                if ($(this).val() !== 'All') {
                    $(this).prop('disabled', true);
                }
            });
        } else {
            // Если выбран какой-либо другой элемент, блокируем элемент 'All'
            $('#table_name option[value="All"]').prop('disabled', true);
        }

        if( selectedValue == 'Publications') {
            $('#type_publication_div').show();
        }
        if( selectedValue == 'SecurityDocuments') {
            $('#type_documents_div').show();
            $('#type_property_div').show();
        }
        if( selectedValue == 'Monographs') {
            $('#type_monographs_div').show();
        }
        if( selectedValue == 'Grant') {
            $('#type_grants_div').show();
        }
        if(selectedValue == 'Event') {
            $('#type_participations_div').show();
            $('#type_events_div').show();
            $('#type_levels_div').show();
        }

        $('#table_name').select2();
        $('#type_publication').select2()
        $('#type_documents').select2();
        $('#type_property').select2();
        $('#type_monographs').select2();
        $('#type_grants').select2();
        $('#type_participations').select2();
        $('#type_events').select2();
        $('#type_levels').select2();// Обновляем select2
        updateHiddenField(); // Обновляем скрытое поле
    });

    // Слушатель событий select2:unselect
    $('#table_name').on('select2:unselect', function(e) {
        var selectedElement = e.params.data;
        var selectedValue = selectedElement.id;

        // Если удалённый элемент удовлетворяет условию, разблокируем остальные
        if (selectedValue === 'All') { // Замените SPECIFIC_VALUE на ваше значение
            $('#table_name option').each(function() {
                $(this).prop('disabled', false);
            });
        } else {
            // Если нет выбранных элементов, разблокируем элемент 'All'
            if ($('#table_name').val().length === 0) {
                $('#table_name option[value="All"]').prop('disabled', false); // Замените 'All' на ваше значение
            }
        }

        if(selectedValue == 'Publications') {
            $('#type_publication_div').hide();
        }
        if( selectedValue == 'SecurityDocuments') {
            $('#type_documents_div').hide();
            $('#type_property_div').hide();
        }
        if(selectedValue == 'Monographs') {
            $('#type_monographs_div').hide();
        }
        if(selectedValue == 'Grant') {
            $('#type_grants_div').hide();
        }
        if(selectedValue == 'Event') {
            $('#type_participations_div').hide();
            $('#type_events_div').hide();
            $('#type_levels_div').hide();
        }
        $('#table_name').select2();
        $('#type_publication').select2();
        $('#type_documents').select2();
        $('#type_property').select2();
        $('#type_monographs').select2();
        $('#type_grants').select2();
        $('#type_participations').select2();
        $('#type_events').select2();
        $('#type_levels').select2();

        updateHiddenField(); // Обновляем скрытое поле

    });

    // Обновляем скрытое поле при загрузке страницы
    updateHiddenField();



    var select2Input = $('#id_full_name_author_publications');



    
});
