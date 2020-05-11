import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid

@app.route('/handleApplication', methods = ["POST"])
def handleApplication():

    #------Get Data from Front-end-----#
    jsonData = request.json

    response = jsonData["response"] #get the response from the user
    responderEmail = jsonData["responderEmail"] #get the email of the responder
    applicantEmail = jsonData["applicantEmail"].lower() #get the email of the applicant


    #-----Database Connection------#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?"(applicantEmail,))

    signupUserData = cursor.fetchone() #fetching the row from signup
    signupUserData = list(signupUserData) #convert that string into a python list

    #data for the user table
    fullname = signupUserData[0]
    email = signupUserData[1]
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
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
        connection.commit()
        connection.close()
        return (jsonify({"Success" : "Your invitation has been accepted"}))

    #decline the invite
    elif response.lower() == "declined":
        #find the user in signup table
        cursor.execute("SELECT * FROM  signup WHERE [email] = ?"(email,))
        #take out the row of that user
        row = list(cursor.fetchone())

        #modify the row
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
    jsonData = request.json

    userName = jsonData["userName"]
    userEmail = jsonData["userEmail"]
    points = jsonData["points"] #the points that were previously deducted

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())

    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    userData[4] += points #add the points that were previously deducted

    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The points deduction has been done."
    }))


@app.route('/shutDownGroup', methods = ["POST"])
def shutDownGroup():

    #------Get Data from Front-end-----#
    jsonData = request.json

    groupName = jsonData['groupName']

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Delete the row-----#
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?", (groupName,))

    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The group has been deleted."
    }))

@app.route('/issuePointDeduction', methods = ["POST"])
def issuePointDeduction():

    jsonData = request.json

    userName = jsonData["userName"]
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())

    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    userData[4] -= 5

    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The points deduction has been done."
    }))


@app.route('/issuePointIncrement', methods = ["POST"])
def issuePointIncrement():

    jsonData = request.json

    userName = jsonData["userName"]
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())

    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    userData[4] += 5

    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "The points increment has been done."
    }))

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
