// Make sure we wait to attach our handlers until the DOM is fully loaded.

// We will handle SU priviledges here

$(document).ready(function() {

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

  $(document.body).on("click", "#test2btn", function(event) {
    // event.preventDefault();
    // var text = $("#test2txt").val().trim()
    // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    // console.log("text value:", text)
    // var msg = {
    //   textmsg: text 
    // }
    // let groupName = $("#groupName").val().trim()
    // let invitees = []

    // for(let i=0; i< chipInstance.chipsData.length; i++){
    //   invitees.push(chipInstance.chipsData[i].tag)
    // }

    // let newGroup = {
    //   groupName : groupName,
    //   invitees : invitees
    // }

    // $.post("/createGroup", newGroup)
    // .then(function(data) {
    //   console.log("Create Group POST call worked with", JSON.stringify(newGroup));
    // });

  });

});