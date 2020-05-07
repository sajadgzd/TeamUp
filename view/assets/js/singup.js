// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();
  var elems = document.querySelectorAll('.chips');
  var instances = M.Chips.init(elems, {});

  let elem = $(".chips")
  var instance = M.Chips.getInstance(elem);

  $(document.body).on("click", "#signup-button", function(event) {
    event.preventDefault();
    let firstname = $("#first_name").val().trim()
    let lastname = $("#last_name").val().trim()
    let email = $("#email").val().trim()
    let password = $("#password").val().trim()
    let referringMember = $("#referringMember").val().trim()
    let interests = []
    // console.log("CHIP 0:\t", instance.chipsData)
    for(let i=0; i< instance.chipsData.length; i++){
      interests.push(instance.chipsData[i].tag)
    }

    let user = {
      firstname: firstname,
      lastname: lastname,
      email: email,
      password: password,
      referringMember: referringMember,
      interests: interests
    }

    console.log("FORM COMPLETED:\v", JSON.stringify(user))

    $.post("/signup", user)
    .then(function(data) {
      console.log("signup POST wroked");
    });

  });

  

});