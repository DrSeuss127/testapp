import requests
import json
import subprocess

"""
PARAMETERS:
    SEVERITY_THRESHOLD: Type of severity threshold to fail the jenkins build [Low, Medium, High, Critical]
    AGE: Number of preceding days to be considered for evaluation 
        (Ex. If set to "1", will retrieve the scans, today and yesterday)
    FAIL_JOB: Boolean Flag for deciding whether to fail the Job or not (Defaults to False)
    ACTIVE: Will only retrieve Active Findings if set to 'True'
    URL: URL endpoint of the findings configuration API (<defect_dojo_host_name>/api/v2/findings)
    HEADERS: Additional Args needed to send GET request from Defect Dojo
""" 

SEVERITY_THRESHOLD = 'Critical'
AGE = 7 
FAIL_JOB = False
ACTIVE = True
URL = 'https://defectdojo.aws.devops.com.ph/api/v2/findings'
HEADERS = {'content-type': 'application/json',
            'Authorization': 'Token 10498fe57df09d7cf800601657ac931a366b31b2'}

def get_findings(url, headers):
    """
    Sends API GET requests to defect dojo findings endpoint
    """
    r = requests.get(url, headers=headers, verify=True) # set verify to False if ssl cert is self-signed
    content = r.__dict__
    bytes = content["_content"]

    # Deserialize the bytes object into a dictionary
    return json.loads(bytes.decode())

def evaluate_severity(findings_dictionary=None):
    """
    Returns True if one of the results reached the SEVERITY_THRESHOLD
    """

    for res in findings_dictionary['results']:
        if (res['age'] <= AGE) and (res['active'] == ACTIVE):
            if res['severity'] == SEVERITY_THRESHOLD:
                
                print("\n****************************************")
                print(f"{SEVERITY_THRESHOLD} Severity Found!!! Aborting..." )
                print(res['description'])
                print("****************************************\n")

                return True

def fail_jenkins_stage(FAIL_JOB):
    if FAIL_JOB:

        # Run the Bash script to exit the stage
        result = subprocess.run('exit 1', check=True, shell=True)

        # Check the return code of the script to see if it was successful
        if result.returncode == 0:
            print("Script ran successfully")
        else:
            print("Script failed with return code", result.returncode)
            print(result.stderr.decode())
    else: 
        print(f"No {SEVERITY_THRESHOLD} Severity Found")


# --------- Start here ---------
findings_dictionary = get_findings(URL, HEADERS)
FAIL_JOB = evaluate_severity(findings_dictionary=findings_dictionary)
fail_jenkins_stage(FAIL_JOB=FAIL_JOB)

