function create_user() {
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
             alert(this.responseText);
         }
    };
    xhttp.open("POST", "/register", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send('{"username": "'+ username +'", "password": "'+ password +'"}');
}