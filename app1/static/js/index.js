window.onload = initAll;

var show;
function initAll() {
    show =document.getElementById('show_calculation');
    show.onclick = check_nutri;

}
function  check_nutri() {

     var gen = document.getElementById("id_gender");
    var gen_result = gen.options[gen.selectedIndex].value;

    var age = document.getElementById("id_age").value;
    var height = document.getElementById("id_height").value;
    var weight = document.getElementById("id_weight").value;
    var bodyfat = document.getElementById("id_bodyfat").value;
    var bodyphy = document.getElementById("id_bodyphy").value;
    var ageexercise = document.getElementById("id_exercise").value;

    var activity = document.getElementById("id_activity");
    var activity_result = activity.options[activity.selectedIndex].value;


    var blood_pressure = document.getElementById("id_blood_pressure").value;
    var sugar = document.getElementById("id_sugar").value;
    var vitamin= document.getElementById("id_vitamin").value;
    var mineral = document.getElementById("id_mineral").value;
    var blood_group = document.getElementById("id_blood_group").value;
    var meal = document.getElementById("id_meal").value;

    var food_habbit = document.getElementById("id_food_habbit");
    var food_habbit_result = food_habbit.options[food_habbit.selectedIndex].value;


    var food_preference = document.getElementById("id_food_preference").value;

    var disability = document.getElementById("id_disability");
    var disability_result = disability.options[disability.selectedIndex].value;


    var medical_issues = document.getElementById("id_medical_issues");
    var medical_issues_result = medical_issues.options[medical_issues.selectedIndex].value;


    var diseases = document.getElementById("id_diseases").value;


  var url ="/check_nutri?gender"&age


    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
    }
  };
  req.open("GET", "", true);
  // req.send();

}