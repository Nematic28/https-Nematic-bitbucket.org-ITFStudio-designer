/**
 * Created by bykovsky on 07.07.2015.
 */
$(function () {
    var $product_type = $('.type-of-product-content');
    $product_type.each(function(){
        var $half_height = ($(this).children('img').height() / 2).toString() ;
        $(this).children('img').css({
            'clip' : 'rect(auto auto '+$half_height+'px auto)',
            top: $half_height+'px'
        });
        $(this).children('img').hover(function(){
            $(this).css({
                'clip' : 'rect('+$half_height+'px auto auto auto)',
                top: '-'+$half_height+'px'
            });
        },function(){
            $(this).css({
                'clip' : 'rect(auto auto '+$half_height+'px auto)',
                top: $half_height+'px'
            });
        });
    });
});
$(function () {
    var $product = $('.type-of-product');
    var $count = $product.length;
    $product.parent().removeClass().addClass(function(){
        if ($count < 2) {
            return false;
        }
        else if ($count == 2){
            return false;
        }
        else if ($count == 3){
            return 'three';
        }
        else {
            return 'more-than-three';
        }
    });

    console.log($count)
});