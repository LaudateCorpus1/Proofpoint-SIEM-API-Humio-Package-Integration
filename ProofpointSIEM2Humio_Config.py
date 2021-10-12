import logging


#Set Logging Level and file name
pfpt_log_level = logging.DEBUG
log_file = 'PFPT_SIEMapi2Humio.log'

#Code version - do not alter
pfpt_version = '1.0'

#####Proofpoint API Config Information
SIEM_API_url = 'https://tap-api-v2.proofpoint.com/v2/siem/all?format=json&sinceSeconds=3600'
SIEM_API_user_name = ''
SIEM_API_password = ''


#####Humio HEC configuration
Humio_base = ''
HumioHECurl = Humio_base+'/api/v1/ingest/hec/raw'
#sample full HEC URL = http://192.168.1.229:8080/api/v1/ingest/hec/raw

HumioHECContent_pfpt  = "{'Content-Type': 'application/json', 'Accept':'application/json'}"
HumioHECverify = False

#Humio HEC Token for Clicks Permitted events
HumioHECtoken_pfpt_ClicksPermitted = ''
#Humio HEC Token for Clicks Blocked events
HumioHECtoken_pfpt_ClicksBlocked = ''
#Humio HEC Token for Messages Delivered events
HumioHECtoken_pfpt_MessagesDelivered = ''
#Humio HEC Token for Messages Blocked events
HumioHECtoken_pfpt_MessagesBlocked = ''