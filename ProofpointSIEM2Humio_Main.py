#!/usr/bin/env python

#python imports
import requests
import base64
import logging
import sys

#local imports
import ProofpointSIEM2Humio_Config as config
from Send2HumioHEC import Send_to_HEC as humio

class PFPT_SIEM_2_Humio():

    def get_PFPT_SIEM(self):

        #get version from config file and configure logging
        version = config.pfpt_version
        log_level = config.pfpt_log_level
        logging.basicConfig(filename=config.log_file, filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)

        logging.info('PFPTSIEM2Humio v' + version + ' : Starting data collection process')
        
        #construct API call
        logging.info('PFPTSIEM2Humio v' + version + ' : Constructing API call')
        userAndPass = config.SIEM_API_user_name + ':' + config.SIEM_API_password
        b64val = base64.b64encode(userAndPass.encode()).decode()
        headers = {'Authorization' : 'Basic %s' %  b64val}
        payload = {}

        #attempt to contact PFPT SIEM API
        logging.info('PFPTSIEM2Humio v' + version + ' : Making API call to Proofpoint SIEM API')
        try: 
            response = requests.get(config.SIEM_API_url, headers=headers, data=payload)
            response_code = str(response.status_code)
            pfpt_response = response.json()
            logging.info('PFPTSIEM2Humio v' + version + ' : Call to the Proofpoint SIEM API response code was = ' + response_code)
        
        except Exception as e:
            logging.info('PFPTSIEM2Humio v' + version + ' : Call to the Proofpoint SIEM API response code was = ' + response_code)
            logging.error('PFPTSIEM2Humio v' + version + ' : Error contacting the Proofpoint SIEM API = ' + e.message + '  ' + e.args)
            sys.exit('PFPTSIEM2Humio v' + version + ' : Unable to collect Proofpoint data, please correct any issues and try again')


        pfpt_clicksPermitted = pfpt_response['clicksPermitted']  
        pfpt_clicksBlocked = pfpt_response['clicksBlocked']
        pfpt_messagesDelivered = pfpt_response['messagesDelivered']
        pfpt_messagesBlocked = pfpt_response['messagesBlocked'] 

        #evaluate and send clicks permitted events
        if len(pfpt_clicksPermitted) > 0:
            num_cp = str(len(pfpt_clicksPermitted))
            logging.info('PFPTSIEM2Humio v' + version + ' : Preparing to send ' + num_cp + ' ClicksPermitted Events to Humio')
            for cp in pfpt_clicksPermitted:
                event_type = 'ClicksPermitted'
                humio.send_to_HEC(cp, event_type)

        #evaluate and send clicks blocker events
        if len(pfpt_clicksBlocked) > 0:
            num_cb = str(len(pfpt_clicksBlocked))
            logging.info('PFPTSIEM2Humio v' + version + ' : Preparing to send ' + num_cb + ' ClicksBlocked Events to Humio')
            for cb in pfpt_clicksBlocked:
                event_type = 'ClicksBlocked'
                humio.send_to_HEC(cb, event_type, num_cb)

        #evaluate and send messagesDelivered events
        if len(pfpt_messagesDelivered) > 0:
            num_md = str(len(pfpt_messagesDelivered))
            logging.info('PFPTSIEM2Humio v' + version + ' : Preparing to send ' + num_md + ' MessagesDelivered Events to Humio')
            for md in pfpt_messagesDelivered:
                event_type = 'MessagesDelivered'
                humio.send_to_HEC(md, event_type, num_md)

        #evaluate and send messagesBlocked events
        if len(pfpt_messagesBlocked) > 0:
            num_mb = str(len(pfpt_messagesBlocked))
            logging.info('PFPTSIEM2Humio v' + version + ' : Preparing to send ' + num_mb + ' MessagesBlocked Events to Humio')
            for mb in pfpt_messagesBlocked:
                event_type = 'MessagesBlocked'
                humio.send_to_HEC(mb, event_type, num_mb)

pfpt=PFPT_SIEM_2_Humio()
pfpt.get_PFPT_SIEM()