function changeFormAfterSelect() {
  function newForm(data, fields, dict) {
    data = data[0].querySelector('form')
    selected_fields = ["type_of_operation"]
    for (var i = 0; i < fields.length; i++) {
      if (selected_fields.includes(fields[i])) {
        data.querySelector('select[name="' + fields[i] + '"]').value = dict[fields[i]];
        continue;
      }
      data.querySelector('input[name="' + fields[i] + '"]').value = dict[fields[i]];
    }
    return data
  }
  cur_form = event.srcElement.parentElement.parentElement.parentElement.parentElement.parentElement
  saved_fields = ["serial_number", "type_of_defect", "start_date", "end_date", "type_of_operation"]
  formCachdict = {}
  cur_form_d = new FormData(cur_form)
  for (var i = 0; i < saved_fields.length; i++) {

    formCachdict[saved_fields[i]] = cur_form_d.get(saved_fields[i]);
  }
  $.get('/mainapp/add/operation/tech/form/' + event.srcElement.value + '/').then(function(data) {
    $(cur_form).replaceWith(newForm($(data), saved_fields, formCachdict))
  })
}

function changeFormAfterbutton(quantity_of_fields, offset) {
  function newForm(data, dict) {
    data = data[0].querySelector('form')
    selected_fields = ["type_of_operation", "type_of_product"]
    for (key in dict) {
      if (selected_fields.includes(key)) {
        data.querySelector('select[name="' + key + '"]').value = dict[key];
        continue;
      }
      try {
        data.querySelector('input[name="' + key + '"]').value = dict[key];
      } catch (e) {
        continue;

      }
    }
    return data
  }
  cur_form = event.srcElement.parentElement.parentElement.parentElement.parentElement.parentElement
  console.log(cur_form)
  formCachdict = {}
  except_fields = ["csrfmiddlewaretoken"]
  cur_form_d = new FormData(cur_form)
  for (var key of cur_form_d.keys()) {
    if (except_fields.includes(key)) {
      continue;
    }
    formCachdict[key] = cur_form_d.get(key);
  }
  $.get('/mainapp/add/operation/assembly/form/' + (quantity_of_fields + offset) + '/').then(function(data) {
    $(cur_form).replaceWith(newForm($(data), formCachdict))
  })
}

function AddRow(url) {
  $.ajax({
    url: url,
    success: function(data) {
      $('#add_form').append(data);
      lenght_of_elem = document.getElementById("add_form").querySelectorAll("div").length
      document.getElementById("add_form").querySelectorAll("div")[lenght_of_elem - 1].setAttribute('id', lenght_of_elem)
    }
  });
}

function DeleteRow() {
  var forms = document.getElementById("add_form")
  var list_elem = forms.querySelectorAll("div");
  list_elem[list_elem.length - 1].remove()
}

function AddCharForm() {
  var form_idx = $('#id_form-TOTAL_FORMS').val();
  $('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
  $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
}

function RemoveCharForm() {
  var form_idx = $('#id_form-TOTAL_FORMS').val();
  last_elem = document.getElementById('form_set').querySelectorAll("#form_set > table").length
  document.getElementById('form_set').querySelectorAll("#form_set > table")[last_elem - 1].remove()
  $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) - 1);
}

function SaveForms() {
  Can_i_redirect = 0
  $('.allforms').each(function() {
    valuesToSend = $(this).serialize();
    form_id = $(this).find('button');
    $.ajax($(this).attr('action'), {
      method: $(this).attr('method'),
      data: valuesToSend,
      context: this,
      async: false,
      success: function(data) {
        console.log(data.slice(13, -6))
        console.log(data.indexOf('errorlist'))
        if (data.indexOf('error') != -1) {
          $(this).replaceWith(data.slice(13, -6));
        } else {
          console.log("Элемент должен быть удален")
          $(this).remove();
        }
      }
    });
  });
}
