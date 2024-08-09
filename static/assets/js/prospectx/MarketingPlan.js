function MarketPlan(conf) {

    this.options = conf;
    this.rounds = 0;
    this.plans = {};

    this.plans_data = conf.plans_data.replace(/&#39;/g, '"');
    this.plans_data = JSON.parse(this.plans_data)

    this.plan_status = conf.plan_status.replace(/&#39;/g, '"');
    this.plan_status = JSON.parse(this.plan_status)

    this.campaign_gap = conf.campaign_gap.replace(/&#39;/g, '"');
    this.campaign_gap = JSON.parse(this.campaign_gap)

    // Chain constructor with call
    Prospectx.call(this, this.options);
}

MarketPlan.prototype.getPlanById = function (plan_id) {
    var feature = $.grep(this.plan_status, function (e) {
        return e[plan_id];
    });
    return feature[0];
};

MarketPlan.prototype.getPlanGap = function (plan) {
    var t = $.grep(this.campaign_gap, function (e) {
        return e[plan];
    });
    return t[0];
};

MarketPlan.prototype.init = function () {

    var max_arr = Math.max.apply(null, [Number($('#call_break').val()), Number($('#dir_mail_break').val()), Number($('#voice_break').val()), Number($('#rvm_break').val()), Number($('#sms_break').val()), Number($('#email_break').val())]);
    if (max_arr > 0){
        $(".breaking_into").css({'display': "table-row"});
    } else {
        $(".breaking_into").css({'display': "none"});
    }
    let $gap = $('#campaign_gap');
    $gap.empty();
    for (let j = 0; j < max_arr; j++) {
        let ids = parseInt(j) + 1;
        $gap.append('<div class="next_follow_headings">Days Till Next Campaign - '+ids+"</div>");
    }

	let self = this;

    //major market creation
    $(document).on('submit', '#major_market_form', function(e){
        e.preventDefault();
	    self.major_mark_func();
	});

    // Function calls
	this.set_layout();
    let values = this.plans_data;

    let plan_status = this.plan_status;

    //to create new headings on ready page
    let max_val = Math.max.apply(Math, values.map(function(o) { return o.lengths; }))
    let $th = $('#days_heading');
    $th.empty();
    for (let i = 0; i < max_val; i++) {
        let days = parseInt(i) + 1;
        $th.append("<div class='next_follow_headings'>Next Follow Up </div>");
    }
    //enable checked on checkboxes of plans
    values.forEach(function (items) {

        if ('Cold Call' in items) {
            // enabling checkbox of call
            $("#cold_call_plan").prop("checked", true);
            document.getElementById("Cold_Call").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let call_Gap_list = self.campaign_gap.cold_call;

            $("#Cold_Call").show();
            // enable td's of call
            let $call_td = $('#Cold_Call_td');
            $call_td.html('');
            // to create call breaks td
            let $call_break_td = $('#call_break_td');
            $call_break_td.empty();
            let call_breaks = $('#call_break').val();
            for (var p = 0; p < call_breaks; p++){
                let _id = parseInt(p) + 1;
                let call_Gap = call_Gap_list[p];
                $call_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+call_Gap+'" id="call_break'+_id+'" name="call_break'+_id+'">');
            }

            let cold_status = self.getPlanById('Cold Call');
            let cold_st = 'Pending';
            let cold_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let call_ids = parseInt(j) + 1;
                if (typeof cold_status !== 'undefined'){
                    cold_st = cold_status['Cold Call'][j]
                }
                if (typeof cold_st === 'undefined'){
                    cold_st = 'Pending';
                    cold_btn_class = 'plans_data_status';
                }
                if (cold_st !== 'Pending'){
                    cold_btn_class = 'plans_data_success font-10';
                }
                $call_td.append("<div class='plans_data_class'><input min='0' max='100'  class='form-control planner-custom-input' type='number' value=1 id=Cold_Call"+call_ids+" name=Cold_Call"+call_ids+"> <span class='"+cold_btn_class+"'>"+cold_st+"</span> </div>");
                // $call_td.append("<div><input min='0' max='4' style='display:inline-block; width:95px;' class='form-control planner-custom-input' type='number' value=1 id=Cold_Call"+call_ids+" name=Cold_Call"+call_ids+"> <button class='"+cold_btn_class+"' type='button' style='display:inline-block; margin-left:20px;'>"+cold_st+"</button></div>");
            }
            $("#Cold_Call_td").css({'opacity': "100"});

            // enabling exit plans of call
            $(".call_exit").show();

            //creating templates on page load
            let $call_temp = $('#Cold_Call_temp');
            console.log("cold temp is: ", $call_temp)
            // Reset templates
            $call_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let touch_status = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];

                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $call_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="Cold_Call_status'+ids+'" name="Cold_Call_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#Cold_Call_status'+ids).val(touch_status);
                $('#Cold_Call'+ids).val(touch_round_after_days);
            }

        }
        if ('Direct Mail' in items) {
            // enabling checkbox of direct mail
            $("#dir_mail_plan_1").prop("checked", true);
            document.getElementById("Direct_Mail").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let dir_Gap_list = self.campaign_gap.direct_mail;

            $("#Direct_Mail").show();
            let $dir_td = $('#Direct_Mail_td');
            $dir_td.html('');
            // to create direct mail breaks td
            let $dir_mail_break_td = $('#dir_mail_break_td');
            $dir_mail_break_td.empty();
            let dir_mail_break = $('#dir_mail_break').val();
            for (var k = 0; k < dir_mail_break; k++){
                let _id = parseInt(k) + 1;
                let d_gap_list = dir_Gap_list[k]
                $dir_mail_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+d_gap_list+'" id="dir_mail_break'+_id+'" name="dir_mail_break'+_id+'">');
            }

            let dir_status = self.getPlanById('Direct Mail');
            let dir_st = 'Pending';
            let dir_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let dir_ids = parseInt(j) + 1;
                if (typeof dir_status !== 'undefined'){
                    dir_st = dir_status['Direct Mail'][j]
                }
                if (typeof dir_st === 'undefined'){
                    dir_st = 'Pending';
                    dir_btn_class = 'plans_data_status';
                }
                if (dir_st !== 'Pending'){
                    dir_btn_class = 'plans_data_success font-10';
                }
                $dir_td.append("<div class='plans_data_class'><input min='0' max='100' class='form-control planner-custom-input' type='number' value=1 id=Direct_Mail"+dir_ids+" name=Direct_Mail"+dir_ids+"> <span class='"+dir_btn_class+"' >"+dir_st+"</span></div>");
            }
            $("#Direct_Mail_td").css({'opacity': "100"});

            // enabling exit plans of direct mail
            $(".dir_mail_exit").show();

            //creating templates on page load
            let $dir_temp = $('#Direct_Mail_temp');
            // Reset templates
            $dir_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let dir_touch_status = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];
                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $dir_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="Direct_Mail_status'+ids+'" name="Direct_Mail_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#Direct_Mail_status'+ids).val(dir_touch_status);
                $('#Direct_Mail'+ids).val(touch_round_after_days);
            }
        }
        if ('Voice Broadcast' in items) {
            // enabling checkbox of voice broadcast
            $("#voice_plan_1").prop("checked", true);
            document.getElementById("Voice_Broadcast").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let voice_Gap_list = self.campaign_gap.voice_broadcast;

            $("#Voice_Broadcast").show();
            let $voice_td = $('#Voice_Broadcast_td');
            $voice_td.html('');
            // to create voice break td
            let $voice_break_td = $('#voice_break_td');
            $voice_break_td.empty();
            let voice_break = $('#voice_break').val();
            for (var m = 0; m < voice_break; m++){
                let _id = parseInt(m) + 1;
                let v_gap_list = voice_Gap_list[m]
                $voice_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+v_gap_list+'" id="voice_break'+_id+'" name="voice_break'+_id+'">');
            }

            let voice_status = self.getPlanById('Voice Broadcast');
            let voice_st = 'Pending'
            let voice_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let voice_ids = parseInt(j) + 1;
                if (typeof voice_status !== 'undefined'){
                    voice_st = voice_status['Voice Broadcast'][j]
                }
                if (typeof voice_st === 'undefined'){
                    voice_st = 'Pending';
                    voice_btn_class = 'plans_data_status';
                }
                if (voice_st !== 'Pending'){
                    voice_btn_class = ' plans_data_success font-10';
                }
                $voice_td.append("<div class='plans_data_class'><input min='0' max='100' class='form-control planner-custom-input' type='number' value=1 id=Voice_Broadcast"+voice_ids+" name=Voice_Broadcast"+voice_ids+"> <span class='"+voice_btn_class+"' >"+voice_st+"</span></div>");
            }
            $("#Voice_Broadcast_td").css({'opacity': "100"});

            // enabling exit plans of voice broadcast
            $(".voice_exit").show();

            //creating templates on page load
            let $voice_temp = $('#Voice_Broadcast_temp');
            // Reset templates
            $voice_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let touch_status1 = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];
                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $voice_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="Voice_Broadcast_status'+ids+'" name="Voice_Broadcast_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#Voice_Broadcast_status'+ids).val(touch_status1);
                $('#Voice_Broadcast'+ids).val(touch_round_after_days);
            }
        }
        if ('RVM' in items) {
            // enabling checkbox of RVM
            $("#rvm_plan_1").prop("checked", true);
            document.getElementById("RVM").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let rvm_Gap_list = self.campaign_gap.RVM;

            $("#RVM").show();
            let $rvm_td = $('#RVM_td');
            $rvm_td.html('');
            // to create rvm break td
            let $rvm_break_td = $('#rvm_break_td');
            $rvm_break_td.empty();
            let rvm_break = $('#rvm_break').val();
            for (var n = 0; n < rvm_break; n++){
                let _id = parseInt(n) + 1;
                let r_gap_list = rvm_Gap_list[n]
                $rvm_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+r_gap_list+'" id="rvm_break'+_id+'" name="rvm_break'+_id+'">');
            }

            let rvm_status = self.getPlanById('RVM');
            let rvm_st = 'Pending';
            let rvm_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let rvm_ids = parseInt(j) + 1;
                if (typeof rvm_status !== 'undefined'){
                    rvm_st = rvm_status['RVM'][j]
                }
                if (typeof rvm_st === 'undefined'){
                    rvm_st = 'Pending';
                    rvm_btn_class = 'plans_data_status';
                }
                if (rvm_st !== 'Pending'){
                    rvm_btn_class = 'plans_data_success font-10';
                }
                $rvm_td.append("<div class='plans_data_class'><input min='0' max='100' class='form-control planner-custom-input' type='number' value=1 id=RVM"+rvm_ids+" name=RVM"+rvm_ids+"> <span class='"+rvm_btn_class+"'  >"+rvm_st+"</span></div>");
            }
            $("#RVM_td").css({'opacity': "100"});

            // enabling exit plans of rvm
            $(".rvm_exit").show();

            //creating templates on page load
            let $rvm_temp = $('#RVM_temp');
            // Reset templates
            $rvm_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let touch_status2 = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];
                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $rvm_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="RVM_status'+ids+'" name="RVM_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#RVM_status'+ids).val(touch_status2);
                $('#RVM'+ids).val(touch_round_after_days);
            }
        }
        if ('SMS' in items) {
            // enabling checkbox of SMS
            $("#sms_plan_1").prop("checked", true);
            document.getElementById("SMS").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let sms_Gap_list = self.campaign_gap.SMS;

            $("#SMS").show();
            let $sms_td = $('#SMS_td');
            $sms_td.html('');
            // to create sms_break td
            let $sms_break_td = $('#sms_break_td');
            $sms_break_td.empty();
            let sms_break = $('#sms_break').val();
            for (var o = 0; o < sms_break; o++){
                let _id = parseInt(o) + 1;
                let s_gap_list = sms_Gap_list[o]
                $sms_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+s_gap_list+'" id="sms_break'+_id+'" name="sms_break'+_id+'">');
            }

            let sms_status = self.getPlanById('SMS');
            let sms_st = 'Pending';
            let sms_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let sms_ids = parseInt(j) + 1;
                if (typeof sms_status !== 'undefined'){
                    sms_st = sms_status['SMS'][j]
                }
                if (typeof sms_st === 'undefined'){
                    sms_st = 'Pending';
                    sms_btn_class = 'plans_data_status';
                }
                if (sms_st !== 'Pending'){
                    sms_btn_class = 'plans_data_success font-10';
                }
                $sms_td.append("<div class='plans_data_class'><input min='0' max='100' class='form-control planner-custom-input' type='number' value=1 id=SMS"+sms_ids+" name=SMS"+sms_ids+"> <span class='"+sms_btn_class+"'>"+sms_st+"</span></div>");
            }
            $("#SMS_td").css({'opacity': "100"});

            // enabling exit plans of sms
            $(".sms_exit").show();

            //creating templates on page load
            let $sms_temp = $('#SMS_temp');
            // Reset templates
            $sms_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let touch_status3 = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];
                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $sms_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="SMS_status'+ids+'" name="SMS_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#SMS_status'+ids).val(touch_status3);
                $('#SMS'+ids).val(touch_round_after_days);
            }
        }
        if ('EMAIL' in items) {
            // enabling checkbox of EMAIL
            $("#email_plan_1").prop("checked", true);
            document.getElementById("EMAIL").selectedIndex = items.lengths;
            // exit plan gaps in campaigns
            let email_Gap_list = self.campaign_gap.EMAIL;

            $("#EMAIL").show();
            let $email_td = $('#EMAIL_td');
            $email_td.html('');
            // to create sms_break td
            let $email_break_td = $('#email_break_td');
            $email_break_td.empty();
            let email_break = $('#email_break').val();
            for (var q = 0; q < email_break; q++){
                let _id = parseInt(q) + 1;
                let e_gap_list = email_Gap_list[q]
                $email_break_td.append('<input min="0" max="100" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="'+e_gap_list+'" id="email_break'+_id+'" name="email_break'+_id+'">');
            }

            let email_status = self.getPlanById('EMAIL');
            let email_st = 'Pending';
            let email_btn_class = 'plans_data_status';
            for (var j = 0; j < items.lengths; j++){
                let em_ids = parseInt(j) + 1;
                if (typeof email_status !== 'undefined'){
                    email_st = email_status['EMAIL'][j]
                }
                if (typeof sms_st === 'undefined'){
                    sms_st = 'Pending';
                    sms_btn_class = 'plans_data_status';
                }
                if (email_st !== 'Pending'){
                    email_btn_class = 'plans_data_success font-10';
                }
                $email_td.append("<div class='plans_data_class' ><input min='0' max='100'  class='form-control planner-custom-input' type='number' value=1 id=EMAIL"+em_ids+" name=EMAIL"+em_ids+"> <span class='"+email_btn_class+"'>"+email_st+"</span></div>");
            }
            $("#EMAIL_td").css({'opacity': "100"});

            // enabling exit plans of email
            $(".email_exit").show();

            //creating templates on page load
            let $email_temp = $('#EMAIL_temp');
            // Reset templates
            $email_temp.empty();
            let temps = items.temp_ids.length;
            for (let i = 0; i < temps; i++) {
                // create templates
                let ids = parseInt(i) + 1;
                let temp_id = items.temp_ids[i][0];
                let touch_status4 = items.temp_ids[i][1];
                let touch_round_after_days = items.temp_ids[i][2];
                let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                $email_temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="EMAIL_status'+ids+'" name="EMAIL_status'+ids+'"><option value="Active">Active</option><option value="Pending">Pending</option><option value="InActive">InActive</option></select></div></div>');
                $('#EMAIL_status'+ids).val(touch_status4);
                $('#EMAIL'+ids).val(touch_round_after_days);
            }
        }
    });


	// Events
	// 1
	$(document).on('click', '#open_marketing_template', function(){
	    self.marketing_template_button();
	});
	// 2
	$(document).on('click', '#open_planner', function(){
	    self.planning_button();
	});
	// 2.5
	$(document).on('click', '#open_prospect_properties', function(){
	    self.prospects_button();
	});
	// 3
	$(document).on('click', '#cold_call_plan', function(){
	    self.cold_call_plan_func();
	});
	// 4
	$(document).on('click', '#dir_mail_plan_1', function(){
	    self.dir_mail_plan_1_func();
	});
	// 5
	$(document).on('click', '#voice_plan_1', function(){
	    self.voice_plan_1_func();
	});
	// 6
	$(document).on('click', '#rvm_plan_1', function(){
	    self.rvm_plan_func();
	});
	// 7
	$(document).on('click', '#sms_plan_1', function(){
	    self.sms_plan_func();
	});
	// 8
	$(document).on('click', '#email_plan_1', function(){
	    self.email_plan_func();
	});

	$('.rounds-count').on('change', function(event){
	    let rounds = $(this).val(), id = $(this).attr('id');

	    var arr1 = Math.max.apply(null, [Number($('#Cold_Call').val()), Number($('#Direct_Mail').val()), Number($('#Voice_Broadcast').val()), Number($('#RVM').val()), Number($('#SMS').val()), Number($('#EMAIL').val())]);

        self.rounds = arr1;
	    self.add_rounds(id);

	    self.plans[id] = rounds;

        event.stopImmediatePropagation();
        event.preventDefault();
	    console.log($(this).val())
	});

	$('.breaking-into').on('change', function(){
	    console.log("breaking into the: ",$(this).val());
	    let elem_value = $(this).val();
	    //if (elem_value < 5) {
	        let id = $(this).attr('id');
	        let $td = $('#'+id+'_td');
	        $td.empty();


            var arr = Math.max.apply(null, [Number($('#call_break').val()), Number($('#dir_mail_break').val()), Number($('#voice_break').val()), Number($('#rvm_break').val()), Number($('#sms_break').val()), Number($('#email_break').val())]);
            console.log("max array is : ",arr)
            if (arr > 0){
                $(".breaking_into").css({'display': "table-row"});
            } else {
                $(".breaking_into").css({'display': "none"});
            }
	        let $gap = $('#campaign_gap');
	        $gap.empty();
	        for (let j = 0; j < arr; j++) {
	            let ids = parseInt(j) + 1;
	            $gap.append('<div class="next_follow_headings">Days Till Next Campaign - '+ids+"</div>");
	        }

	        for (let i = 0; i < elem_value; i++) {
                let ids = parseInt(i) + 1;
                console.log("td object is: ", id)
	            $td.append('<input min="0" style="display: flex; flex-flow: column; height: 100%; flex-grow : 1;" class="form-control planner-custom-input" type="number" value="1" id="'+id+ids+'" name="'+id+ids+'">');
                }
        //} else
        //{
        //        alert("Select no more than 4 break into!")
        //}
	});




};

MarketPlan.prototype.set_layout = function() {
    $("#related_temp").hide();
    $("#plan_temp").hide();
    $("#related_prospects").hide();

    $("#Cold_Call").hide();
    $("#Direct_Mail").hide();
    $("#Voice_Broadcast").hide();
    $("#RVM").hide();
    $("#SMS").hide();
    $("#EMAIL").hide();

    $("#cold_plan_days").hide();
    $("#dir_mail_plan_days").hide();
    $("#voice_plan_days").hide();
    $("#rvm_plan_days").hide();
    $("#sms_plan_days").hide();
    $("#email_plan_days").hide();

//    hiding plans for all marketings
    $(".call_exit").hide();
    $(".dir_mail_exit").hide();
    $(".voice_exit").hide();
    $(".rvm_exit").hide();
    $(".sms_exit").hide();
    $(".email_exit").hide();

    //getting major market list


    $.ajax({
         type: "POST",
         url: window.location.origin+"/marketing/get_markets",
//         data: JSON.stringify(data),
         contentType: "application/json; charset=utf-8",
         dataType: "json",
         success: function (result) {
             if(result.status==200)
             {
                let $markets = $("#markets");
                // Reset days counts
                $markets.empty();
                let data = result.market_data
                for (let i = 0; i < data.length; i++) {
                    let id = data[i].id;
                    let title = data[i].title
                    $markets.append('<option value="'+title+'">'+title+'</option>');
                }
             }
             else {
//                 alert(result.message)
             }

         },
         error: function ( result) {
             // error handler
             alert(result.message);
         }
      });

};

/**
* function for opening marketing template
*/
MarketPlan.prototype.marketing_template_button = function() {
    let chk = $('#open_marketing_template:checkbox:checked').length > 0,
        btn1 = $('#cold_call_plan:checkbox:checked').length > 0,
        btn2 = $('#dir_mail_plan_1:checkbox:checked').length > 0,
        btn3 = $('#voice_plan_1:checkbox:checked').length > 0,
        btn4 = $('#rvm_plan_1:checkbox:checked').length > 0,
        btn5 = $('#sms_plan_1:checkbox:checked').length > 0,
        btn6 = $('#email_plan_1:checkbox:checked').length > 0;

    if (chk === true) {
        $("#related_temp").show();
        if (btn1 == true) {
            $("#call_temp").show();
        }else {
            $("#call_temp").hide();
        }

        if (btn2 == true) {
            $("#dir_mail_temp").show();
        }else {
            $("#dir_mail_temp").hide();
        }

        if (btn3 == true) {
            $("#voice_temp").show();
        }else {
            $("#voice_temp").hide();
        }

        if (btn4 == true) {
            $("#rvm_temp_div").show();
        }else {
            $("#rvm_temp_div").hide();
        }

        if (btn5 == true) {
            $("#sms_temp_div").show();
        }else {
            $("#sms_temp_div").hide();
        }

        if (btn6 == true) {
            $("#email_temp_div").show();
        }else {
            $("#email_temp_div").hide();
        }

    } else {
        $("#related_temp").hide();
    }
}

/**
* function for open planner button
*/
MarketPlan.prototype.planning_button = function() {
    var chk1 = $('#open_planner:checkbox:checked').length > 0;
    if (chk1 === true) {
        $("#plan_temp").show();
    } else {
        $("#plan_temp").hide();
    }
}

/**
* function for open Related Prospects
*/
MarketPlan.prototype.prospects_button = function() {
    var chk1 = $('#open_prospect_properties:checkbox:checked').length > 0;
    if (chk1 === true) {
        $("#related_prospects").show();
    } else {
        $("#related_prospects").hide();
    }
}

// function for cold call plan
MarketPlan.prototype.cold_call_plan_func = function() {
    var chk2 = $('#cold_call_plan:checkbox:checked').length > 0;
    if (chk2 === true) {
        $("#Cold_Call").show();
        $("#cold_plan_days").show();
        $("#call_temp").show();
        $("#Cold_Call_td").css({'opacity': "100"});
        $(".call_exit").show();
    } else {
        $("#Cold_Call").hide();
        $("#cold_plan_days").hide();
        $("#call_temp").hide();
        $("#Cold_Call_td").css({'opacity': "0"});
        $(".call_exit").hide();
    }
}

// function for direct email call plan
MarketPlan.prototype.dir_mail_plan_1_func = function() {
    var chk3 = $('#dir_mail_plan_1:checkbox:checked').length > 0;
    if (chk3 === true) {
        $("#Direct_Mail").show();
        $("#dir_mail_plan_days").show();
        $("#dir_mail_temp").show();
        $("#Direct_Mail_td").css({'opacity': "100"});
        $(".dir_mail_exit").show();
    } else {
        $("#Direct_Mail").hide();
        $("#dir_mail_plan_days").hide();
        $("#dir_mail_temp").hide();
        $("#Direct_Mail_td").css({'opacity': "0"});
        $(".dir_mail_exit").hide();
    }
}

// function for voice broadcast call plan
MarketPlan.prototype.voice_plan_1_func = function() {
    var chk4 = $('#voice_plan_1:checkbox:checked').length > 0;
    if (chk4 === true) {
        $("#Voice_Broadcast").show();
        $("#voice_plan_days").show();
        $("#voice_temp").show();
        $("#Voice_Broadcast_td").css({'opacity': "100"});
        $(".voice_exit").show();
    } else {
        $("#Voice_Broadcast").hide();
        $("#voice_plan_days").hide();
        $("#voice_temp").hide();
        $("#Voice_Broadcast_td").css({'opacity': "0"});
        $(".voice_exit").hide();
    }
}

// function for rvm call plan
MarketPlan.prototype.rvm_plan_func = function() {
    var chk5 = $('#rvm_plan_1:checkbox:checked').length > 0;
    if (chk5 === true) {
        $("#RVM").show();
        $("#rvm_plan_days").show();
        $("#rvm_temp_div").show();
        $("#RVM_td").css({'opacity': "100"});
        $(".rvm_exit").show();
    } else {
        $("#RVM").hide();
        $("#rvm_plan_days").hide();
        $("#rvm_temp_div").hide();
        $("#RVM_td").css({'opacity': "0"});
        $(".rvm_exit").hide();
    }
}

// function for sms call plan
MarketPlan.prototype.sms_plan_func = function() {
    var chk6 = $('#sms_plan_1:checkbox:checked').length > 0;
    if (chk6 === true) {
        $("#SMS").show();
        $("#sms_plan_days").show();
        $("#sms_temp_div").show();
        $("#SMS_td").css({'opacity': "100"});
        $(".sms_exit").show();
    } else {
        $("#SMS").hide();
        $("#sms_plan_days").hide();
        $("#sms_temp_div").hide();
        $("#SMS_td").css({'opacity': "0"});
        $(".sms_exit").hide();
    }
}

// function for email call plan
MarketPlan.prototype.email_plan_func = function() {
    var chk7 = $('#email_plan_1:checkbox:checked').length > 0;
    if (chk7 === true) {
        $("#EMAIL").show();
        $("#email_plan_days").show();
        $("#email_temp_div").show();
        $("#EMAIL_td").css({'opacity': "100"});
        $(".email_exit").show();
    } else {
        $("#EMAIL").hide();
        $("#email_plan_days").hide();
        $("#email_temp_div").hide();
        $("#EMAIL_td").css({'opacity': "0"});
        $(".email_exit").hide();
    }
}

MarketPlan.prototype.add_rounds = function(id) {
    console.log("rounds is: ", id)


    // Next follow up
    this.next_follow_up();
    var pln = " ";
    if (id == 'Cold_Call'){
        pln = 'Cold Call';
    } else if (id == 'Direct_Mail'){
        pln = 'Direct Mail';
    } else if (id == 'Voice_Broadcast'){
        pln = 'Voice Broadcast';
    } else {
        pln = id;
    }

    let count = $('#'+id).val()
    var data = {
          seq : $('#seq_id').val(),
          user_name : $('#user_name').val(),
          temp_count : count,
          market_plan : pln,
      };

    $.ajax({
         type: "POST",
         async: false,
         cache: false,
         url: window.location.origin+"/marketing/create_plan_template",
         data: JSON.stringify(data),
         contentType: "application/json; charset=utf-8",
         dataType: "json",
         success: function (result) {
             if(result.status==200)
             {
                let $td = $('#'+id+'_td');
                // Reset days counts
                $td.empty();

                let $temp = $('#'+id+'_temp');
                // Reset templates
                $temp.empty();
                let temps = result.temp_ids.length;
                for (let i = 0; i < temps; i++) {
                    let tmp_ids = parseInt(i) + 1;

                    $td.append("<div class='column plans_data_class'><input min='0' max='100' class='form-control planner-custom-input' type='number' value=1 id="+id+tmp_ids+" name="+id+tmp_ids+"> <span class='plans_data_status'>Pending</span></div>");

                    // create templates
                    let ids = parseInt(i) + 1;
                    let temp_id = result.temp_ids[i];
                    console.log(temp_id);
                    let suc_url = window.location.origin+"/marketing/marketing_template/"+temp_id;
                    console.log("suc_url is: ", suc_url);
                    $temp.append('<div><div class="template_list_title"><a style="background-color:##c5e8ff;" class="card-link btn-block p-1" target="_blank" href="'+suc_url+'">Touch ' +ids+ '</a></div><div class="template_list_status"><select class="custom-select form-control-sm" id="'+id+"_status"+ids+'" name="'+id+"_status"+ids+'"><option value="active">Active</option><option value="pending">Pending</option><option value="inactive">Inactive</option></select></div></div>');
                }

                console.log("ended")
             }
             else {
//                 alert(result.message)
             }

         },
         error: function ( result) {
             // error handler
             alert(result.message);
         }
      });
};



MarketPlan.prototype.next_follow_up = function(id) {
    let $th = $('#days_heading');
    // Reset
    $th.empty();

    for (let i = 0; i < this.rounds; i++) {
        let days = parseInt(i) + 1;
        $th.append("<div class='next_follow_headings'>Next Follow Up  </div>");
    }
};

MarketPlan.prototype.major_mark_func = function() {
    var data = {
          mark_title : $('#mark_title').val(),
          market : $('#market').val(),
          state : $('#state').val(),
      };

    $.ajax({
         type: "POST",
         url: window.location.origin+"/marketing/major_market",
         data: JSON.stringify(data),
         contentType: "application/json; charset=utf-8",
         dataType: "json",
         success: function (result) {
             if(result.status==200)
             {
                let $markets = $("#markets");
                $markets.empty();
                let data = result.market_data;
                let id = data.id.toString();
                let title = data.title.toString();
                $markets.append('<option selected value="'+title+'">'+title+'</option>');
                $('#major_modal').modal('toggle');
             }
             else {
//                alert(result.message);
             }

         },
         error: function ( result) {
            // alert(result.message);
         }
      });

};