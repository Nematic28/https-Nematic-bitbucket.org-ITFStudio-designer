$(function(){

    var $form = $('.options form');
    function FilterPopup($el) {
        color = false; texture = false;
        if ($el.find('.color-picker input[type=radio]:checked').length>0) {
          color = $el.find('.color-picker input[type=radio]:checked').data("id");   
        }
        if ($el.find('.texture-picker input[type=checkbox]:checked').length>0) {
         texture = true; 
         
        
        }
        
        
        $el.parents(".popup").find('.main-picker .pattern').each(function() {
         $(this).hide();
         if (!$el.find('.texture-picker input[type=text]').val() || $(this).data("name").toUpperCase().indexOf($el.find('.texture-picker input[type=text]').val().toUpperCase())>-1) {
            if (!color || $(this).data('color') == color) {
              
              if (!texture || ($(this).data('texture') && $el.find('.texture-picker input[type=checkbox][data-id='+$(this).data('texture')+']:checked').length>0)) {
                $(this).show();

              }
            }
         }
         
        });


    }


    $(document).on("click",'input[data-popup=1]',function() {
        $("#popup_"+$(this).val()).toggle();

    });
    $(document).on("click",'input[data-popup=close]',function() {
       $(this).parents(".popup-overlay").hide();
    });

    
    $('.options form input').change(function(){
        if ($(this).parents("[data-filter=1]").length>0) {
            FilterPopup($(this).parents("[data-filter=1]"));

        } else
        {
            $form.find("input[name=id_click]").val($(this).val());
            $form.submit();
        }
    });
    
    $('.options form input[type=text]').on("keydown",function() {
        FilterPopup($('input').parents("[data-filter=1]"));
        if(event.keyCode == 13) {
            event.preventDefault();
            return false;
        }        
        
    });

    $("#popup_"+$form.find("input[name=id_click]").val()).toggle();



});