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
                              complimentsorcomplaints TEXT,\
                              inbox                TEXT\
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
