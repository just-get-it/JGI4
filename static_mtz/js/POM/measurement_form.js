




// $(document).on('submit','#addlabel_form',function(e){
// 	e.preventDefault();


// 	$.ajax({
// 		type:'POST',
// 		url:'/userdetail/seller_profile/',
// 		data:{
// 			label:$('#label_input_field').val(),
// 			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
// 		},
// 		success:function(){
// 			location.reload(true);
// 		}
// 	});
// });




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




$('#measurement_label').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/measurements_form/',
		data:{
			measurement_ajax_label:$('#measurement_label').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		cache:false,
		dataType:"json",
		success:function(data){
			var ht='<option value="" disabled selected>------</option>';
			// console.log(data.bol);
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
			});
			$('#measurement_fit').html(ht);
			}
			else{
				$('#measurement_fit').html(ht);
				$('#measurement_season').html(ht);
			}
		}
	});
});







$('#measurement_fit').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/measurements_form/',
		data:{
			measurement_ajax_fit_label:$('#measurement_label').val(),
			measurement_ajax_fit:$('#measurement_fit').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		cache:false,
		dataType:"json",
		success:function(data){
			var ht='<option value="" disabled selected>------</option>';
			// console.log(data.bol);
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
			});
			$('#measurement_season').html(ht);
			}
			else{
				$('#measurement_season').html(ht);
			}
		}
	});
});










$('#measurement_category').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/measurements_form/',
		data:{
			measurement_ajax_category:$('#measurement_category').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		cache:false,
		dataType:"json",
		success:function(data){
			var ht='<option value="" disabled selected>------</option>';
			// console.log(data.bol);
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.name+`">`+value.name+`</option>`
			});
			$('#measurement_subcategory').html(ht);
			}
			else{
				$('#measurement_subcategory').html(ht);
				$('#measurement_supercategory').html(ht);
			}
		}
	});
});







$('#measurement_subcategory').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/measurements_form/',
		data:{
			measurement_ajax_subcategory_category:$('#measurement_category').val(),
			measurement_ajax_subcategory:$('#measurement_subcategory').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		cache:false,
		dataType:"json",
		success:function(data){
			var ht='<option value="" disabled selected>------</option>';
			// console.log(data.bol);
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.name+`">`+value.name+`</option>`
			});
			$('#measurement_supercategory').html(ht);
			}
			else{
				$('#measurement_supercategory').html(ht);
			}
		}
	});
});









$('#measurement_supercategory').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/measurements_form/',
		data:{
			measurement_ajax_supercategory_category:$('#measurement_category').val(),
			measurement_ajax_supercategory_subcategory:$('#measurement_subcategory').val(),
			measurement_ajax_supercategory:$('#measurement_supercategory').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
		cache:false,
		dataType:"json",
		success:function(data){
			var ht='';
			console.log(data.bol);
			if (data.bol){
				$.each(data.data,function(index,value){
					ht=ht+`<div class="row mb-4">
				<div class="col-3 centered">
					<h6><b>`+value.label+`</b></h6>
				</div>
				<div class="col-3 centered">
					<input type="number" name="attribute`+(index+1)+`" step="0.01" class="attri_input" required>
				</div>
				<div class="col-3 centered">
					<input type="number" name="grading`+(index+1)+`" step="0.01" class="attri_input" required>
				</div>
				<div class="col-3 centered">
					<input type="number" name="tolerance`+(index+1)+`" step="0.01" class="attri_input" required>
				</div>
			</div>`;
				});
				$('#POM_fields').html(ht);
			}
			else{
				ht="<b>Sorry No Points of Measurements are created by admin for this Category of Products</b>"
				$('#POM_fields').html(ht);
			}
		}
	});
});