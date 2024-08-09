$(function () {
    $("#sales-form-horizontal").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "slide",
        // Enables all steps from the begining
        enableAllSteps: true,
        // Removes the number from the title
        titleTemplate: "#title#",
        enableFinishButton: true,
        enableKeyNavigation: true,
        showFinishButtonAlways: true,
        onFinished: function (event, currentIndex) {
            var form = $(this);
            form.submit();
        },
        onInit: function (event, currentIndex) {
            $('#Next').parent().hide();
            $('#Previous').parent().hide();
        },
        labels: {
            finish: "Save",
        },
        onStepChanged: function (event, currentIndex) {
            console.log(currentIndex);
            if (currentIndex === 0) {
                $('#Finish').parent().hide();

                if ($("#deals").val() === "" || $("#deals").val().trim() === "") {
                    $('#Next').parent().addClass('disabled');
                    $('#Next').removeAttr('href');
                }
                // $("#deals").keyup(function () {
                //     if ($(this).val() !== "" && $(this).val().trim() !== "") {
                //         $('#Next').parent().removeClass('disabled');
                //         $('#Next').attr('href', '#next');
                //     } else {
                //         $('#Next').parent().addClass('disabled');
                //         $('#Next').removeAttr('href');
                //     }
                // });

            } else if (currentIndex === 1) {

                if ($("#attending_showing").val() === "" || $("#attending_showing").val().trim() === "") {
                    $('#Finish').parent().addClass('disabled');
                    $('#Finish').removeAttr('href');
                    $('#Finish').parent().show();
                }
            }
        }
    });



    // $("#sales-form-horizontal .actions").insertBefore("#sales-form-horizontal .steps ");


    // @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    $("#transactions_horizontal_form").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "slide",
        // Enables all steps from the begining
        enableAllSteps: true,
        // Removes the number from the title
        titleTemplate: "#title#",
        enableFinishButton: true,
        enableKeyNavigation: true,
        showFinishButtonAlways: true,
        onFinished: function (event, currentIndex) {
            $('#Save').addClass('disabled');
            var form = $(this);
            form.submit();
        },
        onInit: function (event, currentIndex) {
            $('#Next').parent().hide();
            $('#Previous').parent().hide();
        },
        labels: {
            finish: "Save",
        },
        onStepChanged: function (event, currentIndex) {
            console.log(currentIndex);

        }
    });
    // $("#transactions_horizontal_form .actions").insertBefore("#transactions_horizontal_form .steps ");
    // $('.wizard_select2').select2()

    // Cash Buyer form
    $("#cashbuyer_horizontal_form").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "slide",
        // Enables all steps from the begining
        enableAllSteps: true,
        // Removes the number from the title
        titleTemplate: "#title#",
        enableFinishButton: true,
        enableKeyNavigation: true,
        showFinishButtonAlways: true,
        onFinished: function (event, currentIndex) {
            $('#Save').addClass('disabled');
            var form = $(this);
            form.submit();
        },
        onInit: function (event, currentIndex) {
            $('#Next').parent().hide();
            $('#Previous').parent().hide();
        },
        labels: {
            finish: "Save",
        },
        onStepChanged: function (event, currentIndex) {
            console.log(currentIndex);
        }
    });

    $("#seller_form").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "slide",
        enableAllSteps: true,
        titleTemplate: "#title#",
        enableFinishButton: true,
        enableKeyNavigation: true,
        showFinishButtonAlways: true,
        onFinished: function (event, currentIndex) {
            $('#Save').addClass('disabled');
            var form = $(this);
            form.submit();
        },
        onInit: function (event, currentIndex) {
            $('#Next').parent().hide();
            $('#Previous').parent().hide();
        },
        labels: {
            finish: "Save",
        },
        onStepChanged: function (event, currentIndex) {

            if (currentIndex === 3) {
                var sqft_val = $("#sqft").val();
                if (sqft_val==""){
                  var edit = $("#edit_handler");
                  var lead_id = $(edit).attr('sid');
                    calc(edit.val(), lead_id)
                }
            }
        }

    });

    $('.wizard_select2').select2();
    $(".js-example-placeholder-multiple").select2({
        placeholder: "Type Of Investor"
    });
    $(".xforce_filestyle").filestyle({ buttonName: "btn-primary" });
});




$(document).ready(function () {


    $("#info").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#info').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrinfo = cont_info;
        var parsereinfo = new DOMParser;
        var domparsereinfo = parsereinfo.parseFromString(encodedStrinfo, 'text/html');
        var decodedStringinfo = domparsereinfo.body.textContent;
        var info = $("#info").summernote('code', decodedStringinfo);
        // $('#email_content').val(email_content);

    }

    $("#details").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#details').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrdetails = cont_details;
        var parseredetails = new DOMParser;
        var domparseredetails = parseredetails.parseFromString(encodedStrdetails, 'text/html');
        var decodedStringdetails = domparseredetails.body.textContent;
        var details = $("#details").summernote('code', decodedStringdetails);
        // $('#email_content').val(email_content);

    }
    $("#miscellaneous_notes").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#miscellaneous_notes').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrnotess = cont_miscellaneous_notes;
        var parserenotess = new DOMParser;
        var domparserenotess = parserenotess.parseFromString(encodedStrnotess, 'text/html');
        var decodedStringnotess = domparserenotess.body.textContent;
        var miscellaneous_notes = $("#miscellaneous_notes").summernote('code', decodedStringnotess);
        // $('#email_content').val(email_content);

    }

    $("#mao_details").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#mao_details').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrmao = cont_mao_details;
        var parseremao = new DOMParser;
        var domparseremao = parseremao.parseFromString(encodedStrmao, 'text/html');
        var decodedStringmao = domparseremao.body.textContent;
        var mao_details = $("#mao_details").summernote('code', decodedStringmao);
        // $('#email_content').val(email_content);

    }

    $("#note_for_agent").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#note_for_agent').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStragent = cont_note_for_agent;
        var parsereagent = new DOMParser;
        var domparsereagent = parsereagent.parseFromString(encodedStragent, 'text/html');
        var decodedStringagent = domparsereagent.body.textContent;
        var note_for_agent = $("#note_for_agent").summernote('code', decodedStringagent);
        // $('#email_content').val(email_content);

    }



    $("#other_terms").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#other_terms').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrother = cont_other_terms;
        var parsereother = new DOMParser;
        var domparsereother = parsereother.parseFromString(encodedStrother, 'text/html');
        var decodedStringother = domparsereother.body.textContent;
        var other_terms = $("#other_terms").summernote('code', decodedStringother);
        // $('#email_content').val(email_content);

    }

    $("#deal_details").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#deal_details').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrdeals = cont_deal_details;
        var parseredeals = new DOMParser;
        var domparseredeals = parseredeals.parseFromString(encodedStrdeals, 'text/html');
        var decodedStringdeals = domparseredeals.body.textContent;
        var deal_details = $("#deal_details").summernote('code', decodedStringdeals);
        // $('#email_content').val(email_content);

    }



    $("#detailed_source").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#detailed_source').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrsorce = cont_detailed_source;
        var parseresorce = new DOMParser;
        var domparseresorce = parseresorce.parseFromString(encodedStrsorce, 'text/html');
        var decodedStringsorce = domparseresorce.body.textContent;
        var detailed_source = $("#detailed_source").summernote('code', decodedStringsorce);
        // $('#email_content').val(email_content);

    }

    $("#notes").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#notes').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStrnotes = cont_notes;
        var parserenotes = new DOMParser;
        var domparserenotes = parserenotes.parseFromString(encodedStrnotes, 'text/html');
        var decodedStringnotes = domparserenotes.body.textContent;
        var notes = $("#notes").summernote('code', decodedStringnotes);
        // $('#email_content').val(email_content);

    }
    $("#additional_notes").summernote('isEmpty');
    // $( "#Finish" ).click(function() {

    if ($('#additional_notes').summernote('isEmpty')) {
        // alert('editor content is empty');
    }
    else {
        var encodedStraddi = cont_additional_notes;
        var parsereaddi = new DOMParser;
        var domparsereaddi = parsereaddi.parseFromString(encodedStraddi, 'text/html');
        var decodedStringaddi = domparsereaddi.body.textContent;
        var additional_notes = $("#additional_notes").summernote('code', decodedStringaddi);
        // $('#email_content').val(email_content);

    }




});
jQuery(window).scroll(function () {
    var scrollBottom = jQuery(document).height() - jQuery(window).height() - jQuery(window).scrollTop();
    // alert(scrollBottom);
    if (scrollBottom > 100) {
        jQuery('.xforce_steps .wizard > .actions').show();
        jQuery('.xforce_steps .wizard > .actions').css({ "position": "fixed", "width": "80%", "right": "30px", "z-index": "900" });
    } else {
        jQuery('.xforce_steps .wizard > .actions').css({ "position": "relative", "width": "100%", "right": "0px", "z-index": "900" });
    }
});


$(document).ready(function () {  
    $('.call_attempt_btn .dropdown-menu a').on('click', function(){
        $('.call_attempt_btn .dropdown-toggle').html($(this).html());
        $("input#textbox").val($(this).html());
    });
    //$("input#textbox").val($('.call_attempt_btn .dropdown-menu a').html());
    var count = 1;
    $('.seller_details_btn').on('click', function () {
        
        $( ".seller_details_div" ).slideDown( "fast", function() {
            $(".seller_details_div").show();
          });
        if($('.seller_details_div .row').length =='3'){
            $(".seller_details_btn").prop('disabled', true);
        } 
         
        // alert($('.seller_details_div .row').length);
       
        var html = '<div id="seller_node_id__'+count+'" class="row"><div class="col-xl-3 col-lg-4 col-md-4 "><div class="form-group"><label>Seller Name ' + count + '<span class="text-danger">*</span></label><input placeholder="Name" class="form-control required" id="seller_name'+ count +'" name="seller_name' + count + '" required type="text"></div></div><div class="col-xl-3 col-lg-4 col-md-4 "><div class="form-group"><label>Seller Phone Number ' + count + '<span class="text-danger"> *</span></label><input placeholder="Phone Number"  class="form-control required" id="seller_phone' + count + '" name="seller_phone' + count + '" required type="text"></div></div><div class="col-xl-3 col-lg-4 col-md-4 "><div class="form-group"><label>Seller Email ' + count + '<span class="text-danger">*</span></label><input placeholder="Email"  class="form-control required" id="seller_email' + count + '" name="seller_email' + count + '" required type="text"></div></div> <div class="col-xl-3 col-lg-4 col-md-4 "><button class="btn btn-danger btn-sm seller_info_btn seller_info_del_'+count+' " type="button"> <i class="fa fa-trash"></i></button></div></div>'
        $(".seller_details_div").append(html);
        count++;
        $(".seller_info_btn ").on('click', function () {
            var node_id = $(this).parent().parent().attr('id'); 
            $( '#'+node_id ).remove();
        });
    }); 
    var table = $('#example').DataTable( {
        scrollY:        300,
        scrollX:        true,
        scrollCollapse: true,
        paging:         false,
        fixedColumns:   {
            leftColumns: 0,
            rightColumns: 1
        }
    } );
    $('#loader_id').removeClass('loading');

    $('#submit_offer_datatable').DataTable();
//plugin bootstrap minus and plus
//http://jsfiddle.net/laelitenetwork/puJ6G/
$('.btn-number').click(function(e){
    e.preventDefault();
    
    fieldName = $(this).attr('data-field');
    type      = $(this).attr('data-type');
    var input = $("input[name='"+fieldName+"']");
    var currentVal = parseInt(input.val());
    if (!isNaN(currentVal)) {
        if(type == 'minus') {
            
            if(currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            } 
            if(parseInt(input.val()) == input.attr('min')) {
                $(this).attr('disabled', true);
            }

        } else if(type == 'plus') {

            if(currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) == input.attr('max')) {
                $(this).attr('disabled', true);
            }

        }
    } else {
        input.val(0);
    }
});
$('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});
$('.input-number').change(function() {
    
    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());
    
    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the minimum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        alert('Sorry, the maximum value was reached');
        $(this).val($(this).data('oldValue'));
    }
    
    
});
$(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) || 
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
});

 function calc(edit, lead_id) {
         if (edit == 'yes') {
                 console.log("on");
                 $.ajax({
                     type: 'GET',
                     url: "/seller/total_view/" + lead_id + "/",
                     success: function (data) { // on success..
                         if (data["msg"] == "succesful_call") {

                             $("#sqft").val(data["SqFt:"]);
                             $("#lot_size").val(data["Lot Size:"]);
                             $("#property_type").val(data["Property Type:"]);
                             $("#year_built").val(data["Year Built:"]);
                             $("#year_assessed").val(data["Year Assessed:"]);
                             $("#tax_assessment").val(data["Tax Assessment:"])
                             // $("#xforce_section").removeClass("d-none")
                             toastr.success("Total View data found.");

                         }
                         else if(data["msg"]=="unsuccesful_call"){
                              toastr.error("Total View data not found.");
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

         }
    }
 
