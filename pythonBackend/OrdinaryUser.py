import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory



########## ORDINARY USER CODE ##########

# CREATING MOD REQUEST #~HELPER
def sendModRequest(target, message, request_type):
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO moderationRequests (subject,message,type,status,number) VALUES(?,?,?,?,?)",(target,message,request_type,"OPEN",None))
    connection.commit()
    connection.close()

### SENDING REPORTS/APPEALS ###

@app.route('/appealReputation', methods = ["POST"])
def appealReputation():
    #GET FRONT END DATA
    jsonData = request.json
    userEmail = jsonData["email"] # email of the user appealing
    appealMessage = jsonData["appealMessage"]

    sendModRequest(userEmail, appealMessage, "REP_APPEAL")
    return jsonify({"Success: appeal has been submitted."})

@app.route('/reportUser', methods = ["POST"])
def reportUser():
    #GET FRONT END DATA
    jsonData = request.json
    targetEmail = jsonData["email"] #email of the user being reported
    reportMessage = jsonData["reportMessage"]
    sendModRequest(targetEmail, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})

@app.route('/reportGroup', methods = ["POST"])
def reportGroup():
    #GET FRONT END DATA
    jsonData = request.json
    groupName = jsonData["groupName"] #name of the group being reported
    reportMessage = jsonData["reportMessage"]
    sendModRequest(groupName, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})


### END SENDING REPORTS/APPEALS ###

### ALTER REPUTATION ###
@app.route('/referenceReputation', methods = ["POST"])
def referenceReputation():
    #GET FRONT END DATA
    jsonData = request.json
    referredUserEmail = jsonData["referredUser"] #The new guy
    referringUserEmail = jsonData["referringUser"] #The OG
    points = jsonData["points"] # num of points user wants to add to referred user
    
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  users WHERE [email] = ?", (referredUserEmail,))
    referredUserData = list(cursor.fetchone())

    cursor.execute("SELECT * FROM  users WHERE [email] = ?", (referringUserEmail,))
    referringUserData = list(cursor.fetchone())

    if referringUserData[5] == "VIP":
        referredUserData[4] += points
    else:
        referredUserData[4] += points
    
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (referredUserEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES (?,?,?,?,?,?,?,?,?,?,?)",tuple(referredUserData))
    connection.commit()


    referredUsersList = json.loads(referringUserData[11])
    referredUsersList.remove(referredUserEmail)
    referredUsersList = json.dumps(referredUsersList)
    referringUserData[11] = referredUsersList
    
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (referringUserEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES (?,?,?,?,?,?,?,?,?,?,?)",tuple(referringUserData))
    connection.commit()
    connection.close()
    managePointStatus(referredUserEmail)
    return (jsonify({
        "Message": "Points have been submitted to the new user."
    }))


@app.route('/createGroup', methods=["POST"])
def createGroup():
    jsonData = request.json

    groupName = jsonData["groupName"]
    creator = jsonData["email"] # email of creator
    status = "ACTIVE"
    posts = json.dumps([])
    memberPolls = json.dumps([])
    groupPolls = json.dumps([])
    members = json.dumps([{
        "member": creator,
        "warnings": 0,
        "praises": 0,
        "kicks": 0,
        "taskscompleted":0}])
    groupData = []
    groupData.extend([groupName, status, posts, memberPolls, groupPolls, members])

    # add new group to DB
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()
    return jsonify({"Message" : "Group successfully created."})


########## END ORDINARY USER CODE ##########




