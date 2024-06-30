$(document).ready(function() {
    // Инициализация select2 один раз
    $('#type_publication').select2();

    // Функция для обновления скрытого поля
    function updateTypePublicationSelect() {
        var selectedValues = $('#type_publication').val();

        $('#type_publication_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_publication').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_publication option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_publication option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_publication').select2();
            updateTypePublicationSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_publication').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;

            // Разблокируем все элементы
            $('#type_publication option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_publication').select2();
            updateTypePublicationSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypePublicationSelect();



    $('#type_documents').select2();

    // Функция для обновления скрытого поля
    function updateTypeDocumentsSelect() {
        var selectedValues = $('#type_documents').val();

        $('#type_documents_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_documents').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_documents option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_documents option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_documents').select2();
            updateTypeDocumentsSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_documents').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;

            // Разблокируем все элементы
            $('#type_documents option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_documents').select2();
            updateTypeDocumentsSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypeDocumentsSelect();


    $('#type_property').select2();

    // Функция для обновления скрытого поля
    function updateTypePropertySelect() {
        var selectedValues = $('#type_property').val();

        $('#type_property_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_property').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_property option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_property option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_property').select2();
            updateTypePropertySelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_property').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Разблокируем все элементы
            $('#type_property option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_property').select2();
            updateTypePropertySelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypePropertySelect();



    $('#type_monographs').select2();

    // Функция для обновления скрытого поля
    function updateTypeMonographsSelect() {
        var selectedValues = $('#type_monographs').val();

        $('#type_monographs_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_monographs').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_monographs option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_monographs option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_monographs').select2();
            updateTypeMonographsSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_monographs').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Разблокируем все элементы
            $('#type_monographs option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_monographs').select2();
            updateTypeMonographsSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypeMonographsSelect();



    $('#type_grants').select2();

    // Функция для обновления скрытого поля
    function updateTypeGrantSelect() {
        var selectedValues = $('#type_grants').val();

        $('#type_grants_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_grants').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;

            // Блокируем все остальные элементы
            $('#type_grants option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_grants option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_grants').select2();
            updateTypeGrantSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_grants').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;

            // Разблокируем все элементы
            $('#type_grants option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_grants').select2();
            updateTypeGrantSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypeGrantSelect();





    $('#type_participations').select2();

    // Функция для обновления скрытого поля
    function updateTypeParticipationSelect() {
        var selectedValues = $('#type_participations').val();

        $('#type_participations_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_participations').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_participations option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_participations option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_participations').select2();
            updateTypeParticipationSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_participations').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Разблокируем все элементы
            $('#type_participations option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_participations').select2();
            updateTypeParticipationSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypeParticipationSelect();



    $('#type_events').select2();

    // Функция для обновления скрытого поля
    function updateTypeEventSelect() {
        var selectedValues = $('#type_events').val();

        $('#type_events_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_events').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;


            // Блокируем все остальные элементы
            $('#type_events option').each(function() {
                $(this).prop('disabled', true);
            });

            // Снимаем блокировку с выбранного элемента
            $('#type_events option[value="' + selectedValue + '"]').prop('disabled', false);

            // Обновляем select2 и скрытое поле
            $('#type_events').select2();
            updateTypeEventSelect();
        }
    });

    // Слушатель событий select2:unselect
    $('#type_events').on('select2:unselect', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;
            

            // Разблокируем все элементы
            $('#type_events option').each(function() {
                $(this).prop('disabled', false);
            });

            // Обновляем select2 и скрытое поле
            $('#type_events').select2();
            updateTypeEventSelect();
        }
    });

    // Обновляем скрытое поле при загрузке страницы
    updateTypeEventSelect();
});
