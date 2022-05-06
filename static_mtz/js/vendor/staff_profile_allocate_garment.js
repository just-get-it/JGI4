




function float_order(email_i,order_no){
		$.ajax({
			type:'POST',
			url:'/userdetail/staff_profile/orders/'+order_no.toString()+'/allocate_garment',
			data:{
				email_ajax_float:email_i,
				csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
			},
	    	cache:false,
	    	dataType: "json",
			success:function(data) {
				if (data.bol){
					alert("Order Floated !");
				}
				else{
					alert("Order Already Floated !");
				}
			}
		});
	}