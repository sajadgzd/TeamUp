import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid

@app.route('/handleApplication', methods = ["POST"])
def handleApplication():

    jsonData = request.json

    response = jsonData["response"]
    responder = jsonData["responder"]
    applicantEmail = jsonData["applicantEmail"].lower()

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?"(applicantEmail,))

    signupUserData = cursor.fetchone() #fetching the row from signup
    signupUserData = list(signupUserData) #convert that string into a python list

    #data for the user table
    email = signupUserData[1]
    fullname = signupUserData[0]
    password = ""
    groupList = []
    reputationScore = ""
    status = signupUserData[6]
    invitations = []
    blacklist = []
    whitelist = []
    complimentsorcomplaints = []
    inbox = []

    rowData = []
    rowData.append(email)
    rowData.append(fullname)
    rowData.append(password)
    rowData.append(groupList)
    rowData.append(reputationScore)
    rowData.append(status)
    rowData.append(invitations)
    rowData.append(blacklist)
    rowData.append(whitelist)
    rowData.append(complimentsorcomplaints)
    rowData.append(inbox)

    # rowData = json.dumps(rowData)

    # accept the invite
    if response.lower() == "accepted":
        #first update the signup row for this user and change user status
        cursor.execute("SELECT * FROM  signup WHERE [email] = ?"(email,))
        
        row = list(cursor.fetchone())

        cursor.execute("DELETE * FROM signup WHERE [email] = ?", (email,))
        userData[6] = "ORDINARY"
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(row))

        # add the user to the user database
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES(?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
        connection.commit()
        connection.close()
        return (jsonify({"Success" : "Your invitation has been accepted"}))

    #decline the invite
    elif response.lower() == "declined":
        cursor.execute("SELECT * FROM  signup WHERE [email] = ?"(email,))
        
        row = list(cursor.fetchone())
        
        cursor.execute("DELETE * FROM signup WHERE [email] = ?", (email,))
        userData[6] = "DECLINED"
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(row))
        connection.commit()
        connection.close()

        return jsonify({
            "Message": "Sorry, your request to signup has been declined."
        })

@app.route('/blacklistFromServer', methods = ["POST"])
def blacklistFromServer():
    jsonData = request.json

    blacklistUser = jsonData["blacklist"]


    # input UserID
    # if (UserID exists in the User Database):
    #   if (User already not exists in BlackList database):
    #       BlackList_Database.append(UserID)

@app.route('/reverseReputationDeduction', methods = ["POST"])
def reverseReputationDeduction():
    # input UserID
    # if (UserID exists in the UserDatabase):
    #   currentUser.reputationpoint += 5
    #   print("Reputation Deduction is reversed")


@app.route('/shutDownGroup', methods = ["POST"])
def shutDownGroup():
    jsonData = request.json

    groupName = jsonData['groupName']

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?", (groupName,))

    groupData = cursor.fetchone()

    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The group has been deleted."
    }))

@app.route('/issuePointDeduction', methods = ["POST"])
def issuePointDeduction():
    # if (userID exists in the user database):
    #   currentUser.reputationpoint -= 5
    #   print("Reputation Deduction done")

@app.route('/issuePointIncrement', methods = ["POST"])
def issuePointIncrement():
    # if (userID exists in the user database):
    #   currentUser.reputationpoint += 5
    #   print("Reputation Increment done")

@app.route('/banUser', methods = ["POST"])
def banUser():
    # change user status to banned in the signup
    # delete user from the user database





    # if (userID exists in the user database):
    #   if (userID exists in blacklist database):
    #       print("User already banned")
    #   
    #   else:
    #        add user to the blacklist database
    #
    # else:
    #   print("The user you are trying to ban doesn't exist")
    #   
