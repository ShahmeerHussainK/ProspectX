function Tasks(conf) {

    this.options = conf;

    // Chain constructor with call
    Prospectx.call(this, this.options);

}

Tasks.prototype.init = function () {
    let self = this;

    // events
    $("#tasksModal").on("hidden.bs.modal", function () {
        document.getElementById("create_task_form").reset();
        $("#error_div").removeClass("d-block");
        $("#error_div").addClass("d-none");
        $("#success_div").removeClass("d-block");
        $("#success_div").addClass("d-none");

    });

    $("#updatetasksModal").on("hidden.bs.modal", function () {
        document.getElementById("update_task_form").reset();
        $("#update_error_div").removeClass("d-block");
        $("#update_error_div").addClass("d-none");
        $("#update_success_div").removeClass("d-block");
        $("#update_success_div").addClass("d-none");

    });

    // Create Task
    $('#tasksModal').on('submit', '#create_task_form', function () {


        var start_date = $(this).find("input[name=start_date_time]");
        var sd_initial = start_date.val();
        var date = new Date(start_date.val());
        var offsetMiliseconds = date.getTimezoneOffset() * 60000;
        var dateTimePicker = new Date(date.getTime() + offsetMiliseconds);
        var ampm = dateTimePicker.getHours() >= 12 ? 'PM' : 'AM';
        var datestring = (dateTimePicker.getMonth() + 1) + "/" + dateTimePicker.getDate() + "/" + dateTimePicker.getFullYear() + " " +
            getHour(dateTimePicker.getHours()) + ":" + getMinute(dateTimePicker.getMinutes()) + " " + ampm;
        start_date.val(datestring);


        var end_date = $(this).find("input[name=end_date_time]");
        var ed_initial = end_date.val();
        var date2 = new Date(end_date.val());
        var offsetMiliseconds2 = date2.getTimezoneOffset() * 60000;
        var dateTimePicker2 = new Date(date2.getTime() + offsetMiliseconds2);
        var ampm2 = dateTimePicker2.getHours() >= 12 ? 'PM' : 'AM';
        var datestring2 = (dateTimePicker2.getMonth() + 1) + "/" + dateTimePicker2.getDate() + "/" + dateTimePicker2.getFullYear() + " " +
            getHour(dateTimePicker2.getHours()) + ":" + getMinute(dateTimePicker2.getMinutes()) + " " + ampm2;
        end_date.val(datestring2);

        let data = {type: $(this).attr('method'), url: $(this).attr('action'), data: $(this).serialize()};
        self.create_task(data, sd_initial, ed_initial);

        return false;
    });

    // Update Task
    $('#updatetasksModal').on('submit', '#update_task_form', function () {

        var start_date = $(this).find("input[name=start_date_time]");
        var sd_initial = start_date.val();
        var date = new Date(start_date.val());
        var offsetMiliseconds = date.getTimezoneOffset() * 60000;
        var dateTimePicker = new Date(date.getTime() + offsetMiliseconds);
        var ampm = dateTimePicker.getHours() >= 12 ? 'PM' : 'AM';
        var datestring = (dateTimePicker.getMonth() + 1) + "/" + dateTimePicker.getDate() + "/" + dateTimePicker.getFullYear() + " " +
            getHour(dateTimePicker.getHours()) + ":" + getMinute(dateTimePicker.getMinutes()) + " " + ampm;
        start_date.val(datestring);

        var end_date = $(this).find("input[name=end_date_time]");
        var ed_initial = end_date.val();
        var date2 = new Date(end_date.val());
        var offsetMiliseconds2 = date2.getTimezoneOffset() * 60000;
        var dateTimePicker2 = new Date(date2.getTime() + offsetMiliseconds2);
        var ampm2 = dateTimePicker2.getHours() >= 12 ? 'PM' : 'AM';
        var datestring2 = (dateTimePicker2.getMonth() + 1) + "/" + dateTimePicker2.getDate() + "/" + dateTimePicker2.getFullYear() + " " +
            getHour(dateTimePicker2.getHours()) + ":" + getMinute(dateTimePicker2.getMinutes()) + " " + ampm2;
        end_date.val(datestring2);

        let data = {type: $(this).attr('method'), url: $(this).attr('action'), data: $(this).serialize()};
        self.update_task(data, sd_initial, ed_initial);

        return false;
    });

    // Link Task
    $('#savelinkModal').on('submit', '#link_save_task_form', function () {

        var start_date = $(this).find("input[name=start_date_time]");
        var sd_initial = start_date.val();
        var date = new Date(start_date.val());
        var offsetMiliseconds = date.getTimezoneOffset() * 60000;
        var dateTimePicker = new Date(date.getTime() + offsetMiliseconds);
        var ampm = dateTimePicker.getHours() >= 12 ? 'PM' : 'AM';
        var datestring = (dateTimePicker.getMonth() + 1) + "/" + dateTimePicker.getDate() + "/" + dateTimePicker.getFullYear() + " " +
            getHour(dateTimePicker.getHours()) + ":" + getMinute(dateTimePicker.getMinutes()) + " " + ampm;
        start_date.val(datestring);

        var end_date = $(this).find("input[name=end_date_time]");
        var ed_initial = end_date.val();
        var date2 = new Date(end_date.val());
        var offsetMiliseconds2 = date2.getTimezoneOffset() * 60000;
        var dateTimePicker2 = new Date(date2.getTime() + offsetMiliseconds2);
        var ampm2 = dateTimePicker2.getHours() >= 12 ? 'PM' : 'AM';
        var datestring2 = (dateTimePicker2.getMonth() + 1) + "/" + dateTimePicker2.getDate() + "/" + dateTimePicker2.getFullYear() + " " +
            getHour(dateTimePicker2.getHours()) + ":" + getMinute(dateTimePicker2.getMinutes()) + " " + ampm2;
        end_date.val(datestring2);

        let data = {type: $(this).attr('method'), url: $(this).attr('action'), data: $(this).serialize()};
        self.link_task(data, sd_initial, ed_initial);

        return false;
    });
};


function getMinute(min) {
    if(min === 0){
        return "00";
    }else if(min === 1)
    {
        return "01";
    }else if(min === 2)
    {
        return "02";
    }else if(min === 3)
    {
        return "03";
    }else if(min === 4)
    {
        return "04";
    }else if(min === 5)
    {
        return "05";
    }else if(min === 6)
    {
        return "06";
    }else if(min === 7)
    {
        return "07";
    }else if(min === 8)
    {
        return "08";
    }else if(min === 9)
    {
        return "09";
    }else{
        return min;
    }
}


function getHour(hour){

    if (hour === 13)
    {
        return 1;
    }else if (hour === 14)
    {
        return 2;
    }else if (hour === 15)
    {
        return 3;
    }else if (hour === 16)
    {
        return 4;
    }else if (hour === 17)
    {
        return 5;
    }else if (hour === 18)
    {
        return 6;
    }else if (hour === 19)
    {
        return 7;
    }else if (hour === 20)
    {
        return 8;
    }else if (hour === 21)
    {
        return 9;
    }else if (hour === 22)
    {
        return 10;
    }else if (hour === 23)
    {
        return 11;
    }else if (hour === 0)
    {
        return 12;
    }else{
        return hour;
    }
}

function myFunction() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () {
        x.className = x.className.replace("show", "");
    }, 3000);
}

Tasks.prototype.create_task = function (data, sd_initial, ed_initial) {
    $('#create_task_button').attr('disabled', true);

    $.ajax({
        type: data.type,
        url: data.url,
        data: data.data,
        success: function (data) { // on success..
            $('#tasksModal').modal('hide');
            document.getElementById("create_task_form").reset();
            $('#assign_to_create').prop('selectedIndex', 0);
            toastr.success("Task Created Successfully!");
            $('#create_task_button').attr('disabled', false);

            if ($("#calendar_view").is(":visible")) {
                _calendar.fullCalendar('refetchEvents');
            } else {
                prospectxList.prototype.list_view_clicked("all");
            }

        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            $('#create_task_button').attr('disabled', false);
            var err = JSON.parse(xhr.responseText);
            $("#tasksModal").find("input[name=start_date_time]").val(sd_initial);
            $("#tasksModal").find("input[name=end_date_time]").val(ed_initial);

            if (err.message === "There is some error!")
                toastr.error(err.message);

            else {
                $.each(err.task_form, function (key, value) {
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


Tasks.prototype.update_task = function (data, sd_initial, ed_initial) {
    $('#update_task_button').attr('disabled', true);

    $.ajax({
        type: data.type,
        url: data.url,
        data: data.data,
        success: function () { // on success..
            document.getElementById("update_task_form").reset();
            $('#updatetasksModal').modal('hide');
            toastr.success("Task Updated Successfully!");

            $('#update_task_button').attr('disabled', false);

            if ($("#calendar_view").is(":visible")) {
                _calendar.fullCalendar('refetchEvents');
            } else {
                prospectxList.prototype.list_view_clicked("all");
            }


        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            $('#update_task_button').attr('disabled', false);

            $("#updatetasksModal").find("input[name=start_date_time]").val(sd_initial);
            $("#updatetasksModal").find("input[name=end_date_time]").val(ed_initial);
            var err = JSON.parse(xhr.responseText);
            if (err.message === "There is some error!")
                toastr.error(err.message);

            else {
                $.each(err.task_form, function (key, value) {
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


Tasks.prototype.link_task = function (data, sd_initial, ed_initial) {
    $('#link_task_button').attr('disabled', true);

    $.ajax({
        type: data.type,
        url: data.url,
        data: data.data,
        success: function (data) { // on success..
            document.getElementById("link_save_task_form").reset();
            $('#savelinkModal').modal('hide');
            toastr.success("Task Saved Successfully!");

            $('#link_task_button').attr('disabled', false);


            _calendar.fullCalendar('refetchEvents');
            calendar.fullCalendar('refetchEvents');
        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            $('#link_task_button').attr('disabled', false);
            var err = JSON.parse(xhr.responseText);
            $("#savelinkModal").find("input[name=start_date_time]").val(sd_initial);
            $("#savelinkModal").find("input[name=end_date_time]").val(ed_initial);
            if (err.message === "There is some error!")
                toastr.error(err.message);
            else {
                $.each(err.task_form, function (key, value) {
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