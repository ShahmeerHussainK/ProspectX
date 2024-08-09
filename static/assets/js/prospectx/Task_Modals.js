function Task_Modals(conf2) {

    this.options = conf2;

    // Chain constructor with call
    Prospectx.call(this, this.options);

}

Task_Modals.prototype.init = function () {
    let self = this;

    $("#link_task").click(function () {
        var copyText = document.getElementById("hidden_link");
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        document.execCommand("copy");
        toastr.success("Link Copied Successfully");
    });


    $(function () {
        Task_Modals.prototype.modal_Calls();
    });
};

Task_Modals.prototype.modal_Calls = function () {
    $("#updatemodaldeletetask").click(function () {
        var id = $("#id").val();
        $.ajax({
            type: 'GET',
            url: "/task/delete_task/" + id + "/",
            success: function (data) { // on success..
                $('#updatedeleteModal').modal('hide');
                $('#updatetasksModal').modal('hide');
                toastr.success("Task Deleted Successfully");
                if ($("#calendar_view").is(":visible")) {
                    _calendar.fullCalendar('refetchEvents');
                } else {
                    prospectxList.prototype.list_view_clicked("all");
                }
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                var err = JSON.parse(xhr.responseText);
                toastr.error(err.message);
            },
            statusCode: {
                404: function () {
                    alert("page not found");
                }
            }
        });
    });

    $("#update_duplicate_task").click(function (e) {
        e.preventDefault();
        var id = $("#id").val();
        $.ajax({
            type: 'GET',
            url: "/task/duplicate_task/" + id + "/",
            success: function (data) { // on success..
                $('#updatetasksModal').modal('hide');
                toastr.success("Task Duplicated Successfully")
                if ($("#calendar_view").is(":visible")) {
                    _calendar.fullCalendar('refetchEvents');
                } else {
                    prospectxList.prototype.list_view_clicked("all");
                }
            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..
                var err = JSON.parse(xhr.responseText);
                toastr.error(err.message);
            },
            statusCode: {
                404: function () {
                    alert("page not found");
                }
            }
        });
    });

    $("#add_task").click(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: '/task/get_createtask_formsets',
            success: function (data) { // on success..
                $("#create_partial_formsets").html(data['html_form']);
                $('#link-formset').formset({
                    addText: 'Add Reminder',
                    deleteText: 'Remove Reminder'
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
    });
};