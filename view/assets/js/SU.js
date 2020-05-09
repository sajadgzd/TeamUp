// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();
  $('.tabs').tabs();
  
  $('.chips').chips();
  $('.chips-placeholder').chips({
    placeholder: 'Enter a username',
    secondaryPlaceholder: '+User',
  });
  let chipElem = $(".chips")
  var chipInstance = M.Chips.getInstance(chipElem);

  var modalElems = document.querySelectorAll('.modal');
  var modalInstances = M.Modal.init(modalElems, {});

  function getData() {
    $.ajax({
        url: "/test1",
        method: "GET"
    }).then(function(response) {
        console.log("GET root worked fine\n",response);
        $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");
    });
  };
  getData();

  $(document.body).on("click", "#test2btn", function(event) {
    event.preventDefault();
    var text = $("#test2txt").val().trim()
    $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    console.log("text value:", text)

    var msg = {
      textmsg: text 
    }

    $.post("/test2", msg)
    .then(function(data) {
      console.log("got data back from POST call", data.textmsg);
      alert("POST worked...");
    });

  });

});