class BaseUser():

    def __init__(self, name, email, username, interest, cred, rejection):
        self.name = name
        self.email = email
        self.username = username
        self.interest = interest
        self.cred = cred
        self.rejection = rejection


    def login(userID, password):
        # Input account ID, Password
        # 
        # if (the account ID, password in database):
        #   approve user  
        #   successful return status
        #   proceed to the User Page UI
        # 
        # else:
        #   print("Your username and passwords do not match")
        #   stay on the signup page


    def inviteToGroup(senderUserID, groupName, recipientUserID):
        # if (senderUserID && recipientUserID is in User Database) &&
        #       (groupName in Group Database)
        #   row = []
        #   row.append(invite, senderUserID, groupName)
        #   recipientUser_database.table.upload(row)
        #   (backend process)
        #   print(status)


    def handleGroupMeeting(senderUserID, decision, reason, recepientUserID):
        # if (senderUserID && recipientUserID is in User Database) &&
        #   (groupName in Group Database)
        #
        #   row = []
        #   row.append(decision, senderUserID, reason, groupName, recipientUserID)
        #   recipientUser_database.table.upload(row)
        # 
        #   print(status)

    def createMeetupPoll(creatorUserID, pollName, pollType, optionsList):
        # if (UserID is in User Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       row = []
        #       row.append(creatorUserID, pollName, optionsList, pollType, recipientUserID)
        #       Polldatabase.table.upload(row)
        #
        #       print("Poll added to the database")

    def createWarningPoll(pollName, pollType, optionsList, targetUserID):
        # if (UserID is in User Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       row = []
        #       row.append(targetUserID, pollName, optionsList, pollType)
        #       Polldatabase.table.upload(row)
        #       print("Poll added to the database")

    def createPraisePoll(pollName, pollType, optionsList, targetUserID):
        # if (UserID is in User Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       row = []
        #       row.append(targetUserID, pollName, optionsList, pollType)
        #       Polldatabase.table.upload(row)
        #       
        #       print("Poll added to the database")
    
    def createKickPoll(pollName, pollType, optionsList, targetUserID):
        # if (UserID is in User Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       row = []
        #       row.append(targetUserID, pollName, optionsList, pollType)
        #       Polldatabase.table.upload(row)
        #
        #       print("Poll added to the database")
    
    def createCloseGroupPoll(pollName, pollType, optionsList, targetGroupID):
        # if (GroupID is in Group Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       row = []
        #       row.append(targetUserID, pollName, optionsList, pollType)
        #       Polldatabase.table.upload(row)
        #       print("Poll added to the database")
    
    def issueMeetupVote(pollName, UserID, decision):
        # if (UserID is in vip User Database) 
        #
        #    if (vipUserID has not voted yet):
        #       row = []
        #       row.append(UserID, pollName, decison)
        #       Polldatabase.table.upload(row)
        #       print("Your decision has been submitted")
    
    def issueWarningVote(pollName, UserID, decision):
        # if (userID is in User Database && pollName in Poll Database) 
        #
        #    if (userID has not voted yet):
        #       row = []
        #       row.append(UserID, pollName, decision)
        #       Polldatabase.table.upload(row)
        #       print("Your decision has been submitted")
        #
        #   else:
        #       print("You have already submitted your response for this poll")
    
    def issuePraiseVote(pollName, UserID, decision):
        # if (userID is in User Database && pollName in Poll Database) 
        #
        #    if (userID has not voted yet):
        #       row = []
        #       row.append(UserID, pollName, decision)
        #       Polldatabase.table.upload(row)
        #       print("Poll added to the database")

        #       print("Your decision has been submitted")
        #   else:
        #       print("You have already submitted your response for this poll")
    
    def issueKickVote(pollName, UserID, decision):
        # if (userID is in User Database && pollName in Poll Database) 
        #
        #    if (userID has not voted yet):
        #       row = []
        #       row.append(UserID, pollName, decision)
        #       Polldatabase.table.upload(row)
        #       print("Your decision has been submitted")
        #   else:
        #       print("You have already submitted your response for this poll")
    
    
    def issueCompliment(UserId, complimentComment):
        #if (userID exists in the user database):
        #   row = []
        #   row.append(UserID, complimentComment)
        #   Userdatabase.table.upload(row)

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
        #       row = []
        #       row.append(UserID)
        #       Whitelistdatabase.table.upload(row)
        #       print("User added to your whitebox")
        #
        # else:
        #   print("The user you are trying to whitelist doesn't exist")
    
    def addToBlackBox(userID):
        #if (userID exists in the user database):
        #   if (userID exists in self.blackbox database):
        #       print("User already to blackbox")
        #   
        #   else:
        #       row = []
        #       row.append(UserID)
        #       blacklistdatabase.table.upload(row)
        #       print("User added to your blackbox")
        #       print("User banned")
        #
        # else:
        #   print("The user you are trying to ban doesn't exist")