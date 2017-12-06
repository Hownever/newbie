function login_input_check() {
    if (!document.getElementById) {
        return false;
    }
    document.getElementById("username").oninput = function() {
        var UserName = document.getElementById("username").value;
        if (UserName.length < 6 && UserName.length > 0) {
            document.getElementById("tishi").innerHTML = "<font color='red'>*长度小于6</font>";
        } else {
            document.getElementById("tishi").innerHTML = "<font color='red'></font>";
        }
    }
}