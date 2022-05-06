filecount = 1

function upload(event) {
    var form = document.getElementById('form')
    var formdata = new FormData(form);
    var url1 = "/upload/" + String(filecount)
    $.ajax({
        url: url1,
        type: "POST",
        data: formdata,
        cache: false,
        processData: false,
        contentType: false,
        success: function(data) {
            alert('success');
            filecount = filecount + 1
        }
    });
    return false;
}

function deletefile(event) {
    var unique_id1 = getCookie("unique_id");
    $("button").click(function() {
        $.ajax({
            url: "/delete",
            type: "POST",
            data: {
                id_no: $(this).attr('id'),
                unique_id: unique_id1
            },
            success: function(data) {}
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