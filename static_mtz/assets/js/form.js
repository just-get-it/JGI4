filecount = 1

filecount2 = 1

function upload() {
    var form = document.getElementById('form');
    var formdata = new FormData(form);
    var url1 = "/daily_report/upload/" + String(filecount);
    $.ajax({
        url: url1,
        type: "POST",
        data: formdata,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            filecount = filecount + 1;
        }
    });
    return true;
}

function upload2() {
    var form = document.getElementById('form');
    var formdata = new FormData(form);
    var url1 = "/daily_report/upload2/" + String(filecount2);
    $.ajax({
        url: url1,
        type: "POST",
        data: formdata,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            filecount2 = filecount2 + 1;
        }
    });
    return true;
}


function deletefile(event) {
    var unique_id1 = getCookie("unique_id");
    $(".pqrst").click(function () {
        $.ajax({
            url: "/daily_report/delete",
            type: "POST",
            data: {
                id_no: $(this).attr('id'),
                unique_id: unique_id1
            },
            success: function (data) { }
        });
    });
}


function deletefile2(event) {
    var unique_id1 = getCookie("unique_id");
    $(".pqrs").click(function () {
        $.ajax({
            url: "/daily_report/delete2",
            type: "POST",
            data: {
                id_no: $(this).attr('id'),
                unique_id: unique_id1
            },
            success: function (data) { }
        });
    });
}

function getCookie(name) {
    // Split cookie string and get all individual name=value pairs in an array
    var cookieArr = document.cookie.split(";");

    // Loop through the array elements
    for (var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split("=");

        /* Removing whitespace at the beginning of the cookie name
        and compare it with the given string */
        if (name == cookiePair[0].trim()) {
            // Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }

    // Return null if not found
    return null;
}




(function ($) {

    $.fn.time = function (options) {

        let start = false;
        let end = false;
        $('#start_time').on('change', function () {
            start = true;
            console.log("changed start")
            $('#end_time').on('change', function () {
                console.log("changed end")
                let number_of_hours = document.getElementById("number_of_hours")
                let start = document.getElementById("start_time")
                let end = document.getElementById("end_time")

                let h1 = Number(String(start.value).slice(0, 2));
                let h2 = Number(String(end.value).slice(0, 2));
                number_of_hours.value = String(h2 - h1);
            });
        });
    };
}(jQuery));


$(document).ready(function () {
    $('.fileUploader').time({
        MessageAreaText: "No files selected. Please select a file."
    });
});