function Event_Stream(conf2) {

    this.options = conf2;

    // Chain constructor with call
    Prospectx.call(this, this.options);

}

Event_Stream.prototype.init = function () {
    let self = this;

    // Event_Stream.prototype.Get_Pills_from_localstorage();
    var uri = '/events/' + facility_name + '/' + user_id;
    console.log(uri);
    const es = new ReconnectingEventSource(uri);
    Event_Stream.prototype.Event_stream_listeners(es);
};


Event_Stream.prototype.Get_Pills_from_localstorage = function () {
    if (localStorage.getItem(user_id + "_task_pill")) {
        $("#task_pill").html(localStorage.getItem(user_id + "_task_pill"));
    }
    if (localStorage.getItem(user_id + "_notification_pill")) {
        $("#notification_pill").html(localStorage.getItem(user_id + "_notification_pill"));
    }
};

Event_Stream.prototype.Event_stream_listeners = function (es) {

    function GetMonthName(monthNumber) {
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      return months[monthNumber - 1];
}

    es.onopen = function () {
        console.log('connected3333');
    };

    es.onerror = function () {
        console.log('connection error');
    };

    es.addEventListener('stream-reset', function (e) {
        console.log("in stream reset");
        e = JSON.parse(e.data);
        console.log('stream reset: ' + JSON.stringify(e.channels));
    }, false);

    es.addEventListener('stream-error', function (e) {
        console.log("in stream error");
        // hard stop
        es.close();
        e = JSON.parse(e.data);
        console.log('stream error: ' + e.condition + ': ' + e.text);
    }, false);

    es.addEventListener('message', function (e) {
        console.log("in message");
        console.log(e.data);
        console.log(user_id);
        if (e.data === '"logout"') {
            console.log("in logout");
            es.close();
        }
        else if (e.data === '"Task"') {
            console.log("in Task")
            let task_pill = $("#task_pill").text();
            task_pill = parseInt(task_pill) + 1;
            $("#task_pill").html(task_pill);
        } else{
            let pill = $("#notification_pill").text();
            pill = parseInt(pill) + 1;
            $("#notification_pill").html(pill);
            var numItems = $('.notify-item').length;
            console.log(numItems);
            if(numItems === 6) {
                $('.notifications').find('a').last().remove();
            }
            console.log("i am" +user_id );

            var msg = e.data.replace(/\"/g, "");

            var d = new Date();

            var month = d.getMonth()+1;
            var day = d.getDate();
            var output =
                ((''+month).length<2 ? '0' : '') + GetMonthName(month) + '. ' +
                ((''+day).length<2 ? '0' : '') + day + ', ' +
                d.getFullYear();
            var markup =
                "                        <a href=\"/notification/notification_list\" class=\"dropdown-item notify-item\">\n" +
                "                            <div class=\"notify-icon bg-danger\"><i class=\"mdi mdi-message-text-outline\"></i>\n" +
                "                            </div>\n" +
                "                            <p class=\"notify-details\">"+ msg +"<span class=\"text-muted\">Date:" +
                "                                        "+ output +"</span></p>\n" +
                "                        </a>\n";

            $(".notifications").prepend(markup);

            // localStorage.setItem(user_id + "_notification_pill", pill);
        }
    }, false);
};
