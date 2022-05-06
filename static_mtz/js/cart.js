var sum = 0;
var total = 0;
if (user == "AnonymousUser") {
  if (localStorage.getItem("cart") == null) {
    var cart = "{}";
    localStorage.setItem("cart", cart);
  } else {
    cart = JSON.parse(localStorage.getItem("cart"));
    updateCart(cart);
  }
}
for (var item in cart) {
  if (cart[item][2] == null) {
    delete cart[item];
  }
}
$(".cart").on("click", function () {
  var idstr = this.id.toString();
  var action = this.dataset.action;

  if (user == "AnonymousUser") {
    // console.log("user:", user);
    if (cart[idstr] != undefined) {
      cart[idstr][0] += 1; // if cart has item then +1
    } else {
      qty = 1;
      name = document.getElementById("name" + idstr).innerHTML; //namepr1 id given to card title
      price = document.getElementById("price" + idstr).innerHTML;
      cart[idstr] = [qty, name, parseInt(price.slice(3))];
    }
    updateCart(cart);
  } else {
    updateuserorder(idstr, action, user);
  }
});

function updateuserorder(productId, action, user) {
  //console.log("user log in:",user)
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action, user: user }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}

function updateCart(cart) {
  sum = 0;
  total = 0;
  for (var item in cart) {
    if (cart[item][0] == 0) {
      //document.getElementById('div'+item).innerHTML='<button id="'+ item +'" class="btn-sm btn-dark cart"><b>Add to Cart</b></button>';
      delete cart[item];
      continue;
    }
    var itemprice = cart[item][2];
    var itemqty = cart[item][0];
    var itemtotal = itemqty * itemprice;
    sum += cart[item][0];
    total += itemtotal;
  }
  //   document.getElementById("popcart").innerHTML = "Cart(" + sum + ")";
  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartView(cart);
}

function updateCartView(cart) {
  // console.log("updateCartView");
  if (
    sum != 0 &&
    document.getElementById("totalcartitems") != null &&
    document.getElementById("totalcarprice") != null
  ) {
    document.getElementById("totalcartitems").innerHTML = "" + sum;
    //console.log(total);
    document.getElementById("totalcarprice").innerHTML = " Rs. " + total;
  }
  for (var item in cart) {
    var itemname = cart[item][1];
    var itemprice = cart[item][2];
    var itemqty = cart[item][0];
    var itemtotal = itemqty * itemprice;
    var str =     
    `<style>
    .add{		
      border: none;
      border-radius:50%  ;
      background-color: transparent;

    }
    .add:hover{
      background-color: #1dd1a1;
    }
    .minus{
      border: none;
      border-radius:50%;
      background-color: transparent;
    }
    .minus:hover{
      background-color: #ff6b6b;
    }
    .text_box{
      border: none;
      background-color: #e1f1f1;
      text-align: center;
    }
    .delete_btn{
      border: none;
      background-color: transparent;
    }
  </style>

  <div class="box-element container d-none d-lg-block">
            <div class="cart-row">
                            <div style="flex:2"></div>
                            <div style="flex:2"><strong>Items</strong></div>
                            <div style="flex:1"><strong>Price</strong></div>
                            <div style="flex:1"><strong>Quantity</strong></div>
                            <div style="flex:1"><strong>Total</strong></div>
            </div>
            <div class="cart-row">
    				<div style="flex:2 " ><img class="row-image" src="{{item.product.image1.url}}"></div>
    				<div style="flex:2"><p>${itemname}</p></div>
    				<div style="flex:1"><p name="price" id="price+${item}" style="display:inline">Rs. ${itemprice}</p></div>
    				<div style="flex:1">
                       <!-- <p class="quantity">${itemqty}</p> -->
                        <div class="quantity">
                        <img data-product="${item}" data-action="remove"  id="remove${item}" name="remove${item}" class=" minus"  style="display: inline;width: 18px;" alt="down" onclick="remQuant(${item})"src="https://cdn.iconscout.com/icon/free/png-64/minus-111-434087.png">
                        <input type="text" class="quantity text_box" id="${item}" name="${item}" value="${itemqty}" style="width: 50px;display: inline;">
                        <img data-product="${item}" data-action="add" id="add${item}" name="add${item}" class=" add" style="display: inline; width: 20px;" alt="up" onclick="addQuant(${item})"   src="https://cdn.iconscout.com/icon/free/png-64/add-insert-control-point-plus-31700.png">
							</div>

                        <div>
                            <span class="pl-4">
                            <button type="button" class=" btn deleteitem" id=${item} ><i class="far fa-trash-alt " style="color: crimson;"></i></button>
                            </span>
                        </div>
            </div>
    				<div style="flex:1"><p name="total" id="total+${item}"style="display: inline"> Rs. ${itemtotal}</p></div>
              </div>
  </div>            
              ` +
      `<div class="coniatner d-lg-none">
              <hr>
              <div class="row">
                <div class="col-4">
                  <div><img class="row-image" src="{{item.product.image1.url}}" alt="No image found"></div>
                </div>
                <div class="col-8">
                  <p><b>${itemname}</b></p>
                  <div class="row ">
                      <div class="pl-3 pb-3"><p name="price" id="price+${item}" style="display:inline"> <b> Rs.</b> <strong style="color:#27ae60;"> ${itemprice}</strong></p></div>
                  </div>
                  <div class="row ">
                    <div  class="col-8 p-2">
                      <img data-product="${item}" data-action="remove"  id="remove${item}" name="remove${item}" class="minus "  style="display: inline;width: 18px;" alt="down" onclick="remQuant(${item})"src="https://cdn.iconscout.com/icon/free/png-64/minus-111-434087.png">
                      <input type="text" class="quantity text_box" id="${item}" name="${item}" value="${itemqty}" style="width: 50px;display: inline;">
                      <img data-product="${item}" data-action="add" id="add${item}" name="add${item}" class="add " style="display: inline; width: 20px;" alt="up" onclick="addQuant(${item})"   src="https://cdn.iconscout.com/icon/free/png-64/add-insert-control-point-plus-31700.png">
                    </div>
                    <div class="col-4 p-0">
                    <span class="divbtn">
                      <button type="button" class="btn deleteitem" id=${item} ><i class="far fa-trash-alt " style="color: crimson;"></i></button>
                    </span>
                  </div>
                  </div>                  
                  </div>
              </div>

        </div>`;

    $("#anonymousitems").append(str);
  }
}

//var getQuoteButton = document.getElementsByClassName('deleteitem');
////getQuoteButton.onclick = myFunction;
//getQuoteButton.addEventListener("click", myFunction);
//function myFunction(i){
//console.log(i.toString());
//
////    delete cart[i];
////    updateCart(cart);
////    document.getElementById("anonymousitems").innerHTML="";
////    updateCartView(cart);
//}

$(".deleteitem").on("click", function () {
  var idd = this.id.toString();
  // console.log(idd);
  delete cart[idd];
  updateCart(cart);
  document.getElementById("anonymousitems").innerHTML = "";
  updateCartView(cart);
  location.reload();
});

function addwishlist(idstr) {
  console.log("called");
  var url = "/wishlists/";
  action = "add";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: idstr, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
    });
}
