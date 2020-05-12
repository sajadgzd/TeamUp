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
      if(response["Success"]){
        console.log(response["Success"]);
        M.toast({html: `${response["Success"]}`})
        console.log(response["userData"][5])
        if(response["userData"][5] == "SUPER USER" || response["userData"][5] == "DEMOCRATIC SUPER USER"){
          window.location = '/SU';
        }
        else if(response["userData"][5] == "OU"){
          window.location = '/OU';
        }
        else if(response["userData"][5] == "VIP"){
          window.location = '/VIP';
        }

        localStorage.setItem('email', response["userData"][0]);
        let printStorage = localStorage.getItem('email');
        console.log("email logged in:\t", printStorage);
        // localStorage.removeItem('userEmail')
        // printStorage = localStorage.getItem('userEmail');
        // console.log(printStorage);

      }
      else if (response["Error"]){
        console.log(response["Error"]);
        M.toast({html: `${response["Error"]}`})
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