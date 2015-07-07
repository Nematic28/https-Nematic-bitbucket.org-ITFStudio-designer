/**
 * Created by bykovsky on 07.07.2015.
 */
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
})