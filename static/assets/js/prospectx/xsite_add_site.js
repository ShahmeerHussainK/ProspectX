function Xsite_AddSite_Setup(conf) {

    this.options = conf;
    // Chain constructor with call
    Prospectx.call(this, this.options);
}

Xsite_AddSite_Setup.prototype.init = function () {
    let self = this;

    $(document).ready(function () {
        Xsite_AddSite_Setup.prototype.PreProcessing();
        Xsite_AddSite_Setup.prototype.Validations();
    });

    $(document).on('click', '#Next', function () {
        $('#Next').parent().addClass('disabled');
        $('#Next').removeAttr('href');
    });

    $(document).on('focus', '#phone', function () {
        Xsite_AddSite_Setup.prototype.Phone_field_events("focus", $(this));
    });
    $(document).on('blur', '#phone', function () {
        Xsite_AddSite_Setup.prototype.Phone_field_events("blur", $(this));
    });
    $(document).on('focus', '#zip', function () {
        Xsite_AddSite_Setup.prototype.ZipCode_field_events("focus", $(this));
    });
    $(document).on('blur', '#zip', function () {
        Xsite_AddSite_Setup.prototype.ZipCode_field_events("blur", $(this));
    });
    $(document).on('blur', '#email', function () {
        Xsite_AddSite_Setup.prototype.Email_field_events("blur");
    });

    $(document).on('change', 'input[type=\'radio\']', function () {
        Xsite_AddSite_Setup.prototype.Domain_type_selection()
    });

    $("#purchase_domain_btn").click(function () {
        toastr.success("Domain is available for purchase");
        $("#domain_purchase_confirmation_modal").modal('hide');
        Xsite_AddSite_Setup.prototype.Next();
    });

    $(document).on('click', '.site_category', function () {
        Xsite_AddSite_Setup.prototype.Site_Category_Selection($(this))
    });

};

Xsite_AddSite_Setup.prototype.PreProcessing = function () {
    $('#Next').parent().addClass('disabled');
    $('#Next').removeAttr('href');

    $('#phone').css("padding-left", "78px");
    $('.iti__country-list').css("width", "310px");
    $('.iti__country-list').css("list-style", "none !important");
    $('.iti__country-list').css("padding", "5px 10px");

    $("#dial_code").val($("#phone").intlTelInput("getSelectedCountryData").dialCode);
};

Xsite_AddSite_Setup.prototype.Phone_field_events = function (type, obj) {
    if (type === "focus") {
        var placeholder = obj.attr('placeholder');
        var mask = placeholder.replace(/[0-9]/g, "9");
        obj.inputmask({"mask": mask});
    } else {
        if ($("#is_validated").val() !== "valid") {
            $("#phone_error").removeClass('d-none');
            $("#phone_error").html($("#is_validated").val());
        } else {
            $("#phone_error").addClass('d-none');
        }
    }
};

Xsite_AddSite_Setup.prototype.ZipCode_field_events = function (type, obj) {
    if (type === "focus") {
        var mask = "99999";
        obj.inputmask(mask, {"placeholder": ""});
    } else {
        if (obj.val().length !== 5) {
            $("#zip_error").removeClass('d-none');
        } else {
            $("#zip_error").addClass('d-none');
        }
    }
};

Xsite_AddSite_Setup.prototype.Email_field_events = function (type) {
    if (!Xsite_AddSite_Setup.prototype.validateEmail($("#email").val())) {
        $("#email_error").removeClass('d-none');
    } else {
        $("#email_error").addClass('d-none');
    }
};

Xsite_AddSite_Setup.prototype.Domain_type_selection = function () {
    if ($('#customRadio1').is(':checked')) {
        $("#existing_domain").hide();
        $("#new_domain").show();
        $("#domain2").val("");
    } else if ($('#customRadio2').is(':checked')) {
        $("#existing_domain").show();
        $("#new_domain").hide();
        $("#domain1").val("");
    }
};

Xsite_AddSite_Setup.prototype.Site_Category_Selection = function (obj) {
    $(".site_category").removeAttr("style");
    if (obj.attr("mydata") === "1") {
        obj.css("color", "white");
        obj.addClass("active_category");
        obj.css("background", "#7367EF");
        Xsite_AddSite_Setup.prototype.Next();
    }
};

Xsite_AddSite_Setup.prototype.Validations = function () {

    $('#elemdiv :input[required]').keydown(function (e) {
        if (this.value.length === 0 && e.which === 32) e.preventDefault();
    });

    $('#email').keydown(function (e) {
        if (this.value.length === 0 && e.which === 32) e.preventDefault();
    });

    function validate() {
        var empty = false;
        $('#elemdiv :input[required]').each(function () {
            if ($(this).val() === '' || $(this).val().trim() === '') {
                empty = true;
            }
        });
        if (empty || $("#is_validated").val() !== "valid" || $("#zip").val().length !== 5 || !Xsite_AddSite_Setup.prototype.validateEmail($("#email").val())) {
            $('#Next').parent().addClass('disabled');
            $('#Next').removeAttr('href');
        } else {
            $('#Next').parent().removeClass('disabled');
            $('#Next').attr('href', '#next');
        }

    }

    (function () {
        $('#phone').change(validate);
        $('#email').keyup(validate);
        $('#elemdiv :input[required]').keyup(validate);
    })()

};

Xsite_AddSite_Setup.prototype.Next = function () {
    $('#Next').parent().removeClass('disabled');
    $('#Next').attr('href', '#next');
    $('#Next').click();
};

Xsite_AddSite_Setup.prototype.validateEmail = function ($email) {
    var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    return ($email.length > 0 && emailReg.test($email))
};

function nexttab_link(pk) {
    $(".xsite_desgin_thumbnail").removeAttr("style");
    $("div").find("[mydata='" + pk + "']").css("border", "2px solid #7367EF");
    $('input[name="site_design"]').val(pk);
    Xsite_AddSite_Setup.prototype.Next();
}

function blockSpecialChar(e) {
    var k = e.keyCode;
    return ((k > 64 && k < 91) || (k > 96 && k < 123) || k == 8 || k == 95 || k == 45 || (k >= 48 && k <= 57));
}

function Check_domain_Availability() {
    $('#OK').addClass('disabled');
    $('#OK').removeAttr('onclick');
    if ($('#domain2').val()) {
        $.ajax({
            type: 'GET',
            url: "/xsite/check_domain_availability/" + $('#domain2').val() + $('#extension').val() + "/0/",
            success: function (data) { // on success..
                if (data['message'] === 'Domain exists') {
                    toastr.success(data['message']);
                    $('#Next').parent().removeClass('disabled');
                    $('#Next').attr('href', '#next');
                    $('#Next').click();
                } else {
                    $('#OK').removeClass('disabled');
                    $('#OK').attr('onclick', "javascript:Check_domain_Availability()");
                    toastr.error(data['message']);
                }

            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                var err = JSON.parse(xhr.responseText);
                $('#OK').removeClass('disabled');
                $('#OK').attr('onclick', "javascript:Check_domain_Availability()");
                toastr.error(err.message);
            },
            statusCode: {
                404:
                    function () {
                        alert("page not found");
                    }
            }
        });
    } else {
        $('#OK').removeClass('disabled');
        $('#OK').attr('onclick', "javascript:Check_domain_Availability()");
        toastr.info("Please enter domain name")
    }
}


function Check_domain_Availability2() {
    $('#search').addClass('disabled');
    $('#search').removeAttr('onclick');
    if ($('#domain1').val()) {
        $.ajax({
            type: 'GET',
            url: "/xsite/check_domain_availability/" + $('#domain1').val() + $('#price').val() + "/" + $('#duration').val() + "/",
            success: function (data) { // on success..
                if (data['message'] === 'Domain does not exist') {
                    $("#domain_price").html(data['amount']);
                    $("#domain_purchase_confirmation_modal").modal('show');
                    $('#search').removeClass('disabled');
                    $('#search').attr('onclick', "javascript:Check_domain_Availability2()");
                } else {
                    $('#search').removeClass('disabled');
                    $('#search').attr('onclick', "javascript:Check_domain_Availability2()");
                    toastr.error("Domain is already taken");
                }
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                var err = JSON.parse(xhr.responseText);
                $('#search').removeClass('disabled');
                $('#search').attr('onclick', "javascript:Check_domain_Availability2()");
                toastr.error(err.message);
            },
            statusCode: {
                404:
                    function () {
                        alert("page not found");
                    }
            }
        });
    } else {
        $('#search').removeClass('disabled');
        $('#search').attr('onclick', "javascript:Check_domain_Availability2()");
        toastr.info("Please enter domain name")
    }
}

Xsite_AddSite_Setup.prototype.Site_Type_Selection = function (type) {
    if (type === "landing_page") {
        $(".type").removeAttr("style");
        document.getElementById(type).style.color = "white";
        document.getElementById(type).style.backgroundColor = "#7367EF";

        $.ajax({
            type: 'GET',
            url: "/xsite/get_site_designs/" + $(".active_category").attr("mydata") + "/" + type + "/",
            success: function (data) { // on success..
                $(".design_section").empty();

                if ($(".active_category").attr("mydata") === "1") {
                    if (data['buyer_sites'].length === 0 && data['seller_sites'].length === 0) {
                        $(".design_section").append('<div class="col-md-12">\n' +
                            '                             <h4 class="mt-0 header-title">3. Select Your Design</h4>\n' +
                            '                             <h5 class="text-center" style="margin-top: 110px;">No Site Design are available for your selection</h5>\n' +
                            '                        </div>');
                    } else {
                        $(".design_section").append('<div class="col-md-12">\n' +
                            '                                                <h4 class="mt-0 header-title">3. Select Your Design</h4>\n' +
                            '                                                <div class="desgin_selection_message">\n' +
                            '                                                    Please Note: The copy in the images does not reflect the exact\n' +
                            '                                                    content pack\n' +
                            '                                                    you have chosen.\n' +
                            '                                                </div>\n' +
                            '                                            </div>');

                        if (data['buyer_sites'].length !== 0) {
                            $(".design_section").append('<div class="col-md-12">\n' +
                                '                            <div class="desgin_selection_message">\n' +
                                '                                Buyer Sites\n' +
                                '                            </div>\n' +
                                '                        </div>');
                            data['buyer_sites'].forEach(function (item, index) {
                                if (item !== null) {
                                    markup = "<div class=\"col-md-4\">\n" +
                                        "    <div mydata=\"" + item.id + "\" class=\"card xsite_desgin_thumbnail\">\n" +
                                        "        <div onclick=\"javascript:nexttab_link(" + item.id + ")\" style=\"cursor: pointer;\"\n" +
                                        "             class=\"shadow\"\n" +
                                        "             role=\"menuitem\">\n" +
                                        "        <p class=\"text-center text-muted  mb-3 mt-3\">" + item.template_name + "</p>\n" +
                                        "        <img class=\"card-img-bottom\" style=\"border-bottom-right-radius: .5rem; border-bottom-left-radius: .5rem;\" src=\"/media" + item.template_image + "\" alt=\"Card image cap\">\n" +
                                        "        </div>\n" +
                                        "    </div>\n" +
                                        "</div>";

                                    $(".design_section").append(markup);
                                }
                            });
                        }

                        if (data['seller_sites'].length !== 0) {
                            $(".design_section").append('<div class="col-md-12">\n' +
                                '                            <div class="desgin_selection_message">\n' +
                                '                                Seller Sites\n' +
                                '                            </div>\n' +
                                '                        </div>');
                            data['seller_sites'].forEach(function (item, index) {
                                if (item !== null) {
                                    markup = "<div class=\"col-md-4\">\n" +
                                        "    <div mydata=\"" + item.id + "\" class=\"card xsite_desgin_thumbnail\">\n" +
                                        "        <div onclick=\"javascript:nexttab_link(" + item.id + ")\" style=\"cursor: pointer;\"\n" +
                                        "             class=\"shadow\"\n" +
                                        "             role=\"menuitem\">\n" +
                                        "        <p class=\"text-center text-muted  mb-3 mt-3\">" + item.template_name + "</p>\n" +
                                        "        <img class=\"card-img-bottom\" style=\"border-bottom-right-radius: .5rem; border-bottom-left-radius: .5rem;\" src=\"/media" + item.template_image + "\" alt=\"Card image cap\">\n" +
                                        "        </div>\n" +
                                        "    </div>\n" +
                                        "</div>";

                                    $(".design_section").append(markup);
                                }
                            });
                        }
                    }
                } else {
                    if (data['sites'].length === 0) {
                        $(".design_section").append('<div class="col-md-12">\n' +
                            '                             <h4 class="mt-0 header-title">3. Select Your Design</h4>\n' +
                            '                             <h5 class="text-center" style="margin-top: 110px;">No Site Design are available for your selection</h5>\n' +
                            '                        </div>');
                    } else {
                        $(".design_section").append('<div class="col-md-12">\n' +
                            '                                                <h4 class="mt-0 header-title">3. Select Your Design</h4>\n' +
                            '                                                <div class="desgin_selection_message">\n' +
                            '                                                    Please Note: The copy in the images does not reflect the exact\n' +
                            '                                                    content pack\n' +
                            '                                                    you have chosen.\n' +
                            '                                                </div>\n' +
                            '                                            </div>');
                        data['sites'].forEach(function (item, index) {
                            if (item !== null) {
                                markup = "<div class=\"col-md-4\">\n" +
                                    "    <div mydata=\"" + item.id + "\" class=\"card xsite_desgin_thumbnail\">\n" +
                                    "        <div onclick=\"javascript:nexttab_link(" + item.id + ")\" style=\"cursor: pointer;\"\n" +
                                    "             class=\"shadow\"\n" +
                                    "             role=\"menuitem\">\n" +
                                    "        <p class=\"text-center text-muted  mb-3 mt-3\">" + item.template_name + "</p>\n" +
                                    "        <img class=\"card-img-bottom\" style=\"border-bottom-right-radius: .5rem; border-bottom-left-radius: .5rem;\" src=\"/media" + item.template_image + "\" alt=\"Card image cap\">\n" +
                                    "        </div>\n" +
                                    "    </div>\n" +
                                    "</div>";

                                $(".design_section").append(markup);
                            }
                        });
                    }
                }
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                var err = JSON.parse(xhr.responseText);
                toastr.error(err.message);
            },
            statusCode: {
                404:
                    function () {
                        alert("page not found");
                    }
            }
        });

        Xsite_AddSite_Setup.prototype.Next();
    }
};