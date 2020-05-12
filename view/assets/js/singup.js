// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();
  // var elems = document.querySelectorAll('.chips');
  // var instances = M.Chips.init(elems, {});

  // let elem = $(".chips")
  // var instance = M.Chips.getInstance(elem);

  var selectElems = document.querySelectorAll('select');
  var selectInstances = M.FormSelect.init(selectElems, {});

  var selectInstance = M.FormSelect.getInstance(selectElems);


  function getData() {
    $.ajax({
        url: "/getAllUserEmails",
        method: "GET"
    }).then(function(response) {
        console.log("GOT BACK SOMETHING")
        console.log("NOW: \n", response.allUsersEmail.length);
        console.log("NOW Obj: \n", response);

        for(let i = 0; i< response.allUserEmail.length; i++){
          console.log(response.allUserEmail[i])
           $('#referMemberSelect').append(`<option value="${response.allUserEmail[i]}"> 
                                       ${response.allUserEmail[i]} 
                                  </option>`); 
        }

  // $('#referMemberSelect').append(`<option value="${optionValue}"> 
  //                                      ${optionText} 
  //                                 </option>`); 
        
    });
  };
  getData();




  $(document.body).on("click", "#signup-button", function(event) {
    event.preventDefault();
    let firstname = $("#first_name").val().trim()
    let lastname = $("#last_name").val().trim()
    let fullname = firstname + " " + lastname
    let email = $("#email").val().trim()
    let password = $("#password").val().trim() 
    // let referringMember = $("#referringMember").val().trim()
    let referringMember = $('#referMemberSelect').val()

    let interests = $("#interests").val().trim()

    let user = {
      fullname: fullname,
      email: email,
      interests: interests,
      credentials: password,
      reference: referringMember,
    }

    console.log("FORM COMPLETED:\v", JSON.stringify(user))

    $.post("/signupApplication", JSON.stringify(user))
    .then(function(response) {
      console.log("signup POST wroked with JSON:\t");
      M.toast({html: 'Signed Up!'})
    });

  });


  $(document.body).on("click", "#checkStatus-button", function(event) {
    event.preventDefault();
    let checkStatusEmail = $("#checkStatusEmail").val().trim()

    let statusEmail = {
      email : checkStatusEmail
    }

    $.post("/checkStatus", statusEmail)
    .then(function(data) {
      console.log("signup POST wroked with JSON:\t" + JSON.stringify(data));
      let form = $("#lastItemForm")

      if (data.Status == "PENDING" || data.Status == "USER" || data.Status == "APPEALED" || data.Status == "BLACKLISTED"){
        form.append('<div class="col s2 m2 info center-align" style="">' +
                      data.Message +
                      '</div>')
      }
      else if (data.Status = "REJECTED"){
        form.append('<div class="col s2 m2 info center-align" style="">' +
        data.Message +
        '</div>').append('<form class="col s12 m12" id="appeal-form" style="">' +
                            '<h5 class="center-align register">Write your appeal</h5>' +
                            '<div class="input-field col s12">' +
                              '<input id="appealInput" type="text" class="validate" required>' +
                              '<label for="appealInput">Appeal Message</label>' +
                            '</div>' +
                            '<div class="input-field col s6" id="lastItemForm" >' +
                              '<a href="#" id="checkStatus-button" class="btn waves-effect waves-light light-blue accent-4">Submit</a> <br><br>' +
                            '</div>' +
                          '</form>')
        
      }
      else {
        form.append('<div class="col s2 m2 info center-align" style="">' +
        data.Message +
        '</div>')
      }
    });

  });

});