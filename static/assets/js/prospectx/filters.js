function Filters(conf) {

    this.options = conf;
    this.prospectx_new = [
        {name: 'Full Name', column: 'fullname'},
        {name: 'First Name', column: 'firstname'},
        {name: 'Last Name', column: 'lastname'},
        {name: 'Mailing Address', column: 'mailingaddress'},
        {name: 'Mailing Address 2', column: 'mailingaddress2'},
        {name: 'Mailing City', column: 'mailingcity'},
        {name: 'Mailing State', column: 'mailingstate'},
        {name: 'Mailing Zip', column: 'mailingzip'},
        {name: 'Property Address', column: 'propertyaddress'},
        {name: 'Property Address 2', column: 'propertyaddress2'},
        {name: 'Property City', column: 'propertycity'},
        {name: 'Property State', column: 'propertystate'},
        {name: 'Property Zip', column: 'propertyzip'},
        {name: 'Email', column: 'email'},
        {name: 'Email2', column: 'email2'},
        {name: 'Phone Landline', column: 'phonelandline'},
        {name: 'Phone Cell', column: 'phonecell'},
        {name: 'Phone Other', column: 'phoneother'},
        {name: 'Phone 1', column: 'phone1'},
        {name: 'Phone 2', column: 'phone2'},
        {name: 'Phone 3', column: 'phone3'},
        {name: 'Phone 4', column: 'phone4'},
        {name: 'Phone 5', column: 'phone5'},
        {name: 'Phone 6', column: 'phone6'},
        {name: 'Phone 7', column: 'phone7'},
        {name: 'Phone 8', column: 'phone8'},
        {name: 'Phone 9', column: 'phone9'},
        {name: 'Phone 10', column: 'phone10'},
        {name: 'Custom 1', column: 'custome1'},
        {name: 'Custom 2', column: 'custome2'},
        {name: 'Custom 3', column: 'custome3'},
        {name: 'Custom 4', column: 'custome4'},
        {name: 'Custom 5', column: 'custome5'},
        {name: 'Custom 6', column: 'custome6'},
        {name: 'Custom 7', column: 'custome7'},
        {name: 'Custom 8', column: 'custome8'},
        {name: 'Custom 9', column: 'custome9'},
        {name: 'Custom 10', column: 'custome10'},
        {name: 'Notes', column: 'notes'},
    ];

    //apply_filter

    // Chain constructor with call
    Prospectx.call(this, this.options);
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


Filters.prototype.init = function () {
    let self = this;

    // hide filter div on page load
    $("#filters-div").hide();

    // loading table
    self.initial_page_load();

    Filters_Action.prototype.init_filters_datatable();

    $(document).on('click', '.clear-all-filters', function (event) {
        $("#list1").val([]).change();
        $("#list2").val([]).change();
        $("#tag1").val([]).change();
        $("#tag2").val([]).change();
        $("#filter-form")[0].reset();

        $("#label-or").removeClass("active");
        $("#label-and").addClass("active")

    });


    // Filters_Action.prototype.init_filters_datatable();

    // handling enter

    $('#input-search').keypress(function (e) {
        var key = e.which;
        if (key == 13)  // the enter key code
        {
            e.preventDefault();
            $(".btn-apply-filter").click()
        }
    });

    $(document).on('click', '.btn-apply-filter', function (event) {
        let $from = $('#filter-form');
        let form_data = $("#filter-form").serializeArray();
        var obj = {'name': 'action', 'value': 'all'};
        form_data.push(obj);
        let data = {type: $from.attr('method'), url: $from.attr('action'), data: form_data};
        // self.apply_filters(data);
        event.preventDefault();
        last_filter_status = "filters";
        last_form_data = {type: $from.attr('method'), url: $from.attr('action'), data: form_data};
        Filters_Action.prototype.init_filters_datatable();
    });

    // Add Filter lil
    $(".add-filter").click(function () {
        let html = '', name = '';
        html += '<li class="list-inline-item event-list">';
        html += '<div class="p-2 border border-primary bg-lighten-primary">';
        html += '<div class="row">';
        html += '<div class="col-md-4">';
        html += '<select name="select-key" class="form-control custom-select">';
        html += '<option value="-1">Select Field to Filter</option>';
        $.each(self.prospectx_new, function (key, prospect) {
            if (prospect['column'] === 'custome1' || prospect['column'] === 'custome2' || prospect['column'] === 'custome3') {
                name = self.options.custom_fields[prospect['column']];
            } else {
                name = prospect['name'];
            }
            html += '<option value="' + prospect['column'] + '">' + name + '</option>';
        });
        html += '</select>';
        html += '</div>';
        html += '<div class="col-md-4">';
        html += '<select name="select-con" class="form-control custom-select">';
        html += '<option value="contains">contains</option>';
        html += '<option value="not_contains">doesn\'t contain</option>';
        html += '<option value="is_empty">is empty</option>';
        html += '<option value="is_not_empty">is not empty</option>';
        html += '</select>';
        html += '</div>';
        html += '<div class="col-md-3">';
        html += '<div class="form-group mb-0">';
        html += '<input name="select-val" class="form-control form-control-md" type="text">';
        html += '</div>';
        html += '</div>';
        html += '<div class="col-md-1">';
        html += '<div class="form-group mb-0 mt-1">';
        html += '<button class="btn btn-danger btn-sm btn-delete-optional-filters-li hidding-li-button" type="button">';
        html += '<i class="fa fa-trash"></i>';
        html += '</button>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</li>';


        $(".optional-ul").append(html)
    });


    $('.hidding-li-button').click(function () {
        $('.hide-this-li').hide("slide");
    });

    // Delete Filter li
    $(".optional-ul").on('click', ".btn-delete-optional-filters-li", function () {
        $(this).closest('li').remove();
    });

    //on select
    $('#page-select-existing-filter').on('change', this.select_page_existing_filter);

    // save filter
    $(".btn-save-filter").click(this.save_filters);

    // filter button toggle
    $("#filter-toggle-button").click(function () {
        $("#" +
            "filters-div").toggle();
    });

    Filters.prototype.toast();
    Filters.prototype.btn_clicks();
    Filters.prototype.handle_information_div();
    Filters.prototype.telmasking();


    $(".list_count").change(function () {
        var index = $(this).prop('selectedIndex');
        Filters.prototype.list_data(index);
    });

    $(document).on('click', '.view_details', function (e) {
        e.preventDefault();
        var id = $(this).attr("mydata");
        let data_param = {type: 'GET', url: '/filter/get_prospect_details/' + id + "/", id: id};
        Filters.prototype.get_prospect_data(data_param);
    });

    $('#view_deatils_modal').on('submit', '#view_details_modal_form', function () {
        let data = {type: $(this).attr('method'), url: $(this).attr('action'), data: $(this).serialize()};
        self.update_prospect(data);

        return false;
    });

};

Filters.prototype.initial_page_load = function () {
    var $form = $("#filter-form").serializeArray();
    var obj = {'name': 'action', 'value': 'all'};
    $form.push(obj);
    let data = {type: "post", url: "/filter/apply_filter", data: $form};
    // Filters.prototype.apply_filters(data);
    last_filter_status = "default";
    last_form_data = data;

};

Filters.prototype.apply_filters = function (data) {
    var csrftoken = getCookie('csrftoken');
    Filters_Action.prototype.del_result_count();
    $.ajax({
        headers: {"X-CSRFToken": csrftoken},
        type: data.type,
        url: data.url,
        data: data.data,
        success: function (response) { // on success..
            if (response["prospects_count"] >= 0) {
                let count = response["prospects_count"];
                let action = "select_all";
                Filters_Action.prototype.set_result_count(count, action)
            } else {
                var prospects_data = JSON.parse(response['prospects']);
                Filters.prototype.load_table2(prospects_data);

            }

        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            alert("in fail")
            let err = JSON.parse(xhr.responseText);
            console.log(err);
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};

Filters.prototype.save_filters = function () { // set last form data and status here
    let form_data = $("#filter-form").serializeArray()
    var obj = '';
    var obj2 = '';
    let check_class = $(this).attr("id")
    if (check_class == "btn-save-filter-old") {
        var selected_filter = $("#select-existing-save-filter").val();
        obj = {'name': 'action', 'value': 'old_filter'}
        obj2 = {'name': 'filter_name', 'value': selected_filter}

    } else if (check_class == "btn-save-filter-new") {
        let filter_name = $("#new-save-filter-name").val();
        obj = {'name': 'action', 'value': 'new_filter'}
        obj2 = {'name': 'filter_name', 'value': filter_name}

    }
    form_data.push(obj)
    form_data.push(obj2)
    let data = {type: $("#filter-form").attr('method'), data: form_data};

    $.ajax({
        type: data.type,
        url: 'save_filters',
        data: data.data,
        success: function (response) { // on success..
            $(".create-filter-modal").modal('hide');
            $(".existing-filter-modal").modal('hide');
            $(".bs-example-modal-save-filter").modal('hide');
            if (response["action"] == "new_filter") {


                $('.select-existing-filter')
                    .append($("<option></option>")
                        .attr("value", response["new_filter_id"])
                        .text(response["new_filter_name"]));

                $('.save-filer-partial-select')
                    .append($("<option></option>")
                        .attr("value", response["new_filter_id"])
                        .text(response["new_filter_name"]));

            }

        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            let err = JSON.parse(xhr.responseText);
            console.log(err);
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};

Filters.prototype.load_table2 = function (prospects) {
    var filters_table1 = $(".mytable");
    filters_table1.empty();
    if ($.fn.DataTable.isDataTable(".mytable")) {

        $('.mytable').dataTable().fnClearTable();
        $('.mytable').dataTable().fnDestroy();
    }

    var table_header = '<thead>\n' +
        '                            <tr>\n' +
        '                                <th></th>\n' +
        '                                <th>Name</th>\n' +
        '                                <th>Mailing Full Address</th>\n' +
        '                                <th>Property Full Address</th>\n' +
        '                                <th>List Count</th>\n' +
        '                                <th>Tags</th>\n' +
        '                                <th>Sequence</th>\n' +
        '                                <th>Action</th>\n' +
        '                            </tr>\n' +
        '                            </thead><tbody>';

    filters_table1.html(table_header);

    prospects.forEach(function (prospect, index) {
        // var myrow = "<tr><td>gh</td><td>gdfg</td><td>fg</td><td>gfg</td><td>dfgf</td><td>fgfdg</td><td>gdf</td><td>fgdf</td> </tr>"
        var table_row = '<tr><td><div class="custom-control custom-checkbox mb-2"><input type="checkbox" cus_id="' + prospect["id"] + '" class="custom-control-input pros_ins" id="customCheck' + prospect["id"] + '" /><label class="custom-control-label" for="customCheck' + prospect["id"] + '"> </label></div></td><td><a  mydata="' + prospect["id"] + '" class="btn-link view_details" href="javascript:void(0);">' + prospect["fullname"] + '</a></td><td>' + prospect["mailingaddress"] + '</td><td>' + prospect["propertyaddress"] + '</td><td>' + prospect["list_count"] + '</td><td>' + prospect["tag_count"] + '</td><td>' + prospect["sequence"] + ' </td><td><div class=" " role="group" aria-label="action btns">\n' +
            '                                                <button mydata="' + prospect["id"] + '" type="button"\n' +
            '                                                        class="btn btn-primary btn-sm view_details" data-toggle="modal"\n' +
            '                                                        data-placement="top" title=""\n' +
            '                                                        data-original-title="Update"><i\n' +
            '                                                        class="mdi mdi-pencil-box-outline"></i></button>\n' +
            '                                                <button mydata="' + prospect["id"] + '" type="button" class="btn btn-primary btn-sm update_prospect"\n' +
            '                                                        data-toggle="tooltip"\n' +
            '                                                        data-placement="top" title="" data-original-title="Edit"><i\n' +
            '                                                        class="mdi mdi-grease-pencil"></i></button>\n' +
            '                                                <button mydata="' + prospect["id"] + '" type="button" class="btn btn-danger btn-sm delete_prospect" data-toggle="modal"\n' +
            '                                                        data-target="#exampleModal{{ prospect.id }}">\n' +
            '                                                    <i class="mdi mdi-trash-can-outline"></i>\n' +
            '                                                </button></div></td></tr>'


        filters_table1.append(table_row);
        // filters_table1.append(myrow)

    });

    filters_table1.append('</tbody>');


    Filters_Action.prototype.init_filters_datatable();

};

Filters.prototype.select_page_existing_filter = function () {
    var val = $(this).val();
    if (val != -1) {
        let data = {'filter_id': $(this).val()};
        last_form_data = data;
        last_filter_status = "save_filter";
        Filters_Action.prototype.init_filters_datatable();
    }
};

Filters.prototype.btn_clicks = function () {
    $(document).on('click', '.deletelist', function () {
        var link = "window.location.href='" + $(this).attr('mylink') + "'";
        $('#modaldeletelist').attr("onClick", link);
        $('#deletelistModal').modal('show');
    });

    $(document).on('click', '.deletetag', function () {
        var link = "window.location.href='" + $(this).attr('mylink') + "'";
        $('#modaldeletetag').attr("onClick", link);
        $('#deletetagModal').modal('show');
    });

    $(document).on('click', '.delete_prospect', function () {
        var prospect = $(this).attr("mydata");
        var link = "window.location.href='" + '/filter/delete_prospect/' + prospect + '/' + "'";
        $('#btn_delete_prospect').attr("onClick", link);
        $('#delete_prospect_modal').modal('show');
    });

    $(document).on('click', '.update_prospect', function () {
        var prospect = $(this).attr("mydata");
        window.location.href = "/filter/update_prospect/" + prospect + "/";
    });
};

Filters.prototype.handle_information_div = function () {
    $(".personal_info_edit_div").hide();
    $(".personal_info_btn").hide();

    $(document).on('frmFormComplete', function (event, form, response) {
        $(".personal_info_btn").click(function () {
            $(".personal_info_div").show();
            $(".personal_info_edit_div").hide();
            $(this).hide();
            $(".personal_info_edit_btn").show();
        });
    });

    $(".personal_info_edit_btn").click(function () {
        $(".personal_info_div").hide();
        $(".personal_info_edit_div").show();
        $(this).hide();
        $(".personal_info_btn").show();
    });

    $(".prospect-information-modal").on("hidden.bs.modal", function () {
        $(".personal_info_div").show();
        $(".personal_info_edit_div").hide();
        $(".personal_info_btn").hide();
        $(".personal_info_edit_btn").show();
    });
};

Filters.prototype.toast = function () {
    if (error_type === "info") {
        toastr.info(msg);
        window.location.href = "/filter/filter_page"
    } else if (error_type === "success") {
        toastr.success(msg);
        window.location.href = "/filter/filter_page"
    } else if (error_type === "error") {
        toastr.error(msg);
        window.location.href = "/filter/filter_page"
    } else if (error_type === "warning") {
        toastr.warning(msg);
        window.location.href = "/filter/filter_page"
    }
};

Filters.prototype.telmasking = function () {
    var input = document.querySelector('.edit_phone');
    var errorMap = ["Invalid number", "Invalid country code", "Too short", "To long", "Invalid number"];

    $('.edit_phonelandline').focus(function () {
        var mask = "999-999-9999";
        $(this).inputmask(mask, {"placeholder": ""});
    });

    $('.edit_phoneother').focus(function () {
        var mask = "999-999-9999";
        $(this).inputmask(mask, {"placeholder": ""});
    });

    $('.edit_phone1, .edit_phone2, .edit_phone3, .edit_phone4, .edit_phone5, .edit_phone6, .edit_phone7, .edit_phone8, .edit_phone9, .edit_phone10 ').focus(function () {
        var mask = "999-999-9999";
        $(this).inputmask(mask, {"placeholder": ""});
    });

    $('.edit_mailingzip').focus(function () {
        $(this).inputmask("99999", {"placeholder": ""});
    });

    $('.edit_propertyzip').focus(function () {
        $(this).inputmask("99999", {"placeholder": ""});
    });

    $('.edit_phone').focus(function () {
        var placeholder = $(this).attr('placeholder');
        var mask = placeholder.replace(/[0-9]/g, "9");
        $(this).inputmask({"mask": mask});
    });


    input.addEventListener("blur", function () {
        $(".edit_phonecell").val($(".edit_phone").intlTelInput("getNumber"));
        if (input.value.trim()) {
            if ($(this).intlTelInput("isValidNumber")) {
                $('#is_validated').val('valid');
            } else {
                $('#is_validated').val(errorMap[$(this).intlTelInput("getValidationError")]);
            }
        } else {
            $('#is_validated').val('Invalid Number');
        }
    });
};

Filters.prototype.list_data = function (index) {
    var list_count = $("#view_deatils_modal").data("list_count");
    $(".Cold_Call_Pending").html(list_count[index]['Cold_Call_Pending']);
    $(".Cold_Call_Sent").html(list_count[index]['Cold_Call_Sent']);
    $(".Direct_Mail_Pending").html(list_count[index]['Direct_Mail_Pending']);
    $(".Direct_Mail_Sent").html(list_count[index]['Direct_Mail_Sent']);
    $(".Voice_Broadcast_Pending").html(list_count[index]['Voice_Broadcast_Pending']);
    $(".Voice_Broadcast_Sent").html(list_count[index]['Voice_Broadcast_Sent']);
    $(".RVM_Pending").html(list_count[index]['RVM_Pending']);
    $(".RVM_Sent").html(list_count[index]['RVM_Sent']);
    $(".SMS_Pending").html(list_count[index]['SMS_Pending']);
    $(".SMS_Sent").html(list_count[index]['SMS_Sent']);
    $(".Email_Pending").html(list_count[index]['Email_Pending']);
    $(".Email_Sent").html(list_count[index]['Email_Sent']);
};

Filters.prototype.get_prospect_data = function (data_param) {
    $.ajax({
        type: data_param.type,
        url: data_param.url,
        success: function (data) { // on success..
            // Show Modal
            $('#view_deatils_modal').modal('show');
            var prospect = data['prospect_obj'];

            $('#view_details_modal_form').attr('action', '/filter/update_prospect_Ajax/' + data_param.id + '/');
            if (prospect.fullname !== null) {
                $('.view_details_name').html(prospect.fullname);
            } else {
                $('.view_details_name').html(' N/A');
            }
            $('.view_details_mailing_address').html(prospect.mailingaddress);
            $('.view_details_property_address').html(prospect.propertyaddress);
            $('.view_details_email').html(prospect.email);
            $('.view_details_email2').html(prospect.email2);
            $('.view_details_phone_landline').html(prospect.phonelandline);
            $('.view_details_phone_other').html(prospect.phoneother);
            $('.view_details_phone_cell').html(prospect.phonecell);
            $('.view_details_phone_1').html(prospect.phone1);
            $('.view_details_phone_2').html(prospect.phone2);
            $('.view_details_phone_3').html(prospect.phone3);
            $('.view_details_phone_4').html(prospect.phone4);
            $('.view_details_phone_5').html(prospect.phone5);
            $('.view_details_phone_6').html(prospect.phone6);
            $('.view_details_phone_7').html(prospect.phone7);
            $('.view_details_phone_8').html(prospect.phone8);
            $('.view_details_phone_9').html(prospect.phone9);
            $('.view_details_phone_10').html(prospect.phone10);
            if (prospect.opt_out === "yes") {
                $('.view_details_optout').prop('checked', true);
            }

            if (prospect.donotcall === "yes") {
                $('.view_details_dnc').prop('checked', true);
            }
            $('.view_details_custom1').html(prospect.custome1);
            $('.view_details_custom2').html(prospect.custome2);
            $('.view_details_custom3').html(prospect.custome3);
            $('.view_details_custom4').html(prospect.custome4);
            $('.view_details_custom5').html(prospect.custome5);
            $('.view_details_custom6').html(prospect.custome6);
            $('.view_details_custom7').html(prospect.custome7);
            $('.view_details_custom8').html(prospect.custome8);
            $('.view_details_custom9').html(prospect.custome9);
            $('.view_details_custom10').html(prospect.custome10);
            $('.view_details_vacancy').html(prospect.vacant);
            $('.view_details_notes').html(prospect.notes);


            // $(".listss").val(prospect.list).attr('selected', 'selected');

            $('.edit_fullname').val(prospect.fullname);
            $('.edit_firstname').val(prospect.firstname);
            $('.edit_lastname').val(prospect.lastname);
            $('.edit_mailingaddress').val(prospect.mailingaddress);
            $('.edit_mailingaddress2').val(prospect.mailingaddress2);
            $('.edit_mailingcity').val(prospect.mailingcity);
            $('.edit_mailingstate').val(prospect.mailingstate);
            $('.edit_mailingzip').val(prospect.mailingzip);
            $('.edit_propertyaddress').val(prospect.propertyaddress);
            $('.edit_propertyaddress2').val(prospect.propertyaddress2);
            $('.edit_propertycity').val(prospect.propertycity);
            $('.edit_propertystate').val(prospect.propertystate);
            $('.edit_propertyzip').val(prospect.propertyzip);
            $('.edit_email').val(prospect.email);
            $('.edit_email2').val(prospect.email2);
            $('.edit_phonelandline').val(prospect.phonelandline);
            $('.edit_phonecell').val(prospect.phonecell);
            if (prospect.phonecell !== null) {
                $('.edit_phone').intlTelInput("setNumber", prospect.phonecell);
            } else {
                $('.edit_phone').intlTelInput("setCountry", 'US');
                $('.edit_phone').val(prospect.phonecell);
            }
            $('.edit_phoneother').val(prospect.phoneother);
            $('.edit_phone1').val(prospect.phone1);
            $('.edit_phone2').val(prospect.phone2);
            $('.edit_phone3').val(prospect.phone3);
            $('.edit_phone4').val(prospect.phone4);
            $('.edit_phone5').val(prospect.phone5);
            $('.edit_phone6').val(prospect.phone6);
            $('.edit_phone7').val(prospect.phone7);
            $('.edit_phone8').val(prospect.phone8);
            $('.edit_phone9').val(prospect.phone9);
            $('.edit_phone10').val(prospect.phone10);
            $('.edit_custome1').val(prospect.custome1);
            $('.edit_custome2').val(prospect.custome2);
            $('.edit_custome3').val(prospect.custome3);
            $('.edit_custome4').val(prospect.custome4);
            $('.edit_custome5').val(prospect.custome5);
            $('.edit_custome6').val(prospect.custome6);
            $('.edit_custome7').val(prospect.custome7);
            $('.edit_custome8').val(prospect.custome8);
            $('.edit_custome9').val(prospect.custome9);
            $('.edit_custome10').val(prospect.custome10);
            $('.edit_vacant').val(prospect.vacant);
            if (prospect.opt_out === "yes") {
                $('.edit_opt_out').prop('checked', true);
            }

            if (prospect.donotcall === "yes") {
                $('.edit_donotcall').prop('checked', true);
            }

            var encodedStr = prospect.notes;
            var parser = new DOMParser;
            var dom = parser.parseFromString(encodedStr, 'text/html');
            var decodedString = dom.body.textContent;

            if (decodedString !== "null") {
                $(".edit_notes").val(decodedString);
            } else {
                $(".edit_notes").val("");
            }

            $(".list_data tr").remove();
            $(".tag_data tr").remove();
            $('.list_count option').remove();

            var list_count = data['list_count'];
            $("#view_deatils_modal").data({"list_count": list_count});
            $(".Cold_Call_Pending").html(list_count[0]['Cold_Call_Pending']);
            $(".Cold_Call_Sent").html(list_count[0]['Cold_Call_Sent']);
            $(".Direct_Mail_Pending").html(list_count[0]['Direct_Mail_Pending']);
            $(".Direct_Mail_Sent").html(list_count[0]['Direct_Mail_Sent']);
            $(".Voice_Broadcast_Pending").html(list_count[0]['Voice_Broadcast_Pending']);
            $(".Voice_Broadcast_Sent").html(list_count[0]['Voice_Broadcast_Sent']);
            $(".RVM_Pending").html(list_count[0]['RVM_Pending']);
            $(".RVM_Sent").html(list_count[0]['RVM_Sent']);
            $(".SMS_Pending").html(list_count[0]['SMS_Pending']);
            $(".SMS_Sent").html(list_count[0]['SMS_Sent']);
            $(".Email_Pending").html(list_count[0]['Email_Pending']);
            $(".Email_Sent").html(list_count[0]['Email_Sent']);

            var lists = data['lists'];
            // console.log(lists.id);
            lists.forEach(function (item, index) {
                if (item !== null) {
                    var link = '/filter/delete_list/' + prospect.id + '/' + item['id'] + '/';
                    markup = "<tr>\n" +
                        "                                                                                        <td>" + item['list_name'] + "</td>\n" +
                        "                                                                                        <td>" + item['created_at'] + "</td>\n" +
                        "                                                                                        <td>\n" +
                        "                                                                                            <a id=\"deletelist\" mylink=\"" + link + "\"\n" +
                        "                                                                                              style=\"color:white;cursor: pointer;\" class=\"btn btn-danger btn-sm deletelist\"><i\n" +
                        "                                                                                                    class=\"mdi mdi-trash-can-outline\"></i></a>\n" +
                        "                                                                                        </td>\n" +
                        "                                                                                    </tr>";

                    $('.list_count').append("<option value=\"" + item['id'] + "\">" + item['list_name'] + "</option>");
                    tableBody = $(".list_data");
                    tableBody.append(markup);
                }
            });

            var tags = data['tags'];
            tags.forEach(function (item, index) {
                if (item !== null) {
                    var link = '/filter/delete_tag/' + prospect.id + '/' + item['id'] + '/';
                    markup = "<tr>\n" +
                        "                                                                                        <td>" + item['tag_name'] + "</td>\n" +
                        "                                                                                        <td>" + item['created_at'] + "</td>\n" +
                        "                                                                                        <td>\n" +
                        "                                                                                            <a  id=\"deletetag\" mylink=\"" + link + "\"\n" +
                        "                                                                                                style=\"color:white;cursor: pointer;\" class=\"btn btn-danger btn-sm deletetag\"><i\n" +
                        "                                                                                                    class=\"mdi mdi-trash-can-outline\"></i></a>\n" +
                        "                                                                                        </td>\n" +
                        "                                                                                    </tr>";
                    tableBody = $(".tag_data");
                    tableBody.append(markup);
                }
            });


        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            alert("error")
        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};

Filters.prototype.update_prospect = function (data) {
    // $('#update_task_button').attr('disabled',true);

    $.ajax({
        type: data.type,
        url: data.url,
        data: data.data,
        success: function () { // on success..
            document.getElementById("view_details_modal_form").reset();
            $('#view_deatils_modal').modal('hide');
            toastr.success("Prospect Updated Successfully!");
        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            // $('#update_task_button').attr('disabled',false);
            var err = JSON.parse(xhr.responseText);
            if (err.message === "There is some error!")
                toastr.error(err.message);

            else {
                $.each(err.update_prospect_form, function (key, value) {
                    toastr.error(value + "\n");
                });
            }

        },
        statusCode: {
            404: function () {
                alert("page not found");
            }
        }
    });
};