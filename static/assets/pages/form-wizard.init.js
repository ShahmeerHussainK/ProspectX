/*
 Template Name: Veltrix - Responsive Bootstrap 4 Admin Dashboard
 Author: Themesbrand
 File: Form wizard chart Init
 */

$(function () {
    $("#form-horizontal").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "slide",
        onFinished: function (event, currentIndex) {
            var form = $(this);
            form.submit();
        },
        onStepChanged: function (event, currentIndex) {
            if (currentIndex === 3) {
                if ($("#company_name").val() === "") {
                    $('#Next').parent().addClass('disabled');
                    $('#Next').removeAttr('href');
                } else {
                    $('#Next').parent().removeClass('disabled');
                    $('#Next').attr('href', '#next');
                }
            } else if (currentIndex === 4) {
                $('#Next').parent().addClass('disabled');
                $('#Next').removeAttr('href');
            }
            else if (currentIndex === 5) {
                $('#Finish').click();
                $('#Finish').parent().addClass('disabled');
                $('#Finish').removeAttr('href');
                $('#Previous').parent().addClass('disabled');
                $('#Previous').removeAttr('href');
            }
        }
    });


    $("#form-horizontal .actions").insertBefore("#form-horizontal .steps ");

    var tel_input = document.querySelector('#phone');
    var errorMap = ["Invalid number", "Invalid country code", "Too short", "To long", "Invalid number"];
    var intl = $('#phone').intlTelInput({
        separateDialCode: true,
        autoFormat: true,
        defaultCountry: "auto",
        utilsScript: "/static/assets/js/utils.js"
    });

    tel_input.addEventListener("keyup", function () {
        $("#dial_code").val($("#phone").intlTelInput("getSelectedCountryData").dialCode);
        if (tel_input.value.trim()) {
            if ($(this).intlTelInput("isValidNumber")) {
                $('#is_validated').val('valid');
            }
            else{
                $('#is_validated').val(errorMap[$(this).intlTelInput("getValidationError")]);
            }
        } else {
            $('#is_validated').val('Invalid Number');
        }
    });
});
