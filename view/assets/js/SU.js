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

  let email = localStorage.getItem('email');
  console.log("email logged in:\t", email);

  $("#userEmail").text(email);


    emailData = {
      email: email
    }
    $.post("/getUserData", JSON.stringify(emailData))
    .then(function(response) {
      // console.log("call worked with\t " + JSON.stringify(response));
      $("#userEmail").text(response["userData"][1]);
      $("#reputationScore").text(response["userData"][4]);
    });


  $(document.body).on("click", "#createGroup-button", function(event) {
    event.preventDefault();


    let groupName = $("#groupName").val().trim()

    createGroupData = {
      groupName: groupName,
      email: email
    }

    // console.log(JSON.stringify(createGroupData))

    $.post("/createGroup", JSON.stringify(createGroupData))
    .then(function(response) {
      // console.log("call worked with\t " + JSON.stringify(response));
    });

    location.reload();

  });


  $.post("/getUserData", JSON.stringify(emailData))
  .then(function(response) {
    console.log("GROUUPS::::\t " + JSON.stringify(response["userData"][3]));

    for(let i=0; i<response["userData"][3].length; i++){

      console.log("LOOOPING")
      let groupName = response["userData"][3][i]

      groupNameJSON = {
        groupName: groupName
      }

      $.post("/getGroupData", JSON.stringify(groupNameJSON))
      .then(function(response) {
        console.log("GroupData ACTIVE AND CLOSED\t " + JSON.stringify(response));
        console.log("GroupData ACTIVE AND CLOSED\t " + JSON.stringify(response["groupData"][1]));

        if((response["groupData"][1]) == "ACTIVE"){

          $("#groupsDiv").append('<div class="col s12 m4">' +
                                  `<div class="card blue-grey darken-1">` +
                                    `<div class="card-content white-text">` +
                                      `<span class="card-title">${response["groupData"][0]}</span>` +
                                    `</div>` +
                                    `<div class="card-action">` +
                                      `<a href="/groupMainPage" target=”_blank”>View</a>` +
                                    `</div>` +
                                  `</div>` +
                                `</div>`)
        }



      });


    }


  
  });




});