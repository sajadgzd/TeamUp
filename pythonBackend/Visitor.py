import sqlite3
import json
from flask import Flask, jsonify, render_template, request, send_from_directory



@app.route('/signup', methods = ["POST"])
def signUp():
    jsonData = request.json
    #
    rowData = [] #Data to be uploaded to database
    rowData.append(jsonData["fullname"])
    rowData.append(jsonData["email"].lower())
    rowData.append(jsonData["interests"])
    rowData.append(jsonData["credentials"])
    rowData.append(jsonData["reference"].lower())
    rowData.append("")                      # appeal (does not exist on initial sign up)
    rowData.append("PENDING")
     
    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))

    userData = cursor.fetchone()

    cursor.execute("SELECT * FROM users WHERE [email] = ?",(jsonData["reference"].lower(),))
    referrerData = cursor.fetchone()

    if userData is not None:
        connection.close()
        return (jsonify({
            "Message": "Sorry, an account with this email already exists. Please check your application status instead."
        }))

    elif referrerData is None:
        connection.close()
        return jsonify({
            "Message": "Sorry, the referrer you have entered does not exist in the system."
        })
        
    else:
        cursor.execute("INSERT INTO signup (fullname,email,interests,credentials,reference,appeal,status) VALUES(?,?,?,?,?,?,?)",tuple(rowData))

        # add new user to inviter's list of referred users
        referrerData = list(referrerData)
        referredUserList = json.loads(referrerData[11])
        referredUserList.append(jsonData["email"].lower())
        referrerData[11] = json.dumps(referredUserList)
        cursor.execute("DELETE FROM users WHERE [email] = ?", (referrerData[0]))
        cursor.execute("INSERT INTO users (email,fullname,password,groupList,reputationScore,status,invitations,blacklist,whitelist,compliments,inbox,referredUsers) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",tuple(referrerData))
        connection.commit()
        connection.close()
    #
    return (jsonify({
        "Message": "Thank you for registering! Your application is pending approval."
    }))

@app.route('/checkStatus', methods = ["POST"])
def checkStatus():
    jsonData = request.json

    connection = sqlite3.connect(r"./database.db")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM signup WHERE [email] = ?",(jsonData["email"].lower(),))
    userData = cursor.fetchone()
    connection.close()
    if userData is not None:
        if userData[6] == "PENDING":
            return (jsonify({
                "Status" : "PENDING",
                "Message": "Your application is pending approval."
            }))
        elif userData[6] == "USER":
            return (jsonify({
                "Status" : "USER",
                "Message": "Congratulations! Your account has been approved. Please sign in with the email and credentials you've provided."
            }))
        elif userData[6] == "APPEALED":
            return (jsonify({
                "Status" : "APPEALED",
                "Message": "Your appeal is pending approval."
            }))
        elif userData[6] == "BLACKLISTED":
            return (jsonify({
                "Status" : "BLACKLISTED",
                "Message": "You have been blacklisted from Team Up."
            }))
        elif userData[6] == "REJECTED":
            return (jsonify({
                "Status" : "REJECTED",
                "Message": "Sorry, your application did not pass our first round of approval. Please write an appeal message telling us why you'd be a great fit for this community."
            }))
    return (jsonify({
        "Message": "Sorry, we couldn't find any users related to this email. Please sign up."
    }))


@app.route("/appealRejection", methods = ["POST"])
def appealRejection():
 
    jsonData = request.json
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

    # add appeal to SU moderation queue
    cursor.execute("INSERT INTO moderationRequests (subject,message,type,status,number) VALUES(?,?,?,?,?)",(email,appealMessage,"SIGNUP_APPEAL","OPEN",None))

    connection.commit()
    connection.close()
    return (jsonify({"Success" : "appeal has been submitted."}))
        
