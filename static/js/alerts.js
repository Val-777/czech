async function getExercise(api_url) {
  const response = await fetch(api_url, {
    method: 'GET',
    credentials: "same-origin",
    // credentials: 'include',
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
    // credentials: 'include',
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

function setCookie(name, value, days) {
  var expires = "";
  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

$(function () {
  const exercise_type = $(location).attr('pathname').split('/').reverse()[1];
  $('#' + exercise_type).toggleClass('list-group-item-info');
  const api_url = '/get_exercise/' + exercise_type + '/'
  getExercise(api_url).then(function (exercise) {
    $(".js-german").text(exercise.german);
    $("#checkbtn, #id_czech").prop('disabled', false);
    $("#id_czech").focus();
    setCookie("id", exercise.id, 1);
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
        if (result.correct_answer.length > 1) {
          const solutions = [];
          result.correct_answer.forEach(function (solution) {
            solutions.push('<b>' + solution + '</b>');
          });
          $("#correct_answer").html(solutions.join(' oder '));
        } else {
          $("#correct_answer").html('<b>' + result.correct_answer + '</b>');
        }
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
        setCookie("id", exercise.id, 1);
      });
    });
  });
})
