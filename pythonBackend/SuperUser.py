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

    userData = cursor.fetchone() #fetching the row from signup
    userData = json.loads(userData) #convert that string into a python list
    fullname = userData[0]
    email = userData[0]


    # accept the invite

    if response.lower() == "accepted":
        cursor.execute("INSERT INTO users (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(rowData))


    #decline the invite


    # input UserID
    # if (UserID exists in the pending application database):
    #   if (decision == accept):
    #       remove the user from PendingUser Database
    #       add the user to the User Database
    #       print("User Registered Successfully")
    #   
    #   elif (decision == deny):
    #       if(number_of_times_denied > 1):
    #           add to blacklist
    #        
    #       number_of_times_denied += 1
    #       print("User Registration denied")

@app.route('/blacklistFromServer', methods = ["POST"])
def blacklistFromServer():
    jsonData = request.json


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
    # input groupName
    # if(groupName exist in the Groups Database):
    #   GroupsDatabase.remove(groupName)
    #   print("Group was shutdown successfully")
    #
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
