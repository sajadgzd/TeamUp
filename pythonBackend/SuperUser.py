import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid


########## SUPER USER CODE ##########

@app.route('/handleApplication', methods = ["POST"])
def handleApplication():

    #------Get Data from Front-end-----#
    jsonData = request.json

    response = jsonData["response"] #ACCEPT or DECLINE
    # responderEmail = jsonData["responderEmail"] #get the email of the responder
    applicantEmail = jsonData["applicantEmail"].lower() #get the email of the applicant


    #-----Database Connection------#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(applicantEmail,))

    signUpUserData = cursor.fetchone() #fetching the row from signup
    signUpUserData = list(signUpUserData) #convert that string into a python list

    #data for the user table
    fullname = signUpUserData[0]
    email = signUpUserData[1]
    password = signUpUserData[3]
    groupList = []
    groupList = json.dumps(groupList)
    reputationScore = 0
    status = None
    invitations = []
    invitations = json.dumps(invitations)
    blacklist = []
    blacklist = json.dumps(blacklist)
    whitelist = []
    whitelist = json.dumps(whitelist)
    compliments = []
    compliments = json.dumps(compliments)
    inbox = []
    inbox = json.dumps(inbox)
    referredUsers = []
    referredUsers = json.dumps(referredUsers)

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
    rowData.append(compliments)
    rowData.append(inbox)
    rowData.append(referredUsers)


    # accept the invite
    if response.lower() == "accepted":
        #first update the signup row for this user and change user status
        rowData[5] = "OU"
        
        signUpUserData[6] = "USER"
        

        cursor.execute("DELETE * FROM signup WHERE [email] = ?", (email,))
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(signUpUserData))
        connection.commit()

        # add the user to the user database
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
        connection.commit()
        connection.close()
        return (jsonify({"Message" : "{} is now registered to Team Up.".format(email)}))

    #decline the invite
    elif response.lower() == "declined":

        signUpUserData[6] = "REJECTED"
        #modify the row
        cursor.execute("DELETE * FROM signup WHERE [email] = ?", (email,))
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(signUpUserData))
        connection.commit()
        connection.close()
        return jsonify({
            "Message": "{} will be notified that their application has been rejected.".format(email)
        })

@app.route('/blacklistFromServer', methods = ["POST"])
def blacklistFromServer():
    jsonData = request.json

    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the visitor information-----#
    cursor.execute("SELECT * FROM signup where [email] = ?",(userEmail,))
    visitorData = list(cursor.fetchone())

    #modify the visitor signup row
    visitorData[6] = "BLACKLISTED"
    cursor.execute("DELETE * FROM signup WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(visitorData))
    connection.commit()
    connection.close()

    return jsonify({
            "Message": "The visitor has been added to blacklist."
        })



@app.route('/reverseReputationDeduction', methods = ["POST"])
def reverseReputationDeduction():
    jsonData = request.json
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())

    userData[4] += 5 #
    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "{}'s point deducation has been reversed.".format(userEmail)
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
    cursor.execute("SELECT * FROM users WHERE [groupName] = ?",(groupName,))
    groupData = cursor.fetchone()
    groupData = list(groupData)
    groupData[1] = "CLOSED"
    cursor.execute("DELETE * FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "{} has been closed.".format(groupName)
    }))

@app.route('/issuePointDeduction', methods = ["POST"])
def issuePointDeduction():

    jsonData = request.json
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())
    userData[4] -= 5
    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    managePointStatus(userEmail)
    return (jsonify({
        "Message": "{} has 5 points deducted from their score.".format(userEmail)
    }))


@app.route('/issuePointIncrement', methods = ["POST"])
def issuePointIncrement():
    
    jsonData = request.json
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the user information-----#
    cursor.execute("SELECT * FROM users where [email] = ?",(userEmail,))
    userData = list(cursor.fetchone())
    userData[4] += 5
    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

    managePointStatus(userEmail)
    return (jsonify({
        "Message": "{} has 5 points added from their score.".format(userEmail)
    }))

@app.route('/banUser', methods = ["POST"])
def banUser():

    jsonData = request.json
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the signup information-----#
    cursor.execute("SELECT * FROM signup where [email] = ?",(userEmail,))
    visitorData = list(cursor.fetchone())

    #modify the signup row
    visitorData[6] = "BLACKLISTED"
    cursor.execute("DELETE * FROM signup WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(visitorData))



    #Get the users information
    cursor.execute("SELECT * FROM users WHERE [email] = ?", (userEmail,))
    userData = list(cursor.fetchone())

    #modify the user row
    userData[5] = "BLACKLISTED"
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))

    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "{} has been blacklisted from Signup and Users table.".format(userEmail)
    }))

########## END SUPER USER CODE ##########