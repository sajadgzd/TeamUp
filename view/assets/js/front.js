// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();

  function getData() {
    $.ajax({
        url: "/test1",
        method: "GET"
    }).then(function(response) {
        // console.log(response);
        console.log("HELLOOOOOO\n");
        $("#test1").append("<p style='font-weight: bold'> Type: " + response.tasks[0].description + "</p><br>");
    });
  };
  getData();

  // var server = "http://127.0.0.1:5000";
  // var send_msg = {'name':""};
  // function update_var(){
  //     var name = String($("#test2name").val());
  //     send_msg['name']=name;
  //     console.log("update var")
  // }
  
  // function pushData(){
  //     var appdir="/";
  //     update_var();
  //     console.log(send_msg)
  //     $.ajax({
  //             type: "POST",
  //             url:server + appdir,
  //             data: JSON.stringify(send_msg),
  //             dataType: 'json',
  //             contentType: 'application/json',
  //         }).done(function(data) {
  //             $('#Response').html(data['message']);
  //         });
  
  // }
  // pushData();

  $(document.body).on("click", "#test2btn", function(event) {
    event.preventDefault();
    var text = $("#test2txt").val().trim()
    $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")

    var msg = {
      textmsg: text 
    }

    // Send the POST request.
    $.ajax({
        type: "POST",
        url: "/test2",
        data: JSON.stringify(msg)
    }).then(
        function() {
            console.log(msg);
            // Reload the page to get the updated list
            location.reload();
        }
    );
});

});