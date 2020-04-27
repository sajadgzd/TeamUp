class BaseUser():

    def __init__(self, name, email, username, interest, cred, rejection):
        self.name = name
        self.email = email
        self.username = username
        self.interest = interest
        self.cred = cred
        self.rejection = rejection


    def login(name, email, interest, cred, ref):
        pass

    def inviteToGroup(username):
        pass

    def handleGroupMeeting():
        pass

    def createMeetupPoll():
        pass

    def createWarningPoll():
        pass

    def createPraisePoll():
        pass
    
    def createKickPoll():
        pass
    
    def createCloseGroupPoll():
        pass
    
    def issueMeetupVote():
        pass
    
    def issueWarningVote():
        pass
    
    def issuePraiseVote():
        pass
    
    def issueKickVote():
        pass
    
    def issueCloseGroupPoll():
        pass
    
    def issueCompliment():
        pass
    
    def addToWhiteBox():
        pass
    
    def addToBlackBox():
        pass