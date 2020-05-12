import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid


########## VIP USER CODE ##########
@app.route('/createDemocraticSuperUserPoll', methods = ["POST"])
def createDemocraticSuperUserPoll():

    jsonData = request.json
    #GET DATA FROM FRONT END#
    pollData = {}
    pollData["pollCreator"] = jsonData["creatorFullName"]
    pollData["targetedMemberEmail"] = jsonData["targetedMemberEmail"]
    pollData["targetedMemberName"] = jsonData["targetedMemberName"]
    pollData["pollTitle"] = jsonData["pollTitle"]
    pollData["pollPrompt"] = jsonData["pollPrompt"]
    pollData["pollType"] = "ELECT DEMOCRATIC SU"
    pollData["pollStatus"] = "ACTIVE"

    pollVoteOptions = {}
    for option in jsonData["pollVoteOptions"]:
        pollVoteOptions[option] = 0
    pollData["pollVoteOptions"] = pollVoteOptions
    pollData["voters"] = []
    pollData["result"] = None
    #

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM democraticSU")
    rowData = list(cursor.fetchone())


    userFlag = rowData[1]
    pollFlag = rowData[2]
    if userFlag == 1:
        return (jsonify({"Message": "Sorry a Democratic Super User already exists. You cannot create a poll."}))
    if pollFlag == 1:
        return (jsonify({"Message": "Sorry a poll  already exists. Please particpate in the current poll."}))

    pollData = json.dumps(pollData)
    rowData[0] = pollData
    rowData[2] = 1
    cursor.execute("DELETE FROM democraticSU")
    cursor.execute("INSERT INTO democraticSU (poll,userexists,pollexists) VALUES(?,?,?)",tuple(rowData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The democratic super user poll has been created."
    })


@app.route('/issueDemocraticSuperUserVote', methods = ["POST"])
def issueDemocraticSuperUserVote():

    #GET JSON DATA
    jsonData = request.json
    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["email"] # whoever is responding to the poll

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #REGISTER VOTE
    cursor.execute("SELECT * FROM democraticSU")
    rowData = list(cursor.fetchone())
    memberPolls = json.loads(rowData[0])
    memberPolls["pollVoteOptions"][pollResponse] += 1
    memberPolls["voters"].append(pollResponder)
    memberPolls = json.dumps(memberPolls)
    row[0] = memberPolls
    cursor.execute("DELETE FROM democraticSU")
    cursor.execute("INSERT INTO democraticSU (poll,userexists,pollexists) VALUES(?,?,?)",tuple(rowData))
    connection.commit()
    

    sumVotes = 0 #Count of the total sum of votes
    totalMembers = 0
    cursor.execute("SELECT * FROM users")
    for userRow in cursor.fetchall():
        if userRow["status"] == "VIP":
            totalMembers += 1
    maxResponseCount = 0 # Checks to see if it's actually unanimous
    answer = None #Answer field
    for option,voteCount in memberPolls["pollVoteOptions"].items():
        sumVotes += voteCount
        if voteCount > maxResponseCount:
            maxResponseCount = voteCount
            answer = option


    if sumVotes == (totalMembers -1) == maxResponseCount: #We have all votes, and they were unanimous
        if answer.lower() == "yes":
            #change targeted member to democratic SU
            cursor.execute("SELECT * FROM users WHERE [email] = ?",(memberPolls["targetedMemberName"],))
            userData = list(cursor.fetchone())
            userData[5] = "DEMOCRATIC SUPER USER"
            cursor.execute("DELETE FROM users WHERE [email] = ?", (invitee,))
            cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
            connection.commit()

            #Note down that a democratic SU exists
            rowData[1] = 1
            rowData[2] = 0
            cursor.execute("DELETE FROM democraticSU")
            cursor.execute("INSERT INTO democraticSU (poll,userexists,pollexists) VALUES(?,?,?)",tuple(rowData))
            connection.commit()
        else:
            #Poll failed, clear everything and allow for a new one to start
            rowData[0] = "Empty"
            rowData[1] = 0
            rowData[2] = 0
            cursor.execute("DELETE FROM democraticSU")
            cursor.execute("INSERT INTO democraticSU (poll,userexists,pollexists) VALUES(?,?,?)",tuple(rowData))
            connection.commit()
    elif sumVotes == (totalMembers -1): #We have all teh votes, and they weren't unanimous
            #Poll failed, clear everything and allow for a new one to start
            rowData[0] = "Empty"
            rowData[1] = 0
            rowData[2] = 0
            cursor.execute("DELETE FROM democraticSU")
            cursor.execute("INSERT INTO democraticSU (poll,userexists,pollexists) VALUES(?,?,?)",tuple(rowData))
            connection.commit()
    connection.close()
    return (jsonify({"Message": "Your vote has been submitted."}))

########## VIP USER CODE ##########
