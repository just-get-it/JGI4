function addlabel() {
    lab = document.getElementById('addlabel');
    lab.style.display = "block";
}


function cross() {
    lab = document.getElementById('addlabel');
    lab.style.display = "none";
}



function crossfit() {
    lab = document.getElementById('addfit');
    lab.style.display = "none"
}


function addfit() {
    lab = document.getElementById('addfit');
    lab.style.display = "block";
}





function crossseason() {
    lab = document.getElementById('addseason');
    lab.style.display = "none"
}


function addseason() {
    lab = document.getElementById('addseason');
    lab.style.display = "block";
}

$(document).on('submit', '#addlabel_form', function(e) {
    e.preventDefault();


    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/',
        data: {
            label: $('#label_input_field').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function() {
            location.reload(true);
        }
    });
});




$('#season_label').on('change', function() {
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/',
        data: {
            season_ajax_label: $('#season_label').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '<option value="" disabled selected>------</option>';
            if (data.bol) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<option value="` + value.slug + `">` + value.name + `</option>`
                });
                $('#season_fit').html(ht);
            } else {

                $('#season_fit').html(ht);
            }
        }
    });
});