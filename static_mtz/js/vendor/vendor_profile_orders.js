

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
