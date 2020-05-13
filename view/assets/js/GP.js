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

  // $(document.body).on("click", "#meetupVoteButton", function(event) {
  //   event.preventDefault()
  //   console.log("RADIO BUTTON CLICKED")
  //   var radioValue = $("input[name='meetupChoices']:checked").val();
  //   if(radioValue){
  //     console.log(("YOUR CHOICE HERE IS" + radioValue))
  //       alert("YOUR CHOICE HERE IS:\t" + radioValue);
  //   }
  // });

  groupNameJSON = {
    groupName: groupName
  }

  $.post("/getGroupData", JSON.stringify(groupNameJSON))
  .then(function(response) {
    // console.log("GroupData ACTIVE AND CLOSED\t " + JSON.stringify(response));
    console.log("GroupData\t " + JSON.stringify(response["groupData"][4]));
    let groupPollList = response["groupData"][4]; // closing and meetup
    let memberPollList = response["groupData"][3]; // kick praise warn

    for(let i=0; i< groupPollList.length; i++) {
      let pTags = "";
      console.log("LOOK",groupPollList[i]["pollVoteOptionsList"])
      for(let j=0; j<groupPollList[i]["pollVoteOptionsList"].length; j++){
        pTags += `<p>` +
                  `<label>` +
                    `<input name="meetupChoices" type="radio" value="${groupPollList[i]["pollVoteOptionsList"][j]}"/>` +
                    `<span>${groupPollList[i]["pollVoteOptionsList"][j]}</span>` +
                  `</label>` +
                `</p>`
      }

      $("#showAllPolls").append(`<form class="col s12 m12" id="reg-form">` +
      `<h6><b>${groupPollList[j]["pollCreator"]}</b> posted the following poll</h6>` +
      `<h6>Title: <b>${groupPollList[j]["pollTitle"]}</b></h6>` +
      `<h6>Description: <b>${groupPollList[j]["pollPrompt"]}</b></h6>` +
      `<br>` +
      `<form action="#">` +
        pTags +
      `</form>` +
      `<a href="#" id="meetupVoteButton" class="btn waves-effect waves-light light-blue accent-4" style="margin-left: 2%">Vote` +
        `<i class="material-icons right">done</i>` +
      `</a>` +
      `</form>`)
    }


    }
  );

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

    // console.log(numOfChoices)
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

      // let pTags = "";
      // for(let i=0; i<pollVoteOptions.length; i++){
      //   pTags += `<p>` +
      //             `<label>` +
      //               `<input name="meetupChoices" type="radio" value="${pollVoteOptions[i]}"/>` +
      //               `<span>${pollVoteOptions[i]}</span>` +
      //             `</label>` +
      //           `</p>`
      // }
      // $("#showAllPolls").append(`<form class="col s12 m12" id="reg-form">` +
      //                             `<h6><b>${email}</b> posted the following poll</h6>` +
      //                             `<h6>Title: <b>${pollTitle}</b></h6>` +
      //                             `<h6>Description: <b>${pollPrompt}</b></h6>` +
      //                             `<br>` +
      //                             `<form action="#">` +
      //                               pTags +
      //                             `</form>` +
      //                             `<a href="#" id="meetupVoteButton" class="btn waves-effect waves-light light-blue accent-4" style="margin-left: 2%">Vote` +
      //                               `<i class="material-icons right">done</i>` +
      //                             `</a>` +
      //                           `</form>`)
      
    });

  });

  $("#closingPoll-button").click(function(){

    let pollTitle = $("#closingPollTitle").val().trim()
    let pollPrompt = $("#closingPollDescription").val().trim()
    let pollType = "CLOSE"
    let pollVoteOptions = ["Yes", "No"]

    let closingPollData = {
      groupName: groupName,
      pollCreator: email,
      pollTitle: pollTitle,
      pollPrompt: pollPrompt,
      pollType: pollType,
      pollStatus: "ACTIVE",
      pollVoteOptions: pollVoteOptions
    }

    // console.log("INPUT for createCloseGroupPoll POST", JSON.stringify(closingPollData));

    $.post("/createCloseGroupPoll", JSON.stringify(closingPollData))
    .then(function(response) {
      console.log("got response back from createCloseGroupPoll POST call", JSON.stringify(response));
      M.toast({html: response["Message"]})
    });


  });

  // Render List of Members on millde Polls Form 
  $.ajax({
    url: "/getAllUserEmails",
    method: "GET"
  }).then(function(response) {
      // console.log("ALLUSEREMAILS Data:\n",response["allUsersEmail"])
      for(let i = 0; i< response.allUsersEmail.length; i++){

        // console.log("To be add to DropDown:\t", response["allUsersEmail"][i])
        if (response["allUsersEmail"][i] != email){
          $('#targetedMemberEmail').append(`<option value="${response["allUsersEmail"][i]}"> 
                                              ${response["allUsersEmail"][i]} 
                                            </option>`); 
        }
      }
      $('select').formSelect();
  });

  $("#polls-button").click(function(){

    let pollTitle = $("#pollTitle").val().trim()
    let pollPrompt = $("#pollDescription").val().trim()
    let pollType = $('#pollSelect').val()
    let targetedMember = $("#targetedMemberEmail").val()
    let pollStatus = "ACTIVE"
    let pollVoteOptions = ["Yes", "No"]

    var pollData = {
      pollCreator: email,
      groupName: groupName,
      pollTitle: pollTitle,
      pollPrompt: pollPrompt,
      pollType: pollType,
      targetedMemberEmail: targetedMember,
      pollStatus: pollStatus,
      pollVoteOptions: pollVoteOptions,
    };

    console.log("INPUT for createPolls POST", JSON.stringify(pollData));

    if(pollType == "WARNING"){
      $.post("/createWarningPoll", JSON.stringify(pollData))
      .then(function(response) {
        console.log("got data back from createWarningPoll POST call", JSON.stringify(response));
        M.toast({html: response["Message"]})
      });
    }
    else if(pollType == "PRAISE"){
      $.post("/createPraisePoll", JSON.stringify(pollData))
      .then(function(response) {
        console.log("got data back from createPraisePoll POST call", JSON.stringify(response));
        M.toast({html: response["Message"]})
      });
    }
    else if(pollType == "KICK"){
      $.post("/createKickPoll", JSON.stringify(pollData))
      .then(function(response) {
        console.log("got data back from createKickPoll POST call", JSON.stringify(response));
        M.toast({html: response["Message"]})
      });
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


  

  





});