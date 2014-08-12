Atlassian-scripts
============

A collection of JIRA, BAMBOO and CONFLUENCE python scripts.


**JIRA**:
==============================================================

1. create_issue.py :-
==============================================================
*For creating a issue and attaching file(s) to it*
- You need to install "jira" module for this script to work. -> `pip install jira`
- Make sure to change the user credentials and jira hostname in the script.
- Attaches *.txt file under /tmp directory of current host, change this to match your requirement.
- Script it working fine(Need some tweaking though), please feel free to send pull requests if you have any suggestions. 


**Coming soon:**

**BAMBOO**:
==============================================================

1. BambooRestAPIClient:-
==============================================================
- You need to install "requests" module for this script to work. -> `pip install requests`
- Make sure to change the user credentails and bamboo hostname in the script.
- Creates a new session everytime the script is executed, It can print the projects, plans, build on Bamboo. 
- Tested on Python 2.7
- You can google for available APIs which Bamboo provides.
