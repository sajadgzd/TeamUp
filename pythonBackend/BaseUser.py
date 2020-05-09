import sqlite3
import json
import requests
from flask import Flask, jsonify, render_template, request, send_from_directory


@app.route('/login', methods = ["POST"])
def login():
    jsonData = request.json

    email = jsonData["email"]
    credentials = jsonData["credentials"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ? AND [credentials] = ?"(jsonData["email"].lower(),credentials))
    found = cursor.fetchone()
    
    if found is not None:
        return jsonify({
            "data": found
        })
    else:
        return jsonify({
            "Error": "Sorry, email or password combination does not exist."
        })

def inviteToGroup(senderUserID, groupName, recipientUserID):
    # if (senderUserID && recipientUserID is in User Database) &&
    #       (groupName in Group Database)
    # 
    #   recipientUserID.inboxDatabase.append(invite)
    #   recipientUserID.inboxDatabase.append(senderUserID)
    #   recipientUserID.inboxDatabase.append(groupName)
    #   (backend process)
    #   print(status)


def handleGroupMeeting(senderUserID, decision, reason, recepientUserID):
    # if (senderUserID && recipientUserID is in User Database) &&
    #       (groupName in Group Database)
    # 
    #   recipientUserID.inboxDatabase.append(decision)
    #   recipientUserID.inboxDatabase.append(reason)
    #   recipientUserID.inboxDatabase.append(senderUserID)
    #   recipientUserID.inboxDatabase.append(groupName)
    #   groupDatabase.append(recipientUserID)
    # 
    #   print(status)

def createMeetupPoll(creatorUserID, pollName, pollType, optionsList):
    # if (UserID is in User Database)
    # 
    #   if (pollName already exists in the Poll Database):
    #       print("Poll already exists")
    #
    #   else:
    #       PollDatabase.append(creatorUserID)
    #       PollDatabase.append(pollName)
    #       PollDatabase.append(optionsList)
    #       PollDatabase.append(pollType
    #       print("Poll added to the database")

def createWarningPoll(pollName, pollType, optionsList, targetUserID):
    # if (UserID is in User Database)
    # 
    #   if (pollName already exists in the Poll Database):
    #       print("Poll already exists")
    #
    #   else:
    #       PollDatabase.append(targetUserID)
    #       PollDatabase.append(pollName)
    #       PollDatabase.append(optionsList)
    #       PollDatabase.append(pollType)
    #       print("Poll added to the database")

def createPraisePoll(pollName, pollType, optionsList, targetUserID):
    # if (UserID is in User Database)
    # 
    #   if (pollName already exists in the Poll Database):
    #       print("Poll already exists")
    #
    #   else:
    #       PollDatabase.append(targetUserID)
    #       PollDatabase.append(pollName)
    #       PollDatabase.append(optionsList)
    #       PollDatabase.append(pollType)
    #       print("Poll added to the database")

def createKickPoll(pollName, pollType, optionsList, targetUserID):
    # if (UserID is in User Database)
    # 
    #   if (pollName already exists in the Poll Database):
    #       print("Poll already exists")
    #
    #   else:
    #       PollDatabase.append(targetUserID)
    #       PollDatabase.append(pollName)
    #       PollDatabase.append(optionsList)
    #       PollDatabase.append(pollType)
    #       print("Poll added to the database")

def createCloseGroupPoll(pollName, pollType, optionsList, targetGroupID):
    # if (GroupID is in Group Database)
    # 
    #   if (pollName already exists in the Poll Database):
    #       print("Poll already exists")
    #
    #   else:
    #       PollDatabase.append(targetGroupID)
    #       PollDatabase.append(pollName)
    #       PollDatabase.append(optionsList)
    #       PollDatabase.append(pollType)
    #       print("Poll added to the database")

def issueMeetupVote(pollName, UserID, decision):
    # if (UserID is in vip User Database) 
    #
    #    if (vipUserID has not voted yet):
    #       pollDatabase.append(pollName)
    #       pollDatabase.append(decision)
    #       print("Your decision has been submitted")

def issueWarningVote(pollName, UserID, decision):
    # if (userID is in User Database && pollName in Poll Database) 
    #
    #    if (userID has not voted yet):
    #       pollDatabase.append(pollName)
    #       pollDatabase.append(decision)
    #       print("Your decision has been submitted")
    #
    #   else:
    #       print("You have already submitted your response for this poll")

def issuePraiseVote(pollName, UserID, decision):
    # if (userID is in User Database && pollName in Poll Database) 
    #
    #    if (userID has not voted yet):
    #       pollDatabase.append(pollName)
    #       pollDatabase.append(decision)
    #       print("Your decision has been submitted")
    #   else:
    #       print("You have already submitted your response for this poll")

def issueKickVote(pollName, UserID, decision):
    # if (userID is in User Database && pollName in Poll Database) 
    #
    #    if (userID has not voted yet):
    #       pollDatabase.append(pollName)
    #       pollDatabase.append(decision)
    #       print("Your decision has been submitted")
    #   else:
    #       print("You have already submitted your response for this poll")


def issueCompliment(UserId, complimentComment):
    #if (userID exists in the user database):
    #   print(UserID.complimentDatabase.append(UserId, complimentComment))
    #   return success status
    #
    #else:
    #   print("The user you are trying to issue a compliment to, doesnt't exist")
    pass

def addToWhiteBox(UserID):
    #if (userID exists in the user database):
    #   if (userID exists in self.whitebox database):
    #       print("User already added to whitebox")
    #   
    #   else:
    #        add user to the self.whitebox database
    #        print("User added to your blackbox")
    #
    # else:
    #   print("The user you are trying to whitelist doesn't exist")

def addToBlackBox(userID):
    #if (userID exists in the user database):
    #   if (userID exists in self.blackbox database):
    #       print("User already to blackbox")
    #   
    #   else:
    #        add user to the self.blackbox database
    #        print("User banned")
    #
    # else:
    #   print("The user you are trying to ban doesn't exist")