function get_tasks()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.responseText, function (key, value) {
                alert(value[0]);
              });
        }
    };
    xhttp.open("GET", "/tasks_current_user", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}