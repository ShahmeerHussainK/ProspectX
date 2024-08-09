$(document).ready(function () { 
    $(".testimonial_btn").on('click', function(){
        // var ele = ('.testimonial_form').clone(true);
        // ('.testimonial_form').after(ele);
        $('.testimonial_form').append($('.testimonial_form').html())
        
    })
    $(".xsite_stats_button_group .btn").click(function(){  
        $(".xsite_stats_button_group .btn.active").removeClass("active");
        $(this).addClass("active");
    });
}); 