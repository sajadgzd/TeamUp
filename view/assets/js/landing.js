// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();
  // init carousel
  var bestProjectsSlider = $('.carousel-bestProjects');
  bestProjectsSlider.carousel();

  //add a new item
  for(let i=0; i<3; i++){
    bestProjectsSlider.append('<div class="carousel-item blue white-text" href="#one!">' +
                    '<h2>TEST TITLE ' + i + '</h2>' +
                    '<p class="white-text">THIS IS A TEST</p>'+
                  '</div>');
  }
  //remove the 'initialized' class which prevents bestProjectsSlider from initializing itself again when it's not needed
  if (bestProjectsSlider.hasClass('initialized')){
      bestProjectsSlider.removeClass('initialized')
  }
  //just reinit the carousel
  bestProjectsSlider.carousel(); 


  //BestUsers
  // init carousel
  var bestUsersSlider = $('.carousel-bestUsers');
  bestUsersSlider.carousel();

  //add a new item
  for(let i=0; i<3; i++){
    bestUsersSlider.append('<div class="carousel-item blue white-text" href="#one!">' +
                    '<h2>TEST TITLE ' + i + '</h2>' +
                    '<p class="white-text">THIS IS A TEST</p>'+
                  '</div>');
  }
  //remove the 'initialized' class which prevents bestUsersSlider from initializing itself again when it's not needed
  if (bestUsersSlider.hasClass('initialized')){
      bestUsersSlider.removeClass('initialized')
  }
  //just reinit the carousel
  bestUsersSlider.carousel(); 

  function getData() {
    $.ajax({
        url: "/best3Projects",
        method: "GET"
    }).then(function(response) {
        console.log("GET root worked fine\n");
        // for(let i=0; i<3; i++){
        //   bestProjectsSlider.append('<div class="carousel-item blue white-text" href="#one!">' +
        //                   '<h2>TEST TITLE ' + i + '</h2>' +
        //                   '<p class="white-text">THIS IS A TEST</p>'+
        //                 '</div>');
        // }
        // //remove the 'initialized' class which prevents bestProjectsSlider from initializing itself again when it's not needed
        // if (bestProjectsSlider.hasClass('initialized')){
        //   bestProjectsSlider.removeClass('initialized')
        // }
        // //just reinit the carousel
        // bestProjectsSlider.carousel(); 
    });

    $.ajax({
      url: "/best3Users",
      method: "GET"
  }).then(function(response) {
      console.log("GET root worked fine\n");
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