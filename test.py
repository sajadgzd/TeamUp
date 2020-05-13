import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory
import uuid

app = Flask(__name__, static_folder='view/assets', template_folder="view")

########## BASE USER CODE ##########
# ADJUST USER STATUS #~HELPER
def managePointStatus(email):
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(email,))
    userData = cursor.fetchone()
    userData = list(userData)

    status = userData[5]
    points = userData[4]

    if status == "VIP" or status == "DEMOCRATIC SUPER USER":
        if points < 25:
            userData[5] = "OU"
    elif status == "OU":
        if points > 30:
            userData[5] = "VIP"
    cursor.execute("DELETE FROM users WHERE [email] = ?", (email,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()


@app.route('/getAllSignUpData', methods = ["GET"])
def getAllSignUpData():

    signUpData = []
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup")
    
    for userData in cursor.fetchall():
        signUpData.append(list(userData))
    connection.close()
    return (jsonify({
        "signUpData": signUpData
    }))


@app.route('/getSignUpData', methods = ["POST"])
def getSignUpData():
    jsonData =json.loads(request.get_data())
    email = jsonData["email"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(email,))
    
    userData = cursor.fetchone()
    userData = list(userData)
    connection.close()
    return (jsonify({
        "signUpData": userData
    }))


@app.route('/getUserData', methods = ["POST"])
def getUserData():
    jsonData =json.loads(request.get_data())
    email = jsonData["email"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(email,))
    
    userData = cursor.fetchone()
    userData = list(userData)
    userData[3] = json.loads(userData[3]) #grouplist
    userData[6] = json.loads(userData[6]) #invitations
    userData[7] = json.loads(userData[7]) #blacklist
    userData[8] = json.loads(userData[8]) #whitelist
    userData[9] = json.loads(userData[9]) #compliments
    userData[10] = json.loads(userData[10]) #inbox
    userData[11] = json.loads(userData[11]) #referredUsers
    connection.close()
    return (jsonify({
        "userData": userData
    }))

@app.route('/getAllUserEmails',methods = ["GET"])
def getAllUserEmails():
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")

    emails = []
    for user in cursor.fetchall():
        emails.append(user[0])
    connection.close()
    return (jsonify({
        "allUsersEmail": emails
    }))

@app.route('/getAllVIPEmails',methods = ["GET"])
def getAllVIPEmails():
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    
    emails = []
    for user in cursor.fetchall():
        if user[5] == "VIP":
            emails.append(user[0])
    connection.close()
    return (jsonify({
        "allVIPEmail": emails
    }))    

@app.route('/getGroupData', methods = ["POST"])
def getGroupData():
    jsonData =json.loads(request.get_data())
    groupName = jsonData["groupName"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM groups WHERE [groupName] = ?",(groupName,))
    
    groupData = cursor.fetchone()
    groupData = list(groupData)

    groupData[2] = json.loads(groupData[2]) #posts
    groupData[3] = json.loads(groupData[3]) #member polls
    groupData[4] = json.loads(groupData[4]) #group polls
    groupData[5] = json.loads(groupData[5]) #member list
    connection.close()
    return (jsonify({
        "groupData": groupData
    }))

@app.route('/loginUser', methods = ["POST"])
def loginUser():
    jsonData =json.loads(request.get_data())

    email = jsonData["email"]
    credentials = jsonData["credentials"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ? AND [password] = ?",(email,credentials))
    userData = cursor.fetchone()

    if userData is not None:
        connection = sqlite3.connect(r"./database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE [email] = ?",(email,))
        userData = cursor.fetchone()
        userData = list(userData)
        userData[3] = json.loads(userData[3]) #grouplist
        userData[6] = json.loads(userData[6]) #invitations
        userData[7] = json.loads(userData[7]) #blacklist
        userData[8] = json.loads(userData[8]) #whitelist
        userData[10] = json.loads(userData[10]) #inbox
        userData[11] = json.loads(userData[11]) #referredUsers
        connection.close()
        return jsonify({
            "Success": "Welcome to Team Up!",
            "userData": userData
        })
    else:
        connection.close()
        return jsonify({
            "Error": "Sorry, email or password combination does not exist."
        })

@app.route('/inviteToGroup', methods = ["POST"])
def inviteToGroup():

    #GET JSON DATA
    jsonData =json.loads(request.get_data())

    inviter = jsonData["inviterEmail"].lower()
    groupName = jsonData["groupName"]
    invitee = jsonData["inviteeEmail"].lower()

    #CONNECT TO DATABASE
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(inviter,))
    inviterData = cursor.fetchone()
    inviterFullname = inviterData[1]
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(invitee,))
    inviteeData = cursor.fetchone()
    inviteeData = list(inviteeData)

    blackList = json.loads(inviteeData[7])
    for blocked in blackList:
        if blocked == inviter:
            connection.close()
            return jsonify({
            "Message": "Sorry, your invitation has been automatically rejected."
        })

    whiteList = json.loads(inviteeData[8])
    for autoAccept in whiteList:
        if autoAccept == inviter:
            #Add group to invitee list
            groupList = json.loads(inviteeData[3])
            if groupName in groupList:
                connection.close()
                return jsonify({"Message": "The user is already in this group."})
            groupList.append(groupName)
            groupList = json.dumps(groupList)
            inviteeData[3] = groupList
            cursor.execute("DELETE FROM users WHERE [email] = ?", (invitee,))
            cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
            connection.commit()

            #Add invitee to group member list
            cursor.execute("SELECT * FROM groups WHERE [groupName] = ?",(groupName,))
            groupData = list(cursor.fetchone())
            memberData = json.loads(groupData[5])
            memberData.append({
                "member": invitee,
                "warnings": 0,
                "praises": 0,
                "kicks": 0,
                "taskscompleted":0
            })
            memberData = json.dumps(memberData)
            groupData[5] = memberData

            cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
            cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
            connection.commit()
            connection.close()
            return jsonify({
                "Message": "Your invitation has been automatically accepted."
            })

    invitations = json.loads(inviteeData[6])
    for invitation in invitations:
        if invitation["groupName"] == groupName:
            connection.close()
            return jsonify({"Message": "This user has already received an invite to this group."})
    invitations.append({
        "inviterFullName": inviterFullname,
        "inviterEmail" :inviter,
        "groupName": groupName
    })

    invitations = json.dumps(invitations)
    inviteeData[6] = invitations
    cursor.execute("DELETE FROM users WHERE [email] = ?", (invitee,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
    connection.commit()
    connection.close()
    return jsonify({
        "Message": "Your invitation has been sent."
    })


@app.route('/handleGroupInvite', methods = ["POST"])
def handleGroupInvite():

    #GET JSON DATA
    jsonData =json.loads(request.get_data())

    inviter = jsonData["inviterEmail"]
    groupName = jsonData["groupName"]
    invitee = jsonData["inviteeEmail"]
    message = jsonData["message"]
    response = jsonData["response"]


    #SQLITE CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE [email] = ?",(invitee,))

    #If they accept the invitation
    if response.lower() == "accept":
        #Add the invitee to the group list
        cursor.execute("SELECT * FROM groups WHERE [groupName] = ?",(groupName,))
        groupData= list(cursor.fetchone())
        memberData = json.loads(groupData[5])
        for data in memberData:
            if data["member"] == invitee:
                connection.close()
                return jsonify({"Message": "You're already in the group!"})
        memberData.append({
                "member": invitee,
                "warnings": 0,
                "praises": 0,
                "kicks": 0,
                "taskscompleted":0
            })
        memberData = json.dumps(memberData)
        groupData[5] = memberData
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()

        #Add the group to the invitee's group list
        cursor.execute("SELECT * FROM users where [email] = ?",(invitee,))
        inviteeData = list(cursor.fetchone())
        groupList = json.loads(inviteeData[3])
        groupList.append(groupName)
        groupList = json.dumps(groupList)
        inviteeData[3] =groupList

        invitationList = json.loads(inviteeData[6])
        deleteIndex = None
        for index,invitation in enumerate(invitationList):
            if invitation["groupName"] == groupName:
                deleteIndex = index
                break
        if deleteIndex is not None:
            del invitationList[deleteIndex]
        invitationList = json.dumps(invitationList)
        inviteeData[6] = invitationList

        cursor.execute("DELETE FROM users WHERE [email] = ?",(invitee,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
        connection.commit()

        #Notify the inviter that they have accepted the invitation
        cursor.execute("SELECT * FROM users where [email] = ?",(inviter,))
        inviterData = list(cursor.fetchone())
        inboxList = json.loads(inviteeData[10])
        inboxList.append({
            "sender": inviter,
            "Message": "Your invitation has been accepted by {}.".format(invitee)
        })
        inboxList = json.dumps(inboxList)
        inviterData[10] =inboxList
        cursor.execute("DELETE FROM users WHERE [email] = ?",(inviter,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviterData))
        connection.commit()
        connection.close()
        return (jsonify({
            "Message": "You've been added to the group {} and your response has been sent to your inviter.".format(groupName)
        }))
    elif response.lower() == "decline":
        #Notify the inviter that their invitation has been declined
        cursor.execute("SELECT * FROM users where [email] = ?",(inviter,))
        inviterData = list(cursor.fetchone())
        inboxList = json.loads(inviterData[10])
        inboxList.append({
            "sender": invitee,
            "Message": message
        })
        inboxList = json.dumps(inboxList)
        inviterData[10] =inboxList
        cursor.execute("DELETE FROM users WHERE [email] = ?",(inviter,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviterData))
        connection.commit()

        #Delete the invitation from the invitee's list
        cursor.execute("SELECT * FROM users where [email] = ?",(invitee,))
        inviteeData = list(cursor.fetchone())
        invitationList = json.loads(inviteeData[6])
        deleteIndex = None
        for index,invitation in enumerate(invitationList):
            if invitation["groupName"] == groupName:
                deleteIndex = index
                break
        if deleteIndex is not None:
            del invitationList[deleteIndex]
        invitationList = json.dumps(invitationList)
        inviteeData[6] = invitationList

        cursor.execute("DELETE FROM users WHERE [email] = ?",(invitee,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
        connection.commit()
        connection.close()
        return (jsonify({
            "Message": "You have declined your invitation to the group {} and your response has been sent to your inviter.".format(groupName)
        }))

### CREATE POLLS SECTION ###

# CREATE MEETUP/CLOSE POLL #~Helper
def createMeetCloseHelper(pollType):
    
    jsonData =json.loads(request.get_data())
    #GET DATA FROM FRONT END#
    groupName = jsonData["groupName"]
    pollData = {}
    pollData["pollCreator"] = jsonData["creatorFullName"]
    pollData["pollTitle"] = jsonData["pollTitle"]
    pollData["pollPrompt"] = jsonData["pollPrompt"]
    pollData["pollType"] = pollType
    pollData["uuid"] = str(uuid.uuid4())
    pollData["pollStatus"] = "ACTIVE"
    
    pollVoteOptions = {}
    for option in jsonData["pollVoteOptions"]:
        pollVoteOptions[option] = 0
    pollData["pollVoteOptions"] = pollVoteOptions
    pollData["voters"] = []
    pollData["result"] = None
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())

    groupPolls = json.loads(groupName[4])
    groupPolls.append(pollData)
    groupPolls = json.dumps(groupPolls)
    groupData[4] = groupPolls

    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()

@app.route('/createMeetupPoll', methods = ["POST"])
def createMeetupPoll():

    createMeetCloseHelper(pollType="MEETUP")
    return (jsonify({
        "Message": "Your Meetup poll has been created."
    }))

@app.route('/createCloseGroupPoll', methods = ["POST"])
def createCloseGroupPoll():
    createMeetCloseHelper(pollType="CLOSE")
    return (jsonify({
        "Message": "Your Close Group poll has been created."
    }))

# CREATE WARNPRAISEKICK POLL #~Helper
def createWarnPraiseKickHelper(pollType):
    jsonData =json.loads(request.get_data())
    #GET DATA FROM FRONT END#
    groupName = jsonData["groupName"]
    pollData = {}
    pollData["pollCreator"] = jsonData["creatorFullName"]
    pollData["targetedMemberEmail"] = jsonData["targetedMemberEmail"]
    pollData["targetedMemberName"] = jsonData["targetedMemberName"]
    pollData["pollTitle"] = jsonData["pollTitle"]
    pollData["pollPrompt"] = jsonData["pollPrompt"]
    pollData["pollType"] = pollType
    pollData["uuid"] = str(uuid.uuid4())
    pollData["pollStatus"] = "ACTIVE"
    pollVoteOptions = {}
    for option in jsonData["pollVoteOptions"]:
        pollVoteOptions[option] = 0
    pollData["pollVoteOptions"] = pollVoteOptions
    pollData["voters"] = []
    pollData["result"] = None
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())

    memberPolls = json.loads(groupName[3])
    memberPolls.append(pollData)
    memberPolls = json.dumps(memberPolls)
    groupData[3] = memberPolls

    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()

@app.route('/createWarningPoll', methods = ["POST"])
def createWarningPoll():
    createWarnPraiseKickHelper(pollType="WARNING")
    return (jsonify({
        "Message": "Your warning poll has been created."
    }))

@app.route('/createPraisePoll', methods = ["POST"])
def createPraisePoll():
    createWarnPraiseKickHelper(pollType="PRAISE")
    return (jsonify({
        "Message": "Your Praise poll has been created."
    }))

@app.route('/createKickPoll', methods = ["POST"])
def createKickPoll():
    createMeetCloseHelper(pollType="KICK")
    return (jsonify({
        "Message": "Your Kick poll has been created."
    }))

### END CREATE POLLS SECTION ###

### ISSUE VOTES SECTION ###
@app.route('/issueMeetupVote', methods = ["POST"])
def issueMeetupVote():

    #GET JSON DATA
    jsonData =json.loads(request.get_data())

    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["email"]
    pollUUID = jsonData["pollUUID"]
    groupName = jsonData["groupName"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()


    #REGISTER VOTE
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    groupPolls = json.loads(groupData[4])
    for index,poll in enumerate(groupPolls):
        if poll["uuid"] == pollUUID:
            poll["voters"].append(pollResponder)
            pollVoteOptions = poll["pollVoteOptions"]
            pollVoteOptions[pollResponse] += 1
            poll["pollVoteOptions"] = pollVoteOptions
            groupPolls[index] = poll
            break
    groupPolls = json.dumps(groupPolls)
    groupData[4] = groupPolls
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()

    #COUNT TOTAL VOTES
    groupPolls = json.loads(groupPolls)
    sumVotes = 0
    for index,poll in enumerate(groupPolls):
        if poll["uuid"] == pollUUID:
            pollVoteOptions = poll["pollVoteOptions"]
            for option,voteCount in pollVoteOptions.items():
                sumVotes += voteCount
            break
    totalMembers = len(groupData[5])


    maxResponseCount = 0
    answer = None
    #IF TOTAL VOTES == TOTAL MEMBERS, CLOSE POLL
    if sumVotes == totalMembers:
        for index,poll in enumerate(groupPolls):
            if poll["uuid"] == pollUUID:
                pollVoteOptions = poll["pollVoteOptions"]
                for option,voteCount in pollVoteOptions.items():
                    if voteCount > maxResponseCount:
                        maxResponseCount = voteCount
                        answer = option
                poll["result"] = answer
                poll["pollStatus"] = "CLOSED"
                groupPolls[index] = poll
                break

        groupPolls = json.dumps(groupPolls)
        groupData[4] = groupPolls
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    connection.close()

    return (jsonify({
        "Message": "Your meetup vote has been submitted."
    }))

@app.route('/issueCloseGroupVote', methods = ["POST"])
def issueCloseGroupVote():

    #GET JSON DATA
    jsonData =json.loads(request.get_data())

    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["email"]
    pollUUID = jsonData["pollUUID"]
    groupName = jsonData["groupName"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()


    #REGISTER VOTE
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    groupPolls = json.loads(groupData[4])
    for index,poll in enumerate(groupPolls):
        if poll["uuid"] == pollUUID:
            poll["voters"].append(pollResponder)
            pollVoteOptions = poll["pollVoteOptions"]
            pollVoteOptions[pollResponse] += 1
            poll["pollVoteOptions"] = pollVoteOptions
            groupPolls[index] = poll
            break
    groupPolls = json.dumps(groupPolls)
    groupData[4] = groupPolls
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()

    #COUNT TOTAL VOTES
    groupPolls = json.loads(groupPolls)
    sumVotes = 0
    for index,poll in enumerate(groupPolls):
        if poll["uuid"] == pollUUID:
            pollVoteOptions = poll["pollVoteOptions"]
            for option,voteCount in pollVoteOptions.items():
                sumVotes += voteCount
            break
    totalMembers = len(groupData[5])


    maxResponseCount = 0
    answer = None
    #IF TOTAL VOTES == TOTAL MEMBERS, CLOSE POLL
    if sumVotes == totalMembers:
        for index,poll in enumerate(groupPolls):
            if poll["uuid"] == pollUUID:
                pollVoteOptions = poll["pollVoteOptions"]
                for option,voteCount in pollVoteOptions.items():
                    if voteCount > maxResponseCount:
                        maxResponseCount = voteCount
                        answer = option
                if maxResponseCount == totalMembers:
                    if answer.lower() == "yes":
                        poll["result"] = answer
                        poll["pollStatus"] = "CLOSED"
                        groupPolls[index] = poll
                         
                        #NOTIFY SUPER USER THAT GROUP MUST BE CLOSED
                        reportMessage = "Members have voted to close this group."
                        cursor.execute("INSERT INTO moderationRequests (subject,message,type,status,number) VALUES(?,?,?,?,?)",(groupName,reportMessage,"CLOSE","OPEN",None))
                        connection.commit()
                else:
                    poll["result"] = answer
                    poll["pollStatus"] = "CLOSED"
                    groupPolls[index] = poll
            break
        groupPolls = json.dumps(groupPolls)
        groupData[4] = groupPolls
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    connection.close()

    return (jsonify({
        "Message": "Your meetup vote has been submitted."
    }))


# REGISTER MEMBER POLL VOTE #~HELPER
def registerVote(cursor,groupName,connection,pollUUID,pollResponder,pollResponse):
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
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
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()

# HANDLE POLL CLOSURE #~HELPER
def handleWarningPraiseKickVote(cursor,groupName,pollType,connection,pollUUID,pollTargetedMemberEmail):
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    memberPolls = json.loads(groupData[3])
    
    sumVotes = 0 #Count of the total sum of votes
    totalMembers = len(groupData[5]) # Cross checks to see if all votes have been registered
    maxResponseCount = 0 # Checks to see if it's actually unanimous
    answer = None #Answer field
    for index,poll in enumerate(memberPolls):
        if poll["uuid"] == pollUUID:
            pollVoteOptions = poll["pollVoteOptions"]
            for option,voteCount in pollVoteOptions.items():
                sumVotes += voteCount
                if voteCount > maxResponseCount:
                    maxResponseCount = voteCount
                    answer = option
            break
    if sumVotes == (totalMembers -1) == maxResponseCount: #We have all votes, and they were unanimous
        for index,poll in enumerate(memberPolls):
            if poll["uuid"] == pollUUID:
                poll["result"] = answer
                poll["pollStatus"] = "CLOSED"
                memberPolls[index] = poll
                break
        groupData[3] = json.dumps(memberPolls) #update member polls
        if answer.lower() == "yes": 
            memberList = json.loads(groupData[5])
            for member in memberList:
                if member["member"] == pollTargetedMemberEmail:
                    member[pollType] += 1
            groupData[5] = json.dumps(memberList)
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    elif sumVotes == (totalMembers - 1): #We have all votes, and they were not unanimous
        for index,poll in enumerate(memberPolls):
            if poll["uuid"] == pollUUID:
                poll["result"] = "Not unanimous"
                poll["pollStatus"] = "CLOSED"
                memberPolls[index] = poll
                break
        groupData[3] = json.dumps(memberPolls) #update member polls
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()

@app.route('/issueWarningVote', methods = ["POST"])
def issueWarningVote():

    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["voterEmail"]
    pollUUID = jsonData["pollUUID"]
    pollTargetedMemberEmail = jsonData["targetedMemberEmail"]
    groupName = jsonData["groupName"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #REGISTER VOTE INTO POLL
    registerVote(cursor = cursor, groupName= groupName, connection= connection,pollUUID=pollUUID,pollResponder=pollResponder,pollResponse=pollResponse)
    #

    #CHECK IF POLL IS COMPLETE - if so, handle the unanimous/non-unanimous outcomes
    handleWarningPraiseKickVote(cursor = cursor,groupName= groupName,pollType = "warnings",connection = connection,pollUUID=pollUUID,pollTargetedMemberEmail=pollTargetedMemberEmail)
    
    #Check the warning count for members and kick out if necessary
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    memberList = json.loads(groupData[5])
    adjustMember = False
    memberIndex = None
    for index,member in enumerate(memberList):
        if member["member"] == pollTargetedMemberEmail:
            if member["warnings"] >= 3: #User needs to be kicked out and points deducted
                memberIndex = index
                adjustMember = True
                break
    if adjustMember:
        del memberList[memberIndex]
        groupData[5] = json.dumps(memberList) #update member warning
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    #

    #Adjust the user's points and notify them about being kicked out
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(pollTargetedMemberEmail,))
    userData = cursor.fetchone()
    userData = list(userData)
    if adjustMember:
        #Deduct points
        userData[4] -= 5

        #Remove from group
        groupList = json.loads(userData[3])
        groupList.remove(groupName)
        userData[3] = json.dumps(groupList)

        #Notify member
        inboxList = json.loads(userData[10])
        inboxList.append({
            "sender": groupName,
            "message": "You've received 3 warnings from {} and incurred a 5 point deduction.".format(groupName)
        })
        userData[10] = json.dumps(inboxList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
        connection.commit()
    #Close Database connection and notify use that their vote has been registered
    connection.close()
    return (jsonify({
        "Message": "Your vote has been submitted."
    }))

@app.route('/issuePraiseVote', methods = ["POST"])
def issuePraiseVote():
    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["voterEmail"]
    pollUUID = jsonData["pollUUID"]
    pollTargetedMemberEmail = jsonData["targetedMemberEmail"]
    groupName = jsonData["groupName"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #REGISTER VOTE INTO POLL
    registerVote(cursor = cursor, groupName= groupName, connection= connection,pollUUID=pollUUID,pollResponder=pollResponder,pollResponse=pollResponse)
    #

    #CHECK IF POLL IS COMPLETE - if so, handle the unanimous/non-unanimous outcomes
    handleWarningPraiseKickVote(cursor = cursor,groupName= groupName,pollType = "praises",connection = connection,pollUUID=pollUUID,pollTargetedMemberEmail=pollTargetedMemberEmail)
    
    #Check the warning count for members and kick out if necessary
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    memberList = json.loads(groupData[5])
    adjustMember = False
    memberIndex = None
    for index,member in enumerate(memberList):
        if member["member"] == pollTargetedMemberEmail:
            if member["praises"] >= 3: #User needs to be kicked out and points deducted
                memberIndex = index
                adjustMember = True
                break
    if adjustMember:
        memberList[memberIndex]["praises"] = 0
        groupData[5] = json.dumps(memberList) #update member praise
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    #

    #Adjust the user's points and notify them that they've received a praise
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(pollTargetedMemberEmail,))
    userData = cursor.fetchone()
    userData = list(userData)
    if adjustMember:
        #Deduct points
        userData[4] += 5

        #Notify member
        inboxList = json.loads(userData[10])
        inboxList.append({
            "sender": groupName,
            "message": "You've received 3 praises from {} and was granted a 5 point increase! Congrats! Keep up the great work!".format(groupName)
        })
        userData[10] = json.dumps(inboxList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
        connection.commit()
    #Close Database connection and notify use that their vote has been registered
    connection.close()
    managePointStatus(pollTargetedMemberEmail)
    return (jsonify({
        "Message": "Your vote has been submitted."
    }))

@app.route('/issueKickVote', methods = ["POST"])
def issueKickVote():
    
    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    pollResponse = jsonData["pollResponse"] #Option they selected
    pollResponder = jsonData["voterEmail"]
    pollUUID = jsonData["pollUUID"]
    pollTargetedMemberEmail = jsonData["targetedMemberEmail"]
    groupName = jsonData["groupName"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #REGISTER VOTE INTO POLL
    registerVote(cursor = cursor, groupName= groupName, connection= connection,pollUUID=pollUUID,pollResponder=pollResponder,pollResponse=pollResponse)
    #

    #CHECK IF POLL IS COMPLETE - if so, handle the unanimous/non-unanimous outcomes
    handleWarningPraiseKickVote(cursor = cursor,groupName= groupName,pollType = "kicks",connection = connection,pollUUID=pollUUID,pollTargetedMemberEmail=pollTargetedMemberEmail)
    
    #Check the kick count and kick out if necessary
    cursor.execute("SELECT * FROM  groups WHERE [groupName] = ?",(groupName,))
    groupData = list(cursor.fetchone())
    memberList = json.loads(groupData[5])
    adjustMember = False
    memberIndex = None
    for index,member in enumerate(memberList):
        if member["member"] == pollTargetedMemberEmail:
            if member["kicks"] >= 1: #User needs to be kicked out and points deducted
                memberIndex = index
                adjustMember = True
                break
    if adjustMember:
        del memberList[memberIndex]
        groupData[5] = json.dumps(memberList) #update member warning
        cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
        cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
        connection.commit()
    #

    #Adjust the user's points and notify them about being kicked out
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(pollTargetedMemberEmail,))
    userData = cursor.fetchone()
    userData = list(userData)
    if adjustMember:
        #Deduct points
        userData[4] -= 10

        #Remove from group
        groupList = json.loads(userData[3])
        groupList.remove(groupName)
        userData[3] = json.dumps(groupList)

        #Notify member
        inboxList = json.loads(userData[10])
        inboxList.append({
            "sender": groupName,
            "message": "You have been kicked from {} and incurred a 10 point deduction.".format(groupName)
        })
        userData[10] = json.dumps(inboxList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
        connection.commit()
    #Close Database connection and notify use that their vote has been registered
    connection.close()
    managePointStatus(pollTargetedMemberEmail)
    return (jsonify({
        "Message": "Your vote has been submitted."
    }))

@app.route('/issueComplimentVote', methods = ["POST"])
def issueCompliment():
    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    complimentReceiverEmail = jsonData["complimentReceiverEmail"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #Increase Compliments/Score
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(complimentReceiverEmail,))
    userData = cursor.fetchone()
    userData = list(userData)
    userData[9] += 1
    if userData[9] >= 3:
        userData[9] = 0
        userData[4] += 5
        inboxList = json.loads(userData[10])
        inboxList.append({
            "sender": "Team Up",
            "message": "You've received 3 compliments and a 5 point increase!"
        })
        userData[10] = json.dumps(inboxList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (complimentReceiverEmail,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
        connection.commit()
    connection.close()

    managePointStatus(complimentReceiverEmail)
    #Return
    return (jsonify({
        "Message": "Your compliment has been sent!"
    }))

###END ISSUE VOTES SECTION###


### ADD TO WHITEBOX/BLACKBOX SECTION ###

# ADD TO AUTOBOX #~HELPER
def addtoAutoBox(cursor,connection,userEmail,emailAddition,index):
    #Add user to autoBox
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(userEmail,))
    userData = cursor.fetchone()
    userData = list(userData)
    autoBox = userData[index]
    autoBox = json.loads(autoBox)
    if emailAddition not in autoBox:
        autoBox.append(emailAddition)
    autoBox = json.dumps(autoBox)
    userData[index] = autoBox
    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()

@app.route('/addToWhiteBox', methods = ["POST"])
def addToWhiteBox():
    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    emailAddition = jsonData["emailAddition"]
    userEmail = jsonData["userEmail"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #Add user to autoBox
    addtoAutoBox(cursor = cursor, connection = connection,userEmail=userEmail ,emailAddition=emailAddition,index = 8)
    connection.close()
    #Return
    return (jsonify({
        "Message": "{} has been registered to your whitebox.".format(emailAddition)
    }))

@app.route('/addToBlackBox', methods = ["POST"])
def addToBlackBox():
    #GET DATA FROM FRONT END
    jsonData =json.loads(request.get_data())
    emailAddition = jsonData["emailAddition"]
    userEmail = jsonData["userEmail"]
    #

    #SQL CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #Add user to autoBox
    addtoAutoBox(cursor = cursor, connection = connection,userEmail=userEmail ,emailAddition=emailAddition,index = 7)
    connection.close()
    #Return
    return (jsonify({
        "Message": "{} has been registered to your blackbox.".format(emailAddition)
    }))
### END ADD TO WHITEBOX/BLACKBOX SECTION ###

########## END BASE USER CODE ##########


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
    jsonData =json.loads(request.get_data())
    userEmail = jsonData["email"] # email of the user appealing
    appealMessage = jsonData["appealMessage"]

    sendModRequest(userEmail, appealMessage, "REP_APPEAL")
    return jsonify({"Success: appeal has been submitted."})

@app.route('/reportUser', methods = ["POST"])
def reportUser():
    #GET FRONT END DATA
    jsonData =json.loads(request.get_data())
    targetEmail = jsonData["email"] #email of the user being reported
    reportMessage = jsonData["reportMessage"]
    sendModRequest(targetEmail, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})

@app.route('/reportGroup', methods = ["POST"])
def reportGroup():
    #GET FRONT END DATA
    jsonData =json.loads(request.get_data())
    groupName = jsonData["groupName"] #name of the group being reported
    reportMessage = jsonData["reportMessage"]
    sendModRequest(groupName, reportMessage, "REPORT")
    return jsonify({"Success: report has been submitted."})

### END SENDING REPORTS/APPEALS ###

### ALTER REPUTATION ###
@app.route('/referenceReputation', methods = ["POST"])
def referenceReputation():
    #GET FRONT END DATA
    jsonData =json.loads(request.get_data())
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
    
    cursor.execute("DELETE FROM users WHERE [email] = ?", (referredUserEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES (?,?,?,?,?,?,?,?,?,?,?)",tuple(referredUserData))
    connection.commit()


    referredUsersList = json.loads(referringUserData[11])
    referredUsersList.remove(referredUserEmail)
    referredUsersList = json.dumps(referredUsersList)
    referringUserData[11] = referredUsersList
    
    cursor.execute("DELETE FROM users WHERE [email] = ?", (referringUserEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,complimentsorcomplaints,inbox) VALUES (?,?,?,?,?,?,?,?,?,?,?)",tuple(referringUserData))
    connection.commit()
    connection.close()
    managePointStatus(referredUserEmail)
    return (jsonify({
        "Message": "Points have been submitted to the new user."
    }))

@app.route('/createGroup', methods=["POST"])
def createGroup():
    jsonData =json.loads(request.get_data())

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
    cursor.execute("SELECT * FROM groups where [groupName] = ?",(groupName,))
    groupDataFLAG = cursor.fetchone()
    if groupDataFLAG is not None:
        connection.close()
        return jsonify({"Message": "Sorry, this group already exists!"})
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()

    # add group to user's grouplist
    cursor.execute("SELECT * from users WHERE [email] = ?",(creator,))
    userData = cursor.fetchone()
    userData = list(userData)
    groupList = json.loads(userData[3])
    groupList.append(groupName)
    userData[3] = json.dumps(groupList)
    cursor.execute("DELETE FROM users WHERE [email] = ?", (creator,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()
    return jsonify({"Message" : "Group successfully created."})

########## END ORDINARY USER CODE ##########

########## SUPER USER CODE ##########

@app.route('/handleApplication', methods = ["POST"])
def handleApplication():

    #------Get Data from Front-end-----#
    jsonData =json.loads(request.get_data())

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


    # accept the applications
    if response.lower() == "accept":
        #first update the signup row for this user and change user status
        rowData[5] = "OU"
        
        signUpUserData[6] = "USER"
        

        cursor.execute("DELETE FROM signup WHERE [email] = ?", (email,))
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(signUpUserData))
        connection.commit()

        # add the user to the user database
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
        connection.commit()
        connection.close()
        return (jsonify({"Message" : "{} is now registered to Team Up.".format(email)}))
    #decline the application
    elif response.lower() == "decline":

        signUpUserData[6] = "REJECTED"
        #modify the row
        cursor.execute("DELETE FROM signup WHERE [email] = ?", (email,))
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(signUpUserData))
        connection.commit()
        connection.close()
        return jsonify({
            "Message": "{} will be notified that their application has been rejected.".format(email)
        })
    #blacklist the application
    elif response.lower() == "blacklist":
        signUpUserData[6] = "BLACKLISTED"
        #modify the row
        cursor.execute("DELETE FROM signup WHERE [email] = ?", (email,))
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(signUpUserData))
        connection.commit()
        connection.close()
        return jsonify({
            "Message": "{} will be notified that their application has been blacklisted.".format(email)
        })

# @app.route('/blacklistFromServer', methods = ["POST"])
# def blacklistFromServer():
#     jsonData =json.loads(request.get_data())

#     userEmail = jsonData["userEmail"]

#     #------Connection-----#
#     connection = sqlite3.connect(r"./database.db")
#     cursor = connection.cursor()

#     #------Get the visitor information-----#
#     cursor.execute("SELECT * FROM signup where [email] = ?",(userEmail,))
#     visitorData = list(cursor.fetchone())

#     #modify the visitor signup row
#     visitorData[6] = "BLACKLISTED"
#     cursor.execute("DELETE FROM signup WHERE [email] = ?", (userEmail,))
#     cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(visitorData))
#     connection.commit()
#     connection.close()

#     return jsonify({
#             "Message": "The visitor has been added to blacklist."
#         })



@app.route('/reverseReputationDeduction', methods = ["POST"])
def reverseReputationDeduction():
    jsonData =json.loads(request.get_data())
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
    jsonData =json.loads(request.get_data())

    groupName = jsonData['groupName']

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Delete the row-----#
    cursor.execute("SELECT * FROM users WHERE [groupName] = ?",(groupName,))
    groupData = cursor.fetchone()
    groupData = list(groupData)
    groupData[1] = "CLOSED"
    cursor.execute("DELETE FROM groups WHERE [groupName] = ?",(groupName,))
    cursor.execute("INSERT INTO groups (groupName,status,posts,memberpolls,groupPolls,members) VALUES(?,?,?,?,?,?)",tuple(groupData))
    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "{} has been closed.".format(groupName)
    }))

@app.route('/issuePointDeduction', methods = ["POST"])
def issuePointDeduction():

    jsonData =json.loads(request.get_data())
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
    
    jsonData =json.loads(request.get_data())
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

    jsonData =json.loads(request.get_data())
    userEmail = jsonData["userEmail"]

    #------Connection-----#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    #------Get the signup information-----#
    cursor.execute("SELECT * FROM signup where [email] = ?",(userEmail,))
    visitorData = list(cursor.fetchone())

    #modify the signup row
    visitorData[6] = "BLACKLISTED"
    cursor.execute("DELETE FROM signup WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(visitorData))



    #Get the users information
    cursor.execute("SELECT * FROM users WHERE [email] = ?", (userEmail,))
    userData = list(cursor.fetchone())

    #modify the user row
    userData[5] = "BLACKLISTED"
    cursor.execute("DELETE FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))

    connection.commit()
    connection.close()

    return (jsonify({
        "Message": "{} has been blacklisted from Signup and Users table.".format(userEmail)
    }))

########## END SUPER USER CODE ##########


########## VIP USER CODE ##########
@app.route('/createDemocraticSuperUserPoll', methods = ["POST"])
def createDemocraticSuperUserPoll():

    jsonData =json.loads(request.get_data())
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
    }))


@app.route('/issueDemocraticSuperUserVote', methods = ["POST"])
def issueDemocraticSuperUserVote():

    #GET JSON DATA
    jsonData =json.loads(request.get_data())
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
    rowData[0] = memberPolls
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
            cursor.execute("DELETE FROM users WHERE [email] = ?", (memberPolls["targetedMemberName"],))
            cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
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


########## VISITOR USER CODE ##########

@app.route('/signupApplication', methods = ["POST"])
def signUpApplication():
    jsonData =json.loads(request.get_data())
    print("MY JSON DATA\n",jsonData)
    # print("@@@@@Can you see this?@@@@@",jsonData)
    #
    rowData = [] #Data to be uploaded to database
    rowData.append(jsonData["fullname"])
    rowData.append(jsonData["email"].lower())
    rowData.append(jsonData["interests"])
    rowData.append(jsonData["credentials"])
    rowData.append(jsonData["reference"])
    rowData.append("None")                      # appeal (does not exist on initial sign up)
    rowData.append("PENDING")
     
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))
    userData = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE [email] = ?",(jsonData["reference"].lower(),))
    referrerData = cursor.fetchone()

    if userData is not None:
        connection.close()
        return (jsonify({
            "Message": "Sorry, an account with this email already exists. Please check your application status instead."
        }))
    else:
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(rowData))

        # add new user to inviter's list of referred users
        referrerData = list(referrerData)
        referredUserList = json.loads(referrerData[11])
        referredUserList.append(jsonData["email"].lower())
        referrerData[11] = json.dumps(referredUserList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (referrerData[0],))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(referrerData))
        connection.commit()
        connection.close()
    #
    return (jsonify({
        "Message": "Thank you for registering! Your application is pending approval."
    }))

@app.route('/checkStatus', methods = ["POST"])
def checkStatus():
    jsonData =json.loads(request.get_data())

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))
    userData = cursor.fetchone()
    connection.close()
    if userData is not None:
        if userData[6] == "PENDING":
            return (jsonify({
                "Status" : "PENDING",
                "Message": "Your application is pending approval."
            }))
        elif userData[6] == "USER":
            return (jsonify({
                "Status" : "USER",
                "Message": "Congratulations! Your account has been approved. Please sign in with the email and credentials you've provided."
            }))
        elif userData[6] == "APPEALED":
            return (jsonify({
                "Status" : "APPEALED",
                "Message": "Your appeal is pending approval."
            }))
        elif userData[6] == "BLACKLISTED":
            return (jsonify({
                "Status" : "BLACKLISTED",
                "Message": "You have been blacklisted from Team Up."
            }))
        elif userData[6] == "REJECTED":
            return (jsonify({
                "Status" : "REJECTED",
                "Message": "Sorry, your application did not pass our first round of approval. Please write an appeal message telling us why you'd be a great fit for this community."
            }))
    return (jsonify({
        "Message": "Sorry, we couldn't find any users related to this email. Please sign up."
    }))


@app.route("/appealRejection", methods = ["POST"])
def appealRejection():
 
    jsonData =json.loads(request.get_data())
    email = jsonData["email"].lower()
    appealMessage = jsonData["appealMessage"]
 
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(email,))
    row = list(cursor.fetchone())
 
    cursor.execute("DELETE FROM signup WHERE [email] = ?", (email,))
    row[5] = appealMessage
    row[6] = "APPEALED"
    cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(row))

    # add appeal to SU moderation queue
    cursor.execute("INSERT INTO moderationRequests (subject,message,type,status,number) VALUES(?,?,?,?,?)",(email,appealMessage,"SIGNUP_APPEAL","OPEN",None))

    connection.commit()
    connection.close()
    return (jsonify({"Message" : "Your appeal has been submitted!"}))
        
########## END VISITOR USER CODE ##########


@app.route('/', methods=['GET'])
def root():
    return render_template("landing.html")
    # return send_from_directory(app.static_folder, 'landing.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/groupMainPage', methods=['GET'])
def groupMainPage():
    return render_template("groupMainPage.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/OU', methods=['GET'])
def OU():
    return render_template("OU.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/SU', methods=['GET'])
def SU():
    return render_template("SU.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/surfing', methods=['GET'])
def surfing():
    return render_template("surfing.html")
    # return send_from_directory(app.static_folder, 'landing.html')

@app.route('/vip', methods=['GET'])
def vip():
    return render_template("vip.html")
    # return send_from_directory(app.static_folder, 'landing.html')


if __name__ == '__main__':
    app.run(debug=True)
