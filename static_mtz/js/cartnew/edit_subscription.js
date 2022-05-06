function deleteSubscriptionItem(Oid) {

    $.ajax({
        type: 'POST',
        url: 'edit',
        data: {
            'action': 'delete',
            'Oid': Oid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log(data);
            location.reload();
        }
    });
}
function stopSubscriptionItem(Oid) {

    $.ajax({
        type: 'POST',
        url: 'edit',
        data: {
            'action': 'stop',
            'Oid': Oid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log(data);
            location.reload();
        }
    });
}