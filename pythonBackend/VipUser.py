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
        #       row = []
        #       row.append(vipUserID, pollName, pollType, optionsList)
        #       database.table.upload(row)

        #   return status
        #  
    
    def issueDemocraticSuperUserVote(pollName, vipUserID, decision):
        # if (vipUserID is in vip User Database && pollName in Poll Database) 
        #       
        #    if (vipUserID has not voted yet):
        #       row = []
        #       row.append(pollName, vipUserID, decision)
        #       database.table.upload(row)
        #       print("Your decision has been submitted")