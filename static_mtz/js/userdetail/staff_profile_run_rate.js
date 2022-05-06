$('#year_mode').on("change", function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/run-rate',
        data: {
            year_mode_ajax: $('#year_mode').val(),
            year_ajax: $('#years').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('content');
            a.innerHTML = data;
            hideLoader();
        }
    });
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/run-rate',
        data: {
            year_mode_ajax: $('#year_mode').val(),
            get_sub_year: true,
            year_ajax: $('#years').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var a = document.getElementById('sub_years');
            ht = `<option disabled selected>------------</option>`;
            for (i = 0; i < data.sub.length; i++) {
                ht += `<option value="` + data.sub[i] + `">` + data.sub[i] + `</option>`;
            }
            a.innerHTML = ht;
            hideLoader();
        }
    });
});



$('#years').on("change", function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/run-rate',
        data: {
            years_ajax: $('#years').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('content');
            a.innerHTML = data;
            hideLoader();
        }
    });
});



$('#years').on("change", function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/run-rate',
        data: {
            years_ajax: $('#years').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('content');
            a.innerHTML = data;
            hideLoader();
        }
    });
});


$('#sub_years').on("change", function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/run-rate',
        data: {
            sub_years_ajax: $('#sub_years').val(),
            sub_years_year_ajax: $('#years').val(),
            sub_years_mode_ajax: $('#year_mode').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('content');
            a.innerHTML = data;
            hideLoader();
        }
    });
});