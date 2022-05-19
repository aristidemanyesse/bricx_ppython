$(function(){
    $("#formAbonnement input").keyup(function(event) {
        $(this).val($(this).val().toUpperCase())
        if ($(this).val().length == 5) {
            $(this).parent("div").next("div").find("input").focus();
        }
    });
})