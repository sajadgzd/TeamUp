import sqlite3
from flask import Flask, jsonify, render_template, request, send_from_directory
import json

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
    compliments = []
    compliments = json.dumps(compliments)
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
    rowData.append(compliments)
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
    compliments = []
    compliments = json.dumps(compliments)
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
    rowData.append(compliments)
    rowData.append(inbox)
    rowData.append(referredUsers)
    cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",tuple(rowData))
    connection.commit()
    connection.close()


clearAllTables()
createSuperUser()
createSuperUser2()
