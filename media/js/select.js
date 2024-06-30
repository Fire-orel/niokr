$(document).ready(function() {
    // Инициализация select2 один раз
    $('#type_publication').select2();

    // Функция для обновления скрытого поля
    function updateTypePublicationSelect() {
        var selectedValues = $('#type_publication').val();
        console.log(selectedValues);
        $('#type_publication_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_publication').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;
            console.log("Selected element: ", selectedElement);
            console.log("Selected value: ", selectedValue);

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
            console.log("Unselected element: ", selectedElement);
            console.log("Unselected value: ", selectedValue);

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
        console.log(selectedValues);
        $('#type_documents_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_documents').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;
            console.log("Selected element: ", selectedElement);
            console.log("Selected value: ", selectedValue);

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
            console.log("Unselected element: ", selectedElement);
            console.log("Unselected value: ", selectedValue);

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
        console.log(selectedValues);
        $('#type_property_select').val(selectedValues);
    }

    // Слушатель событий select2:select
    $('#type_property').on('select2:select', function(e) {
        if (e.params && e.params.data) {
            var selectedElement = e.params.data;
            var selectedValue = selectedElement.id;
            console.log("Selected element: ", selectedElement);
            console.log("Selected value: ", selectedValue);

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
            console.log("Unselected element: ", selectedElement);
            console.log("Unselected value: ", selectedValue);

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
});
