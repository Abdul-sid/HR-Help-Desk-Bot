# -*- coding: utf-8 -*-
import requests
from webexteamsbot import TeamsBot
from importlib import reload
import sys
import json
from jira.client import JIRA
import os
import tempfile

# Jira credentials for integration
jira_server = "<Server Link>"

jira_user = "<Jira User>"
jira_password = "<Jira Password>"

# API Credentials for Employee data fetching
username_api = "<username_api>"
password_api = "<password_api>"

headers_api = {
        "authorization": "<Authoriazation>"
    }

url_get_api = "<API Link>"

jira_server = {'server': jira_server}
jira = JIRA(options=jira_server, basic_auth=(jira_user, jira_password))

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
#   Note: debug mode prints out more details about processing to terminal
#   Note: the `approved_users=approved_users` line commented out and shown as reference
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

def show_card(incoming_msg):

    try:

        # Only allow users to be with the webex bot during one to one/direct conversation
        if incoming_msg.roomType == "group":

            return "Sorry, HR Helpdesk Team bot is not allowed to be interacted from group spaces. Kindly Reach the bot directly on webex"

        else: 
            show_card.room = incoming_msg.roomId

            # Fetch data from data template and convert to json to be used in adaptive card
            with tempfile.TemporaryDirectory() as td:
                f_name = os.path.join(td, 'data.py')
                sys.path.append(td)  # make available for import
                import data

                reload(data)

            Request_Type = json.dumps(data.ReqT_valuesDic)
            show_card.Request_Type_sub = json.dumps(data.Fin_req_types)

            # Making sure Jira server is up and running
            test1 = 'https://support.afiniti.com'
            res1 = requests.get(test1, timeout=5)
            print(res1.status_code)
            print("https://support.afiniti.com => up and running")

            # Adaptive card design in form of JSON
            attachment = """
            {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Welcome to afiniti HR Helpdesk",
                    "wrap": true,
                    "weight": "Bolder"
                },
                { 
                    "type": "TextBlock",
                    "text": "To submit your query, please choose “Service Request” \\n then let us know the details.",
                    "wrap": true
                },
                {
                    "type": "ActionSet",
                    "actions": [
                        {
                            "type": "Action.ShowCard",
                            "title": "Service Request",
                            "card": {
                                "type": "AdaptiveCard",
                                "body": [
                                    {
                                        "type": "TextBlock",
                                        "text": "(*) Means mandatory",
                                        "weight": "Bolder"
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Request Type (*)",
                                        "weight": "Bolder"
                                    },
                                    {
                                        "type": "Input.ChoiceSet",
                                        "id": "Req Values",
                                        "isMultiSelect": false,
                                        "value": "1",
                                        "isRequired": true,
                                        "choices": """ + Request_Type + """
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Summary of your request (*)",
                                        "weight": "Bolder"
                                    },
                                    {
                                        "type": "Input.Text",
                                        "id": "Summary",
                                        "placeholder": "Summary",
                                        "maxLength": 250,
                                        "isMultiline": true
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Description of your request",
                                        "weight": "Bolder"
                                    },
                                    {
                                        "type": "Input.Text",
                                        "id": "Description",
                                        "placeholder": "Description",
                                        "maxLength": 250,
                                        "isMultiline": true
                                    }
                                ],
                                "actions": [
                                    {
                                        "type": "Action.Submit",
                                        "title": "Submit"
                                    }
                                ]
                            }
                        },
                        {
                            "type": "Action.OpenUrl",
                            "title": "Guide",
                            "url": "https://www.dropbox.com/s/nrn8758684cyxig/HR%20HELPDESK%20BOT%20-%20User%20Guide.pptx?dl=0"
                        }
                    ]
                }
            ],
            "type": "AdaptiveCard",
            "version": "1.1"
            }
            }
            """
            backupmessage = "Adaptive Card"

            # Attachement dispatchement back to user
            c = create_message_with_attachment(
                incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(attachment)
            )
            print(c)

    # If the above code couldn't able to run the "except" block will run and respond back to user about the bot unavailability
    except:

        backupmsg = "Apologies, HRHD is not available at the moment \U0001F641 \U0001F635 \n Please try again later"

        r_id = incoming_msg["data"]["roomId"]
        url_thanks = "https://webexapis.com/v1/messages"
        data = {"roomId": r_id, "text": backupmsg, "markdown": backupmsg}
        requests.post(url_thanks, json=data, headers=headers)

        error_msg = "Error in Welcome Message Function - HRHD Error"
        error_notification_group(incoming_msg.personEmail, error_msg)

    return ""

# Function used to send messages to user
def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Function used to send messages to user when there is some issue with the integeration
def create_message_jira_or_webex_unavailable(rid, msgtxt):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://webexapis.com/v1/messages"
    data = {"roomId": rid, "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Function used to dispatch messages to process automation team webex space along with jira ticket creation for bug report
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

    Request_Type_sub = json.dumps(data.Fin_req_types[m["inputs"]['Req Values'].strip()])
    
    # Get Person ID to respond accordingly
    url_pi = "https://webexapis.com/v1/people/" + incoming_msg["data"]["personId"]
    email_i = requests.get(url=url_pi, headers=headers, timeout=10)
    e_i = email_i.json()

    # Get room type to respond accordingly
    url_rt_adp = "https://webexapis.com/v1/rooms/" + incoming_msg["data"]["roomId"]
    rt_adp = requests.get(url=url_rt_adp, headers=headers, timeout=10)
    r_adp = rt_adp.json()
    radp = r_adp["type"]

    # Get email id of the user and then convert list to str eid
    email_adp = e_i["emails"]
    eid = ' '.join(map(str, email_adp))
    id = eid.split("@")[0]

    summ = str(m["inputs"]['Summary'])

    # Make sure the essential input is available
    if 'Summary' not in m["inputs"]:
        Summary = ""
    else:
        Summary = str(m["inputs"]['Summary']).strip()
    if 'Description' not in m["inputs"]:
        Description = ""
    else:
        Description = str(m["inputs"]['Description']).strip()

    
    if Summary == "":
        msgtxt = "Sorry, we didn't catch the: **Summary**\U0001F446 \nPlease fill it in and submit your request again. Thanks \U0001F642"

    # send msg that a required field has been missed
        r_id = incoming_msg["data"]["roomId"]
        url_missing_field = "https://webexapis.com/v1/messages"
        data = {"roomId": r_id, "text": msgtxt, "markdown": msgtxt}
        requests.post(url_missing_field, json=data, headers=headers)

        return ""

    else:

    # In case if any further list of question available which requires input
        if Request_Type_sub[12:14] != "NA" and 'input1' not in m["inputs"]:
            
            attachment = """
            {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Can you please select the location benefit ? (*)",
                    "wrap": true,
                    "weight": "Bolder"
                },
                {
                    "type": "Input.ChoiceSet",
                    "id": "input1",
                    "style": "compact",
                    "isMultiSelect": false,
                    "label": "Benefits Types",
                    "isRequired": true,
                    "choices": """ + Request_Type_sub + """
                }
            ],
            "actions": [
                {
                "type": "Action.Submit",
                "title": "Submit",
                "data": {
                    "Description": " """ + Description.strip().replace("\n", " ") + """ ",
                    "Summary": " """ + Summary.strip().replace("\n", " ") + """ ",
                    "Req Values": " """ + m["inputs"]['Req Values'] + """ "
                }
                }
            ],
            "type": "AdaptiveCard",
            "version": "1.1"
            }
            }
            """

            backupmessage = "Adaptive Card"

            c = create_message_with_attachment(
                show_card.room, msgtxt=backupmessage, attachment=json.loads(attachment)
            )
            print(c)

            url_del = "https://webexapis.com/v1/messages/" + incoming_msg["data"]["messageId"]
            requests.delete(url=url_del, headers=headers, timeout=10)
    
        else:

            # If no further input is require to process
            msgtxt = "HRHD bot has received your request. Kindly give a little time to process it. \U0001F642" 

            # Check whether user is available on jira or not
            userStatus = requests.get("<Jira server API link to check user>"+id, auth=("Username", "Password"), timeout = 10)

            if userStatus.status_code == 200:
                note = "N/A"  

            else:
                note = "The person submitted the ticket does not have Jira account till yet, kindly approach directly using WebEx or Email"                

            # Fetch employee details from API
            fin_api = url_get_api+eid
            res = requests.get(fin_api, auth=(username_api, password_api), headers=headers_api, timeout = 10)

            r_id = incoming_msg["data"]["roomId"]
            url_thanks = "https://webexapis.com/v1/messages"
            data = {"roomId": r_id, "text": msgtxt, "markdown": msgtxt}
            requests.post(url_thanks, json=data, headers=headers)

            # Different Jira API load as per the scenario
            if 'input1' in m["inputs"]:
                benefit_type = m["inputs"]["input1"]

                try:

                    issue_dict = "<Jira Payload 1>"

                except:

                    issue_dict = "<Jira Payload 1>"

            else:
                benefit_type = "NA"

                try:

                    issue_dict = "<Jira Payload 2>"

                except:

                    issue_dict = "<Jira Payload 2>"

            # Jira ticker creation via API
            new_issue = jira.create_issue(fields=issue_dict)
            key = new_issue.key
            iss_link = "https://support.afiniti.com/browse" + key + "/"

            # Adaptive card designs for confirmation of ticket creation along with the information
            attachment = """
                        {
                            "contentType": "application/vnd.microsoft.card.adaptive",
                            "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "The ticket has been created, with the following details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Lighter"
                        },
                        {
                            "type": "TextBlock",
                            "text": "(""" + key + """) """""" ||  """ + Summary.strip().replace("\n", " ") + """",
                            "wrap": true,
                            "spacing": "Large",
                            "size": "Medium",
                            "weight": "Bolder",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Request: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  "Service Request",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Request Type: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + m["inputs"]["Req Values"] + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Benefits Type: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + benefit_type + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Employee contact details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + eid + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Additional Details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ "Country: "+ str(res.json()['country']) + " | Employee Code: " + str(res.json()['employeeCode']) + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text":  "Note: """ + note + """ ",
                            "wrap": true
                        },
                            {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.OpenUrl",
                                    "title": "Ticket Details",
                                    "url": "https://support.afiniti.com/browse/""" + key + """",
                                    "style": "positive"
                                }
                            ]
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2"
                    }
                        }
                        """

            attachment1 = """
                        {
                            "contentType": "application/vnd.microsoft.card.adaptive",
                            "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "The ticket has been created, with the following details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Lighter"
                        },
                        {
                            "type": "TextBlock",
                            "text": "(""" + key + """) """""" ||  """ + Summary.strip().replace("\n", " ") + """",
                            "wrap": true,
                            "spacing": "Large",
                            "size": "Medium",
                            "weight": "Bolder",
                            "color": "Accent"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Request: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  "Service Request",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Request Type: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + m["inputs"]["Req Values"] + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Benefits Type: ",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + benefit_type + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Your contact details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ + eid + """ ",
                            "wrap": true
                        },
                        {
                            "type": "TextBlock",
                            "text": "Additional Details:",
                            "wrap": true,
                            "spacing": "Small",
                            "weight": "Bolder"
                        },
                        {
                            "type": "TextBlock",
                            "text":  " """ "Country: "+ str(res.json()['country']) + " | Employee Code: " + str(res.json()['employeeCode']) + """ ",
                            "wrap": true
                        },
                            {
                            "type": "ActionSet",
                            "actions": [
                                {
                                    "type": "Action.OpenUrl",
                                    "title": "Ticket Details",
                                    "url": "https://support.afiniti.com/browse/""" + key + """",
                                    "style": "positive"
                                }
                            ]
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.2"
                    }
                        }
                        """

            headers = {
                "content-type": "application/json; charset=utf-8",
                "authorization": "Bearer " + teams_token,
            }

            if radp == "group":
                msgtxt = "Thank you <@personEmail:" + eid + "> HR Helpdesk team has received your request. Thank you! \U0001F642 \n To recap, here's the information you shared: \U0001F3AB"
            if radp == "direct":
                msgtxt = "HR Helpdesk team has received your request. Thank you! \U0001F642 \n. To recap, here's the information you shared: \U0001F3AB"

            # Post the Thankyou msg
            r_id = incoming_msg["data"]["roomId"]
            url_thanks = "https://webexapis.com/v1/messages"
            data = {"roomId": r_id, "text": msgtxt, "markdown": msgtxt}
            requests.post(url_thanks, json=data, headers=headers)
        
            create_message_with_attachment(rid=r_id,
                                            msgtxt="Details of the ticket",
                                            attachment=json.loads(attachment1, strict=False))

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


# Temporary function to get card attachment actions (not yet supported
# by webexteamssdk, but there are open PRs to add this functionality)
def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }
    url = "https://webexapis.com/v1/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers, timeout=(10, 10))

    return response.json()


# An example using a Response object.  Response objects allow more complex
# replies including sending files, html, markdown, or text. Rsponse objects
# can also set a roomId to send response to a different room from where
# incoming message was received.

# Set the bot greeting.   
bot.set_greeting(show_card)
bot.add_command("attachmentActions", "*", handle_cards)

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port="<Port>")
