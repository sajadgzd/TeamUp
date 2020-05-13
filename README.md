# TEAM UP
## Table of Contents 
1. [Overview](#overview)
2. [Technologies](#technologies)
3. [Local Installation](#installation)
4. [App ScreenShots](#display)

<a name="overview"></a>
## Overview 
Team Up is a Full Stack web application that will help users find team members to work on
altruistic projects together. The application will have a directory of groups that is
available to users, as well as a directory of registered users that can be used by
users to find team members for a given project.

<a name="technologies"></a>
## Technologies
 * HTML
 * CSS
    * Materialize
 * JavaScript
 * jQuery
     * Ajax calls
 * AOS.js animation library
 * Python
 * Flask
 * SQL Database

<a name="installation"></a>
## Local Installation
### Step 1: Git Clone
Clone the project to your local git repo like the following:
> git clone git@github.com:sajadgzd/softwareEngineeringProject.git

or

> git clone https://github.com/sajadgzd/softwareEngineeringProject.git

The Team Up project and its files should now be in your project folder.

### Step 2: Install Dependencies

Make sure you have **Python3** or above version installed on your system

> Here's a link to OS specific guide to installation of [Python3](https://realpython.com/installing-python/)




### Step 3: Set up SQL Database

1. Go to the root directory **/softwareEngineeringProject**

2. Run the following command in your terminal:


```python
python initializeDB.py
```


### Step 4: Launch the App 
Via terminal type in these bash command once you are in the Team Up root directory

```python
python server.py
```


Go to your browser and type in the corresponding address you see the app is running `http://localhost:5000` in your URL bar.

Now you should see the application open locally.

<a name="display"></a>
## App Screenshot samples
### Landing Page
<img src="/view/assets/images/landing.png">

### Signup Page
<img src="/view/assets/images/signup.png">

### Login Page
<img src="/view/assets/images/login.png">

### A sample screen shot of a user. In this case a Super User
<img src="/view/assets/images/su.png">

### Group page
<img src="/view/assets/images/gp.png">

### Sample feature. Creating a meetup schedule poll
<img src="/view/assets/images/gp2.png">

### Sample feature. Voting for a meetup schedule poll
<img src="/view/assets/images/gp3.png">

