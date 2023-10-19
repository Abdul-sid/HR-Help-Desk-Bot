# HR-Help-Desk-Bot

1. Introduction
2. Prerequisites
3. Jira Server/Cloud Configuration
4. Webex Setup
5. Webex Developer Configuration
6. Local API Setup/Configuration (Optional)
7. Python Environment Setup
8. Implementing the Integration
9. Code Description
10. Bot Deployment
11. Bot Interaction
12. Conclusion
13. References

## 1. Introduction
This technical document provides a step-by-step guide for integrating Jira Server/Cloud with Webex Cloud using REST APIs in Python. 
This integration empowers users to centralize their interactions with various cloud and server-based applications through the Webex platform. 
In this project, we focus on illustrating the integration of Webex with Jira, demonstrating its utility in tasks such as creating, updating, assigning, 
and approving Jira tickets. One of the uses of this integration is to allow employees to raise Jira tickets (for HR queries in this project) directly from Webex.

## 2. Prerequisites
Some requirements need to be fulfilled before starting this project which are mentioned below:

1. Jira Server/Cloud Configuration
2. Webex Setup
3. Webex Developer Configuration
4. Local API Configuration (Optional)
5. Python Environment Setup.
6. Code Editor (Optional)

**Note**: Will be using VS Code as a code editor for this project

## 3. Jira Server/Cloud Configuration
Jira comes in 2 variations which are mentioned below:
1. Jira Cloud
2. Jira Server

Both of the Jira variations configurations will be discussed in this documentation.

### 1. Jira Cloud
After creating a Jira Cloud account, the following steps need to be fulfilled:
* Log in to your Jira Cloud account.
* Go to 'Your profile' > 'Atlassian account' > 'Security'.
* Click on 'API token' and create a new token.
* Save the token securely; you'll need it in the Python script.

**User Email Address** & **API Token** are essential for Jira Cloud Integration.

### 2. Jira Server
The Jira server first needs to get installed on the server, once it is installed then it is essential to create a dedicated account 
for the integration. Once the account has been created then that account's **Username** & **Password** will be used for the integration.

## 4. Webex Setup
Webex accounts need to be created either after installing on the local machine or online on their [application](https://www.webex.com/).

## 5. Webex Developer Configuration
[Webex Developer Account](https://developer.webex.com/) is also required. Once an account has been created below steps need to be taken to create a bot:
1. Log in to the Webex Developer Account.
2. Hover/Click over/on the profile icon location at the upper right of the interface and then click on "My Webex Apps".
3. Click on "Create a New App".
4. Click on "Create a Bot".
5. Fill in the form and then click on the "Add bot" button.
6. Once the form has been submitted, make sure to save **Bot Access Token**, **Bot Name**, **Bot Username**, and **Bot ID**, as this information will be needed for integration.

## 6. Local API Setup/Configuration (Optional)
Although it's not required to set a local API, for this project we will be using local API. The purpose of this local API is to fetch employee data from a local database. 
API development is part of this project so not deep diving into this point.

## 7. Python Environment Setup
Upon installing Python, the below Python modules need to be installed:
1. requests
2. webexteamsbot
3. jira

These Python modules can be installed using the below commands in the terminal:
```bash
pip install requests
```
```bash
pip install webexteamsbot
```
```bash
pip install jira
```

Apart from the above-required modules, other necessary Python modules are not required to get installed as they come up with the Python installation itself.

## 8. Implementing the Integration

### Jira Integration
In the case of Jira Cloud:
* jira_user will be **User Email Address**
* jira_password will be **API Token**

In the case of the Jira Server:
* jira_user will be **Account Username**
* jira_password will be **Account Password**

```python
# Jira credentials for integration
jira_server = "<Server Link>"

jira_user = "<Jira User>"
jira_password = "<Jira Password>"

jira_server = {'server': jira_server}

jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))

issue_dict = "<Jira Payload>"

new_issue = jira.create_issue(fields=issue_dict)
```

### Local API Integration
Local API Integration will be as per need. In our case, we will be using API to fetch employee data from a local database.

```python
# API Credentials for Employee data fetching
username_api = "<username_api>"
password_api = "<password_api>"

headers_api = {
        "authorization": "<Authoriazation>"
    }

url_get_api = "<API Link>"
```

### Webex Bot Integration

```python
# Webex bot credentials
bot_email = "<Webex Bot Email>" Same as "Bot Email" from Webex Developer App
teams_token = "<Webex Bot Token>" # Same as "Bot Access Token" from Webex Developer App
bot_url = "<Webex Bot URL>" # URL on which bot is supposed to get deployed
bot_app_name = "<Webex Bot Name>" # Same as "Bot Name" from Webex Developer App

# If any of the bot environment variables are missing, terminate the app
if not bot_email or not teams_token or not bot_url or not bot_app_name:
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()

# Create a Bot Object
#   Note: debug mode prints out more details about processing to the terminal
#   Note: the `approved_users=approved_users` line was commented out and shown as a reference
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)
```

### Webex API Integration
Webex APIs consist of numerous endpoints, which can be used as per the developer's requirements. Below API integration is done using Webex "Messages" API Endpoint.

```python
headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + "<teams_token>",
    }

url = "https://webexapis.com/v1/messages" # API endpoints will be different as per requirement
data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
response = requests.post(url, json=data, headers=headers)
```

## 9. Code Description
The code consists of several blocks which will be discussed from the high level below. For further details person can check [Botcode.py](https://github.com/Abdul-sid/HR-Help-Desk-Bot/blob/main/Botcode.py) 
& [data.py](https://github.com/Abdul-sid/HR-Help-Desk-Bot/blob/main/data.py), as these 2 main files consist of comments which are describing each part of the code.

### 1. data.py
This Python file fetches data from the Jira project which will be fed dynamically in bot responses when the user interacts with the bot.
The only relevant part of this file is below, apart from this, further will be crafted as per business requirements.

```python
jira = JIRA(basic_auth=('<Username>', '<Password>'), options={'server': '<Jira Server Link>'})

# Expand fields to get the required data
metas = jira.createmeta(projectKeys='<Jira Project Key>', expand='projects.issuetypes.fields')

```

### 2. Botcode.py

### Necessary Imports
Below imports are required for the project.

```python
import requests
from webexteamsbot import TeamsBot
from importlib import reload
import sys
import json
from jira.client import JIRA
import os
import tempfile
```

### Integration Section
This consists of all the integration configurations with different platforms.

```python
# Jira credentials for integration
jira_server = "<Server Link>"

jira_user = "<Jira User>"
jira_password = "<Jira Password>"

jira_server = {'server': jira_server}

jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))

# API Credentials for Employee data fetching
username_api = "<username_api>"
password_api = "<password_api>"

headers_api = {
        "authorization": "<Authoriazation>"
    }

url_get_api = "<API Link>"

# Webex bot credentials
bot_email = "<Webex Bot Email>" 
teams_token = "<Webex Bot Token>"
bot_url = "<Webex Bot URL>"
bot_app_name = "<Webex Bot Name>"

# If any of the bot environment variables are missing, terminate the app
if not bot_email or not teams_token or not bot_url or not bot_app_name:
    if not bot_email:
        print("TEAMS_BOT_EMAIL")
    if not teams_token:
        print("TEAMS_BOT_TOKEN")
    if not bot_url:
        print("TEAMS_BOT_URL")
    if not bot_app_name:
        print("TEAMS_BOT_APP_NAME")
    sys.exit()

# Create a Bot Object
#   Note: debug mode prints out more details about processing to the terminal
#   Note: the `approved_users=approved_users` line was commented out and shown as a reference
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    # approved_users=approved_users,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},
    ],
)
```

### Input Form Webex Section
The first function **show_card** consist of below functionalities:
* Check whether the Jira server is up and running.
* It consists of code that first catches the Jira field which will be supplied from the data.py file,
and dynamically input in the adaptive card form (Input form for Webex).
* Send the adaptive card input form as a bot response to the user in reply to the user's query.
* In case of any error, error logs will be generated without stopping the server.
* Error notification for developer triggers from this function.

```python
def show_card(incoming_msg):

    try:

        # Only allow users to be with the Webex bot during one-to-one/direct conversation
        if incoming_msg.roomType == "group":

            return "Sorry, HR Helpdesk Team bot is not allowed to be interacted from group spaces. Kindly Reach the bot directly on webex"

        else:
.
.
.
.
.
    except:

        backupmsg = "Apologies, HRHD is not available at the moment \U0001F641 \U0001F635 \n Please try again later"

        r_id = incoming_msg["data"]["roomId"]
        url_thanks = "https://webexapis.com/v1/messages"
        data = {"roomId": r_id, "text": backupmsg, "markdown": backupmsg}
        requests.post(url_thanks, json=data, headers=headers)

        error_msg = "Error in Welcome Message Function - HRHD Error"
        error_notification_group(incoming_msg.personEmail, error_msg)

    return ""

```

### Webex Message API Section
Functions consist of a structure through which Webex API is supposed to be used.

```python
# Function used to send messages to the user
def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Function used to send messages to the user when there is some issue with the integration
def create_message_jira_or_webex_unavailable(rid, msgtxt):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/messages"
    data = {"roomId": rid, "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()
```

### Jira Error Notification Section
If there is an error in the main functions, an error notification will be triggered for developers for the rectification
along with the creation of a bug ticket on Jira with the assignee.

```python
# Function used to dispatch messages to process automation team Webex space along with Jira ticket creation for bug report
def error_notification_group(eid, error_hint):
    headers = {
            "content-type": "application/json; charset=utf-8",
            "authorization": "Bearer " + teams_token,
        }

    issue_dict = "<Jira Payload>"

    new_issue = jira.create_issue(fields=issue_dict)
    iss_link = "https://support.afiniti.com/browse/" + new_issue.key + "/"

    r_id = "<Room ID of process automation team>"
    url_thanks = "https://webexapis.com/v1/messages"
    data = {"roomId": r_id, "text": eid + " has submitted the ticket to 'HRHD Bot' but because of an application error ("+error_hint+") request cannot be processed. Kindly look into this issue. ==> " + iss_link, "markdown": eid + " has submitted the ticket to 'HRHD bot' but because of an application error ("+error_hint+") request cannot be processed. Kindly look into this issue. ==> " + iss_link}
    requests.post(url_thanks, json=data, headers=headers)

    r_id = "<Room ID of HR Help desk space>"
    url_thanks = "https://webexapis.com/v1/messages"
    data = {"roomId": r_id, "text": eid + " has submitted the ticket to 'HRHD Bot' but because of an application error, request cannot be processed. Kindly look into this issue.", "markdown": eid + " has submitted the ticket to 'HRHD bot' but because of an application error, request cannot be processed. Kindly look into this issue."}
    requests.post(url_thanks, json=data, headers=headers)
```

### Data Handling Post Input Form Section
Once the form is filled and input by the user, 2nd main function **handle_cards** comes into place
which have below functionalities:
* Catch the user input.
* Validate the input. In case of any issue with the data validation, bot will respond to the user for form resubmission with correctness.
* Check the local APIs and apply the relevant business rules and authentication on the user input.
* Create Jira tickets and assign them to the relevant person.
* This function can be enhanced not only to include all types of requests related to Jira but to other apps as well.

```python
# Function for handling data upon submitting the information
def handle_cards(api, incoming_msg):

    headers = {
    "content-type": "application/json; charset=utf-8",
    "authorization": "Bearer " + teams_token,
    }

    global msgtxt
    x = 0
    m = get_attachment_actions(incoming_msg["data"]["id"])

    with tempfile.TemporaryDirectory() as td:
        f_name = os.path.join(td, 'data.py')
        sys.path.append(td)
        import data
        reload(data)

.
.
.
.
            # Same ticket in HR group
            r_id = "<Room ID of user>"
            url_thanks = "https://webexapis.com/v1/messages"
            data = {"roomId": r_id, "text": "" + eid + " has submitted the ticket", "markdown": "" + eid + " has submitted the ticket"}
            requests.post(url_thanks, json=data, headers=headers)
        
            create_message_with_attachment(rid=r_id,
                                            msgtxt="Details of the ticket",
                                            attachment=json.loads(attachment, strict=False))

            # Below code is to delete the card once it is submitted by the user
            url_del = "https://webexapis.com/v1/messages/" + incoming_msg["data"]["messageId"]
            requests.delete(url=url_del, headers=headers, timeout=10)

    return ""
```

### Final Section
This section consists of server setup details such as **Port Number**.

```python
# Set the bot greeting.   
bot.set_greeting(show_card)
bot.add_command("attachmentActions", "*", handle_cards)

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port="<Port>")
```

# 10. Bot Deployment
This code can be deployed either on the cloud or on private servers. The only thing that need to be made sure
is that the IPs through which Webex Cloud will interact with this bot should be whitelisted in the server where the bot is deployed.

# 11. Bot Interaction
To interact with the bot, the user need to follow below steps:
1. Open Webex.
2. Type the "Bot Email" in the Webex search field situated at the top of the application.
3. Click on the **Blue Message** button.
4. Webex space will be generated.
5. Send a message in that space, bot will reply.

# 12 Conclusion
Although this integration is a simple one between Jira, Webex, and the local database. But it can be enhanced to include
other applications as well within the integrated framework.

# 13. References
Below are important references for this documentation:
* [Jira Cloud Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
* [Jira Server Documentation](https://docs.atlassian.com/software/jira/docs/api/REST/7.6.1/)
* [Webex App](https://www.webex.com/)
* [Webex Developer](https://developer.webex.com/)
* [Webex API Docs](https://developer.webex.com/docs)
* [Webexteamsbot - Python Module](https://github.com/hpreston/webexteamsbot)
* [Jira - Python Module](https://jira.readthedocs.io/)
* [Adaptive Cards Design](https://adaptivecards.io/designer/)
