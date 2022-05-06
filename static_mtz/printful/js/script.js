fabric.Object.prototype.transparentCorners = false;
fabric.Object.prototype.padding = 5;
fabric.Object.prototype.cornerColor = 'blue';
fabric.Object.prototype.cornerStyle = 'circle';

var $ = function(id){return document.getElementById(id)};

// Front Side Tshirt 
var canvas = this.__canvas = new fabric.Canvas('c');
    canvas.setHeight(250);
    canvas.setWidth(163);

function Addtext() { 
var text = document.getElementById('IPtxt').value;    //ADDing Text to Canvas
canvas.add(new fabric.IText(text, {                             
    left: 10,                                               
    top: 10,                                        
    fontFamily: 'arial black',
    fill: '#000',
    fontSize: 30
}));
document.addEventListener("keydown", function(e)
    {
        var keyCode = e.keyCode;

            if(keyCode == 46)
                {
                    canvas.remove(canvas.getActiveObject());
                }
        }, false);
}

document.getElementById('addImg').addEventListener("change", function(e)
            {
                var reader = new FileReader();          //Adding Image from Local machine

                reader.onload = function (event)
                {
                    var imgObj = new Image();
                    imgObj.src = event.target.result;

                    imgObj.onload = function ()
                    {
                        var img = new fabric.Image(imgObj);

                        img.scaleToHeight(150);
                        img.scaleToWidth(150);
                        canvas.centerObject(img);
                        canvas.add(img);
                        canvas.renderAll();
                    };
                };                                              

                if(e.target.files[0])
                {
                    reader.readAsDataURL(e.target.files[0]);
                }

                document.addEventListener("keydown", function(e)
                {
                    var keyCode = e.keyCode;

                    if(keyCode == 46)
                    {
                        canvas.remove(canvas.getActiveObject());
                    }
                }, false);
            }, false);

            var scaleControl = $('resize-img');
            scaleControl.onchange = function() {
                var activeObject = canvas.getActiveObject();
                activeObject.scale(this.value).setCoords();
                canvas.renderAll();
            };
          
            var topControl = document.getElementById('shift-y-axis');
            topControl.onchange = function() {
                var activeObj = canvas.getActiveObject();
                activeObj.setTop(this.value).setCoords();
              canvas.renderAll();
            };
          
            var leftControl = document.getElementById('shift-x-axis');
            leftControl.onchange = function() {
                var activeObj = canvas.getActiveObject();
                activeObj.setLeft(this.value).setCoords();
              canvas.renderAll();
            };

            // canvas.on({
            //     'object:moving': updateControls,
            //     'object:scaling': updateControls,
            //     'object:resizing': updateControls,
            //   });

let url;
function submitURL(e){
    url = document.getElementById("imgURL").value;          //Add  Image from URL
    console.log(url);
                
    fabric.Image.fromURL(url,function(img) {                       
        var oImg = img.set({ left:0, top:0 }).scale(0.9);
        img.scaleToHeight(150);
        img.scaleToWidth(150);
        canvas.centerObject(oImg);
        canvas.add(oImg).renderAll();
        });
    document.addEventListener("keydown", function(e)
    {
        var keyCode = e.keyCode;

        if(keyCode == 46)
        {
            canvas.remove(canvas.getActiveObject());
        }
    }, false);
}


document.getElementById('text-color').onchange = function() {
        canvas.getActiveObject().setFill(this.value);
        canvas.renderAll();
    };
document.getElementById('text-color').onchange = function() {
        canvas.getActiveObject().setFill(this.value);
        canvas.renderAll();
    };
    
    document.getElementById('text-bg-color').onchange = function() {
        canvas.getActiveObject().setBackgroundColor(this.value);
        canvas.renderAll();
    };

    document.getElementById('text-stroke-color').onchange = function() {
        canvas.getActiveObject().setStroke(this.value);
        canvas.renderAll();
    };	

    document.getElementById('text-stroke-width').onchange = function() {
        canvas.getActiveObject().setStrokeWidth(this.value);
        canvas.renderAll();
    };				

    document.getElementById('font-family').onchange = function() {
        canvas.getActiveObject().setFontFamily(this.value);
        canvas.renderAll();
    };
    
    document.getElementById('text-font-size').onchange = function() {
        canvas.getActiveObject().setFontSize(this.value);
        canvas.renderAll();
    };

radios5 = document.getElementsByName("fonttype");  // wijzig naar button
for(var i = 0, max = radios5.length; i < max; i++) {
    radios5[i].onclick = function() {
        
        if(document.getElementById(this.id).checked == true) {
            if(this.id == "text-cmd-bold") {
                canvas.getActiveObject().set("fontWeight", "bold");
            }
            if(this.id == "text-cmd-italic") {
                canvas.getActiveObject().set("fontStyle", "italic");
            }
            if(this.id == "text-cmd-underline") {
                canvas.getActiveObject().set("textDecoration", "underline");
            }
            
            
        } else {
            if(this.id == "text-cmd-bold") {
                canvas.getActiveObject().set("fontWeight", "");
            }
            if(this.id == "text-cmd-italic") {
                canvas.getActiveObject().set("fontStyle", "");
            }  
            if(this.id == "text-cmd-underline") {
                canvas.getActiveObject().set("textDecoration", "");
            }
        }
        
        
        canvas.renderAll();
    }
}


document.getElementById('Tbg1').onclick = function(){
  var bg1 = document.getElementById('TColor');
  bg1.style.background = "#FFFFFF";
  var bg1 = document.getElementById('TBColor');
  bg1.style.background = "#FFFFFF";
  var bg1 = document.getElementById('TRColor');
  bg1.style.background = "#FFFFFF";
  var bg1 = document.getElementById('TLColor');
  bg1.style.background = "#FFFFFF";
}

document.getElementById('Tbg2').onclick = function(){
    var bg1 = document.getElementById('TColor');
    bg1.style.background = "#000000";
    var bg2 = document.getElementById('TBColor');
    bg2.style.background = "#000000";
    var bg3 = document.getElementById('TRColor');
    bg3.style.background = "#000000";
    var bg4 = document.getElementById('TLColor');
    bg4.style.background = "#000000";
  }

document.getElementById('Tbg3').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#0074D9";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#0074D9";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#0074D9";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#0074D9";
  }

  document.getElementById('Tbg4').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#D34B56";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#D34B56";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#D34B56";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#D34B56";
  }
  document.getElementById('Tbg5').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#EADC32";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#EADC32";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#EADC32";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#EADC32";
  }
  document.getElementById('Tbg6').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#3D9970";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#3D9970";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#3D9970";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#3D9970";
  }

  document.getElementById('Tbg7').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#F1A9C4";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#F1A9C4";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#F1A9C4";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#F1A9C4";
  }
  document.getElementById('Tbg8').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#36454F";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#36454F";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#36454F";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#36454F";
  }
  document.getElementById('Tbg9').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#800080";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#800080";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#800080";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#800080";
  }
  document.getElementById('Tbg10').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#D2B48C";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#D2B48C";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#D2B48C";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#D2B48C";
  }
  document.getElementById('Tbg11').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#F28D20";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#F28D20";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#F28D20";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#F28D20";
  }
  document.getElementById('Tbg12').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#B3B3B3";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#B3B3B3";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#B3B3B3";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#B3B3B3";
  }
  document.getElementById('Tbg13').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#3C4477";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#3C4477";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#3C4477";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#3C4477";
  }
  document.getElementById('Tbg14').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background= "#FFE5B4";
    var bg = document.getElementById('TBColor');
    bg.style.background= "#FFE5B4";
    var bg = document.getElementById('TRColor');
    bg.style.background= "#FFE5B4";
    var bg = document.getElementById('TLColor');
    bg.style.background= "#FFE5B4";
  }
  document.getElementById('Tbg15').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#A03245";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#A03245";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#A03245";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#A03245";
  }
  document.getElementById('Tbg16').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#B7410E";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#B7410E";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#B7410E";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#B7410E";
  }
  document.getElementById('Tbg17').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#5DB653";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#5DB653";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#5DB653";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#5DB653";
  }
  document.getElementById('Tbg18').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "#008080";
    var bg = document.getElementById('TBColor');
    bg.style.background = "#008080";
    var bg = document.getElementById('TRColor');
    bg.style.background = "#008080";
    var bg = document.getElementById('TLColor');
    bg.style.background = "#008080";
  }
  document.getElementById('Tbg19').onclick = function(){
    var bg = document.getElementById('TColor');
    bg.style.background = "radial-gradient(circle, rgba(251,169,205,1) 0%, rgba(250,255,128,1) 28%, rgba(133,255,141,1) 53%, rgba(83,162,255,1) 76%)";
    var bg = document.getElementById('TBColor');
    bg.style.background = "radial-gradient(circle, rgba(251,169,205,1) 0%, rgba(250,255,128,1) 28%, rgba(133,255,141,1) 53%, rgba(83,162,255,1) 76%)";
    var bg = document.getElementById('TRColor');
    bg.style.background = "linear-gradient(90deg, rgba(250,255,128,1) 13%, rgba(133,255,141,1) 30%, rgba(83,162,255,1) 49%, rgba(133,255,141,1) 73%, rgba(222,255,131,1) 92%)";
    var bg = document.getElementById('TLColor');
    bg.style.background = "linear-gradient(90deg, rgba(250,255,128,1) 13%, rgba(133,255,141,1) 30%, rgba(83,162,255,1) 49%, rgba(133,255,141,1) 73%, rgba(222,255,131,1) 92%)";
  }

  document.getElementById('colorIP').onchange = function() {
    var bg = document.getElementById('TColor');
    bg.style.background = (this.value);
    var bg = document.getElementById('TBColor');
    bg.style.background = (this.value);
    var bg = document.getElementById('TRColor');
    bg.style.background = (this.value);
    var bg = document.getElementById('TLColor');
    bg.style.background = (this.value);
};

// All side of the product

 function front() {
  var front = document.getElementById('front-Tshirt');
  var back = document.getElementById('back-Tshirt');
  var right = document.getElementById('right-Tshirt');
  var left = document.getElementById('left-Tshirt');
  if(front.style.display === "none"){
    front.style.display = "flex";
    back.style.display = "none";
    right.style.display = "none";
    left.style.display = "none";
  }
};
function back() {
  var front = document.getElementById('front-Tshirt');
  var back = document.getElementById('back-Tshirt');
  var right = document.getElementById('right-Tshirt');
  var left = document.getElementById('left-Tshirt');
  if(back.style.display === "none"){
    front.style.display = "none";
    back.style.display = "flex";
    right.style.display = "none";
    left.style.display = "none";
  }
};
function right() {
  var front = document.getElementById('front-Tshirt');
  var back = document.getElementById('back-Tshirt');
  var right = document.getElementById('right-Tshirt');
  var left = document.getElementById('left-Tshirt');
  if(right.style.display === "none"){
    front.style.display = "none";
    back.style.display = "none";
    right.style.display = "flex";
    left.style.display = "none";
  }
};
function left() {
  var front = document.getElementById('front-Tshirt');
  var back = document.getElementById('back-Tshirt');
  var right = document.getElementById('right-Tshirt');
  var left = document.getElementById('left-Tshirt');
  if(left.style.display === "none"){
    front.style.display = "none";
    back.style.display = "none";
    right.style.display = "none";
    left.style.display = "flex";
  }
};

var Tshirt = window.opener('index.html');
  function tshirt() { 
      Tshirt.location.reload(true); 
  }
var hoodie = window.opener('hoodie.html');
  function hoodie() { 
      hoodie.location.reload(true); 
}