import requests
import json
import sys


####################################################################
####################### Configuration File  ########################

host = '10.40.0.17'
port = '8080'
user='admin'
passcode='CyberPWN@123'
viewname='High Impact Outstanding'
isSSL = False
viewtype='issues'
projectname = 'dvja-master'
bPasswordString = True
# Possible values can be ["High", "Medium","Low"]
ImpactVal = ["High","Medium"]

#Checker List 
Confidential_Checker = ["CONFIG.CONNECTION_STRING_PASSWORD","CONFIG.SPRING_SECURITY_HARDCODED_CREDENTIALS"
,"CONFIG.SPRING_SECURITY_REMEMBER_ME_HARDCODED_KEY"
,"DC.WEAK_CRYPTO","HARDCODED_CREDENTIALS","INSECURE_RANDOM","PREDICTABLE_RANDOM_SEED"
,"RISKY_CRYPTO","SENSITIVE_DATA_LEAK","UNENCRYPTED_SENSITIVE_DATA","WEAK_GUARD","WEAK_PASSWORD_HASH"]

####################################################################
####################################################################
#Do not Change anything below this point.

def makeURL():
    http_url = 'http'
    if (isSSL):
       http_url += 's'
    http_url += '://' + host + ':' + port
    return http_url

def getProjectData():
    try:
        projectname = sys.argv[1]
        print(projectname)
    except Exception as e:
        print (e)
        print("Please provide valid project name")
        exit(1)
    url=makeURL()+'/api/viewContents/projects/v1/All%20Projects?projectId=' + projectname
    r = requests.get(url,auth=(user,passcode),verify=False)
    if(r.ok):
        print("Fetching details for project >> {0}".format(projectname))
        try:
            lines=getViewContentsCSV(viewtype,viewname,projectname)
            for line in lines:
                data = json.loads(line)
                viewList= data['viewContentsV1']['rows']
                print("Number of rows found {0}".format(len(viewList)))
                #print(viewList)
                if len(viewList):
                    if len(ImpactVal):
                        checkForHighImpact(viewList)
                    if bPasswordString:
                        checkForPasswordString(viewList)
        except Exception as e:
            print(e)
            exit(1)
    else:
        r.raise_for_status()

def getViewContentsCSV(vtype, view, project):
    rtext=[]
    url=makeURL()+'/api/viewContents/'+vtype+'/v1/'+view.replace(" ", "%20")+'?projectId='+project+'&rowCount=-1' 
    r = requests.get(url, auth=(user,passcode), verify=False) 
    if(r.ok):
        rtext=r.text.splitlines()
        print("URL used {0}".format(url))
    else:
        r.raise_for_status()
    return rtext

def checkForHighImpact(viewList):
    print("checkForHighImpact")
    for viewRows in viewList:
        if viewRows["displayImpact"] in ImpactVal:
            print(viewRows["displayImpact"])
            raise ValueError('High impact issue found ')  
            #exit(1)
            
def checkForPasswordString(viewList):
    print("checkForPasswordString")
    for viewRows in viewList:
        if viewRows["checker"] in Confidential_Checker:
            print(viewRows["checker"])
            raise ValueError('Restricted Checker found ') 
    

if __name__ == "__main__":
    print("started")
    getProjectData()
    print("done")


