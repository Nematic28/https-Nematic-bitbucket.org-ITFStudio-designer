$(function(){
    // Switch
    var $left_button = $('.nav-left');
    var $right_button = $('.nav-right');

    var $rotations = $('.main-view .image-set');
    var active = 0;

    function rotate()
    {
        $rotations.each(function(key, value){
            if (key != active) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    }

    $left_button.click(function() {
        if($rotations.length < 2) {
            return;
        }
        active++;
        if (active >= $rotations.length) {
            active = 0;
        }
        rotate();
    });

    $right_button.click(function() {
        if ($rotations.length < 2) {
            return;
        }
        active--;
        if (active < 0 ) {
            active = $rotations.length - 1;
        }
        rotate();
    });

    rotate();
});