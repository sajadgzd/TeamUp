from BaseUser import BaseUser

class OrdinaryUser(BaseUser):
    def __init__(self):
        BaseUser.__init__(self)

    def appealReputation(appealMessage):
        # input appealMessage
        # Send the appealMessage to SuperUser inbox database
        # if (append to SuperUser Inbox database status == "success"):
        #   print("Appeal submitted successfully")
    
    def reportUser(UserID, reportMessage):
        # input UserID and reportMessage
        # Send reportMessage to the SuperUser inbox database
        # if (append to SuperUser Inbox database status == "success"):
        #   print("Report submitted successsfully")

    
    def reportGroup(groupName, reportMessage):
        # input groupName and reportMessage
        #
        # if (groupName is in Group Database)
        #   Send reportMessage to the SuperUser inbox database
        #
        #   if (append to SuperUser Inbox databae status == "success"):
        #       print("Report submitted successsfully")
    
    def referenceReputation(UserID, reputationPoints):
        # input UserID and reputationPoints that will be given
        # 
        # if(UserID is in User Database):
        #   currentUser.scorepoints += reputationPoints
        #   print("Initial reputation score has been successfully added")
    


    
    
