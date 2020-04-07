function create_user()
{
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText, function (key, value) {
                if (key == "result") {
                  alert("Account has been crceated");
                }
                if (key == "error" && value == "account already exists") {
                    alert("An account with this username already exists");
                }else if (key == "error" && value == "internal error") {
                    alert("An error has occured, try to re sign up.");
                }
              });
         }
    };
    xhttp.open("POST", "/register", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send('{"username": "'+ username +'", "password": "'+ password +'"}');
}

function signin()
{
    var username = document.getElementById('user_name').value;
    var password = document.getElementById('password').value;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.responseText, function (key, value) {
                if (key == "result") {
                  alert("You've been logged in");
                  window.location.replace("/home");
                  return true;
                }
                if (key == "error" && value == "login or password does not match") {
                    alert("Your username or your password does not match");
                    return false;
                }else if (key == "error" && value == "internal error") {
                    alert("An error has occured, try to re sign in.");
                    return false;
                }
              });
         }
    };
    xhttp.open("POST", "/signin", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send('{"username": "'+ username +'", "password": "'+ password +'"}');
}