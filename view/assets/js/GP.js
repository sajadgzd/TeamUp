// Make sure we wait to attach our handlers until the DOM is fully loaded.
$(document).ready(function() {

  $('.sidenav').sidenav();

  var modalelems = document.querySelectorAll('.modal');
  var modalinstances = M.Modal.init(modalelems, {});

  var dateelems = document.querySelectorAll('.datepicker');
  var dateinstances = M.Datepicker.init(dateelems, {format: "mm/dd/yyyy"});

  var timeelems = document.querySelectorAll('.timepicker');
  var timeinstances = M.Timepicker.init(timeelems, {});

  var selectElems = document.querySelectorAll('select');
  var selectInstances = M.FormSelect.init(selectElems);
 
  let numOfChoices = 2;

  let email = localStorage.getItem('email');
  console.log("email logged in now as:\t", email);

  let groupName = localStorage.getItem('groupName');
  console.log("determined by localStorage you're in groupName:\t", groupName);


  $("#groupName").text(groupName);






  $("#closingPoll-button").click(function(){

    let pollTitle = $("#closingPollTitle").val().trim()
    let pollPrompt = $("#closingPollDescription").val().trim()

    let closingPollData = {
      groupName: groupName,
      pollTitle: pollTitle,
      pollPrompt: pollPrompt
    }

    $.post("/createCloseGroupPoll", closingPollData)
    .then(function(data) {
      console.log("got data back from POST call", JSON.stringify(data));
      alert("POST worked...");
    });


  });



  $("#polls-button").click(function(){
    let createrEmail = "X@gmail.com"

    let pollTitle = $("#pollTitle").val().trim()
    let pollPrompt = $("#pollDescription").val().trim()
    let pollType = $('#pollSelect').val()
    console.log(pollTitle)
    console.log(pollPrompt)
    console.log("poll Type:   ", pollType)

    let targetedMember = $("#targetedMemberEmail").val().trim()
    let pollStatus = "ACTIVE"
    let pollVoteChoice = "yes"
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
        no: pollVoteChoiceValComplement
      },
      voters: createrEmail
    };

    $.post("/createPoll", pollData)
    .then(function(data) {
      console.log("got data back from POST call", JSON.stringify(data));
      alert("POST worked...");
    });

  
  });



  $("#radiobtn").click(function(){
    var radioValue = $("input[name='group1']:checked").val();
    if(radioValue){
        alert("Your chose herew" + radioValue);
    }
  });

  $("#addSchedule-button").click(function(){
    numOfChoices++;
    $(".datechoices").append( `<div data-number='${numOfChoices}'>` +
                                '<div class="input-field col s4">' +
                                  `<input type="text" class="datepicker" id="meetingDateChoice" data-numberDate=${numOfChoices}>` +
                                  '<label for="postText">Date</label>' +
                                '</div>' +
                                '<div class="input-field col s4">' +
                                  `<input type="text" class="timepicker" id="meetingFromTimeChoice" data-numberFromTime=${numOfChoices}>` +
                                  '<label for="postText">From Time</label>' +
                                '</div>' +
                                '<div class="input-field col s4">' +
                                  `<input type="text" class="timepicker" id="meetingToTimeChoice" data-numberToTime=${numOfChoices}>` +
                                  '<label for="postText">To Time</label>' +
                                '</div>' +
                                '</div>')
   
    $('.datepicker').datepicker({format: "mm/dd/yyyy"});
    $('.timepicker').timepicker();                                          

  });



  $(document.body).on("click", "#schedule-button", function(event) {
    event.preventDefault();

    let pollTitle = $("#scheduleTitle").val().trim()
    let pollPrompt = $("#scheduleText").val().trim()
    let pollType = "MEETUP"
    let pollVoteOptions = []

    let date = ""
    let time1 = ""
    let time2 = ""
    let pollVoteChoice = ""; 

    console.log(numOfChoices)
    for(let i=1; i<= numOfChoices; i++){
      date = $(`div[data-number='${i}'] input[id='meetingDateChoice']`).val()
      time1 = $(`div[data-number='${i}'] input[id='meetingFromTimeChoice']`).val()
      time2 = $(`div[data-number='${i}'] input[id='meetingToTimeChoice']`).val()
      pollVoteChoice = date + " From " + time1 + " to " + time2;
      // console.log("POLL MEETUP CHOICE:\t", i , "- ", pollVoteChoice)
      pollVoteOptions.push(pollVoteChoice)
    }

    var meetupPollData = {
      groupName: groupName,
      pollCreator: email,
      pollTitle: pollTitle,
      pollPrompt: pollPrompt,
      pollType: pollType,
      pollStatus: "ACTIVE",
      pollVoteOptions: pollVoteOptions
    }

    // console.log("INPUT for meetupPollData\t", meetupPollData)

    $.post("/createMeetupPoll", JSON.stringify(meetupPollData))
    .then(function(response) {
      console.log("got data back from createMeetupPoll POST call", JSON.stringify(response));
      M.toast({html: response["Message"]})
      
    });

  });


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

  // $(document.body).on("click", "#post-button", function(event) {
  //   event.preventDefault();
  //   var text = $("#postText").val().trim()
  //   // $("#reg-form").append("<p style='font-weight: bold'> Typed: " + text + "</p><br>")
  //   console.log("text value:", text)

  //   var msg = {
  //     textmsg: text 
  //   }

  //   $.post("/postText", msg)
  //   .then(function(data) {
  //     console.log("got data back from POST call", data.textmsg);
  //     alert("POST worked...");
  //   });

  // });

});