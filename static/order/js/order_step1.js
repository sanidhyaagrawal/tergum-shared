$('#templateupload').submit(function(e) {
    e.preventDefault()
    $form = $(this)
    document.getElementById("add_to_order").disabled = true;
    var formData = new FormData(this);
    $("#add_to_order").html('<div class="spinner-border" style="width: 1.25rem; height: 1.25rem;" role="status"></div>');
    $.ajax({
      url: "/en/api/attchment_api",
      type: 'POST',
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
      success: function(data, textStatus, xhr) {
        if (xhr.status == 202) {
          $("#number_of_attachments").text(data.data.length);
          $('#add_to_order').prop('disabled', false);
          if (data.data.length > 0) {
            $('#continue-btn').prop('disabled', false);
          }
          $("#order_list").empty()
          $('#templateupload').each(function() {
            this.reset();
          });
  
          data.data.forEach(function(arrayItem) {
            $("#order_list").append("<p><strong>" + arrayItem.orignal_filename + "</strong></p><samll>" + arrayItem.word_count + " words </samll><button class='tn btn-danger btn-sm' onclick='delete_attachment(" + '"' + arrayItem.attachment_id + '"' + ")'>Delete</button><hr>");
          });
  
          $("#add_to_order").html('Add to order');
          $("#add_to_order").html('<small>' + data.message + '</small>');
          setTimeout(function() {
            $("#add_to_order").html('Add to order');
          }, 2000);
        }
  
      },
      error: function(xhr, errmsg, err) {
        $('#add_to_order').prop('disabled', false);
        $("#add_to_order").html('<small>Something went wrong, try again later.</small>');
        setTimeout(function() {
          $("#add_to_order").html('Add to order');
        }, 2000);
      },
  
    });
  });
  
  
  
  function delete_attachment(attachment_id) {
    $("#add_to_order").html('<div class="spinner-border" style="width: 1.25rem; height: 1.25rem;" role="status"></div>');
  
    $.ajax({
      type: 'DELETE',
      url: "/en/api/attchment/" + attachment_id,
      success: function(data, textStatus, xhr) {
        if (xhr.status == 202) {
          $("#number_of_attachments").text(data.length);
          $('#add_to_order').prop('disabled', false);
          $('#continue-btn').prop('disabled', false);
          $("#order_list").empty()
  
          if (data.length == 0) {
            $('#continue-btn').prop('disabled', true);
          }
  
          data.forEach(function(arrayItem) {
            $("#order_list").append("<p><strong>" + arrayItem.orignal_filename + "</strong></p><samll>" + arrayItem.word_count + " words </samll><button class='tn btn-danger btn-sm' onclick='delete_attachment(" + '"' + arrayItem.attachment_id + '"' + ")'>Delete</button><hr>");
          });
  
          $("#add_to_order").html('Add to order');
  
        }
      },
      error: function(xhr, errmsg, err) {
        $("#continue-btn").html('<small>Something went wrong, try again later</small>');
        setTimeout(function() {
          $("#continue-btn").html('Add to order');
        }, 2000);
      },
    })
  }
  
  $('#continue-btn').click(function(e) {
    e.preventDefault();  
    job_id = $('input[name=job_id]').val(),
  
    $("#continue-btn").html('<div class="spinner-border" style="width: 1.25rem; height: 1.25rem;" role="status"></div>');
    $.ajax({
      type: 'PATCH',
      url: "/api/job/language",
      data: {
        job_id: job_id,
        source_language_id: $('#source_language').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
      },
  
      success: function(data, textStatus, xhr) {
        console.log(data);
        if (xhr.status == 202) {
          window.location.replace('/order/step-2/' + job_id);
        }
      },
      error: function(xhr, errmsg, err) {
        $("#continue-btn").html('<small>Something went wrong, try again later.</small>');
        setTimeout(function() {
          $("#continue-btn").html('Continue');
        }, 2000);
      },
    });
  });