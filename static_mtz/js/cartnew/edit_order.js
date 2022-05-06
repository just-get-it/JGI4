// CURRWORK
function orderUpdate(Oid, value) {
    console.log('CALLED');
    total_element = document.getElementById(Oid + "-total");
    // total_cart_items = document.getElementById('total_cart_items');
    cart_total = document.getElementById("total");
    message=document.getElementById(Oid+"-message");
    $.ajax({
        type: 'POST',
        url: '/cartnew/update/',
        data: {
            'action': 'update',
            'Oid': Oid,
            'quantity': value,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log(data);
            total_element.innerText = "₹" + data["itemTotal"];
            cart_total.innerHTML = "<h5>Total: ₹"+ data['cartTotal'] +"/-</h5>";
            // total_cart_items.innerText = data["cartItems"];
            message.innerText = "Changes have been saved"
        }
    });
}

function deleteOrderItem(Oid) {

    $.ajax({
        type: 'POST',
        url: 'update_existing_order',
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

function quickAddToCart(slug) {
    var quant = 1;
    $.ajax({
        type: 'POST',
        url: '/cartnew/update/',
        data: {
            'action': 'add',
            'product': slug,
            'quantity': quant,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log(data);
            cartItemSpan = document.getElementById("total_cart_items");
            cartItemSpan.innerText = data['cartItems'];
        }
    });
}

function addToCart(slug) {
    var quant = document.getElementById('quantity').value;
    if (quant == "") {
        quant = 1
    } else {
        quant = parseInt(quant);
    }

    $.ajax({
        type: 'POST',
        url: '/cartnew/update/',
        data: {
            'action': 'add',
            'product': slug,
            'size': selected_size,
            'color': selected_color,
            'quantity': quant,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log(data);
            cartItemSpan = document.getElementById("total_cart_items");
            cartItemSpan.innerText = data['cartItems'];
        }
    });
}

function getCartItems(callback) {

    $.ajax({
        type: 'POST',
        url: '/cartnew/update/',
        data: {
            'action': 'get',
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            console.log("THIS IS CARITEMS RETURN: " + data);
            var no_of_items = data["cartItems"];
            console.log("THIS IS NO OF ITEMS: " + no_of_items);
            console.log(data);
            callback(no_of_items);
        }
    });
}