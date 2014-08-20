#!/usr/bin/python

from __future__ import print_function
import sys
import getpass

#Trying to import simplejson first, if not json.
try:
    import simplejson as json
except ImportError:
    import json

#using requests module to handle cookies automatically!
try:
    import requests
except ImportError:
    print("ImportError: This script requires 'requests' moduel to work!")
    sys.exit(1)

class Bclient(object):
    """ Class used for accessing Bamboo REST API """

    def __init__(self, url, user, passwd):
        """ Accepts Bamboo REST API URL, user credentials """
        self.url    = url.rstrip("/")
        self.user   = user
        self.passwd = passwd
 
    def authenticate(self):
        """ Authenticates against Bamboo REST API using provided credentials """
        s   = requests.Session()
        res = s.get(self.url+"/plan?os_authType=basic", auth=(self.user, self.passwd))
        if res.status_code == 200:
            print("INFO: Authentication Successful! \n")
        else:
            print("ERROR: Authentication Failed!")
            sys.exit(1)
        return s
        
    def lsProjects(self, s):
        """ Prints the list of projects on Bamboo """
        projects   = json.loads(s.get(self.url + "/project.json").text)
        ps = {}
        for project in projects['projects']['project']:
            ps["project['name']"] = "project['key']" + "project['link']['href']"
            print("%-35s %-15s %55s" % (project['name'], project['key'], project['link']['href']))
        print("\n")
    
    def buildInfo(self, s):
        """ Prints the build info """
        info = json.loads(s.get(self.url + "/info.json").text)
        print("Build Date: ",info["buildDate"])
        print("Build Number: ", info["buildNumber"])
        print("Build Status:", info["state"])
        print("\n")
 
    def currentUser(self, s):
        """ Prints the current user info """
        user = json.loads(s.get(self.url + "/currentUser.json").text)
        print("UserName: ", user["name"])
        print("Full Name: ", user["fullName"])
        print("Email-ID: ", user["email"])
        print("\n")
    
    def resultInfo(self, s):
        """ List latest builds for all plans on Bamboo """
        result = json.loads(s.get(self.url + "/result.json").text)
        for plan in result['results']['result']:
            print("Plan Name: ", plan["plan"]["name"])
            print("Enabled: ", plan["plan"]["enabled"])
            print("ID: ", plan["id"])
            print("Type: ", plan["plan"]["type"])
            print("Key: ", plan["plan"]["key"])
            print("Short Name: ", plan["plan"]["shortName"])
            print("Short Key: ", plan["plan"]["shortKey"])
            print("Plan Result Number/key: ", plan["plan"]["shortKey"])
            print("State: ", plan["state"])
            print("Link: ", plan["link"]["href"])
            print("LifeCycle State: ", plan["lifeCycleState"])
            print("\n")

    def deployProjects(self,s):
        """ List all deployment projects """
        dps = json.loads(s.get(self.url + "/deploy/dashboard").text)
        dp_dict = {}
        for dp in dps:
            for env in dp["environmentStatuses"]:
                #Making sure it is of prod. Environment and successfully deployed.
                if env["environment"]["name"].lower() == "prod" and env["deploymentResult"]["deploymentState"].lower() == "success":
                    dp_dict[dp["deploymentProject"]["id"]] = []
                    dp_dict[dp["deploymentProject"]["id"]].append(dp["deploymentProject"]["name"])
                    dp_dict[dp["deploymentProject"]["id"]].append(epochtoDate(env["deploymentResult"]["finishedDate"]))
        return dp_dict


         
    def closeconn(self, s):
        """ Closes the Session """
        s.close()

if __name__ == '__main__':
    user = raw_input("User-name: ")
    pswd = getpass.getpass()
    rcl = Bclient("http://<Bamboo hostname>:8085/rest/api/latest/", user, pswd )
    session = rcl.authenticate()
    rcl.lsProjects(session)
    #rcl.currentUser(session)
    rcl.buildInfo(session)
    rcl.resultInfo(session)
    #Checking for successful deployments
    print rcl.deployProjects(session)
    rcl.closeconn(session)
