function Filters_Action(conf) {

    this.options = conf;

    // Chain constructor with call
    Prospectx.call(this, this.options);
}


Filters_Action.prototype.init = function () {
    let self = this;

    $(".select-type").click(this.select_type_handler);
    $(".selected-action").click(this.select_action_handler);

    $(document).on('click', 'input.pros_ins', this.on_check_box_click);
    // Filters_Action.prototype.set_count_for_dt()
    $(document).on('click', '#show-seq', this.show_seq);
};

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

Filters_Action.prototype.on_check_box_click = function (e) {
    let is_checked = false;

    if ($(this).prop("checked") == true) {

        is_checked = true;
    } else if ($(this).prop("checked") == false) {

        is_checked = false;
    }

    if ($(".select-option-btn-results").attr('by') === 'select_all') {
        var cnt;
        let string = $(".select-option-btn-results").text();
        var all_count = parseInt(string.replace(/[^0-9]/g, ""));

        if (is_checked === false) {
            cnt = all_count - 1;
        } else {
            cnt = all_count + 1;
        }

        Filters_Action.prototype.set_result_count(cnt, "select_all");
    } else {


        var count = $(".pros_ins:checked").length;
        Filters_Action.prototype.set_result_count(count, "select_visible");
        if (count == 0) {
            Filters_Action.prototype.del_result_count();
        }
    }
};

Filters_Action.prototype.select_type_handler = function () {
    var sel_val = $(this).attr("value");
    var action_btn = $(".action-btn");
    let $check_box = $('input.pros_ins');
    if (sel_val === 'select_visible') {
        $check_box.prop('checked', true);
        var count = $check_box.length;

        Filters_Action.prototype.set_result_count(count, "select_visible")


    } else if (sel_val === 'select_all') {
        $check_box.prop('checked', true);
        var $from = $("#filter-form");

        var obj = {'name': 'action', 'value': 'count'};

        let data;
        let form_data = last_form_data.data;
        form_data.push(obj);
        last_filter_status = "count";
        data = {type: $from.attr('method'), url: $from.attr('action'), data: form_data};

        Filters.prototype.apply_filters(data);

    } else if (sel_val === 'deselect_all') {
        $('input.pros_ins').prop('checked', false);
        action_btn.addClass("d-none");
        $(".select-option-btn-results").text('0 Selected Records');

    }
};
var removeByAttr = function (arr, attr, value) {
    var i = arr.length;
    while (i--) {
        if (arr[i]
            && arr[i].hasOwnProperty(attr)
            && (arguments.length > 2 && arr[i][attr] === value)) {

            arr.splice(i, 1);

        }
    }
    return arr;
};

Filters_Action.prototype.select_action_handler = function () {
    var action = $(this).attr("action");

    var list_name = '';
    var tag_name = '';
    var list_act = '';
    var tag_act = '';


    if (action == "create_list") {
        if ($(this).attr("id") == "btn-save-new-list") {
            list_name = $("#input-new-list").val();
            list_act = 'new';
        } else if ($(this).attr("id") == "btn-save-list-old") {
            list_name = $(".selected-value").val();
            list_act = 'old';
        }
    } else if (action == "create_tag") {
        if ($(this).attr("id") == "btn-save-new-tag") {
            tag_name = $("#input-new-tag").val();
            tag_act = 'new';
        } else if ($(this).attr("id") == "btn-save-tag-old") {
            tag_name = $(".selected-value-tag").val();
            tag_act = 'old';
        }
    }

    var csrftoken = getCookie('csrftoken');
    var ids = [];
    let perform_by = $(".select-option-btn-results").attr('by');

    ids = Filters_Action.prototype.get_visible_ids();

    var json_ids = JSON.stringify(ids);

    let form_data = last_form_data.data;

    var obj1 = {'name': 'csrfmiddlewaretoken', 'value': csrftoken};
    var obj2 = {'name': 'perform_by', 'value': perform_by};
    var obj3 = {'name': 'table_action', 'value': action};
    var obj4 = {'name': 'visible_ids', 'value': json_ids};
    var obj5 = {'name': 'list_name', 'value': list_name};
    var obj6 = {'name': 'tag_name', 'value': tag_name};
    var obj7 = {'name': 'list_act', 'value': list_act};
    var obj8 = {'name': 'tag_act', 'value': tag_act};

    if (last_filter_status != 'save_filter') {

        removeByAttr(form_data, 'name', 'csrfmiddlewaretoken');
        removeByAttr(form_data, 'name', 'perform_by');
        removeByAttr(form_data, 'name', 'table_action');
        removeByAttr(form_data, 'name', 'visible_ids');
        removeByAttr(form_data, 'name', 'list_name');
        removeByAttr(form_data, 'name', 'tag_name');
        removeByAttr(form_data, 'name', 'list_act');
        removeByAttr(form_data, 'name', 'tag_act');

    }
    form_data.push(obj1);
    form_data.push(obj2);
    form_data.push(obj3);
    form_data.push(obj4);
    form_data.push(obj5);
    form_data.push(obj6);
    form_data.push(obj7);
    form_data.push(obj8);

    let data = {data: form_data};

    $.ajax({
        type: "POST",
        url: "perform_actions",
        data: data.data,
        success: function (response) { // on success..
            console.log(response["prospect"])
            if (action === 'export_to_excel') {
                window.location.href = "/media/filter_action_export_to_excel/prospect_data.xls"
            } else if (action === 'create_list') {
                $(".create-list-modal").modal('hide');
                $(".existing-list-modal").modal('hide');
                $(".bs-modal-list").modal('hide');
                $('#list1')
                    .append($("<option></option>")
                        .attr("value", response["list_id"])
                        .text(list_name));
                $('#list2')
                    .append($("<option></option>")
                        .attr("value", response["list_id"])
                        .text(list_name));

                $('.list-partial-select')
                    .append($("<option></option>")
                        .attr("value", response["list_id"])
                        .text(list_name));
                $('#list_count').val(parseInt($('#list_count').val()) + 1);


                toastr.success("List created successfully")


            } else if (action === 'create_tag') {

                $(".bs-modal-tag").modal('hide');
                $(".existing-tag-modal").modal('hide');
                $(".create-tag-modal").modal('hide');
                $('#tag1')
                    .append($("<option></option>")
                        .attr("value", response["tag_id"])
                        .text(tag_name));
                $('#tag2')
                    .append($("<option></option>")
                        .attr("value", response["tag_id"])
                        .text(tag_name));
                $('.tag-partial-select')
                    .append($("<option></option>")
                        .attr("value", response["tag_id"])
                        .text(tag_name));
                $('#tag_count').val(parseInt($('#tag_count').val()) + 1);
                toastr.success("Tag created successfully")

            } else if (action === 'delete') {
                toastr.success("Prospects deleted successfully")


            } else if (action === 'opt_out') {
                toastr.success("Prospects marked opt out")

            }
            // update table

            if (action !== 'export_to_excel') {
                console.log("init dt")
                console.log("init dt2")
                console.log("init dt3")
                var form_data1 = last_form_data.data;
                var obj = {'name': 'action', 'value': 'all'};
                form_data1.push(obj);
                Filters_Action.prototype.init_filters_datatable();
            }


        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            alert("in fail");
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
Filters_Action.prototype.get_visible_ids = function () {
    var get_prospect_ids = [];

    $('input.pros_ins:checked').each(function () {
        get_prospect_ids.push($(this).attr("cus_id"))
    });

    return get_prospect_ids
};


Filters_Action.prototype.set_result_count = function (count, action) {

    let count_span = $(".select-option-btn-results");
    count_span.text(count + " Selected Records");
    count_span.attr("by", action);
    if (count == 0) {
        var action_btn = $(".action-btn");
        action_btn.addClass("d-none");
    } else {
        var action_btn = $(".action-btn");
        action_btn.removeClass("d-none");
    }

};
Filters_Action.prototype.del_result_count = function () {
    let count_span = $(".select-option-btn-results");
    count_span.text('');
    count_span.attr("by", '');
    var action_btn = $(".action-btn");
    action_btn.addClass("d-none");
};


Filters_Action.prototype.init_filters_datatable = function () {
    Filters_Action.prototype.del_result_count();
    var csrftoken = getCookie('csrftoken');
    var type = (last_filter_status == "save_filter") ? "GET" : "POST";
    var url = (last_filter_status == "save_filter") ? "/filter/existing_filters" : "/filter/apply_filter";
    // var table = $("#filters-result-table").DataTable({
    //     lengthChange: false,
    //     bFilter: false,
    //     serverSide: true,
    //     processing: true,
    //     destroy: true,
    //     ajax: {
    //         "headers": {"X-CSRFToken": csrftoken},
    //         "type": type,
    //         "url": url,
    //         "data": function (d) {
    //
    //             if (last_filter_status != "save_filter") {
    //                 let k, selectKey = [], selectCon = [], selectVal = [], list1 = [], list2 = [], tag1 = [], tag2 = [];
    //                 $.each(last_form_data.data, function (key, val) {
    //                     switch (val.name) {
    //                         case "select-con":
    //                             selectCon.push(val.value);
    //                             d[val.name] = selectCon.toString();
    //                             break;
    //                         case "select-val":
    //                             selectVal.push(encodeURIComponent(val.value));
    //                             d[val.name] = selectVal.toString();
    //                             break;
    //                         case "select-key":
    //                             selectKey.push(encodeURIComponent(val.value));
    //                             d[val.name] = selectKey.toString();
    //                             break;
    //                         case "list1":
    //                             list1.push(val.value);
    //                             d[val.name] = list1.toString();
    //                             break;
    //                         case "list2":
    //                             list2.push(val.value);
    //                             d[val.name] = list2.toString();
    //                             break;
    //                         case "tag1":
    //                             tag1.push(val.value);
    //                             d[val.name] = tag1.toString();
    //                             break;
    //                         case "tag2":
    //                             tag2.push(val.value);
    //                             d[val.name] = tag2.toString();
    //                             break;
    //                         default:
    //                             d[val.name] = val.value;
    //                     }
    //                 });
    //             } else {
    //                 //$.extend( true, d, last_form_data );
    //                 d["filter_id"] = last_form_data["filter_id"]
    //
    //             }
    //         },
    //
    //         "dataSrc": function (d) {
    //             if ("applied_saved_form" in d) {
    //                 var form_array = [];
    //                 var list_total_count = d["list_count_total"];
    //                 var tag_count_total = d["tag_count_total"];
    //                 var elem_list_total = {'name': 'list-count-total', 'value': list_total_count};
    //                 form_array.push(elem_list_total)
    //                 var elem_tag_total = {'name': 'tag-count-total', 'value': tag_count_total};
    //                 form_array.push(elem_tag_total)
    //                 var applied_saved_form = JSON.parse(d["applied_saved_form"])
    //                 form_array = []
    //                 // var len = applied_saved_form[0]["fields"]["filter_name"];
    //                 var form_obj = applied_saved_form[0]["fields"];
    //                 var len = Object.keys(applied_saved_form[0]["fields"]).length;
    //                 var list_count_total_obj = {
    //                     'name': 'list-count-total',
    //                     'value': $("#list_count").val()
    //                 };
    //                 form_array.push(list_count_total_obj);
    //                 var tag_count_total_obj = {
    //                     'name': 'tag-count-total',
    //                     'value': $("#tag_count").val()
    //                 };
    //                 form_array.push(tag_count_total_obj);
    //                 for (var i = 0; i < len; i++) {
    //                     if ("search_query" in form_obj) {
    //                         var elem_obj = {
    //                             'name': 'search_query',
    //                             'value': (form_obj["search_query"] == null ? "" : form_obj["search_query"])
    //                         };
    //                         form_array.push(elem_obj)
    //                         delete form_obj["search_query"];
    //                     } else if ("lists_inc" in form_obj) {
    //                         if (form_obj["lists_inc"]) {
    //                             var list_inc_array = form_obj["lists_inc"].split(',');
    //                             for (i = 0; i < list_inc_array.length; i++) {
    //                                 var elem_obj = {'name': 'list1', 'value': list_inc_array[i]};
    //                                 form_array.push(elem_obj)
    //                             }
    //                         }
    //                         delete form_obj["lists_inc"];
    //                     } else if ("lists_exc" in form_obj) {
    //                         if (form_obj["lists_exc"]) {
    //                             var list_exc_array = form_obj["lists_exc"].split(',');
    //                             for (i = 0; i < list_exc_array.length; i++) {
    //                                 var elem_obj = {'name': 'list2', 'value': list_exc_array[i]};
    //                                 form_array.push(elem_obj)
    //                             }
    //                         }
    //                         delete form_obj["lists_exc"];
    //                     } else if ("tags_inc" in form_obj) {
    //                         if (form_obj["tags_inc"]) {
    //                             var tag_inc_array = form_obj["tags_inc"].split(',');
    //                             for (i = 0; i < tag_inc_array.length; i++) {
    //                                 var elem_obj = {'name': 'tag1', 'value': tag_inc_array[i]};
    //                                 form_array.push(elem_obj)
    //                             }
    //                         }
    //                         delete form_obj["tags_inc"];
    //                     } else if ("tags_exc" in form_obj) {
    //                         if (form_obj["tags_inc"]) {
    //                             var tag_exc_array = form_obj["tags_exc"].split(',');
    //                             for (i = 0; i < tag_exc_array.length; i++) {
    //                                 var elem_obj = {'name': 'tag2', 'value': tag_exc_array[i]};
    //                                 form_array.push(elem_obj)
    //                             }
    //                         }
    //                         delete form_obj["tags_exc"];
    //                     } else if ("list_count_sel" in form_obj) {
    //                         var elem_obj = {'name': 'list-count', 'value': form_obj["list_count_sel"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["list_count_sel"];
    //                     } else if ("tag_count_sel" in form_obj) {
    //                         var elem_obj = {'name': 'tag-count', 'value': form_obj["tag_count_sel"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["tag_count_sel"];
    //                     } else if ("list_inc_radio" in form_obj) {
    //                         var elem_obj = {'name': 'customRadio-list', 'value': form_obj["list_inc_radio"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["list_inc_radio"];
    //                     } else if ("tag_inc_radio" in form_obj) {
    //                         var elem_obj = {'name': 'customRadio-tag', 'value': form_obj["tag_inc_radio"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["tag_inc_radio"];
    //                     } else if ("absentee" in form_obj) {
    //                         var elem_obj = {'name': 'absentee', 'value': form_obj["absentee"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["absentee"];
    //                     } else if ("vacant" in form_obj) {
    //                         var elem_obj = {'name': 'vacant', 'value': form_obj["vacant"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["vacant"];
    //                     } else if ("skipped" in form_obj) {
    //                         var elem_obj = {'name': 'skipped', 'value': form_obj["skipped"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["skipped"];
    //                     }else if ("opt_out" in form_obj) {
    //                         var elem_obj = {'name': 'opt-out', 'value': form_obj["opt_out"]};
    //                         form_array.push(elem_obj);
    //                         delete form_obj["opt_out"];
    //                     } else if ("optional_field_filters_condition_and_or" in form_obj) {
    //                         var elem_obj = {
    //                             'name': 'options-filter-cond',
    //                             'value': form_obj["optional_field_filters_condition_and_or"]
    //                         };
    //                         form_array.push(elem_obj);
    //                         delete form_obj["optional_field_filters_condition_and_or"];
    //                     } else if ("optional_field_filters_select_key" in form_obj) {
    //                         var select_key_array = form_obj["optional_field_filters_select_key"].split(',');
    //                         for (i = 0; i < select_key_array.length; i++) {
    //                             var elem_obj = {
    //                                 'name': 'select-key',
    //                                 'value': form_obj["optional_field_filters_select_key"]
    //                             };
    //                             form_array.push(elem_obj)
    //                         }
    //                         delete form_obj["optional_field_filters_select_key"];
    //                     } else if ("optional_field_filters_select_con" in form_obj) {
    //                         var select_con_array = form_obj["optional_field_filters_select_con"].split(',');
    //                         for (i = 0; i < select_con_array.length; i++) {
    //                             var elem_obj = {
    //                                 'name': 'select-con',
    //                                 'value': form_obj["optional_field_filters_select_con"]
    //                             };
    //                             form_array.push(elem_obj)
    //                         }
    //                         delete form_obj["optional_field_filters_select_con"];
    //                     } else if ("optional_field_filters_select_val" in form_obj) {
    //                         var select_val_array = form_obj["optional_field_filters_select_val"].split(',');
    //                         for (i = 0; i < select_val_array.length; i++) {
    //                             var elem_obj = {
    //                                 'name': 'select-val',
    //                                 'value': form_obj["optional_field_filters_select_val"]
    //                             };
    //                             form_array.push(elem_obj)
    //                         }
    //                         delete form_obj["optional_field_filters_select_val"];
    //                     }
    //
    //                 }
    //                 last_form_data.data = form_array;
    //                 last_filter_status = "save_filter"
    //
    //             }
    //             return d["data"];
    //         },
    //     },
    //
    //     columns: [
    //         {"defaultContent": '<div class="custom-control custom-checkbox mb-2"><input type="checkbox" class="custom-control-input pros_ins" /><label class="custom-control-label"> </label></div>'},
    //         {"data": "fullname"},
    //         {"data": "mailingaddress"},
    //         {"data": "propertyaddress"},
    //         {"data": "list_count"},
    //         {"data": "tag_count"},
    //         {"defaultContent": '<a style="text-decoration: underline; color: blue" href="#" data-toggle="modal" id="show-seq" data-target="#sequence-model">Show Sequences</a>'},
    //         {
    //             "defaultContent": '<div class=" btn-group-sm" role="group" aria-label="action btns"> ' +
    //                 '<button type="button" class="btn btn-secondary btn-sm view_details" data-toggle="modal" data-placement="top" title="" data-original-title="Update"><i class="mdi mdi-pencil-box-outline"></i></button> ' +
    //                 '<button type="button" class="btn btn-info btn-sm update_prospect left_button_margin_js" data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit"><i class="mdi mdi-grease-pencil"></i></button>' +
    //                 '<button type="button" class="btn btn-danger btn-sm delete_prospect" data-toggle="modal"><i class="mdi mdi-trash-can-outline"></i></button></div>'
    //         },
    //
    //     ],
    //     columnDefs: [{
    //         targets: 0,
    //         createdCell: function (td, cellData, rowData, row, col) {
    //             var input = $(td).find("input[type=checkbox]");
    //             input.attr("cus_id", rowData["id"]);
    //             input.attr("id", 'customCheck' + rowData["id"]);
    //             var label = $(td).find("label");
    //             label.attr("for", 'customCheck' + rowData["id"]);
    //         }
    //     }, {
    //         targets: 1,
    //         createdCell: function (td, cellData, rowData, row, col) {
    //             if (cellData == null) {
    //                 $(td).text("N/A")
    //             }
    //             var text = $(td).text();
    //             var htmlStr = '<a href="javascript:void(0);" >' + text + '</a>';
    //             $(td).html(htmlStr);
    //             var title_anc = $(td).find('a');
    //             title_anc.attr("mydata", rowData["id"]);
    //             title_anc.addClass("btn-link view_details");
    //         }
    //     }, {
    //         targets: 2,
    //         createdCell: function (td, cellData, rowData, row, col) {
    //             if (cellData == null) {
    //                 $(td).text("empty")
    //             }
    //
    //         }
    //     }, {
    //         targets: 6,
    //         createdCell: function (td, cellData, rowData, row, col) {
    //             if (cellData == null) {
    //                 $(td).text("empty")
    //             }
    //             var title_anc = $(td).find('a');
    //             title_anc.attr("mydata", rowData["id"]);
    //         }
    //     }, {
    //         targets: 7,
    //         createdCell: function (td, cellData, rowData, row, col) {
    //             var btn1 = $(td).find(".view_details");
    //             btn1.attr("mydata", rowData["id"]);
    //             var btn2 = $(td).find(".update_prospect");
    //             btn2.attr("mydata", rowData["id"]);
    //             var btn3 = $(td).find(".delete_prospect");
    //             btn3.attr("mydata", rowData["id"]);
    //             btn3.attr("data-target", "#exampleModal" + rowData["id"])
    //
    //         }
    //     }
    //     ],
    //
    // });

    // $("#filters-result-table").on('page.dt', function () {
    //     Filters_Action.prototype.del_result_count();
    //     if (last_filter_status == "count") {
    //         removeByAttr(last_form_data.data, 'name', 'action');
    //         var obj = {'name': 'action', 'value': 'all'};
    //         last_form_data.data.push(obj);
    //
    //     }
    // });

};
Filters_Action.prototype.show_seq = function () {
    var id = $(this).attr("mydata");
    $.ajax({
        type: "GET",
        url: "get_sequences",
        data: {"id": id},
        success: function (response) { // on success..
            console.log(response)
            seq_array = response["sequences"];
            var ul = "<ul></ul>"
            if (seq_array.length>0) {
                $(".seq_modal_body").empty();
                seq_array.forEach(function (item, index) {
                    var li = "<li>" + item + "</li>";
                    $(".seq_modal_body").append(li)

                })
                // $(".seq_modal_body").html(ul)
            } else {

                $(".seq_modal_body").empty();
                $(".seq_modal_body").append('<h6>No sequence exists.</h6>');

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