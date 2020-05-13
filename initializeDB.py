import sqlite3
from flask import Flask, jsonify, render_template, request, send_from_directory
import json

def createDB():
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
                                reputationScore      INTEGER,\
                                status               TEXT,\
                                invitations          TEXT,\
                                blacklist            TEXT,\
                                whitelist            TEXT,\
                                compliments          INTEGER,\
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
    if "democraticSU" not in tableList:
        
        cursor.execute("CREATE TABLE democraticSU  (\
                                poll                TEXT,\
                                userexists          INTEGER,\
                                pollexists          INTEGER);"
                        )

        connection.commit()

def clearAllTables():
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM signup")
    connection.commit()
    cursor.execute("DELETE FROM groups")
    connection.commit()
    cursor.execute("DELETE FROM moderationRequests")
    connection.commit()
    cursor.execute("DELETE FROM users")
    connection.commit()

def createSuperUser():
    #-----Database Connection------#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    #data for the user table
    groupList = []
    groupList = json.dumps(groupList)
    status = "SUPER USER"
    invitations = []
    invitations = json.dumps(invitations)
    blacklist = []
    blacklist = json.dumps(blacklist)
    whitelist = []
    whitelist = json.dumps(whitelist)
    inbox = []
    inbox = json.dumps(inbox)
    referredUsers = []
    referredUsers = json.dumps(referredUsers)

    rowData = []
    rowData.append("arun@gmail.com")
    rowData.append("Arun Ajay")
    rowData.append("test")
    rowData.append(groupList)
    rowData.append(500)
    rowData.append(status)
    rowData.append(invitations)
    rowData.append(blacklist)
    rowData.append(whitelist)
    rowData.append(0)
    rowData.append(inbox)
    rowData.append(referredUsers)
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
    connection.commit()
    connection.close()


def createSuperUser2():
    #-----Database Connection------#
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    #data for the user table
    groupList = []
    groupList = json.dumps(groupList)
    status = "SUPER USER"
    invitations = []
    invitations = json.dumps(invitations)
    blacklist = []
    blacklist = json.dumps(blacklist)
    whitelist = []
    whitelist = json.dumps(whitelist)
    inbox = []
    inbox = json.dumps(inbox)
    referredUsers = []
    referredUsers = json.dumps(referredUsers)

    rowData = []
    rowData.append("ajay@gmail.com")
    rowData.append("Arun Ajay")
    rowData.append("test")
    rowData.append(groupList)
    rowData.append(500)
    rowData.append(status)
    rowData.append(invitations)
    rowData.append(blacklist)
    rowData.append(whitelist)
    rowData.append(0)
    rowData.append(inbox)
    rowData.append(referredUsers)
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
    connection.commit()
    connection.close()

createDB()
clearAllTables()
createSuperUser()
createSuperUser2()
