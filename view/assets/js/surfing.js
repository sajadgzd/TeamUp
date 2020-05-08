// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();

  let ProjectsJson;
  let UsersJson;

  function getProjects(n) {
    $.ajax({
        url: "/getProjects",
        method: "GET"
    }).then(function(response) {
        console.log("GET root worked fine\n",response);
        ProjectsJson = response;
        // $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");
        for(let i=0; i<n; i++){
          $("#projects").append('<div class="col s12 m6">' +
          '<div class="card blue-grey darken-1">' +
            '<div class="card-content white-text">' +
              '<span class="card-title">Project Title</span>' +
              '<p>This section contains basic information regarding the item.' +
                '<br>The link below takes the user to view the item in more details' +
              '</p>' +
            '</div>' +
            '<div class="card-action">' +
              '<a href="#">View</a>' +
            '</div>' +
          '</div>' +
        '</div>')
        }
    });
  };
  function getUsers(n) {
    $.ajax({
        url: "/getUsers",
        method: "GET"
    }).then(function(response) {
        console.log("GET root worked fine\n",response);
        UsersJson = response;
        // $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");
        for(let i=0; i<n; i++){
          $("#users").append('<div class="col s12 m6">' +
          '<div class="card blue-grey darken-1">' +
            '<div class="card-content white-text">' +
              '<span class="card-title">Project Title</span>' +
              '<p>This section contains basic information regarding the item.' +
                '<br>The link below takes the user to view the item in more details' +
              '</p>' +
            '</div>' +
            '<div class="card-action">' +
              '<a href="#">View</a>' +
            '</div>' +
          '</div>' +
        '</div>')
        }
    });
  };
  getProjects(4);
  getUsers(4);

  $(document.body).on("click", "#showAll", function(event) {
    // event.preventDefault();
    // var text = $("#test2txt").val().trim()
    // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    // console.log("text value:", text)
    // var msg = {
    //   textmsg: text 
    // }
    // $.post("/test2", msg)
    // .then(function(data) {
    //   console.log("got data back from POST call", data.textmsg);
    //   alert("POST worked...");
    // });

    getProjects(ProjectsJson.length);
    getUsers(UsersJson.length);
    $("#showAll").hide();

  });

});