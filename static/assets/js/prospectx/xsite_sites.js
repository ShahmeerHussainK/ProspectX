function Sites(conf) {
    this.options = conf;

    // Chain constructor with call
    Prospectx.call(this, this.options);
}

Sites.prototype.init = function () {
    let self = this;

    Sites.prototype.toast();
    Sites.prototype.btn_clicks();

    $(document).on('show.bs.modal', '.modal', function (event) {
        var zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function () {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });

    $(document).ready(function () {
        if (allow_sites === "False") {
            $("#force_delete").modal({
                backdrop: 'static',
                keyboard: false
            });
            $('#force_delete').modal('show');
        } else {
            $('#force_delete').modal('hide');
        }
    });

};


function DisplayMessage() {
    toastr.info("You are not allowed to create more than three websites.");
}

Sites.prototype.toast = function () {
    if (msg === "Site deleted successfully!") {
        toastr.success(msg);
    } else if (msg === "Site does not exist!") {
        toastr.info(msg);
    } else if (msg === "There was an error!") {
        toastr.error(msg);
    } else if (msg === "Site content updated successfully!") {
        toastr.success(msg);
    } else if (msg === "Site Added Successfully!") {
        toastr.success(msg);
    } else if (msg) {
        toastr.info(msg);
    }


};

Sites.prototype.btn_clicks = function () {
    $(document).on('click', '.deletebtn', function () {
        var site = $(this).attr("mydata");
        var link = "window.location.href='" + '/xsite/delete/' + site + '/' + "'";
        $('#btn_delete_site').attr("onClick", link);
        $('#deleteWebsiteModal').modal('show');
    });


    $(document).on('click', '.deletebtnajax', function () {
        var site = $(this).attr("mydata");
        $('#btn_delete_site_ajax').attr("mydata", site);
        $('#deleteWebsiteModalAjax').modal('show');
    });

    $(document).on('click', '.btn_delete_site_ajax', function (e) {
        var site = $(this).attr("mydata");
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/xsite/delete_ajax/" + site + "/",
            success: function (data) { // on success..
                toastr.success(data['message']);
                $('#deleteWebsiteModalAjax').modal('hide');
                console.log(data['site_count']);
                if (data['site_count'] === 1) {
                    $('#force_delete').modal('hide');
                    location.reload();
                } else {
                    var websites = data['websites'];
                    tableBody = $(".domain_data");
                    tableBody.empty();
                    websites.forEach(function (item, index) {
                        if (item !== null) {
                            markup = "<tr>\n" +
                                "                                                                                        <td>" + item['domain'] + "</td>\n" +
                                "                                                                                        <td>\n" +
                                "                                                                                            <button mydata=\"" + item['id'] + "\"\n" +
                                "                                                                                                    class=\"btn btn-danger btn-sm shadow-sm deletebtnajax\"><i\n" +
                                "                                                                                                    class=\"mdi mdi-trash-can-outline\"></i></button>\n" +
                                "                                                                                        </td>\n" +
                                "                                                                                    </tr>";
                            tableBody.append(markup);
                        }
                    });
                }

            },
            error: function (xhr, ajaxOptions, thrownError) { // on error..

                let err = JSON.parse(xhr.responseText);
                console.log(err.message);
                if(err.message === "There was an error!"){
                    toastr.error(err.message);
                }
                else{
                    toastr.info(err.message);
                }
            },
            statusCode: {
                404: function () {
                    alert("page not found");
                }
            }
        });
    });

    $(document).on('click', '.email_popup_btn', function () {
        var site = $(this).attr("mydata");
        $.ajax({
            type: "GET",
            url: "/xsite/get_mail_data/" + site + "/",
            success: function (data) { // on success..
                var mail_content = data['mail'];
                $('#email_from').val(mail_content.from_email);
                $('#email_subject').val(mail_content.subject);
                $('#email_detail').val(mail_content.content);
                var url = "/xsite/save_mail/" + site + "/";
                $('#mail_form').attr("action", url);
                $('#email_popup_modal').modal('show');

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
    });

    $('#email_popup_modal').on('submit', '#mail_form', function (e) {
        e.preventDefault();
        let data = {type: $(this).attr('method'), url: $(this).attr('action'), data: $(this).serialize()};
        Sites.prototype.save_mail(data);

        return false;
    });
};

Sites.prototype.save_mail = function (data) {
    $.ajax({
        type: data.type,
        url: data.url,
        data: data.data,
        success: function (data) { // on success..
            $('#email_popup_modal').modal('hide');
            toastr.success(data.message);
        },
        error: function (xhr, ajaxOptions, thrownError) { // on error..
            var err = JSON.parse(xhr.responseText);
            if (err.message === "There is some error!")
                toastr.error(err.message);
            else {
                $.each(err.mail_form, function (key, value) {
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

