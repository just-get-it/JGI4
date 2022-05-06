var labels = true;
var fits = false;
var seasons = false;
var washcare = false;
var trimcard = false;
var manual_docs = false;
var barcode = false;
var products = false;
var inventory = false;
var discounts = false;
var htm = false
var safety = false
var inventory_noti = false;
var garment_weight = false;
var labels_obj = document.getElementById('labels');
var fits_obj = document.getElementById('fits');
var seasons_obj = document.getElementById('seasons');
var washcare_obj = document.getElementById('washcare');
var trimcard_obj = document.getElementById('trimcard');
var manual_docs_obj = document.getElementById('manual_docs');
var barcode_obj = document.getElementById('barcode');
var products_obj = document.getElementById('products');
var inventory_obj = document.getElementById('inventory');
var discounts_obj = document.getElementById('discounts');
var htm_obj = document.getElementById('htm');
var safety_obj = document.getElementById('safety');
var inventory_noti_obj = document.getElementById('inventory_noti');
var garment_weight_obj = document.getElementById('garment_weight');
var address_obj = document.getElementById('address')
var tandc_obj = document.getElementById('tandc');
var carton_obj = document.getElementById('carton');

function showLoader() {
    var processing = document.getElementById('processing');
    processing.style.display = "block";
}




function hideLoader() {
    var processing = document.getElementById('processing');
    processing.style.display = "none";
}




function checkOff() {
    if (labels == true) {
        labels_obj.style.display = "none";
        labels = false
    }
    if (fits == true) {
        fits_obj.style.display = "none";
        fits = false
    }
    if (seasons == true) {
        seasons_obj.style.display = "none";
        seasons = false;
    }
    if (washcare == true) {
        washcare_obj.style.display = "none";
        washcare = false;
    }
    if (trimcard == true) {
        trimcard_obj.style.display = "none";
        trimcard = false;
    }
    if (manual_docs == true) {
        manual_docs_obj.style.display = "none";
        manual_docs = false;
    }
    if (barcode == true) {
        barcode_obj.style.display = "none";
        barcode = false;
    }
    if (products == true) {
        products_obj.style.display = "none";
        products = false;
    }
    if (inventory == true) {
        inventory_obj.style.display = "none";
        inventory = false;
    }
    if (discounts == true) {
        discounts_obj.style.display = "none";
        discounts = false
    }
    if (htm == true) {
        htm_obj.style.display = "none";
        htm = false
    }
    if (safety == true) {
        safety_obj.style.display = "none";
        htm = false
    }
    if (garment_weight == true) {
        garment_weight_obj.style.display = "none";
        garment_weight = false;
    }
    if (address == true) {
        address_obj.style.display = "none";
        address = false;
    }
    if (tandc == true) {
        tandc_obj.style.display = "none";
        tandc = false;
    }
    if (carton == true) {
        carton_obj.style.display = "none";
        carton = false;
    }
}


function showinventory_noti() {
    showLoader();
    // $.ajax({
    // 	type:'POST',
    // 	url:'/userdetail/seller_profile/store',
    // 	data:{
    // 		labels_ajax:true,
    // 		csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    // 	},
    // 	cache:false,
    // 	dataType: "json",
    // 	success:function(data){
    // 		var ht='';
    // 		if (data){
    // 			$.each(data.data,function(index,value){
    // 				ht=ht+`<div class="row mt-3 pb-2 contents">
    // 			<div class="col-1">
    // 				`+value.index+`
    // 			</div>
    // 			<div class="col-3">
    // 				`+value.name+`
    // 			</div>
    // 			<div class="col">
    // 				`+value.slug+`
    // 			</div>
    // 		</div>`;
    // 			});
    // 			$('#labels_content').html(ht);
    // 		}
    // 		hideLoader();
    // 	}
    // });
    checkOff();
    hideLoader();
    inventory_noti_obj.style.display = "block";
    inventory_noti = true;

}

function showgarment_weight() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            garment_weight_objs_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.cate + `
				</div>
				<div class="col">
					` + value.sup_cate + `
				</div>
				<div class="col">
					` + value.size + `
				</div>
				<div class="col">
					` + value.weight + ` gram
				</div>
			</div>`;
                });
                $('#garment_weight_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    garment_weight_obj.style.display = "block";
    garment_weight = true;
}

function showtrim() {
    showLoader();
    hideLoader();
    checkOff();
    trimcard_obj.style.display = "block";
    trimcard = true;
}

function showmanualdocs() {
    showLoader();
    hideLoader();
    checkOff();
    manual_docs_obj.style.display = "block";
    manual_docs = true;
}


function showlabels() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            labels_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                console.log('THIS IS DATA: ' + data);
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col">
					` + value.slug + `
				</div>
			</div>`;
                });
                $('#labels_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    labels_obj.style.display = "block";
    labels = true;

}



function showsafety() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            safety_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col">
					` + value.cate + `
				</div>
				<div class="col">
					` + value.subcate + `
				</div>
				<div class="col">
					` + value.supcate + `
				</div>
				<div class="col">
					` + value.limit + `
				</div>
			</div>`;
                });
                $('#safety_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    safety_obj.style.display = "block";
    safety = true;

}



function showfits() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            fits_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + (parseInt(index) + parseInt(1)) + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col-3">
					` + value.label + `
				</div>
				<div class="col">
					` + value.slug + `
				</div>
				</div>`;
                });
                $('#fits_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    fits_obj.style.display = "block";
    fits = true;

}


function showseasons() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            seasons_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col-3">
					` + value.label + `
				</div>
				<div class="col-3">
					` + value.fit + `
				</div>
				<div class="col"></div>
				</div>`;
                });
                $('#seasons_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    seasons_obj.style.display = "block";
    seasons = true;
}


function showwashcare() {
    showLoader();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            washcare_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					<a href="/userdetail/seller_profile/washcare/` + value.id + `" class="hov-a">` + value.name + `</a>
				</div>
				<div class="col-3">
					` + value.category + `
				</div>
				<div class="col-3">
					` + value.super_category + `
				</div>
				<div class="col">
					` + value.blend + `
				</div>
				</div>`;
                });
                $('#washcare_content').html(ht);
            }
            hideLoader();
        }
    });
    checkOff();
    washcare_obj.style.display = "block";
    washcare = true;
}



function showbarcode() {
    showLoader();
    checkOff();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            barcode_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col-3">
					` + value.label + `
				</div>
				<div class="col-3">
					` + value.fit + `
				</div>
				<div class="col">
					` + value.season + `
				</div>
				</div>`;
                });
                $('#barcode_content').html(ht);
            }
            hideLoader();
        }
    });
    barcode_obj.style.display = "block";
    barcode = true;

}




function showhtm() {
    showLoader();
    checkOff();
    $.ajax({
        type: 'POST',
        url: '/userdetail/seller_profile/store',
        data: {
            htm_ajax: true,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        cache: false,
        dataType: "json",
        success: function(data) {
            var ht = '';
            if (data) {
                $.each(data.data, function(index, value) {
                    ht = ht + `<div class="row mt-3 pb-2 contents">
				<div class="col-1">
					` + value.index + `
				</div>
				<div class="col-3">
					` + value.name + `
				</div>
				<div class="col-3">
					` + value.category + `
				</div>
				<div class="col-3">
					` + value.sub_category + `
				</div>
				<div class="col">
					` + value.super_category + `
				</div>
				<div class="col">
					<a href="` + value.file + `" class="hov-a">File</a>
				</div>
				</div>`;
                });
                $('#htm_content').html(ht);
            }
            hideLoader();
        }
    });
    htm_obj.style.display = "block";
    htm = true;
}


function showproducts() {
    showLoader();
    checkOff();
    hideLoader();
    products_obj.style.display = "block";
    products = true;
}

function showaddress() {
    showLoader();
    checkOff();
    hideLoader();
    address_obj.style.display = "block";
    address = true;
}


function showinventory() {
    showLoader();
    checkOff();
    hideLoader();
    inventory_obj.style.display = "block";
    inventory = true;
}


function showdiscounts() {
    showLoader();
    checkOff();
    discounts_obj.style.display = "";
    discounts = true;
}