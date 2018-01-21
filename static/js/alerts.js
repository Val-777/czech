async function getExercise(api_url) {
  const response = await fetch(api_url, {
    method: 'GET',
  });
  const json = await response.json();
  return json;
}

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

async function checkExercise(data, api_url) {
  const request = {
    credentials: "same-origin",
    method: 'POST',
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Accept": "application/json",
      "Content-Type": "application/json",
      // 'X-Requested-With': 'XMLHttpRequest'
    },
  };
  // without JSON.stringify, request.body will be empty!
  const options = { body: JSON.stringify(data) }
  $.extend(request, options);
  const response = await fetch(api_url, request);
  const json = await response.json();

  return json;
}

$(function () {
  const exercise_type = $(location).attr('pathname').split('/').reverse()[1];
  $('#' + exercise_type).toggleClass('list-group-item-info');
  const api_url = '/get_exercise/' + exercise_type + '/'
  getExercise(api_url).then(function (exercise) {
    $(".js-german").text(exercise.german);
    $("#checkbtn, #id_czech").prop('disabled', false);
    $("#id_czech").focus();
  });

  $("#answer_form").submit(function (e) {
    $("#checkbtn, #id_czech").prop('disabled', true);
    e.preventDefault();
    answer = $("#id_czech").val();
    question = $(".js-german").text();

    options = { answer: answer, german: question }
    checkExercise(options, api_url).then(function (result) {
      if (result.status === true) {
        $(".alert-success").fadeIn(1000)
      } else {
        $("#correct_answer").text(result.correct_answer);
        $(".alert-danger").fadeIn(1000);
      }
    })

    $(document).keypress(function (event) {
      var keycode = event.keyCode || event.which;
      if (keycode == '13') {
        $(".weiter").trigger("click");
      }
    });
  });

  $(".weiter").click(function (e) {
    $(document).unbind("keypress");
    $("#id_czech").val("");
    $(".alert").fadeOut(1000);
    $(".js-german").slideUp("slow", function () {
      getExercise(api_url).then(function (exercise) {
        $(".js-german").text(exercise.german).slideDown("slow");
        $("#checkbtn, #id_czech").prop('disabled', false);
        $("#id_czech").focus();
      });
    });
  });
})
