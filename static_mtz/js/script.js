var a=true;
var mens=true;
var women=false;
var kids=false;
var home=false;
var wom=document.getElementById('women');
var men=document.getElementById('mens');
var kid=document.getElementById('kids');
var hom=document.getElementById('home');
function animateright(){
var catehead=document.getElementById('catehead');
console.log("Here");
catehead.classList.add("animright");
window.setTimeout(function(){
	catehead.classList.remove("animright");
},1000);
if (mens==false){
	men.style.display="inline-flex";
	if (women){
		wom.style.display="none";
		women=false;
	}
	else if (kids){
		kid.style.display="none";
		kids=false;
	}
	else if (home){
		hom.style.display="none";
		home=false;
	}
	mens=true;
}
else{
	men.style.display="none";
	men.style.display="inline-flex";
	mens=true;

}
}
function animateright1(){
var catehead=document.getElementById('catehead1');
console.log("Here");
catehead.classList.add("animright");
window.setTimeout(function(){
	catehead.classList.remove("animright");
},1000);
if (women==false){
	wom.style.display="inline-flex";
	if (mens){
		men.style.display="none";
		mens=false;
	}
	else if (kids){
		kid.style.display="none";
		kids=false;
	}
	else if (home){
		hom.style.display="none";
		home=false;
	}
	women=true;
}
else{
	wom.style.display="none";
	men.style.display="inline-flex";
	mens=true;
	women=false;

}

}
function animateright2(){
var catehead=document.getElementById('catehead2');
console.log("Here");
catehead.classList.add("animright");
window.setTimeout(function(){
	catehead.classList.remove("animright");
},1000);
if (kids==false){
	kid.style.display="inline-flex";
	if (mens){
		men.style.display="none";
		mens=false;
	}
	else if (women){
		wom.style.display="none";
		women=false;
	}
	else if (home){
		hom.style.display="none";
		home=false;
	}
	kids=true;
}
else{
	kid.style.display="none";
	men.style.display="inline-flex";
	mens=true;
	kids=false;

}
}
function animateright3(){
var catehead=document.getElementById('catehead3');
console.log("Here");
catehead.classList.add("animright");
window.setTimeout(function(){
	catehead.classList.remove("animright");
},1000);
if (home==false){
	hom.style.display="inline-flex";
	if (mens){
		men.style.display="none";
		mens=false;
	}
	else if (kids){
		kid.style.display="none";
		kids=false;
	}
	else if (women){
		wom.style.display="none";
		women=false;
	}
	home=true;
}
else{
	hom.style.display="none";
	men.style.display="inline-flex";
	mens=true;
	home=false;

}
}
function showDrop(){
var dropContent=document.getElementById('dropdown-first1');
console.log("here")
if(a){
	dropContent.classList.add('show');
	a=false;
}
else{
	dropContent.classList.remove('show');
	a=true;
}
}


function display(evt, content) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  document.getElementById(content).style.display = "initial";
}



// ============================================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
// Now Starting for Menu ======================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
// ============================================================
var menuformobile=false
function showMenu(){
	var menu=document.getElementById('menu');
	if (menuformobile==false){
		menu.style.display="block";
		menuformobile=true;
	}
	else{
		menu.style.display="none";
		menuformobile=false;
	}
}


var activepro=false

function showProfile(){
	pro=document.getElementById('getprofile');
	if(activepro==false){
		pro.style.display="inline-flex";
		activepro=true;
	}
	else{
		pro.style.display="none";
		activepro=false;
	}
}