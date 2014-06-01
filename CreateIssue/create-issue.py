#!/usr/bin/python

### --- A Python script which connects to JIRA REST API for creating issues and attaching .txt files --- ###

import datetime
import smtplib
import time
import glob
import os
#Checking for jira module to import
try:
    from jira.client import JIRA
except ImportError:
    print "This script requires jira module to work!"
    exit(1)

##Mail sender/receiver list:
sender = "jira@hostname.com" + os.uname()[1] 
receivers = ['user1@example.com, user2@example.com']

##send a mail:
def sendmail(status, msg):
    if status == "failed":
        message = "Subject: FAILED: <subject>" + "\n" +"To:"+ ','.join(receivers)  +"\n" + msg 
    else:
        message = "Subject: SUCCESS: <subject>" + "\n" +"To:"+ ','.join(receivers)  +"\n" + msg
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message)
    except:
        logger.error("Unable to send email")
        exit(1)


#Prepare summary for ticket
def prepSummary(ticket):
    issue_dict = {
                   'project': {'key': ticket},
                   'summary': "Ticket summary goes here",
                   'description': "Ticket description goes here...",
                   'issuetype':{'name': 'Ops Work Request'},
                   'components':[{"id": "10111"}],
    }
    #components entry can be dropped if not required.
    #To get the components and their id's: components = jira.project_components(issue_type)
    return issue_dict

#Connect to jira for authentication
def jiraConnect(user, pswd, host, issue):
    jira = JIRA(basic_auth=(user, pswd), options={'server': host})
    projects = jira.projects()
    for project in projects:
        if project.key == issue:
            issue_id = project.id
    if issue_id:
        tckt = prepSummary(issue)  
        #Creating ticket  
        new_issue = jira.create_issue(fields=tckt)
        print new_issue
        #Attaches the *.txt files under /tmp directory.
        filepath = "/tmp/*.txt"
        files =  glob.glob(filepath)
        if len(files)==0:
            sendmail("failed","Issue created, however file attaching failed")
            exit(1)
        else:
        for file in files:
            jira.add_attachment(new_issue,file)
            jira.add_comment(new_issue, 'Required files are Attached!')
        sendmail("success","Ticket has been created with the required evidence attached!")
        
#main def
def main():
    #server, user credentials 
    user_name  = 'user'
    user_pass  = 'passwd'
    server     = 'http://jiraexample.com:8080'
    issue_type = 'BUG'
    try:
        jiraConnect(user_name, user_pass, server, issue_type)
    except Exception, e:
        sendmail("failed", str(e))
        exit(1)
      
if __name__ == "__main__":
    main()

