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

    if status == "VIP":
        if points < 25:
            userData[5] = "OU"
    elif status == "OU":
        if points > 30:
            userData[5] = "VIP"
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (email,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()
    connection.close()

@app.route('/getUserData', methods = ["POST"])
def getUserData():
    jsonData = request.json
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
    userData[10] = json.loads(userData[10]) #inbox
    userData[11] = json.loads(userData[11]) #referredUsers
    return (jsonify({
        "userData": userData
    }))

@app.route('/getGroupData', methods = ["POST"])
def getGroupData():
    jsonData = request.json
    groupName = jsonData["groupName"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [groupName] = ?",(groupName,))
    groupData = cursor.fetchone()
    groupData = list(groupData)

    groupData[2] = json.loads(groupData[2]) #posts
    groupData[3] = json.loads(groupData[3]) #member polls
    groupData[4] = json.loads(groupData[4]) #group polls
    groupData[5] = json.loads(groupData[5]) #member list

    return (jsonify({
        "groupData": groupData
    }))

@app.route('/login', methods = ["POST"])
def login():
    jsonData = request.json

    email = jsonData["email"]
    credentials = jsonData["credentials"]

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ? AND [credentials] = ?",(email,credentials))
    userData = cursor.fetchone()
    userData = list(userData)

    if userData is not None:
        return jsonify({
            "Sucess": "Welcome to Team Up!"
        })
    else:
        return jsonify({
            "Error": "Sorry, email or password combination does not exist."
        })

@app.route('/inviteToGroup', methods = ["POST"])
def inviteToGroup():

    #GET JSON DAT
    jsonData = request.json

    inviter = jsonData["inviterEmail"].lower()
    inviterFullname = jsonData["inviterFullname"]
    groupName = jsonData["groupName"]
    invitee = jsonData["inviteeEmail"].lower()

    #CONNECT TO DATABASE
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE [email] = ?",(invitee,))

    inviteeData = cursor.fetchone()
    inviteeData = list(inviteeData)

    blackList = json.loads(inviteeData[7])
    for blocked in blackList:
        if blocked["email"] == inviter:
            connection.close()
            return jsonify({
            "Message": "Sorry, your invitation has been automatically rejected."
        })

    whiteList = json.loads(inviteeData[8])
    for autoAccept in whiteList:
        if autoAccept["email"] == inviter:
            #Add group to invitee list
            groupList = json.loads(inviteeData[3])
            groupList.append(groupName)
            groupList = json.dumps(groupList)
            inviteeData[3] = groupList
            cursor.execute("DELETE * FROM users WHERE [email] = ?", (invitee,))
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

            cursor.execute("DELETE * FROM groups WHERE [groupName] = ?",(groupName,))
            cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
            connection.commit()
            connection.close()
            return jsonify({
                "Message": "Your invitation has been automatically accepted!"
            })

    invitations = json.loads(inviteeData[6])
    invitations.append({
        "inviterFullName": inviterFullname,
        "inviterEmail" :inviter,
        "groupName": groupName
    })

    invitations = json.dumps(invitations)
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (invitee,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
    connection.commit()
    connection.close()
    return jsonify({
        "Message": "Your invitation has been sent!"
    })


@app.route('/handleGroupInvite', methods = ["POST"])
def handleGroupInvite():

    #GET JSON DATA
    jsonData = request.json

    inviter = jsonData["inviterEmail"]
    inviterFullname = jsonData["inviterFullName"]
    groupName = jsonData["groupName"]
    invitee = jsonData["inviteeEmail"]
    message = jsonData["message"]
    response = jsonData["response"]


    #SQLITE CONNECTION
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE [email] = ?",(invitee,))

    #If they accept the invitation
    if response.lower() == "accepted":
        #Add the invitee to the group list
        cursor.execute("SELECT * FROM groups WHERE [groupName] = ?",(groupName,))
        groupData= list(cursor.fetchone())
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
        connection.commit()

        #Add the group to the invitee's group list
        cursor.execute("SELECT * FROM users where [email] = ?",(invitee,))
        inviteeData = list(cursor.fetchone())
        groupList = json.loads(inviteeData[3])
        groupList.append(groupName)
        groupList = json.dumps(groupList)
        inviteeData[3] =groupList
        cursor.execute("DELETE FROM users WHERE [email] = ?",(invitee,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviteeData))
        connection.commit()

        #Notify the inviter that they have accepted the invitation
        cursor.execute("SELECT * FROM users where [email] = ?",(inviter,))
        inviterData = list(cursor.fetchone())
        inboxList = json.loads(inviteeData[10])
        inboxList.append({
            "sender": inviter,
            "message": "Your invitation has been accepted by {}.".format(invitee)
        })
        inboxList = json.dumps(inboxList)
        inviterData[10] =inboxList
        cursor.execute("DELETE FROM users WHERE [email] = ?",(inviter,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviterData))
        connection.commit()
        connection.close()
        return (jsonify({
            "message": "You've been added to the group {} and your response has been sent to your inviter.".format(groupName)
        }))
    elif response.lower() == "declined":
        #Notify the inviter that their invitation has been declined
        cursor.execute("SELECT * FROM users where [email] = ?",(inviter,))
        inviterData = list(cursor.fetchone())
        inboxList = json.loads(inviteeData[10])
        inboxList.append({
            "sender": inviter,
            "message": message
        })
        inboxList = json.dumps(inboxList)
        inviterData[10] =inboxList
        cursor.execute("DELETE FROM users WHERE [email] = ?",(inviter,))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(inviterData))
        connection.commit()
        connection.close()
        return (jsonify({
            "message": "You have declined your invitation to the group {} and your response has been sent to your inviter.".format(groupName)
        }))

### CREATE POLLS SECTION ###

# CREATE MEETUP/CLOSE POLL #~Helper
def createMeetCloseHelper(pollType):
    
    jsonData =request.json
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
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
    jsonData =request.json
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
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
    jsonData = request.json

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
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
        connection.commit()
    connection.close()

    return (jsonify({
        "Message": "Your meetup vote has been submitted."
    }))

@app.route('/issueCloseGroupVote', methods = ["POST"])
def issueCloseGroupVote():

    #GET JSON DATA
    jsonData = request.json

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
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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

                        connection = sqlite3.connect(r"./database.db")
                        cursor = connection.cursor()
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
    cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
        connection.commit()

@app.route('/issueWarningVote', methods = ["POST"])
def issueWarningVote():

    #GET DATA FROM FRONT END
    jsonData = request.json
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("DELETE * FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
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
    jsonData = request.json
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("DELETE * FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
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
    jsonData = request.json
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
        cursor.execute("INSERT INTO groups (groupName,status,posts,polls,members) VALUES(?,?,?,?,?)",tuple(groupData))
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
        cursor.execute("DELETE * FROM users WHERE [email] = ?", (pollTargetedMemberEmail,))
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
    jsonData = request.json
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
        cursor.execute("DELETE * FROM users WHERE [email] = ?", (complimentReceiverEmail,))
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
    cursor.execute("DELETE * FROM users WHERE [email] = ?", (userEmail,))
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(userData))
    connection.commit()

@app.route('/addToWhiteBox', methods = ["POST"])
def addToWhiteBox():
    #GET DATA FROM FRONT END
    jsonData = request.json
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
    jsonData = request.json
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

########## END ORDINARY USER CODE ##########

if __name__ == '__main__':
    app.run(debug=True)
