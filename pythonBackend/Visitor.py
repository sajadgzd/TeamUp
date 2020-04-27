import sqlite3


class Visitor():
    def __init__(self, name, email, password, referredBy, topicOfInterest):
        self.name = name
        self.email = email
        self.password = password
        self.referredBy = referredBy
        self.topicOfInterest = topicOfInterest


    def signUp(self):

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


    def appealRejection():
        pass

test = Visitor("ahsan","ahsan@iknox.com", "passwordl","abdul","food")

test.signUp()
