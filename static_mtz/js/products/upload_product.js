






var sizes="<option disabled selected>---------------</option>"








$('#brand_ajax').on("change",function(){
	// alert("Done");
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			brand_ajax_cate:$('#brand_ajax').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
  		cache:false,
  		dataType: "json",
		success:function(data){
			var ht='<option disabled selected>---------------</option>';
			if (data.bol){
				$.each(data.data,function(index,value){
					ht=ht+`<option value="`+value.id+`">`+value.name+`</option>`;
				});
				$('#brand_label').html(ht);
			}
		}
	});
});


function select_subcate(id){
	var id1=parseInt(id,10);
	var input_cate=document.getElementById('input_cate');
	input_cate.value=id;
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			id_ajax_cate:id1,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var prod=document.getElementsByClassName('prod_cate');
			for (i=0;i<prod.length;i++){
				prod[i].classList.add('redu_hei');
				// prod[i].classList.add('opazero');
				setTimeout(function(i){ prod[i].classList.add('opazero'); }.bind(this, i), 1000);
			}


			var ht='';
			if (data.bol){
			$.each(data.data,function(index,value){

				ht=ht+`<div class="col-3 mb-4 prod_subcate" onclick="select_supcate('`+value.id+`','`+id1+`');">
				<img src="`+'/media/'+value.image+`">
				<div class="overlay"></div>
				<div class="overlay_cate">
					<button>`+value.name+`</button>
				</div>
			</div>`
			});
			$('#prod_subcate').html(ht);
			$('#head_upload').html("Select Sub-Category of Product");
			}
			else{

				$('#prod_subcate').html(ht);
			}
		}

	});
}




function select_supcate(id,cate_id){
	var id1=parseInt(id,10);
	var cate_id1=parseInt(cate_id,10);

	var input_subcate=document.getElementById('input_subcate');
	input_subcate.value=id;
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			id_ajax_subcate:id1,
			id_ajax_subcate_cate:cate_id1,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var prod=document.getElementsByClassName('prod_subcate');
			for (i=0;i<prod.length;i++){
				prod[i].classList.add('redu_hei');
				// prod[i].classList.add('opazero');
				setTimeout(function(i){ prod[i].classList.add('opazero'); }.bind(this, i), 1000);
			}


			var ht='';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<div class="col-3 mb-4 prod_supcate" onclick="select_supcate_oi('`+value.id+`');">
				<img src="`+'/media/'+value.image+`">
				<div class="overlay"></div>
				<div class="overlay_cate">
					<button>`+value.name+`</button>
				</div>
			</div>`
			});
			$('#prod_supcate').html(ht);
			$('#head_upload').html("Select Category of Product");
			}
			else{

				$('#prod_supcate').html(ht);
			}
		}

	});
}



function select_supcate_oi(id){

	var id1=parseInt(id,10);
	//console.log('I was called');
	var input_supcate=document.getElementById('input_supcate');
	input_supcate.value=id;
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			id_ajax_supcate:id1,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var prod=document.getElementsByClassName('prod_supcate');
			for (i=0;i<prod.length;i++){
				prod[i].classList.add('redu_hei');
				// prod[i].classList.add('opazero');
				setTimeout(function(i){ prod[i].classList.add('opazero'); }.bind(this, i), 1000);
			}



			var left=document.getElementsByClassName('to_be_hidden');
			for (i=0;i<left.length;i++){
				left[i].classList.remove('hide');
			}
			//console.log(data.reqs[3]);

		

			var ht='';
			if (data.bol){
				//console.log(data.labels);
			for (i=0;i<data.labels.length;i++){
				var labl="label";
				var lb=labl.concat((data.labels[i]).toString());
				var id=document.getElementById(lb);
				id.style.display='block';
			}


			if(data.reqs[0]==false){
				var element=document.getElementById("unitsection");
				element.style.display='none';
			}
			if(data.reqs[1]==false){
				var element=document.getElementById("colorsection");
				element.style.display='none';
			}
			if(data.reqs[2]==false){
				var element=document.getElementById("pricesection");
				element.style.display='none';
			}
			if(data.reqs[3]==false){
				//console.log('here');
				var element=document.getElementById("stocksection");
				element.style.display='none';
			}
			if(data.reqs[4]==false){
				//console.log('here');
				var element=document.getElementById("brandsection");
				element.style.display='none';
				var element=document.getElementById("otherbrands");
				element.style.display="none";
				var ele=document.getElementById("brandother");
				ele.style.display="block";

			}
			if(data.reqs[5]==false){
				//console.log('here');
				var element=document.getElementById("labelsection");
				element.style.display='none';
			}
			if(data.reqs[6]==false){
				//console.log('here');
				var element=document.getElementById("uploads");
				element.style.display='none';
			}
			if(data.reqs[7]==false){
				//console.log('here');
				var element=document.getElementById("variations");
				element.style.display='none';
			}
			if(data.reqs[8]==false){
				//console.log('here');
				var element=document.getElementById("sizers");
				element.style.display='none';
			}

			if(data.reqs[9]==false){
				//console.log('here');
				var element=document.getElementById("otherbrand");
				element.style.display='none';
			}

			if(data.reqs[10]==false){
				//console.log('here');
				var element=document.getElementById("deplink");
				element.style.display='none';
			}
			if(data.reqs[11]==false){
				//console.log('here');
				var element=document.getElementById("nondeplink");
				element.style.display='none';
			}
			if(data.reqs[12]==false){
				//console.log('here');
				var element=document.getElementById("descriptions");
				element.style.display='none';
			}
			if(data.reqs[13]==false){
				//console.log('here');
				var element=document.getElementById("independent-attributes");
				element.hidden=true;

				var element=document.getElementById("Vitalinf");
				element.style.display='none';
			}

			if(data.reqs[14]==false){
				//console.log('here');
				var element=document.getElementById("fitsection");
				element.style.display='none';
			}
			if(data.reqs[15]==false){
				//console.log('here');
				var element=document.getElementById("seasonsection");
				element.style.display='none';
			}

			if(data.reqs[15]==false){
				//console.log('here');
				var element=document.getElementById("washcaresection");
				element.style.display='none';
			}
			if(data.reqs[16]==false){
				//console.log('here');
				var element=document.getElementById("services");
				element.style.display='none';
			}





			$.each(data.data,function(index,value){

				if(value.input_type=='Text')
				{
				ht=ht+`<div class="container mt-2 mb-2">
					<div class="row">
						<input type="text" placeholder="`+value.name+`" name="attribute`+(index+1)+`" class="input_attribute">
						<p style="font-size: .6em; margin-left: 4vw">`+value.description+`</p>
					</div>
				</div>`}
				else
				{
					ht=ht+
					`<div class="container mt-2 mb-2">
						<div class="row">
						<select class="input_attribute" name="attribute`+(index+1)+`">
						<option disabled selected>`+value.name+`</option>`
						v=value.values.split(",");
						for (a in v)
						{
							ht=ht+`<option value="`+v[a].trim()+`">`+v[a].trim()+`</option>`

						}
						ht=ht+`</select><p style="font-size: .6em; margin-left: 4vw">`+value.description+`</p>

						
					</div></div>`
				}

			});
			safety_stock=parseInt(data.limit);
			ama=document.getElementById('safety_stock1');
			//console.log(data.limit);
			ama.value=data.limit;
			$('#form_upload_product').html(ht);
			$('#head_upload').html("Attributes of Product");
			document.getElementById('Vitalinf').click();
			}
			else{

				$('#form_upload_product').html(ht);
			}


		}

	});
	var form_jh=document.getElementById('form_upload_product');
	form_jh.classList.remove('hide');
}




$('#slug').on('input',function(){
	var slug=$('#slug').val();
	if (slug.length<10){
		var ht=''
		ht='<p style="font-size: .8em;color:red;margin-left:2vw;">Please Enter at Least 10 Characters</p>';
		$('#slug_update').html(ht);
	}
	else if (slug.length>50){
		ht='<p style="font-size: .8em;color:red;margin-left:2vw;">Slug Must be less than 50 Characters</p>';
		$('#slug_update').html(ht);

	}
	else{
		$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			slug_ajax_prod:slug,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {

			if (data.bol){
				ht='<p style="font-size: .8em;color:green;margin-left:2vw;">Congratulations You can Take This !!</p>';
				$('#slug_update').html(ht);
				var x=document.getElementsByName("slug")[0];
				x.style.border="2px solid gray";

			}
			else{
				ht='<p style="font-size: .8em;color:red;margin-left:2vw;">Sorry This is Taken ! Please try more</p>';
				$('#slug_update').html(ht);
				

			}
		}

		});

	}

});


var image_count = 1
var size_image_counter = {
    '1': 0,
    '2': 0,
    '3': 0,
    '4': 0,
    '5': 0,
    '6': 0,
    '7': 0,
    '8': 0,
    '9': 0,
    '10': 0,
}

function addSizeImage(size) {
    var sizesection = document.getElementById('sizeimagesection' + size);
    size_image_counter[size]++;
    if (size_image_counter[size] <= 10) {
        // var td = document.createElement("td");
        // td.innerHTML = `<input type="file" name="` + size + `sizeimage` + size_image_counter[size] + `">`;
        // sizesection.appendChild(td);
        var col = document.createElement("div");
        col.innerHTML = `<input type="file" name="` + size + `-sizeimage-` + size_image_counter[size] + `" style="margin: 10px;"><br> <input type="checkbox" id="` + size + `isactual` + size_image_counter[size] + `" name="` + size + `-isactual-` + size_image_counter[size] + `" value=true style="margin-left: 10px;">
		<label for="` + size + `isactual` + size_image_counter[size] + `"> Is Actual Image</label>`
        col.setAttribute("class", "col");
        var br = document.createElement("br")
        sizesection.appendChild(col);
        sizesection.appendChild(br);
        // var col = `<div class="col-1"><input type="file" name="` + size + `sizeimage` + size_image_counter[size] + `"></div>`;
    }

}

function addimage() {
    image_count = image_count + 1;
    //var ht=$('#images_upload').html();
    var objTo = document.getElementById('images_upload');
    var divtest = document.createElement("span");
    divtest.innerHTML = `<div class="file-upload" style="display:inline-table;">
		 				 <button class="file-upload-btn" type="button" id="imagebutton` + image_count + `" onclick="$('#file-upload-input` + image_count + `').trigger( 'click' )">Add Image</button>
						  <input type="checkbox" id="isactual` + image_count + `" name="isactual` + image_count + `" value=true style="margin-left: 10px;"><label for="isactual` + image_count + `"> Is Actual Image</label>
 					 <div class="image-upload-wrap" id="image-upload-wrap` + image_count + `">
  					  <input class="file-upload-input" id="file-upload-input` + image_count + `" name="file-upload-input` + image_count + `" type='file' onchange="readURL(this,` + image_count + `);" accept="image/*" />
  					  <div class="drag-text">
     				 <h3 style="font-size: 20px;">Drag and drop a file or select add Image</h3>
    				</div>
  					</div>
 				 <div class="file-upload-content" id="file-upload-content`+image_count+`">
    				<img class="file-upload-image" id="file-upload-image`+image_count+`" style="width:280px;height:350px;" src="#" alt="your image" />
    				<div class="image-title-wrap" id="image-title-wrap`+image_count+`">
   				   <button type="button" onclick="removeUpload(`+image_count+`)" class="remove-image">Remove <span class="image-title" id="image-title`+image_count+`">Uploaded Image</span></button>
   				 </div>
  				</div>
						</div>`;
    objTo.appendChild(divtest);
	/*ht=ht+`
	<div class="file-upload" style="display:inline-table;">
		 				 <button class="file-upload-btn" type="button" id="imagebutton`+image_count+`" onclick="$('#file-upload-input`+image_count+`').trigger( 'click' )">Add Image</button>

 					 <div class="image-upload-wrap" id="image-upload-wrap`+image_count+`">
  					  <input class="file-upload-input" id="file-upload-input`+image_count+`" name="file-upload-input`+image_count+`" type='file' onchange="readURL(this,`+image_count+`);" accept="image/*" />
  					  <div class="drag-text">
     				 <h3 style="font-size: 20px;">Drag and drop a file or select add Image</h3>
    				</div>
  					</div>
 				 <div class="file-upload-content" id="file-upload-content`+image_count+`">
    				<img class="file-upload-image" id="file-upload-image`+image_count+`" style="width:280px;height:350px;" src="#" alt="your image" />
    				<div class="image-title-wrap" id="image-title-wrap`+image_count+`">
   				   <button type="button" onclick="removeUpload(`+image_count+`)" class="remove-image">Remove <span class="image-title" id="image-title`+image_count+`">Uploaded Image</span></button>
   				 </div>
  				</div>
						</div>`;
	$('#images_upload').html(ht);*/
	if (image_count>=50){
		var addmore=document.getElementById('addmore');
		addmore.style.display="none";
		// console.log("giver nonne");
	}
}




$('#product_group').on("change",function(){
	//alert("Done");
	var product_group_type=$('#product_group').val();
	$.ajax({
		type:'POST',
		url:'/userdetail/seller_profile/upload_product',
		data:{
			product_group_type:$('#product_group').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
  		cache:false,
  		dataType: "json",
		success:function(data){
			if (data.bol){
				var ht='<br><p><b>User Specific Details</b></p><table>';
				$.each(data.data,function(index,value){
					//console.log(value);
					console.log(value);
					if(value[1]=="Text"){
					ht=ht+`<tr><td><label style="width:200px;">`+value[0]+`: </label></td>
					<td><input class="input_attribute additionalopts" style="width:300px;" type="text" name="`+value[0]+`" placeholder="`+value[0]+`" ></td>
					</tr>`;}
					else if(value[1]=="Drop Down"){
					ht=ht+`<tr><td><label style="width:200px;">`+value[0]+`: </label></td>
					<td><select class="input_attribute" style="width:300px;" name=`+value[0]+`">
						<option disabled selected>`+value[0]+`</option>`
						v=value[2].split(",");
						for (a in v)
						{
							ht=ht+`<option value="`+v[a].trim()+`">`+v[a].trim()+`</option>`

						}
						`</select>
						</td>
					</tr>`;
					}
					else if(value[1]=="Date"){
						ht=ht+`<tr><td><label style="width:200px;">`+value[0]+`: </label></td>
					<td><input class="input_attribute additionalopts" style="width:300px;" type="date" name="`+value[0]+`" placeholder="`+value[0]+`" ></td>
					</tr>`;
					}
				});
				ht=ht+`</table></div>`;
				$('#catbygroup').html(ht);
			}
			else{
				var ht='<br><table>';
				$.each(data.data,function(index,value){
					//console.log(value);
					console.log(value);
	
					//ht=ht+`<tr><td><label>`+value+`: </label></td><td><input class="input_attribute additionalopts" style="width:300px;" type="text" name="`+value+`" placeholder="`+value+`" ></td></tr>`;
				});
				ht=ht+`</table></div>`;
				$('#catbygroup').html(ht);
			}
			if(product_group_type=="Fashion")
				$('#forfashion').hidden=false;
			else
				$('#notforfashion').hidden=false;
		}
	});
});






// var size_count=1
// function addsize(){
// 	size_count=size_count+1;
// 	var ht=$('#size'+size_count.toString()).html();
// 	ht=ht+`<div class="col">
// 		<select name="size`+size_count.toString()+`" id="" class="input_attribute" required style="padding-left: .5vw;width:100%;">
// 			`+sizes+`
// 		</select>
// 	</div>
// 	<div class="col">
// 							<select class="input_attribute" name="color`+size_count.toString()+`">
// 								<optgroup label="Major Colors">
// 							{% for a in majcolors  %}
// 								<option value="{{a}}">{{a}}</option>
// 							{% endfor %}
// 								<optgroup label="Other Colors">
// 							{% for a in otcolors  %}
// 								<option value="{{a}}">{{a}}</option>
// 							{% endfor %}
// 							</select>
// 			</div>
//
//
// 	<div class="col">
// 		<input type="color" name="color`+size_count.toString()+`" class="input_attribute" placeholder="Color of Product" required style="padding-left: .5vw;width:100%;"number>
// 	</div>
// 	<div class="col">
// 		<input type="number" name="price`+size_count.toString()+`" class="input_attribute" placeholder="Selling Price of Product" required style="padding-left: .5vw;width:100%;"number>
// 	</div>
// 	<div class="col">
// 		<input type="number" name="c_price`+size_count.toString()+`" class="input_attribute" placeholder="Cost Price of Product" required style="padding-left: .5vw;width:100%;">
// 	</div>
// 	<div class="col">
// 		<input type="number" name="quantity`+size_count.toString()+`" class="input_attribute" placeholder="Quantity of Product" required style="padding-left: .5vw;width:100%;"number>
// 	</div>
// 	<div class="col">
// 		<input type="number" name="safety_stock`+size_count.toString()+`" class="input_attribute" placeholder="Safety Stock of Product" value="`+safety_stock+`" required style="padding-left: .5vw;width:100%;">
// 	</div>`;
// 	$('#size'+size_count.toString()).html(ht);
// 	if (size_count>=10){
// 		var addmore=document.getElementById('addmore_size');
// 		addmore.style.display="none";
// 		// console.log("giver nonne");
// 	}
// }



