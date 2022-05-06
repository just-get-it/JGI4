// CURRWORK
function cartUpdate(Oid, value) {
    console.log('CALLED');
    total_element = document.getElementById(Oid + "-cartItem");
    total_cart_items = document.getElementById('total_cart_items');
    cart_total = document.getElementById("cart_total");
    free_delivery = document.getElementById("free-delivery")
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
            cart_total.innerText = "Total: ₹" + data["cartTotal"] + "/-";
            if((data['cartTotal'])>10000){
                       free_delivery.innerHTML= "<p>You are eligible for free delivery</p>"
            } else {
                free_delivery.innerHTML = "<p>You are not eligible for free delivery</p>"
            }
        }
    });
}

function deleteCart(Oid) {
    $.ajax({
        type: 'POST',
        url: '/cartnew/update/',
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

function addToB2BCart(slug) {
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
            'sizes': JSON.stringify(selectedB2Bsizes),

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