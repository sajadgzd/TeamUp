from OrdinaryUser import OrdinaryUser

class VipUser(OrdinaryUser):
    def __init__(self):
        OrdinaryUser.__init__(self)
    
    def createDemocraticSuperUserPoll(vipUserID, pollName, pollType, optionsList):
        # if (vipUserID is in vip User Database)
        # 
        #   if (pollName already exists in the Poll Database):
        #       print("Poll already exists")
        #
        #   else:
        #       PollDatabase.append(pollName)
        #       PollDatabase.append(optionsList)
        #       PollDatabase.append(pollType)
        #       print("Poll added to the database")
        #  
    
    def issueDemocraticSuperUserVote(pollName, vipUserID, decision):
        # if (vipUserID is in vip User Database && pollName in Poll Database) 
        #
        #    if (vipUserID has not voted yet):
        #       pollDatabase.append(pollName)
        #       pollDatabase.append(decision)
        #       print("Your decision has been submitted")