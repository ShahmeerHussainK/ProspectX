function Prospectx(options) {

    var self = this;

    this.options = options;

    this.init();

    // Events
    $(document).on('click', '#back_to_admin', function (e) {
        e.preventDefault();
        Prospectx.prototype.back_to_admin();
    });

    $(document).on('click', '#logout', function (e) {
        // alert("here");
        e.preventDefault();
        Prospectx.prototype.logout();
    });
}

Prospectx.prototype.init = function () {

    var user_id = localStorage.getItem("user_id");
    this.stream_connection(user_id);

    this.is_superuser();
    this.is_admin_user();


};

Prospectx.prototype.stream_connection = function (user_id) {


};
// Prospectx.prototype.up_over_tasks = function() {
//     let url = '/task/upcoming_overdue_task/';
//
//     if($(this).text().trim()=="List View"){
//
//     }
//     $.ajax({
//         type: 'GET',
//         url: url,
//         success: function (data) {
//             console.log("in sucses")
//             console.log(data)
//             prospectxList.prototype.create_sidebar(data)
//             prospectxList.prototype.create_task_table(data["tasks"], data["subusers"])
//
//         },
//         error: function (xhr, ajaxOptions, thrownError) { // on error..
//             alert("error")
//         },
//         statusCode: {
//             404: function () {
//                 alert("page not found");
//             }
//         }
//     });
//
// }
Prospectx.prototype.is_superuser = function () {
    let role = localStorage.getItem("user_role");
    if (role === 'Super User') {
        // $("#back_to_admin").show();
        $("#back_to_admin").css('display', 'block');
    } else {
        // $("#back_to_admin").hide();
        $("#back_to_admin").css('display', 'none');
    }
};

Prospectx.prototype.is_admin_user = function () {
    let role = localStorage.getItem("role");
    if (role === 'Admin User') {
        $("#payment4").show();
        $("#users4").show();
        $("#affiliate4").show();
    } else {
        $("#payment4").hide();
        $("#users4").hide();
        $("#affiliate4").hide();
    }
};

Prospectx.prototype.back_to_admin = function () {
    window.location.href = "/user/login/" + localStorage.getItem("user_id");
    // localStorage.removeItem("user_id");
    // localStorage.removeItem("role");
    localStorage.removeItem("user_role");
};

Prospectx.prototype.logout = function () {
    localStorage.removeItem("role");
    localStorage.removeItem("image_name");
    localStorage.removeItem("user_id");
    window.location.href = "/logout"
};
Prospectx.prototype.getFormattedDate = function (dateStr, format) {
    var date = new Date(dateStr),
        fullYear = date.getFullYear(),
        year = fullYear.toString().substr(2, 2),
        month = date.getMonth(),
        monthDigits = (month < 9) ? '0' + (month + 1) : (month + 1),
        monthShortName = this.monthNames[month],
        day = (date.getDate() < 10) ? '0' + date.getDate() : date.getDate(),
        formattedDate;

    switch (format) {
        case 'M d, yy':
            formattedDate = monthShortName + ' ' + day + ', ' + fullYear;
            formattedDate = monthShortName + ' ' + day + ', ' + fullYear;
            break;
        case 'ddMy':
            formattedDate = day + monthShortName + year;
            break;
        case 'yy-mm-dd':
            formattedDate = fullYear + '-' + monthDigits + '-' + day;
            break;
        case 'dd-mm-yy':
            formattedDate = day + '-' + monthDigits + '-' + fullYear;
            break;
        case 'dd-M':
            formattedDate = day + '-' + monthShortName;
            break;
        default://dd-M-yy
            formattedDate = day + '-' + monthShortName + '-' + fullYear;
            break;
        case 'mm/dd/yy':
            formattedDate = day + '-' + monthShortName;
            alert(formattedDate)
            break;
    }

    return formattedDate;
};

