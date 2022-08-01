$(document).ready(function() {
    $('.select2').select2({
        placeholder: "Thành phố, sân bay",
        allowClear: true,
        width: 'resolve'
    });

    $('.timepicker').datetimepicker({
        timepicker:false,
        format:'Y-m-d'
    });
});


