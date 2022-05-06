		/*$("#sign_up").click(function(){
				alert("Hello");
			})*/
			
			$("#sign_up").submit(function(){
				var flag=new Array();
				var i=0;
				if($.trim($("#first_name").val())==""){
				   $(".first_name").html("Please enter first name").css('color','red');
				   flag[i]=false;
				   i=i+1;	
				}else{
					$(".first_name").html("");
					flag[i]=true;
				    i=i+1;
				}
				if($.trim($("#last_name").val())==""){
				   $(".last_name").html("Please enter last name").css('color','red');
				   flag[i]=false;
				   i=i+1;
				}else{
					$(".last_name").html("");
					flag[i]=true;
				    i=i+1;
				}
				
				
				var email=$.trim($("#phone_email").val());

				if(email==""){
				   $(".phone_email").html("Please enter Phone no or Email address").css('color','red');
				   flag[i]=false;
				   i=i+1;
				}else{
					
					var isnum = /^\d+$/.test(email);
					if(isnum==true){
						if(email.length!=10){
							$(".phone_email").html("Please enter valid mobile no").css('color','red');
							 flag[i]=false;
							 i=i+1;
						}else{
							$(".phone_email").html("");
							flag[i]=true;
							i=i+1; 
						}
						
					}else{
						 var regexp = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
						 if(regexp.test(email)==false){
							 $(".phone_email").html("Please enter valid Email address").css('color','red');
							 flag[i]=false;
							 i=i+1;
						 }else{
							$(".phone_email").html("");
							flag[i]=true;
							i=i+1;
						 }
					}
				}
				
				
				
				if($.trim($("#new_password").val())==""){
				   $(".new_password").html("Please enter New password").css('color','red');
				   flag[i]=false;
				   i=i+1;
				}else{
					$(".new_password").html("");
					flag[i]=true;
				    i=i+1;
				}
				
				
				
				
				var n=0;
				
				for(j=0;j<i;j++){
					if(flag[j]==false){
						n=n+1;
					}
				}
				
				if(n>0){
					return false;
				}else{
					return true;
				}
			})