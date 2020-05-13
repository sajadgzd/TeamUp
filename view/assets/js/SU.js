// Make sure we wait to attach our handlers until the DOM is fully loaded.

// We will handle SU priviledges here

$(document).ready(function() {

  $('.sidenav').sidenav();
  $('.tabs').tabs();
  
  // $('.chips').chips();
  // $('.chips-placeholder').chips({
  //   placeholder: 'Enter a username',
  //   secondaryPlaceholder: '+User',
  // });
  // let chipElem = $(".chips")
  // var chipInstance = M.Chips.getInstance(chipElem);

  var modalElems = document.querySelectorAll('.modal');
  var modalInstances = M.Modal.init(modalElems, {});

  var selectElems = document.querySelectorAll('select');
  var selectInstances = M.FormSelect.init(selectElems, {});

  var selectInstance = M.FormSelect.getInstance(selectElems);

  let email = localStorage.getItem('email');
  console.log("email logged in:\t", email);

  $("#userEmail").text(email);





  $(document.body).on("click", "#createInvite-button", function(event) {
    event.preventDefault();
    let groupName = $("#createInviteGroupList").val()
    let inviterEmail = email
    let inviteeEmail = $("#createInviteUserList").val()

    createInviteData = {
      groupName: groupName,
      inviterEmail: inviterEmail,
      inviteeEmail: inviteeEmail
    }

    // console.log("createInviteData input:\t", JSON.stringify(createInviteData))

    $.post("/inviteToGroup", JSON.stringify(createInviteData))
    .then(function(response) {
      console.log("inviteToGroup call worked with\t " + JSON.stringify(response));
      M.toast({html: response["Message"]})
    });


  });


  $.ajax({
    url: "/getAllUserEmails",
    method: "GET"
  }).then(function(response) {
      // console.log("GOT BACK SOMETHING")
      // console.log("NOW: \n", response.allUsersEmail.length);
      // console.log("Data:\n",response["allUsersEmail"])

      for(let i = 0; i< response.allUsersEmail.length; i++){
        // console.log(response["allUsersEmail"][i])
        if(response["allUsersEmail"][i] != email){
          $('#whiteEmailAddition').append(`<option value="${response["allUsersEmail"][i]}"> 
                                              ${response["allUsersEmail"][i]} 
                                           </option>`); 
          $('#blackEmailAddition').append(`<option value="${response["allUsersEmail"][i]}"> 
                                              ${response["allUsersEmail"][i]} 
                                            </option>`);
          $('#createInviteUserList').append(`<option value="${response["allUsersEmail"][i]}"> 
                                              ${response["allUsersEmail"][i]} 
                                            </option>`);                           
        }
          
      }
      $('select').formSelect();
      
  });

  $(document.body).on("click", "#addWhite-button", function(event) {

    // console.log("EMAIL ADDITION: \t", $('#whiteEmailAddition').val())
    let addWhiteData = {
      userEmail: email,
      emailAddition: $('#whiteEmailAddition').val()
    }

    $.post("/addToWhiteBox", JSON.stringify(addWhiteData))
    .then(function(response) {
      // console.log("ADD TO WHITEBOX call worked with\t " + JSON.stringify(response));
      M.toast({html: response["Message"]})
    });
  })

  $(document.body).on("click", "#addBlack-button", function(event) {

    // console.log("BLACK EMAIL ADDITION: \t", $('#blackEmailAddition').val())
    let addBlackData = {
      userEmail: email,
      emailAddition: $('#blackEmailAddition').val()
    }

    $.post("/addToBlackBox", JSON.stringify(addBlackData))
    .then(function(response) {
      // console.log("ADD TO BLACKBOX call worked with\t " + JSON.stringify(response));
      M.toast({html: response["Message"]})
    });
  })


    emailData = {
      email: email
    }
    $.post("/getUserData", JSON.stringify(emailData))
    .then(function(response) {
      // console.log("getUserData call worked with\t " + JSON.stringify(response));
      $("#userEmail").text(response["userData"][1]);
      $("#reputationScore").text(response["userData"][5] + " with a Reputation Score of " + response["userData"][4]);
    });


  $(document.body).on("click", "#createGroup-button", function(event) {
    event.preventDefault();


    let groupName = $("#groupName").val().trim()

    createGroupData = {
      groupName: groupName,
      email: email
    }

    console.log("CREATE GROUP DATA input:\t", JSON.stringify(createGroupData))

    $.post("/createGroup", JSON.stringify(createGroupData))
    .then(function(response) {
      // console.log("CREATE GROUP call worked with\t " + JSON.stringify(response));
    });

    // location.reload();

  });


  $.post("/getUserData", JSON.stringify(emailData))
  .then(function(response) {

    console.log("get User Data GROUPS:\t " + JSON.stringify(response["userData"][3]));

    for(let i=0; i<response["userData"][3].length; i++){

      let emailToPass = localStorage.getItem('email')
      let groupName = response["userData"][3][i]

      groupNameJSON = {
        groupName: groupName
      }

      $.post("/getGroupData", JSON.stringify(groupNameJSON))
      .then(function(response) {
        // console.log("GroupData ACTIVE AND CLOSED\t " + JSON.stringify(response));
        // console.log("GroupData ACTIVE AND CLOSED\t " + JSON.stringify(response["groupData"][1]));

        if((response["groupData"][1]) == "ACTIVE"){

          $("#groupsDiv").append('<div class="col s12 m4">' +
                                  `<div class="card blue-grey darken-1">` +
                                    `<div class="card-content white-text">` +
                                      `<span class="card-title">${response["groupData"][0]}</span>` +
                                    `</div>` +
                                    `<div class="card-action">` +
                                      `<a href="/groupMainPage">View</a>` +
                                    `</div>` +
                                  `</div>` +
                                `</div>`)

        localStorage.setItem('groupName', response["groupData"][0]);
        localStorage.setItem('email', emailToPass);
        // let printStorage = localStorage.getItem('groupName');
        // let printEmailToPass = localStorage.getItem('email');
        // console.log("determined by localStorage you're in groupName:\t", printStorage);
        // console.log("determined by localStorage you're in EMAIL:\t", printEmailToPass);

        }
      });
    }

    // GERENATE WHITE LIST
    for(let i=0; i<response["userData"][8].length; i++){

      // console.log("LOOOPING in GetUserData for WhiteList", response["userData"][8][i])
      $("#whiteListDiv").append('<div class="col s4 m2">' +
                              `<div class="card blue-grey darken-1">` +
                                `<div class="card-content white-text"> User Email: `  +
                                  `<span class="card-title">${response["userData"][8][i]}</span>` +
                                `</div>` +
                              `</div>` +
                            `</div>`)

    }

    // GENERATE BLACK LIST
    for(let i=0; i<response["userData"][7].length; i++){

      // console.log("LOOOPING in GetUserData for BLACK LIST", response["userData"][7][i])
      $("#blackListDiv").append('<div class="col s4 m2">' +
                              `<div class="card blue-grey darken-1">` +
                                `<div class="card-content white-text"> User Email: `  +
                                  `<span class="card-title">${response["userData"][7][i]}</span>` +
                                `</div>` +
                              `</div>` +
                            `</div>`)

    }

    // GENERATE Group LIST in options invitations
    for(let i=0; i<response["userData"][3].length; i++){
      // console.log("LIST OF ALL GROUPS::", response["userData"][3][i])

    $('#createInviteGroupList').append(`<option value="${response["userData"][3][i]}"> 
          ${response["userData"][3][i]} 
        </option>`);
    }
    $('select').formSelect();


    // GENERATE INVITATION CARDS
    // console.log("First Invitation::", response["userData"][6][0]["groupName"])
    for(let i=0; i<response["userData"][6].length; i++){
      // console.log("LIST OF ALL Invitations::", response["userData"][6][0])
      $("#showInvitations").append(`<div class="col s12 m4">` +
                                      `<div class="card blue-grey darken-1">` +
                                        `<div class="card-content white-text">` +
                                          `<span class="card-title">${response["userData"][6][i]["groupName"]}</span>` +
                                          `<p>Invitation Sent From:</p>` +
                                          `<p>${response["userData"][6][0]["inviterEmail"]}</p>` +
                                        `</div>` +
                                        `<div class="card-action">` +
                                          `<a href="#" id="handleInviteAccept-button" groupName=${response["userData"][6][i]["groupName"]} 
                                          inviterEmail=${response["userData"][6][0]["inviterEmail"]} >Accept</a>` +
                                          // `<a class="" href="#inviteDeclineIntital">Decline</a>` +
                                          `<div id="inviteDeclineMessageDiv">` +
                                            `<h6>Please explain the reason why you'd like to decline the invitation?</h6>` +
                                            `<div class="input-field col s12">` +
                                              `<input id="inviteDeclineMessage" type="text" class="validate" required>` +
                                              `<label for="inviteDeclineMessage">Reason</label>` +
                                           `</div>` +
                                          `</div>` +
                                          `<a href="#" class="" id="inviteDeclineSubmit-button" 
                                          groupName=${response["userData"][6][i]["groupName"]} 
                                          inviterEmail=${response["userData"][6][0]["inviterEmail"]}>Decline</a>` +
                                        `</div>` +
                                    `</div>`)
    }

  });

  let signupData = {
    email: email
  }


    function getData() {
    $.ajax({
        url: "/getAllSignUpData",
        method: "GET"
    }).then(function(response) {
        console.log("GET root worked fine\n",JSON.stringify(response));
        // $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");

      for(let i=0; i<response["signUpData"].length; i++){
        for(let j=0; j<response["signUpData"][i].length; i++){
            // console.log("LOOOPING \t", response["signUpData"][i][6])

            if((response["signUpData"][i][6]) == "PENDING"){
            $("#NewRegistrationsTab").append(`<div class="col s12 m4 NewDiv" id=${response["signUpData"][i][1]}>` +
                                                `<div class="card blue-grey darken-1">` +
                                                  `<div class="card-content white-text">` +
                                                    `<span class="card-title">${response["signUpData"][i][0]}</span>` +
                                                    `<p id="applicantEmail">${response["signUpData"][i][1]}</p>` +
                                                    `<p>New User Registration Request<br></p>` +
                                                  `</div>` +
                                                  `<div class="card-action">` +
                                                    `<a href="#" id="handle-button">ACCEPT</a>` +
                                                    `<a href="#" id="handle-button">DECLINE</a>` +
                                                  `</div>` +
                                                `</div>` +
                                              `</div>`)
          }
          else if((response["signUpData"][i][6]) == "APPEALED"){
            $("#NewRegistrationsTab").append(`<div class="col s12 m4 NewDiv" id=${response["signUpData"][i][1]}>` +
                                                `<div class="card blue-grey darken-1">` +
                                                  `<div class="card-content white-text">` +
                                                    `<span class="card-title">${response["signUpData"][i][0]}</span>` +
                                                    `<p id="applicantEmail">${response["signUpData"][i][1]}</p>` +
                                                    `<p>${response["signUpData"][i][5]}</p>` +
                                                  `</div>` +
                                                  `<div class="card-action">` +
                                                    `<a href="#" id="handle-button">ACCEPT</a>` +
                                                    `<a href="#" id="handle-button">BLACKLIST</a>` +
                                                  `</div>` +
                                                `</div>` +
                                              `</div>`)
          }
        }
      }

    });
  };
  getData();


  $(document.body).on("click", "#handle-button", function(event) {

    // console.log("BUTTON TEXT: ", $("#applicantEmail").text())

    let handleAppData = {
      response: $(this).text(), //acc dec bl
      applicantEmail: $("#applicantEmail").text()
    }
  
    $.post("/handleApplication", JSON.stringify(handleAppData))
    .then(function(response) {
          // console.log(response["Message"])
          M.toast({html: response["Message"]})
          location.reload()
        }
      );

  });

  // $("#inviteDeclineMessageDiv").hide()
  // $(document.body).on("click", "#inviteDeclineIntital", function(event) {
  //   $("#inviteDeclineMessageDiv").show()
  // }); 
  // $(document.body).on("click", "#inviteDeclineSubmit-button", function(event) {
    
  // })

  $(document.body).on("click", "#handleInviteAccept-button", function(event) {

    let handleInviteAccept = {
      inviterEmail: $(this).attr("inviterEmail"), 
      groupName: $(this).attr("groupName"),
      inviteeEmail: email,
      message: $(this).val().trim(),
      response: "accept",
    }

    console.log("handleInviteAccept INPUT:\t", handleInviteAccept)
  
    $.post("/handleGroupInvite", JSON.stringify(handleInviteAccept))
    .then(function(response) {
              console.log("GOT THIS BACK FROM handleGroupInvite", response)
              console.log(response["Message"])
              M.toast({html: response["Message"]})
    //       location.reload()
        }
      );

  }); 



  $(document.body).on("click", "#inviteDeclineSubmit-button", function(event) {

    let inviteDeclineSubmit = {
      inviterEmail: $(this).attr("inviterEmail"), 
      groupName: $(this).attr("groupName"),
      inviteeEmail: email,
      message: $("#inviteDeclineMessage").val().trim(),
      response: "decline",
    }

    console.log("inviteDeclineSubmit INPUT:\t", JSON.stringify(inviteDeclineSubmit))
  
    $.post("/handleGroupInvite", JSON.stringify(inviteDeclineSubmit))
    .then(function(response) {
          console.log("GOT THIS BACK FROM handleGroupInvite",response)
          console.log(response["Message"])
          M.toast({html: response["Message"]})
          // location.reload()
        }
      );

  });







});