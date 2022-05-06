





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

$('#brand').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/buisness/placeorder/',
		data:{
			placeorder_ajax_brand:$('#brand').val(),
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
		url:'/buisness/placeorder/',
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
		url:'/buisness/placeorder/',
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
		url:'/buisness/placeorder/',
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
		url:'/buisness/placeorder/',
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

//to load style-component
$('#super_category').change(function(){
        $.ajax({
			type:'POST',
            cache:false,
            url:'/buisness/loadStyle',
            data:{
                'super_cate':$('#super_category').val(),
                 'category':$("#category").val(),
				 'sub_cate':$("#sub_category").val()
            },
            success:function(data){
                  console.log(data);
                 $("#load_components").html(data);
            }
        });
        $.ajax({
			type:'POST',
            cache:false,
            url:'/buisness/loadStyle',
            data:{
                'super_cate':$('#super_category').val(),
                 'category':$("#category").val(),
				 'sub_cate':$("#sub_category").val(),
				 'garment':true
            },
            success:function(data){
                  console.log(data);
                  $('#garment_matching_parameters').html(data);
            }
        });
});

$('.size_radio, input[type="radio"]').change(function(){
        sector=$("#sector").val();
        size=$(this).val();
        sizes=$("#size_id").val();
        colors=$("#color_id").val();
        if(sector){
            if(size=='Default'){
                $.ajax({
                    url:'/buisness/loadTable',
                    type:'POST',
                    cache:false,
                    dataType: "json",
                    data:{
                        'size':size,
                        'sector':sector,
                        'category':$("#category").val(),
                        'sub_cate':$("#sub_category").val(),
                        'super_cate':$("#super_category").val(),
                        'labels':$("#label").val(),
                        'fits':$("#fit").val()
                    },
                    success:function(data){
                        var hts='', i=0;
                        var htr=''
                        var table=''
                        var comb='<option value="" disabled selected>------</option>';
                        $.each(data.size, function(key, value){
                            hts=hts+`<td value='`+value.name+`'>`+value.name+`</td>`;
                            //console.log(hts);
                        });
                        $.each(data.ratio, function(key, value){
                            htr=htr+`<td value='`+value+`'>`+value+`</td>`;
                            //console.log(htr);
                        });
                        $.each(data.ratios, function(key, value){
                            value=JSON.stringify(value);
                            comb=comb+`<option value='`+value+`'>Ratio `+i+`</option>`
                            i=i+1;
                        });
                         table=`<table class="drop_third1" style="box-shadow: 0 0 1px black;background: transparent;margin-top: 1vh;width:100%;"><tr><th>SIZE</th>`+hts+`</tr><tr><th>RATIO</th>`+htr+`</tr></table>`
                         $("#id_sizeTable").html(table);
                         $("#id_combinations").html(comb);
                         if(data.consumption){
                            $('#table_fabric_consumption').val(data.consumption);
                         }else{$('#table_fabric_consumption').val(0);}
                         $("#id_combinations").prop('disabled', false);
                         //console.log(table);
                    }
                });
            }else{
                if(colors && sizes){
                    $('#fabric_consumption').val('0');
                    $("#id_combinations").prop('disabled', 'disabled');
                    var dispatch = new $("textarea[id='dispatch']").map(function(){return $(this).val();}).get();


                     console.log(dispatch)
                    $.ajax({
                        type:'POST',
                        url:'/buisness/loadStyle',
                        data:{
                            'size':size,
                            'color':colors,
                            'sizes':sizes,
                            'dispatch[]':dispatch
                        },
                        success:function(data){
                            $("#id_sizeTable").html(data);
                        }
                    });
                }else{
                    alert('One of the or both field color or sizes is empty'+'<br>'+'please fill them');
                    $(this).prop('checked', false);
                }
            }

        }else{
            alert("please select 'sector' section");
             $(this).prop('checked', false);
        }

});

$('#id_combinations').change(function(){
    values=$(this).val();
    var val =$.parseJSON(values);
    var ratio=val.ratio.split(',');
    var hts='', htr='', table='';
    $.each(val.size, function(key, value){
        hts=hts+`<td value='`+value.name+`'>`+value.name+`</td>`
    });
    $.each(ratio, function(key, value){
        htr=htr+`<td value='`+value+`'>`+value+`</td>`;
    });
    table=`<table class="drop_third1" style="box-shadow: 0 0 1px black;background: transparent;margin-top: 1vh;width:100%;"><tr><th>SIZE</th>`+hts+`</tr><tr><th>RATIO</th>`+htr+`</tr></table>`
    $("#id_sizeTable").html(table);
    $('#table_fabric_consumption').val(val.fabric_consumption);

});


$('#fabric_code').change(function(){
    $.ajax({
		url: '/buisness/autoFill',
		type:'POST',
		cache:false,
		data: {
			"fabric_code": $(this).val()
        },
        dataType: 'json',
        success: function(data) {
        $('#fabric_blend').val(data.fabric_blend);
        $('#epi').val(data.epi);
        $('#ppi').val(data.ppi);
        $('#gsm').val(data.gsm);
        $('#wrap').val(data.wrap);
        $('#weft').val(data.weft);
        $('#fabric_width').val(data.width);
        $('#fabric_supplier').val(data.supplier);
        $('#fabric_description').val(data.description);
        $('#finish').val(data.finish);
        $('#fabric_direction').val(data.fabric_direction);
        $('#fabric_print_type').val(data.fabric_print_type);
        $('#fabric_print_design').val(data.fabric_print_design);
    	},
    	error: function(data) {console.log('Data could not be retrieved')}
	});
	$.ajax({
		url:'/buisness/loadStyle',
	    type:'POST',
		cache:false,
		data:{
			'fabric_code':$(this).val()
		},
		success:function(data){
			$('#load_fabric').html(data);
		}
	});
});


$('#sector').change(function(){
    if ($(this).val() == 'add-sector') {
         $("#sector_id").html('<input value="" name="sector" id="sector" class="drop_half2"  placeholder="Enter sector name" style="box-shadow: 0 0 1px black;background: transparent;padding: .5vw;margin-top: 1vh;width:100%;">');
    }
});

$('#garment_matching_parameters').change(function(){
    $.ajax({
        url: '/buisness/loadStyle',
		type:'POST',
		cache:false,
		data: {
			'garment_matching_id': $(this).val()
        },
        dataType: 'json',
        success:function(data){
            var hts='<option value="" disabled selected>------</option>'
            $.each(data.level, function(key, value){
                hts=hts+`<option value='`+value+`'>`+value+`</option>`;
            });
            console.log(hts);
            $('#garment_matching_level').html(hts);
        }
    });
});

$('#garment_matching_level').change(function(){
    $.ajax({
        url: '/buisness/loadStyle',
		type:'POST',
		cache:false,
		data: {
		    'super_cate':$('#super_category').val(),
            'category':$("#category").val(),
			'sub_cate':$("#sub_category").val(),
			'garment_name': $(this).val()
        },
        dataType: 'json',
        success:function(data){
            var hts=''
            console.log(data);
            $.each(data.requirements, function(key, value){
                hts=hts+`<p>`+value+`</p>`;
            });
            console.log(hts);
            $('#garment_matching_requirements').html(hts);
        }
    });
});

$('#calculate_avg').click(function(){
    var poms = new $("select[id='poms']").map(function(){return $(this).val();}).get();
    var compo_data = new $("select[id='comp']").map(function(){return $(this).val();}).get();
    var manual_size_quantity= new $("input[name='size_quantity']").map(function(){return $(this).val();}).get();
    var manual_sizes= new $("select[name='size_assort']").map(function(){return $(this).val();}).get();
    var manual_colors= new $("select[name='size_color']").map(function(){return $(this).val();}).get();
    var manual_size_array= makearray(manual_size_quantity, manual_sizes, manual_colors);
    $.ajax({
        url:'/buisness/calculate_total_fabric_consumption',
        type:'POST',
        cache:false,
        data:{
            'components[]':compo_data,
            'poms_radio[]':poms,
            'trims_data':$('#fabric_code').val(),
            'size_pattern_manual_assortment[]':manual_size_array,
            'colors[]':manual_colors,
            'manual_sizes[]':manual_sizes,
            'manual_size_quantity[]':manual_size_quantity,
            'garment_matching_id':$('#garment_matching_parameters').val(),
            'garment_matching_level':$('#garment_matching_level').val(),
            'table_fabric_consumption':$('#table_fabric_consumption').val(),
            'repeat_size':$('#repeat_size').val(),
            'wastage':$('#wastage').val()
        },
        dataType:'json',
        success:function(data){
            $('#fabric_consumption').val(data.total);
        }
    });
});

function makearray(manual_size_quantity, manual_sizes, manual_colors){
    var manual_size_array= new Array();
    console.log(manual_sizes.length);
    for(var i=0; i<manual_sizes.length; i++){
        if(manual_sizes[i]){
            manual_size_array.push(manual_colors[i]+', '+manual_sizes[i]+', '+manual_size_quantity[i]);
        }

    }
    return manual_size_array;
}