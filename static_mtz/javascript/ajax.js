const sendbutton = document.getElementById('sendbutton')
var count=0;
var voice=false;
var value = "I got nothing related to your query";
sendbutton.addEventListener('click', buttonClickHandler);
sendbutton.addEventListener('keyup', keydown)
const messageslistnew1 = document.getElementById('messageslistnew1')
const messageslistnew2 = document.getElementById('messageslistnew2')
const messageslistnew3 = document.getElementById('messageslistnew3')
const messageslistnew4 = document.getElementById('messageslistnew4')

function speak(){
    console.log("function speak executing")
    var msg = new SpeechSynthesisUtterance(value);
    window.speechSynthesis.speak(msg);   
}
function voiceupdater(){
    console.log("voiceupdate function called")
    if(voice===true){
    voice=false;
    element = document.getElementById("whatsapp");
    // element.innerHTML = element.innerHTML + `<p class="messageslist"><img id="image" src="../static/bot3.jpeg" alt="bot" >Text to speech feature has been deactivated.</p>`
    element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >Text to speech feature has been deactivated.</p>`)

    value = "Text to speech feature has been deactivated."
    speak();
    }
    else{
    voice=true;
    element = document.getElementById("whatsapp");
    // element.innerHTML = element.innerHTML + `<p class="messageslist"><img id="image" src="../static/bot3.jpeg" alt="bot" >Text to speech feature has been activated.</p>`
    element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >Text to speech feature has been activated.</p>`)

    value="Text to speech feature has been activated."
    speak();
    }


}


function buttonClickHandler(){
    element = document.getElementById("whatsapp");
    count++;

    


    // element.innerHTML = element.innerHTML + ` <p class="messageslist" id="usermessage">${document.getElementById('senderbutton').value}<img id="image" src="../static/user.jpeg" alt="bot" ></p>`
    element.insertAdjacentHTML('beforeend',  `<p class="messageslist" id="usermessage">${document.getElementById('senderbutton').value}<img id="image" src="../../static/images/user.jpeg" alt="bot" ></p>`)


    console.log(document.getElementById('senderbutton').value)
    
    console.log('Button Clicked', count);



    let n = document.getElementById('form1')



    const xhr = new XMLHttpRequest();
    url = 'justgetit.in/botsearch/?question='
    url = url + (document.getElementById('senderbutton').value) ;
    // print(url);
    xhr.open('GET', url , true);
    xhr.onprogress = function(){
        console.log('On progress');
    }
    xhr.onload = function () {
       console.log("Onload Function running....") 
       fetch('justgetit.in/static/sample.txt').then(
       response => response.text()).then(data => {
       element = document.getElementById("whatsapp");
    //    element.innerHTML = element.innerHTML + `<p class="messageslist"><img id="image" src="../static/bot3.jpeg" alt="bot" >${data}</p>`
       element.insertAdjacentHTML('beforeend',  `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >${data}</p>`)

       value=data;
       if(voice===true)
       speak();


        if(count===4)
        {
        //  element.innerHTML = element.innerHTML + `<p class="messageslist"><img id="image" src="../static/bot3.jpeg" alt="bot" >Hope you are having a great time talking to me. Rate your experience out of 5</p>`
         element.insertAdjacentHTML('beforeend',  `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >Hope you are having a great time talking to me. Rate your experience out of 5</p>`)

         value = "Hope you are having a great time talking to me. Rate your experience out of 5"
         if(voice===true)
         speak();
        }
        
    

       });
    }
    xhr.send();
    console.log("function completed running");
    n.reset();


   }

    messageslistnew1.addEventListener('click', function buttonClickHandlernew1() {
    console.log("orders")
    const xhr = new XMLHttpRequest();
    url = 'justgetit.in/botsearch/?question='
    url = url + "orders" ;
    xhr.open('GET', url , true);
    xhr.onprogress = function(){
        console.log('On progress');
    }
    xhr.onload = function () {
       console.log("Onload Function running...") 
       fetch('justgetit.in/static/sample.txt').then(
       response => response.text()).then(data => {
       element = document.getElementById("whatsapp");
       element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >${data}</p>`)
       if(voice===true){
        value = data
        speak();}
       
    

       });
    }
    xhr.send();
    console.log("function completed running");
    

    
});
messageslistnew3.addEventListener('click', function buttonClickHandlernew3() {
    console.log("complaints")

    const xhr = new XMLHttpRequest();
    url = 'justgetit.in/botsearch/?question='
    url = url + "complaints" ;
    xhr.open('GET', url , true);
    xhr.onprogress = function(){
        console.log('On progress');
    }
    xhr.onload = function () {
       console.log("Onload Function running") 
       fetch('justgetit.in/static/sample.txt').then(
       response => response.text()).then(data => {
       element = document.getElementById("whatsapp");
       element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >${data}</p>`)
       if(voice===true){
        value = data
        speak();}
    

       });
    }
    xhr.send();
    console.log("function completed running");
});
messageslistnew2.addEventListener('click', function buttonClickHandlernew2() {
    console.log("wishlist")

    const xhr = new XMLHttpRequest();
    url = 'justgetit.in/botsearch/?question='
    url = url + "wishlist" ;
    xhr.open('GET', url , true);
    xhr.onprogress = function(){
        console.log('On progress');
    }
    xhr.onload = function () {
       console.log("Onload Function running") 
       fetch('justgetit.in/static/sample.txt').then(
       response => response.text()).then(data => {
       element = document.getElementById("whatsapp");
       element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >${data}</p>`)
       if(voice===true){
        value = data
        speak();}

       });
    }
    xhr.send();
    console.log("function completed running");

});
messageslistnew4.addEventListener('click', function buttonClickHandlernew4() {
    console.log("executive")
    data = "Connected to the JGI BOT"
    element = document.getElementById("whatsapp");
    element.insertAdjacentHTML('beforeend', `<p class="messageslist"><img id="image" src="../../static/images/bot3.jpeg" alt="bot" >${data}</p>`)
    if(voice===true){
    value = data
    speak();}

});






function keydown(e) {
    var x = e.keyCode;
    console.log('Function Keydown Called')
    if(x == 13){
    buttonClickHandler()
    
    }
}







