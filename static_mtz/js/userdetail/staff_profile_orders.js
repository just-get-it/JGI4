









$('#season_label').on('change',function(){
	// $.ajax({
	// 	type:'POST',
	// 	url:'/userdetail/seller_profile/',
	// 	data:{
	// 		season_ajax_label:$('#season_label').val(),
	// 		csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
	// 	},
 //    	cache:false,
 //    	dataType: "json",
	// 	success:function(data) {
	// 		var ht='<option value="" disabled selected>------</option>';
	// 		if (data.bol){
	// 		$.each(data.data,function(index,value){
	// 			ht=ht+`<option value="`+value.slug+`">`+value.name+`</option>`
	// 		});
	// 		$('#season_fit').html(ht);
	// 		}
	// 		else{

	// 			$('#season_fit').html(ht);
	// 		}
	// 	}
	// });
	window.location='/userdetail/staff'
});


var anarray=[];
var counter=0;

function showSubActi(x){
		var get_div=document.getElementById('sub_acti'+x.toString())

		var plus=document.getElementById('plus'+x.toString());
		if (get_div.style.display==="block"){
				get_div.style.display="none";
				counter=counter-1;
		}
		else{
			get_div.style.display="block";
			anarray[counter]=get_div;
			counter=counter+1;
		}
		for(i=0;i<counter-1;i++){
			anarray[i].style.display="none";
		}


}
