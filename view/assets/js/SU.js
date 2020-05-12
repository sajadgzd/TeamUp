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
      console.log("call worked with\t " + JSON.stringify(response));
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
      console.log("call worked with\t " + JSON.stringify(response));
    });

  });

});