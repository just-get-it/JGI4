var acti = false
var profile_acti = document.getElementById('profile_acti');
var profile_data = document.getElementById('profile_data');
var profile_desc = document.getElementById('profile_desc');
var profile_noti = document.getElementById('profile_noti');
var profile_staff = document.getElementById('profile_staff');
var profile_vendor = document.getElementById('profile_vendor')
var profile_b2b = document.getElementById('profile_b2b');
var datahgf = false;
var desc = false;
var noti = false;
var staff = false;
var vendor = false;
var b2b = false;




function showtodayactivity() {
    profile_acti.classList.remove('hide_row');
    if (acti) {
        profile_acti.classList.add('hide_row');
    }
    if (datahgf) {
        profile_data.classList.add('hide_row');
    }
    if (desc) {
        profile_desc.classList.add('hide_row');
    }
    if (noti) {
        profile_noti.classList.add('hide_row');
    }
    if (staff) {
        profile_staff.classList.add('hide_row');
    }
    if (vendor) {
        profile_vendor.classList.add('hide_row');
    }
    if (b2b) {
        profile_b2b.classList.add('hide_row');
    }
    acti = true
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/',
        data: {
            profile_activity_ajax: true,
            profile_activity_ajax_cate: 'today',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = `<div class="container">
				<div class="row">
					<h3 class="fontcabin">Activities</h3>
					<!-- <a href="/userdetail/staff_profile/activities" style="margin-left: auto" class="hov-a">Show All</a> -->
				</div>
				<div class="row mt-2">`;
            if (data.bol) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="col-12 mt-2">
							<h6><b>Order No</b> - ` + value[0].order + `</h6>
							<table style="width: 100%" class="acti_table">
								<tr>
									<th>Activity Title</th>
									<th>Created Date</th>
									<th>Lap</th>
									<th>Planned Date</th>
									<th>Custom Lap</th>
									<th>Custom Date</th>
									<th>Status of Activity</th>
									<th>Actual Date</th>
								</tr>`;
                });
                alert(ht);
                $('#profile_acti').html(ht);
            } else {

                $('#profile_acti').html(ht);
            }
        }
    });
}



function showupdateresp() {
    var up = document.getElementById('update_resp');
    up.classList.remove('hide_row');
}

function remupresp() {

    var up = document.getElementById('update_resp');
    up.classList.add('hide_row');
}



function showupdatebudget() {
    var up = document.getElementById('update_budget');
    up.classList.remove('hide_row');
}

function remupbudget() {

    var up = document.getElementById('update_budget');
    up.classList.add('hide_row');
}






$('#run_sector_filter').on('change', function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile',
        data: {
            sector_update_ajax: $('#run_sector_filter').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('graph_content');
            a.innerHTML = data;
            hideLoader();
        }
    });
});


$('#budget_sector_years').on('change', function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/',
        data: {
            sector_year_update_ajax: $('#run_sector_filter').val(),
            sector_year_ajax: $('#budget_sector_years').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: true,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('graph_content');
            a.innerHTML = data;
            var b = document.getElementById('async_code');
            eval(b.innerHTML);
            hideLoader();
        }
    });
});



$('#run_year_filter').on('change', function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/',
        data: {
            sector_mode_update_ajax: $('#run_sector_filter').val(),
            sector_mode_year_ajax: $('#budget_sector_years').val(),
            sector_mode_ajax: $('#run_year_filter').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: true,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('graph_content');
            a.innerHTML = data;
            var b = document.getElementById('async_code');
            eval(b.innerHTML);
            hideLoader();
        }
    });
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/',
        data: {
            sector_mode_custom_ajax: $('#run_year_filter').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: true,
        dataType: "json",
        success: function(data) {
            var a = document.getElementById('budget_custom');
            ht = ``;
            for (i = 0; i < data.sub.length; i++) {
                ht += `<option value="` + data.sub[i] + `">` + data.sub[i] + `</option>`;
            }
            a.innerHTML = ht;
            hideLoader();
        }
    });
});



$('#budget_custom').on("change", function() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/staff_profile/',
        data: {
            sector_custom_update_ajax: $('#run_sector_filter').val(),
            sector_custom_year_ajax: $('#budget_sector_years').val(),
            sector_custom_mode_ajax: $('#run_year_filter').val(),
            sector_custom_ajax: $('#budget_custom').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: true,
        dataType: "html",
        success: function(data) {
            var a = document.getElementById('graph_content');
            a.innerHTML = data;
            var b = document.getElementById('async_code');
            eval(b.innerHTML);
            hideLoader();
        }
    });
});