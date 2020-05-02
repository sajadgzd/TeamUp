from BaseUser import BaseUser

class SuperUser(BaseUser):
    def __init__(self):
        BaseUser.__init__(self)

    def handleApplication(UserID, decision):
        # input UserID
        # if (UserID exists in the pending application database):
        #   if (decision == accept):
        #       remove the user from PendingUser Database
        #       row = []
        #       row.append(UserID, decision)
        #       database.table.upload(row)
        #       print("User Registered Successfully")
        #   
        #   elif (decision == deny):
        #       if(number_of_times_denied > 1):
        #           add to blacklist
        #        
        #       number_of_times_denied += 1
        #       print("User Registration denied")

    
    def blacklistFromServer(UserID):
        # input UserID
        # if (UserID exists in the User Database):
        #   if (User already not exists in BlackList database):
        #       row = []
        #       row.append(UserID)
        #       BlackList_Database.table.upload(row)


    def reverseReputationDeduction(UserID, decision):
        # input UserID
        # if (UserID exists in the UserDatabase):
        #   databasetable.currentUser.reputationpoint += 5
        #   print("Reputation Deduction is reversed")
    
    def shutDownGroup(groupName):
        # input groupName
        # if(groupName exist in the Groups Database):
        #   GroupsDatabase.remove(groupName)
        #   print("Group was shutdown successfully")
        #
    
    def issuePointDeduction(UserID):
        # if (userID exists in the user database):
        #   currentUser.reputationpoint -= 5
        #   print("Reputation Deduction done")
    
    def issuePointIncrement(UserID, ):
        # if (userID exists in the user database):
        #   currentUser.reputationpoint += 5
        #   print("Reputation Increment done")

    def banUser(UserID):
        # if (userID exists in the user database):
        #   if (userID exists in blacklist database):
        #       print("User already banned")
        #   
        #   else:
        #       row = []
        #       row.append(UserID)
        #       BlackList_Database.table.upload(row)
        #
        # else:
        #   print("The user you are trying to ban doesn't exist")
        #   
