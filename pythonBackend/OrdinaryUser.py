import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory

def sendModRequest(target, message, request_type):
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO moderationRequests (subject,message,type,status,number) VALUES(?,?,?,?,?)",(target,message,request_type,"OPEN",None))
    connection.commit()
    connection.close()

# SENDING REPORTS/APPEALS

@app.route('/appealReputation', methods = ["POST"])
def appealReputation():
    jsonData = request.json
    userEmail = jsonData["email"].lower() # email of the user appealing
    appealMessage = jsonData["appealMessage"]
    sendModRequest(userEmail, appealMessage, "REP_APPEAL")
    return jsonify({"Success: appeal has been submitted."})

@app.route('/reportUser', methods = ["POST"])
def reportUser():
    jsonData = request.json
    targetEmail = jsonData["email"].lower()
    reportMessage = jsonData["reportMessage"]
    sendModRequest(targetEmail, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})

@app.route('/reportGroup', methods = ["POST"])
def reportGroup():
    jsonData = request.json
    groupName = jsonData["groupName"]
    reportMessage = jsonData["reportMessage"]
    sendModRequest(groupName, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})

# END REPORTS/APPEALS

# ALTER REPUTATION
@app.route('/referenceReputation', methods = ["POST"])
def referenceReputation():
    jsonData = request.json
    referredUserEmail = jsonData["referredUser"]
    referringUserEmail = jsonData["referringUser"]
    points = jsonData["points"] # num of points user wants to add to referred user
    
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  users WHERE [email] = ?", (referredUserEmail,))
    referredUserData = list(cursor.fetchone())

    cursor.execute("SELECT * FROM  users WHERE [email] = ?", (referringUserEmail,))
    referringUserData = list(cursor.fetchone())

    if points > 10 and referringUserData[5] != "VIP":
        return jsonify({"Error": "Only VIPs can give more than 10 points to their referred user."})

    elif points > 20:
        return jsonify({"Error": "VIPs can only award 0-20 points."})

    else:
        referredUserData[4] += points
        cursor.execute("DELETE * FROM users WHERE [email] = ?", (referredUserEmail,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES (?,?,?,?,?,?,?,?,?,?,?)",tuple(referredUserData))
        connection.commit()
        connection.close()
        return jsonify({"Success" : "points awarded to referred user"})






