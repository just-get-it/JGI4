

//
// var tagline=document.getElementById('design_tagline_input');
// tagline.focus();
// tagline.select();



function get_design_profile(){
  $('#design_profile_input').click();
}


function sendmessage(email,name){
  var a=prompt("Please Enter your message for "+name.toString(),"Hello !");
  if (a!=null){
    window.location.href="/mydesign/messages?message="+a.toString()+"&to="+email.toString();
  }
}


function follow(email){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  console.log($('input[name=csrfmiddlewaretoken]').val());
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/'+email.toString(),
		data:{
      follow:"True",
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {
      window.location.href="/mydesign/profile/"+email.toString();
      // processing.style.display="none";
		}
	});
}


function unfollow(email){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  console.log($('input[name=csrfmiddlewaretoken]').val());
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/'+email.toString(),
		data:{
      unfollow:"True",
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

      window.location.href="/mydesign/profile/"+email.toString();
      // processing.style.display="none";
		}
	});
}


function cancelrequest(email){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  // console.log($('input[name=csrfmiddlewaretoken]').val());
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/'+email.toString(),
		data:{
      cancelrequest:"True",
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

      window.location.href="/mydesign/profile/"+email.toString();
      // processing.style.display="none";
		}
	});
}



function unfriend(email){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  // console.log($('input[name=csrfmiddlewaretoken]').val());
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/'+email.toString(),
		data:{
      unfriend:"True",
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

      window.location.href="/mydesign/profile/"+email.toString();
      // processing.style.display="none";
		}
	});
}



function addfriend(email){
  var processing = document.getElementById('processing');
  processing.style.display="block";
  // console.log($('input[name=csrfmiddlewaretoken]').val());
  $.ajax({
		type:'POST',
		url:'/mydesign/profile/'+email.toString(),
		data:{
      addfriend:"True",
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
    },
    	cache:false,
    	dataType: "json",
		success:function(data) {

      window.location.href="/mydesign/profile/"+email.toString();
      // processing.style.display="none";
		}
	});
}
