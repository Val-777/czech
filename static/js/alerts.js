async function getExercise() {
  const response = await fetch('/ajax/get_exercise', {
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

async function checkExercise(data) {
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
  // console.log(setup);
  const response = await fetch('/ajax/get_exercise', request);
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

    options = { answer: answer, german: question }
    checkExercise(options).then(function (result) {
      result.status ?
        $(".alert-success").fadeIn(1000).delay(2000).fadeOut(2000) :
        $(".alert-danger").fadeIn(1000).delay(2000).fadeOut(2000);
    })

  });
})
