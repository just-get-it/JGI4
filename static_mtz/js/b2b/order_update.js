





// $('#season_label').on('change',function(){
// 	$.ajax({
// 		type:'POST',
// 		url:'/userdetail/seller_profile/',
// 		data:{
// 			season_ajax_label:$('#season_label').val(),
// 			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
// 		},
//     	cache:false,
//     	dataType: "json",
// 		success:function(data) {
// 			var ht="";
// 			if (data.data[0].name){
// 			$.each(data.data,function(index,value){
// 				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
// 			});
// 			$('#season_fit').html(ht);
// 			}
// 			else{
// 				alert("You must have add corresponding Fit for the Label");
// 			}
// 		}
// 	});
// });

$('#brand_ajax').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder',
		data:{
			placeorder_ajax_brand:$('#brand_ajax').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option value="" disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
			});
			$('#label').html(ht);
			}
			else{
				$('#label').html(ht);
				$('#fit').html(ht);
				$('#season').html(ht);
			}
		}
	});
});







$('#label').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder',
		data:{
			placeorder_ajax_label:$('#label').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option value="" disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
			});
			$('#fit').html(ht);
			}
			else{
				$('#fit').html(ht);
				$('#season').html(ht);
			}
		}
	});
});







$('#fit').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder',
		data:{
			placeorder_ajax_fit:$('#fit').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option value="" disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
			});
			$('#season').html(ht);
			}
			else{
				$('#season').html(ht);
			}
		}
	});
});








$('#category').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder',
		data:{
			placeorder_ajax_category:$('#category').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option value="" disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.name+`">`+value.name+`</option>`
			});
			$('#sub_category').html(ht);
			}
			else{
				$('#sub_category').html(ht);
				$('#super_category').html(ht);
			}
		}
	});
});









$('#sub_category').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder',
		data:{
			placeorder_ajax_sub_category_category:$('#category').val(),
			placeorder_ajax_sub_category:$('#sub_category').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option value="" disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.name+`">`+value.name+`</option>`
			});
			$('#super_category').html(ht);
			}
			else{
				$('#super_category').html(ht);
			}
		}
	});
});






// $('#season').on('change',function(){
// 	$.ajax({
// 		type:'POST',
// 		url:'/buisness/order_update',
// 		data:{
// 			placeorder_ajax_season:$('#season').val(),
// 			placeorder_ajax_season_brand:$('#brand_ajax').val(),
// 			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
// 		},
//     	cache:false,
//     	dataType: "json",
// 		success:function(data) {
// 			var ht='<option value="" disabled selected>------</option>';
// 			if (data.bol){
// 			$.each(data.data,function(index,value){
// 				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
// 			});
// 			$('#size_ajax').html(ht);
// 			}
// 			else{
// 				$('#size_ajax').html(ht);
// 			}
// 		}
// 	});
// });

// 
// $('#size_by_sizeset').on('input',function(){
// 	$.ajax({
// 		type:'POST',
// 		url:'/buisness/order_update/{{order.order_no}}',
// 		data:{
// 			placeorder_ajax_sizeset:$('#size_by_sizeset').val(),
// 			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
// 		},
//     	cache:false,
//     	dataType: "json",
// 		success:function(data) {
// 			var ht="Sorry this Size does not exist !! (Try between 28 to 48 (even))";
// 			if (data.bol){
// 				ht=`<table class="meas_chart mt-4 mb-2" style="width:50%;margin-left:25%;">
// 				<tr>
// 				<th>Brand(`+data.size+`)</th>
// 				<th>Data</th>
// 				<tr>`
// 				$.each(data.kh,function(index,value){
// 				ht=ht+`<tr>
// 				<th>`+value.label+`</th>
// 				<td>`+data.li[index]+`</td>
// 				</tr>`
// 				});
// 				ht=ht+"</table>"
// 				$('#table_sizeset').html(ht);
// 			}
// 			else{
// 				$('#table_sizeset').html(ht);
// 			}
// 		}
// 	});
// });
