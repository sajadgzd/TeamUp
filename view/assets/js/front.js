// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();

  function getData() {
    $.ajax({
        url: "/",
        method: "GET"
    }).then(function(response) {
        console.log(response);
    });
  };
  getData();

});