import sqlite3


class Visitor():
    def __init__(self, name, email, password, referredBy, topicOfInterest):
        self.name = name
        self.email = email
        self.password = password
        self.referredBy = referredBy
        self.topicOfInterest = topicOfInterest


    def signUp(self):
        # Take in the following info from visitor: name, email, password, credentials, referral
        #
        # if (user already exists in the PendingUsers database):
        #   print("Please wait while your current application status is under review")
        #
        # if (user already exists in the User Database):
        #   print("Account already exists, Sign in")
        #
        # if (the user exists in the blacklist database):
        #   print("You are banned, signup denied")
        #
        # else:
        #   row = []
        #   row.append(name, email, password, credentials, referral)
        #   Userdatabase.table.upload(row)
        #   user application status returned
        #   verify that application has been submitted

        connection = sqlite3.connect(r"./database.db")
        cursor = connection.cursor()
        found = []
        cursor.execute("SELECT * FROM signup WHERE [email] = ?",(self.email,))
        for row in cursor.fetchall():
            found.append(row)

        if len(found) != 0:
            print("user alreayd exists")
        else:
            cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,rejectionCount) VALUES(?,?,?,?,?,0)",(self.name,self.email,self.topicOfInterest,self.password,self.referredBy))
            connection.commit()
        connection.close()
        #attempt to upload information into signup database.


    def appealRejection(userID, message):
        # Vistor inputs an appeal message 
        # 
        # if (the visitor userID exists in the PendingUser Database):
        #   fetch the User data
        #   row = []
        #   row.append(UserID, message)
        #   SuperUser.Database.table.upload(row) #send the user's message and appeal request to SuperUser
        #    
        # 
        # if (the appeal request submitted to the User database successfully):
        #   return the application status
        # else:
        #   return failed status
        

test = Visitor("ahsan","ahsan@iknox.com", "passwordl","abdul","food")

test.signUp()
