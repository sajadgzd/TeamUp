import sqlite3


connection = sqlite3.connect(r"./database.db")
cursor = connection.cursor()


cursor.execute("SELECT name from sqlite_master WHERE type = 'table';")
tableList = []

for table in cursor.fetchall():
     tableList.append(str(table[0]))

print(tableList)

if "signup" not in tableList:
     cursor.execute("CREATE TABLE signup  (\
                              fullname                TEXT,\
                              email                   TEXT PRIMARY KEY,\
                              interests               TEXT,\
                              credentials             TEXT,\
                              reference               TEXT,\
                              appeal                  TEXT,\
                              status                  TEXT\
                         );"
                         )
     connection.commit()

if "users" not in tableList:
     cursor.execute("CREATE TABLE users  (\
                              email                TEXT PRIMARY KEY,\
                              fullname             TEXT,\
                              password             TEXT,\
                              groupList            TEXT,\
                              reputationScore      TEXT,\
                              status               TEXT,\
                              invitations          TEXT,\
                              blacklist            TEXT,\
                              whitelist            TEXT,\
                              compliments          TEXT,\
                              inbox                TEXT,\
                              referredUsers        TEXT\
                         );"
                         )
     connection.commit()

if "groups" not in tableList:
     cursor.execute("CREATE TABLE groups  (\
                              groupName            TEXT PRIMARY KEY,\
                              status               TEXT,\
                              posts                TEXT,\
                              memberPolls          TEXT,\
                              groupPolls           TEXT,\
                              members              TEXT);"
                    )
     connection.commit()

if "moderationRequests" not in tableList:

     """
     subject: subject of request (can be self, another user, or group)
     message: accompanying message for request
     type: REP_APPEAL, SIGNUP_APPEAL, REPORT
     status: OPEN, CLOSED
     number: sequential number of request
     """
     
     cursor.execute("CREATE TABLE moderationRequests  (\
                              subject             TEXT,\
                              message             TEXT,\
                              type                TEXT,\
                              status              TEXT,\
                              number              INTEGER PRIMARY KEY);"
                    )

     connection.commit()