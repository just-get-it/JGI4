


var tagline=document.getElementById('design_tagline_input');
tagline.focus();
// tagline.select();



function get_design_profile(){
  $('#design_profile_input').click();
}

$('#design_profile_input').change(function() {
  var processing = document.getElementById('processing');
  processing.style.display="block";
  var fd = new FormData();
  var files = $('#design_profile_input')[0].files[0];
  var csrf= $('input[name=csrfmiddlewaretoken]').val();
  fd.append('design_profile_input', files);
  fd.append('csrfmiddlewaretoken',csrf);
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/',
		data:fd,
    processData: false,
    contentType: false,
		success:function(data) {
      $("#user_profile_image").removeAttr("src").attr("src", data.img);
      processing.style.display="none";
		}
	});
});


$('#design_tagline_input').change(function() {
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/',
		data:{
      tagline_ajax:$('#design_tagline_input').val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

		}
	});
});



$('#design_about_input').change(function() {
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/',
		data:{
      about_ajax:$('#design_about_input').val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

		}
	});
});



function updateInterest(id_interest){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/',
		data:{
      id_interest_ajax:id_interest,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {
      processing.style.display="none";
      var a=document.getElementById('design_interest_content');
      a.classList.add("opa_animation");
      setTimeout(function(){
        a.classList.remove("opa_animation");
      },5000);
      var ht='';
      if (data.interest){
        $.each(data.interest,function(index,value){
  				ht=ht+`	<div class="interest_area" onclick="updateInterest(`+value.id+`)">`+value.name+` <i class="fas fa-plus fa-xs" style="color:black;"></i></div>`
  			});
        a.innerHTML=ht;
      }
		}
	});
}
