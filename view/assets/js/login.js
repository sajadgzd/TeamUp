// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();

  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, {});
  let elem = $(".modal")
  var instance = M.Modal.getInstance(elem);


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
    // console.log("text value:", text)

    var userlogin = {
      email: email,
      credentials: password 
    }

    console.log("LOGIN FORM COMPLETED:\v", JSON.stringify(userlogin))

    $.post("/loginUser", JSON.stringify(userlogin))
    .then(function(response) {
      console.log("login POST call worked");
      // if(true){
      //   localStorage.setItem('userEmail', 'e@gmail.com');
      //   let printStorage = localStorage.getItem('userEmail');
      //   console.log(printStorage);
        // localStorage.removeItem('userEmail')
        // printStorage = localStorage.getItem('userEmail');
        // console.log(printStorage);
      }
    });

    // loginFirstTime = true;
    // if(loginFirstTime){
    //   instance.open();

    //   let newEmail = $("#newEmail").val().trim()
    //   let newPassword = $("#newPassword").val().trim()
    //   // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    //   // console.log("text value:", text)
  
    //   var userlogin = {
    //     newEmail: newEmail,
    //     newPassword: newPassword 
    //   }

    //   $.post("/newPassword", newPassword)
    //   .then(function(response) {
    //     console.log("new pass POST call worked");
    //   });

    //   loginFirstTime = false
    // }

    

  });

  

});