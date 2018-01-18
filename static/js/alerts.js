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

async function getExercise() {
  const response = await fetch('/ajax/get_exercise', {
    method: 'GET',
  });
  const json = await response.json();
  return json;
}

async function checkExercise(data) {
  const setup = {
    credentials: "same-origin",
    method: 'POST',
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Accept": "application/json",
      "Content-Type": "application/json",
      'X-Requested-With': 'XMLHttpRequest'
    },
  };
  const merged = $.extend(options, setup);
  const response = await fetch('/ajax/get_exercise', merged);
  const json = await response.json();

  return json;
}

$(function () {
  getExercise().then(function (exercise) {
    $(".js-german").text(exercise.german);
    $("#checkbtn").prop('disabled', false);
    console.log(exercise);
  });

  $("#answer_form").submit(function (e) {
    e.preventDefault();
    answer = $("#id_czech").val();
    question = $(".js-german").text();

    options = { answer: answer, question: question }
    checkExercise(options).then(function () {
      console.log('');
    })
    // console.log(options);
    // console.log($(".js-german").text() + answer);
    // check(answer);
  });
})
