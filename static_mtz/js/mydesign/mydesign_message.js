








function startnewchat(){
	var addchat=document.getElementById('addchat');
	addchat.classList.remove('hide_row');
}


function closestartchat(){
	var addchat=document.getElementById('addchat');
	addchat.classList.add('hide_row');
}

$('#staff_position').on('change',function(){
	$.ajax({
		type:'POST',
		url:'/mydesign/messages/',
		data:{
			staff_ajax_cate:$('#staff_cate').val(),
			position_ajax_staff:$('#staff_position').val(),
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='<option disabled selected>------</option>';
			if (data.bol){
			$.each(data.data,function(index,value){
				ht=ht+`<option value="`+value.email+`">`+value.email+`</option>`
			});
			$('#staff').html(ht);
			}
			else{

				$('#staff').html(ht);
			}
		}
	});
});

var success_chat=document.getElementById('success_chat');


$('#msgcontainer').scrollTop($('#msgcontainer')[0].scrollHeight);

var scrolled = false;
function updateScroll(){
    if(!scrolled){
        var element = document.getElementById("msgcontainer");
        element.scrollTop = element.scrollHeight;
    }
}

function updateScroll1(){

        var element = document.getElementById("msgcontainer");
        element.scrollTop = element.scrollHeight;

}

$("#msgcontainer").on('scroll', function(){
    scrolled=true;
});
setInterval(updateScroll,1000);

function showchat(chatid,email){
	var showchatforid=document.getElementById('showchatforid');
	showchatforid.classList.remove('hide_row');
	$.ajax({
		type:'POST',
		url:'/mydesign/messages/',
		data:{
			chats_ajax_id:chatid,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			success_chat.value=chatid
			var ht='';
			if (data.bol){
				$.each(data.data,function(index,value){

					if ((value.sent_by_user1 && email==value.user1) || (value.sent_by_user2 && email==value.user2)) {
						ht=ht+`<div class="container"><div class="row" style="margin-top:.5vh;margin-right:5px;margin-left:15vw;background:rgba(48,197,255,.8);padding:1vw;padding-top:.5vw;padding-bottom:.5vw;border-radius:.4vw;">
						<h6 style="font-family'Cabin', sans-serif;color:black;">`+value.message+`</h6>
						<h6 style="font-family:'Cabin', sans-serif;font-size:.5em;color:black;margin-top:1vh;margin-left:auto;">`+value.created_on.substring(11,16)+`</h6>
						</div></div>`;
					}
					else{
						ht=ht+`<div class="container"><div class="row" style="margin-top:2px;margin-left:5px;margin-right:10vw;background:rgba(48,197,255,.2);padding:5px;">
						<h6 style="font-family:'Cabin', sans-serif;"><b></b></h6>
						<h6 style="font-family'Cabin', sans-serif;color:black;">`+value.message+`</h6>
						<h6 style="font-family:'Cabin', sans-serif;font-size:.5em;color:black;margin-top:1vh;margin-left:auto;">`+value.created_on.substring(11,16)+`</h6>
						</div></div>`;
					}
				});
				$('#msgcontainer').html(ht);
			}
			else{
				// alert("here");
				$('#msgcontainer').html(ht);
			}
		}
	});
}


function hidechatforid(){
	var showchatforid=document.getElementById('showchatforid');
	showchatforid.classList.add('hide_row')
}



function sendreply(){
	var message=document.getElementById('rep_but').value;
	var today=new Date();
	$.ajax({
		type:'POST',
		url:'/mydesign/messages/',
		data:{
			chats_ajax:success_chat.value,
			message_ajax:message,
			csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
		},
    	cache:false,
    	dataType: "json",
		success:function(data) {
			var ht='';
			if (data.bol){
						ht=$('#msgcontainer').html()+`<div class="container"><div class="row" style="margin-top:2px;margin-right:5px;margin-left:15vw;background:rgba(48,197,255,.8);padding:1vw;padding-top:.5vw;padding-bottom:.5vw;border-radius:.4vw;">
						<h6 style="font-family:'Cabin', sans-serif;color:black;"><b></b></h6>
						<h6 style="font-family'Cabin', sans-serif;color:black;">`+message+`</h6>
						<h6 style="font-family:'Cabin', sans-serif;font-size:.5em;color:black;margin-top:1vh;margin-left:auto;">`+today.getHours() + ":" + today.getMinutes()+`</h6>
						</div>`;


				$('#msgcontainer').html(ht);
			}
			updateScroll1();
		}
	});
}
