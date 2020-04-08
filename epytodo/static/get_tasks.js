function get_tasks()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
         if (this.readyState == 4 && this.status == 200) {
            alert(this.responseText);
        }
    };
    xhttp.open("GET", "/tasks_current_user", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
}