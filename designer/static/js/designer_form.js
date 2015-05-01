$(function(){

    var $form = $('.options form');

    $('input').change(function(){
        $form.submit();
    });
});