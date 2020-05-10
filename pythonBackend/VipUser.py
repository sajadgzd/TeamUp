import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid

@app.route('/createDemocraticSuperUserPoll', methods = ["POST"])
def createDemocraticSuperUserPoll():
    jsonData = request.json
    groupName = jsonData["groupName"]
    pollCreator = jsonData["pollCreator"]
    targetedMemberEmail = jsonData["email"]
    targetedMemberName = jsonData["fullname"]
    memberstatus = jsonData["memberstatus"]
    pollTitle = jsonData["pollTitle"]
    pollData["uuid"] = str(uuid.uuid4())
    pollPrompt = jsonData["pollPrompt"]
    pollType = "DEMOCRATIC"
    pollStatus = "ACTIVE"
    pollOptions = jsonData["pollVoteOptions"]
    pollVoteOptions = {}
    for option in pollOptions:
        pollVoteOptions[option] = 0
    voters = []

    pollData = {}
    pollData["pollCreator"] = pollCreator
    pollData["targetedMemberEmail"] = targetedMemberEmail
    pollData["targetedMemberName"] = targetedMemberName
    pollData["pollTitle"] = pollTitle
    pollData["uuid"] = str(uuid.uuid4())
    pollData["pollPromopt"] = pollPrompt
    pollData["pollType"] = pollType
    pollData["pollStatus"] = pollStatus
    pollData["pollVoteOptions"] = pollVoteOptions
    pollData["voters"] = voters
    pollData["result"] = None

     
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?"(groupName,))
    groupData = list(cursor.fetchone())

    groupPolls = json.loads(groupName[3])
    groupPolls.append(pollData)
    groupPolls = json.dumps(groupPolls)
    groupData[3] = groupPolls

    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()

    return (jsonify{
        "Message": "Your Praise poll has been created."
    })


@app.route('/issueDemocraticSuperUserVote', methods = ["POST"])
def issueDemocraticSuperUserVote():
    jsonData = request.json

    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["email"] # whoever is responding to the poll
    pollUUID = jsonData["pollUUID"] #uuid for that pole
    groupName = jsonData["groupName"] #groupname for the poll

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?"(groupName,))

    groupData = list(cursor.fetchone())
    memberPolls = json.loads(groupData[3])
    for index,poll in enumerate(memberPolls):
        if poll["uuid"] == pollUUID:
            poll["voters"].append(pollResponder)
            pollVoteOptions = poll["pollVoteOptions"]
            pollVoteOptions[pollResponse] += 1 
            poll["pollVoteOptions"] = pollVoteOptions
            memberPolls[index] = poll
            break
    

    memberPolls = json.dumps(memberPolls)
    groupData[3] = memberPolls
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
    connection.commit()

    memberPolls = json.loads(memberPolls)
    sumVotes = 0
    for index,poll in enumerate(memberPolls):
        if poll["uuid"] == pollUUID:
            pollVoteOptions = poll["pollVoteOptions"]
            for option,voteCount in pollVoteOptions.items():
                sumVotes += voteCount
            break

    totalVipMembers = 0
    for member in groupData[5]:
        if member["memberstatus"] == "vip":
            totalVipMembers += 1

    maxResponseCount = 0
    answer = None
    if sumVotes == totalVipMembers-1:
        for index,poll in enumerate(memberPolls):
            if poll["uuid"] == pollUUID:
                pollVoteOptions = poll["pollVoteOptions"]
                for option,voteCount in pollVoteOptions.items():
                    if voteCount > maxResponseCount:
                        maxResponseCount = voteCount
                        answer = option
                poll["result"] = answer
                poll["pollStatus"] = "CLOSED"
                memberPolls[index] = poll
                break
        
        if maxResponseCount == totalVipMembers-1:
            memberPolls = json.dumps(memberPolls)
            groupData[3] = memberPolls
            cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
            cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
        connection.commit()
    connection.close()
    
    ####HELPER

    return (jsonify({
        "Message": "Your vote has been submitted."
    }))
