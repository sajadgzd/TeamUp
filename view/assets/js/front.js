// Make sure we wait to attach our handlers until the DOM is fully loaded.
(function($){
    $(function(){
  
      $('.sidenav').sidenav();
  
    }); // end of document ready
  })(jQuery); // end of jQuery name space
  
  $(document).ready(function() {

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