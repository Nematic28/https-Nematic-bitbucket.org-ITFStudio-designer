$(function(){

    var $form = $('.options form');



    $(document).on("click",'input[data-popup=1]',function() {
        $("#popup_"+$(this).val()).toggle();

    });
    $(document).on("click",'input[data-popup=close]',function() {
       $(this).parents(".popup-overlay").hide();
    });

    $('input').change(function(){
            $form.find("input[name=id_click]").val($(this).val());
            $form.submit();
    });

    $("#popup_"+$form.find("input[name=id_click]").val()).toggle();

});