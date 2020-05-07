// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();


  // function getData() {
  //   $.ajax({
  //       url: "/test1",
  //       method: "GET"
  //   }).then(function(response) {
  //       console.log("GET root worked fine\n",response);
  //       $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");
  //   });
  // };
  // getData();

  $(document.body).on("click", "#login-button", function(event) {
    event.preventDefault();
    let email = $("#email").val().trim()
    let password = $("#password").val().trim()
    // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    // console.log("text value:", text)

    var userlogin = {
      email: email,
      password: password 
    }

    console.log("LOGIN FORM COMPLETED:\v", JSON.stringify(userlogin))

    $.post("/login", userlogin)
    .then(function(data) {
      console.log("login POST call worked");
    });

  });

  

});