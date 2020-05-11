// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();
  // $('.chips').chips();
  // $('.chips-placeholder').chips({
  //   placeholder: 'Enter a username',
  //   secondaryPlaceholder: '+Interest',
  // });

  // var chip = {
  //   tag: 'chip content',
  //   image: '', //optional
  // };
  // var elem = $('.chips')
  // var instance = M.Chips.getInstance(elem);
  // instance.selectChip(2); // Select 2nd chip

  var modalelems = document.querySelectorAll('.modal');
  var modalinstances = M.Modal.init(modalelems, {});

  var dateelems = document.querySelectorAll('.datepicker');
  var dateinstances = M.Datepicker.init(dateelems, {format: "mm/dd/yyyy"});

  var timeelems = document.querySelectorAll('.timepicker');
  var timeinstances = M.Timepicker.init(timeelems, {});

  var selectElems = document.querySelectorAll('select');
  var selectInstances = M.FormSelect.init(selectElems);
 
  

  let numOfChoices = 2;

  $("#polls-button").click(function(){
    let pollTitle = $("#pollTitle").val().trim()
    let pollPrompt = $("#pollDescription").val().trim()
    let pollType = $('#pollSelect').val()
    console.log(pollTitle)
    console.log(pollPrompt)
    console.log("poll Type:   ", pollType)

    let targetedMember = $("#targetedMember").val().trim()
    let pollStatus = "ACTIVE"
    let pollVoteChoice = $("#targetedMember").val()
    let pollVoteChoiceVal = 0;
    let pollVoteChoiceValComplement = 1;

    if (pollVoteChoice == "yes"){
      pollVoteChoiceVal = 1
      pollVoteChoiceValComplement = 0;
    }

    let votersArray = []


    var pollData = {
      pollTitle: pollTitle,
      pollPrompt: pollPrompt,
      pollType: pollType,
      targetedMember: targetedMember,
      pollStatus: pollStatus,
      pollVoteOptions: {
        yes: pollVoteChoiceVal,
        no: pollVoteChoiceVal
      },
      voters: votersArray
    };

  
  });



  $("#radiobtn").click(function(){
    var radioValue = $("input[name='group1']:checked").val();
    if(radioValue){
        alert("Your chose " + radioValue);
    }
  });
  $("#addSchedule-button").click(function(){
    $(".datechoices").append('<div class="input-field col s4">' +
                                                  '<input type="text" class="datepicker">' +
                                                  '<label for="postText">Date</label>' +
                                                '</div>' +
                                                '<div class="input-field col s4">' +
                                                  '<input type="text" class="timepicker">' +
                                                  '<label for="postText">From Time</label>' +
                                                '</div>' +
                                                '<div class="input-field col s4">' +
                                                  '<input type="text" class="timepicker">' +
                                                  '<label for="postText">To Time</label>' +
                                                '</div>')
    numOfChoices++;
    $('.datepicker').datepicker({format: "mm/dd/yyyy"});
    $('.timepicker').timepicker();                                          

  });

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

  $(document.body).on("click", "#post-button", function(event) {
    event.preventDefault();
    var text = $("#postText").val().trim()
    // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    console.log("text value:", text)

    var msg = {
      textmsg: text 
    }

    $.post("/postText", msg)
    .then(function(data) {
      console.log("got data back from POST call", data.textmsg);
      alert("POST worked...");
    });

  });



  $(document.body).on("click", "#schedule-button", function(event) {
    event.preventDefault();
    var text = $("#scheduleText").val().trim()
    // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
    console.log("text value:", text);

    let date = ""
    let time1 = ""
    let time2 = ""

    let choices = []

    for(let i=0; i<numOfChoices.length; i++){
      choices.push(date + " From " + time1 + " to " + time2)
    }

    var schedule = {
      textmsg: text,
      choices: choices
    }

    $.post("/postText", msg)
    .then(function(data) {
      console.log("got data back from POST call", data.textmsg);
      alert("POST worked...");
    });

  });

});