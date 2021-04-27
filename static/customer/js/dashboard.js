$('#login').click(function(e) {
    e.preventDefault();
    $('#login').prop('disabled', true);
    $('#google-btn').prop('disabled', true);
    $("#login").html('<div class="spinner-border" style="width: 1.25rem; height: 1.25rem;" role="status"></div>');
    $.ajax({
      type: 'POST',
      url: "{% url 'users:login_api' %}",
      data: {
        email: $('#email').val(),
        password: $('#password').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
      success: function(data, textStatus, xhr) {
        console.log(data);
        if (xhr.status == 200) {
          $('#login').prop('disabled', false);
          $('#google-btn').prop('disabled', false);
          $("#login").html('<small>' + data.error + '</small>');
          setTimeout(function() {
            $("#login").html('Login');
          }, 2000);
        } else if (xhr.status == 202) {
          window.location.replace('/');
        }
      },
      error: function(xhr, errmsg, err) {
        $('#login').prop('disabled', false);
        $('#google-btn').prop('disabled', false);
        $("#login").html('<small>Something went wrong, try again later.</small>');
        setTimeout(function() {
          $("#login").html('Login');
        }, 2000);
      },
    });
  });