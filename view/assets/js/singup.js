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
        // console.log("NOW: \n", response.allUsersEmail.length);
        console.log("Data:\n",response["allUsersEmail"])

        for(let i = 0; i< response.allUsersEmail.length; i++){
          console.log(response["allUsersEmail"][i])
           $('#referMemberSelect').append(`<option value="${response["allUsersEmail"][i]}"> 
                                       ${response["allUsersEmail"][i]} 
                                  </option>`); 
            
        }
        $('select').formSelect();
        
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
      console.log(response["Message"]);
      M.toast({html: `${response["Message"]}`})
    });

  });


  $(document.body).on("click", "#checkStatus-button", function(event) {
    event.preventDefault();
    let checkStatusEmail = $("#checkStatusEmail").val().trim()

    let statusEmail = {
      email : checkStatusEmail
    }

    console.log("EMAIL CHECK\t", checkStatusEmail);


    $.post("/checkStatus", JSON.stringify(statusEmail))
    .then(function(data) {
     
      console.log("CHECK STATUS POST wroked with JSON:\t" + JSON.stringify(data));
      let form = $("#checkResultDiv")

      // count++

      $(".statusResp").remove()
      $(".statusResp").remove()
      
      

      if (data.Status == "PENDING" || data.Status == "USER" || data.Status == "APPEALED" || data.Status == "BLACKLISTED"){
        form.append('<div class="col s12 m12 info center-align statusResp" id="statusResp" style="">' +
                      data.Message +
                      '</div>')
      }
      else if (data.Status == "REJECTED"){
        form.append('<div class="col s12 m12 info center-align statusResp" id="statusResp" style="">' +
        data.Message +
        '</div>').append('<form class="col s12 m12 statusResp" id="appeal-form" style="">' +
                            '<h5 class="center-align register">Write your appeal</h5>' +
                            '<div class="input-field col s12">' +
                              '<input id="appealInput" type="text" class="validate" required>' +
                              '<label for="appealInput">Appeal Message</label>' +
                            '</div>' +
                            '<div class="input-field col s6" >' +
                              '<a href="#" id="appeal-button" class="btn waves-effect waves-light light-blue accent-4">Submit</a> <br><br>' +
                            '</div>' +
                          '</form>')

        $(document.body).on("click", "#appeal-button", function(event) {
            let appealData = {
              email: $("#checkStatusEmail").val().trim(),
              appealMessage: $("#appealInput").val().trim()
            }

            console.log("appealData\t", JSON.stringify(appealData))

            $.post("/appealRejection", JSON.stringify(appealData))
            .then(function(response) {
              console.log("DATA BACK FROM APPEAL POST REQ: \t", response)
              $("#appeal-form").append(`<h6>  ${response["Message"]} </h6>`)

            })
          })

        
      }
      else {
        form.append('<div class="col s12 m12 info center-align statusResp" id="statusResp" style="">' +
        data.Message +
        '</div>')
      }


    });

  });

});