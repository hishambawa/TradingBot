document.getElementById("login-form").addEventListener("submit", function(e) {
    e.preventDefault();

    let form = this.elements;

    let username = form['username'].value;
    let password = form['password'].value;

    sessionStorage.setItem("user", username);
    window.location.href = "dashboard.html?user=" + username;
});