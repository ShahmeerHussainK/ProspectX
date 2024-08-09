function Xsite_Dashboard(conf) {

    this.options = conf;

    // Chain constructor with call

    Prospectx.call(this, this.options);
}

Xsite_Dashboard.prototype.init = function () {
    let self = this;

    Xsite_Dashboard.prototype.init_Datatable();

};

Xsite_Dashboard.prototype.toast = function () {
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

Xsite_Dashboard.prototype.change_lead_status = function (data) {
    toastr.error("here");
    $.ajax({
        type: data.type,
        url: data.url,
        success: function (data) { // on success..

            toastr.success(data.message);
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

};


Xsite_Dashboard.prototype.init_Datatable = function () {
    if (audience_type === "Buyer") {
        Xsite_Dashboard.prototype.get_buyer_site_data();
    } else {
        Xsite_Dashboard.prototype.get_seller_site_data();
    }
};


function jsfunction(id) {
    var x = document.getElementById(id).value;

    $.ajax({
        type: "GET",
        url: "/xsite/change_lead_status/" + id + "/" + x + "/",
        success: function (data) { // on success..
            $("#datatable-leads").dataTable().fnDestroy();
            $("#datatable-leads-won").dataTable().fnDestroy();
            $("#datatable-leads-dead").dataTable().fnDestroy();
            Xsite_Dashboard.prototype.init_Datatable();
            $("#open-leads").html(data['other']);
            $("#won-leads").html(data['won']);
            $("#dead-leads").html(data['dead']);
            toastr.success(data.message);
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
}

function mark_read(id) {
    $.ajax({
        type: "GET",
        url: "/xsite/change_read_status/" + id + "/",
        success: function (data) { // on success..
            $("#datatable-leads").dataTable().fnDestroy();
            $("#datatable-leads-won").dataTable().fnDestroy();
            $("#datatable-leads-dead").dataTable().fnDestroy();
            Xsite_Dashboard.prototype.init_Datatable();
            $("#open-leads").html(data['other']);
            $("#won-leads").html(data['won']);
            $("#dead-leads").html(data['dead']);
            toastr.success(data.message);
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
}


Xsite_Dashboard.prototype.get_buyer_site_data = function () {
    $('#datatable-leads').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    // status = row['lead']['status'].status_name;
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    address = "-";
                    city = "-";
                    state = "-";
                    return "<strong>" + address + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + city + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + state + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<p class=\"m-0 text-muted\"> What are you looking for? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row['what_are_you_looking_for'].option_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });

    $('#datatable-leads-won').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads_won/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    // status = row['lead']['status'].status_name;
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    address = "-";
                    city = "-";
                    state = "-";
                    return "<strong>" + address + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + city + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + state + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<p class=\"m-0 text-muted\"> What are you looking for? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row['what_are_you_looking_for'].option_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });

    $('#datatable-leads-dead').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads_dead/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    // status = row['lead']['status'].status_name;
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    address = "-";
                    city = "-";
                    state = "-";
                    return "<strong>" + address + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + city + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + state + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<p class=\"m-0 text-muted\"> What are you looking for? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row['what_are_you_looking_for'].option_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });
};

Xsite_Dashboard.prototype.get_seller_site_data = function () {
    $('#datatable-leads').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row.street_address) {
                        address = row.street_address
                    } else {
                        address = "-"
                    }

                    if (row.city) {
                        city = row.city
                    } else {
                        city = "-"
                    }

                    if (row.state) {
                        state = row.state
                    } else {
                        state = "-"
                    }
                    if (row.zip) {
                        zip = row.zip
                    } else {
                        zip = "-"
                    }
                    return "<strong>" + address + ", " + city + " </strong>\n" +
                        "<p class=\"m-0 text-muted\">" + state + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + zip + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row['is_home_listed']) {
                        listing_name = row['is_home_listed'].listing_name
                    } else {
                        listing_name = "-"
                    }
                    if (row.asking_price) {
                        price = row.asking_price
                    } else {
                        price = "-"
                    }
                    return "<span class=\"m-0 text-muted\"> Asking Price: </span><strong> $" + price + "</strong> \n" +
                        "<p class=\"m-0 text-muted\"> Is Home Listed? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + listing_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });

    $('#datatable-leads-won').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads_won/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row.street_address) {
                        address = row.street_address
                    } else {
                        address = "-"
                    }

                    if (row.city) {
                        city = row.city
                    } else {
                        city = "-"
                    }

                    if (row.state) {
                        state = row.state
                    } else {
                        state = "-"
                    }
                    if (row.zip) {
                        zip = row.zip
                    } else {
                        zip = "-"
                    }
                    return "<strong>" + address + ", " + city + " </strong>\n" +
                        "<p class=\"m-0 text-muted\">" + state + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + zip + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row['is_home_listed']) {
                        listing_name = row['is_home_listed'].listing_name
                    } else {
                        listing_name = "-"
                    }
                    if (row.asking_price) {
                        price = row.asking_price
                    } else {
                        price = "-"
                    }
                    return "<span class=\"m-0 text-muted\"> Asking Price: </span><strong> $" + price + "</strong> \n" +
                        "<p class=\"m-0 text-muted\"> Is Home Listed? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + listing_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });

    $('#datatable-leads-dead').DataTable({
        "serverSide": true,
        "processing": true,
        "ajax": "/xsite/get_leads_dead/" + site + "/",
        aoColumns: [
            {
                mData: null,
                mRender: function (data, type, row) {
                    status = row['status'].status_name;
                    if (status === "New") {
                        status_new = "<option selected=\"\" value=\"New\">New</option>\n";
                    } else {
                        status_new = "<option value=\"New\">New</option>\n";
                    }
                    if (status === "Follow Up") {
                        status_follow_up = "<option selected=\"\" value=\"Follow Up\">Follow Up</option>\n";
                    } else {
                        status_follow_up = "<option value=\"Follow Up\">Follow Up</option>\n";
                    }
                    if (status === "Pending") {
                        status_pending = "<option selected=\"\" value=\"Pending\">Pending</option>\n";
                    } else {
                        status_pending = "<option value=\"Pending\">Pending</option>\n";
                    }
                    if (status === "Won") {
                        status_won = "<option selected=\"\" value=\"Won\">Won</option>\n";
                    } else {
                        status_won = "<option value=\"Won\">Won</option>\n";
                    }
                    if (status === "Dead") {
                        status_dead = "<option selected=\"\" value=\"Dead\">Dead</option>\n";
                    } else {
                        status_dead = "<option value=\"Dead\">Dead</option>\n";
                    }
                    if (row.is_marked_read) {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Mark Unread</a>"
                    } else {
                        is_marked_read = "<a href=\"javascript:mark_read(" + row.id + ")\">Unread</a>"
                    }
                    return "<select id=\"" + row.id + "\" class=\"custom-select\" onchange=\"jsfunction(" + row.id + ")\"> \n" +
                        status_new +
                        status_pending +
                        status_follow_up +
                        status_won +
                        status_dead +
                        "</select>\n" +
                        "<div class=\"readAction text-center\">" +
                        is_marked_read +
                        "</div>\n";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    return "<strong>" + row.fullname + "</strong>\n" +
                        "<p class=\"m-0 text-muted\">" + row.phone + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + row.email + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row.street_address) {
                        address = row.street_address
                    } else {
                        address = "-"
                    }

                    if (row.city) {
                        city = row.city
                    } else {
                        city = "-"
                    }

                    if (row.state) {
                        state = row.state
                    } else {
                        state = "-"
                    }
                    if (row.zip) {
                        zip = row.zip
                    } else {
                        zip = "-"
                    }
                    return "<strong>" + address + ", " + city + " </strong>\n" +
                        "<p class=\"m-0 text-muted\">" + state + "</p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + zip + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },
            {
                mData: null,
                mRender: function (data, type, row) {
                    if (row['is_home_listed']) {
                        listing_name = row['is_home_listed'].listing_name
                    } else {
                        listing_name = "-"
                    }
                    if (row.asking_price) {
                        price = row.asking_price
                    } else {
                        price = "-"
                    }
                    return "<span class=\"m-0 text-muted\"> Asking Price: </span><strong> $" + price + "</strong> \n" +
                        "<p class=\"m-0 text-muted\"> Is Home Listed? </p>\n" +
                        "<div>\n" +
                        "<span class=\"text-primary\">\n" +
                        "<strong>" + listing_name + "</strong>\n" +
                        "</span>\n" +
                        "</div>";
                }
            },

        ],
    });
};

