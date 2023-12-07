window.onload =  function() {
    if (!localStorage.getItem("cookieConsent")) {
        alert("This website uses cookie to enhance user experience. By proceeding you accept the use of cookies.");
        localStorage.setItem("cookieConsent", "true");
    }
}