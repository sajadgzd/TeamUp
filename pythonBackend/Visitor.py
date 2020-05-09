import sqlite3
import json
import requests
from flask import Flask, jsonify, render_template, request, send_from_directory



@app.route('/signup', methods = ["POST"])
def signUp(self):
    jsonData = requests.json
    #
    rowData = [] #Data to be uploaded to database
    rowData.append(jsonData["fullname"])
    rowData.append(jsonData["email"].lower())
    rowData.append(jsonData["interests"])
    rowData.append(jsonData["credentials"])
    rowData.append(jsonData["reference"])
    rowData.append("")
    rowData.append("PENDING")
     
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    found = []
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))
    for row in cursor.fetchall():
        found = list(row)
        break
    if len(found) != 0:
        connection.close()
        return (jsonify({
            "Message": "Sorry, an account with this email already exists. Please check your application status instead."
        }))
    else:
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(rowData))
        connection.commit()
    connection.close()
    #
    return (jsonify({
        "Message": "Thank you for registering! Your application is pending approval."
    }))

@app.route('/checkStatus', methods = ["POST"])
def checkStatus(self):
    jsonData = requests.json

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    found = []
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))
    for row in cursor.fetchall():
        found = row
        break
    connection.close()
    if len(found) != 0:
        if found[6] == "PENDING":
            return (jsonify({
                "Status" : "PENDING",
                "Message": "Your application is pending approval."
            }))
        elif found[6] == "USER":
            return (jsonify({
                "Status" : "USER",
                "Message": "Congratulations! Your account has been approved. Please sign in with the email and credentials you've provided."
            }))
        elif found[6] == "APPEALED":
            return (jsonify({
                "Status" : "APPEALED",
                "Message": "Your appeal is pending approval."
            }))
        elif found[6] == "BLACKLISTED":
            return (jsonify({
                "Status" : "BLACKLISTED",
                "Message": "You have been blacklisted from Team Up."
            }))
        elif found[6] == "REJECTED":
            return (jsonify({
                "Status" : "REJECTED",
                "Message": "Sorry, your application did not pass our first round of approval. Please write an appeal message telling us why you'd be a great fit for this community."
            }))
    return (jsonify({
        "Message": "Sorry, we couldn't find any users related to this email. Please sign up."
    }))


@app.route("/appealRejection", methods = ["POST"])
def appealRejection(self):
 
    jsonData = requests.json
    email = jsonData["email"].lower()
    appealMessage = jsonData["appealMessage"]
 
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(email,))
    row = list(cursor.fetchone())
 
    cursor.execute("DELETE * FROM signup WHERE [email] = ?", (email,))
    row[5] = appealMessage
    row[6] = "APPEALED"
    cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(row))
    connection.commit()
    connection.close()
    return (jsonify({"Success" : "appeal has been submitted."}))
        
