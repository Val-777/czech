// $(function() {
//         Alert = {
//         show: function($div, msg) {
//             $div.find('.alert-msg').text(msg);
//             if ($div.css('display') === 'none') {
//             // fadein, fadeout.
//             $div.fadeIn(1000).delay(2000).fadeOut(2000);
//             }
//         },
//         warn: function(msg) {
//             this.show($('#alert-warn'), msg);
//         }
//         }
//         $('body').on('click', '.alert-close', function() {
//             $(this).parents('.alert').hide();
//         });
//         $('#warn').click(function() {
//         Alert.warn('This is warning alert.')
//         });
// });
function extern (){
    var german = $('.js-german');
    czech = $.ajax({
                url: '/ajax/get_exercise',
                dataType: 'json',
                success: function (exercise) {
                    german.text(exercise['german']);
                    return exercise['czech'];
                }
            });
    return czech;
}

$(function() {
    real_answer = extern();
    window.setTimeout(function (){
        console.log(real_answer['responseJSON']['czech']);
        real_answer = real_answer['responseJSON']['czech'];
        // $('#checkbtn').on('click', function (){
        $('#form').submit(function(e){
            e.preventDefault();
            answer = $('#id_czech').val();
            console.log(real_answer == answer);
            // check(answer);
        });
    }, 500);
});

// $('#form').submit(function(e){
//     $.post('/url/', $(this).serialize(), function(data){ ... 
//        $('.message').html(data.message);
//        // of course you can do something more fancy with your respone
//     });
//     e.preventDefault();
// });


// function check(answer){

// }