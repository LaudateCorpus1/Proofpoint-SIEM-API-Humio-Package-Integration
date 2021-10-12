#!/usr/bin/env python

import requests
import logging
import sys

#local imports
import ProofpointSIEM2Humio_Config as config

class Send_to_HEC():

    def send_to_HEC(event_data, event_type, num_events):

        HumioHECurl = config.HumioHECurl
        HumioHECcontent = config.HumioHECContent_pfpt
        HumioHECverify = config.HumioHECverify
        log_level = config.pfpt_log_level

        version = config.pfpt_version
        logging.basicConfig(filename=config.log_file, filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)
        
        logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Sending data to Humio HEC')

        if event_type == 'ClicksPermitted':
            HumioHECtoken =config.HumioHECtoken_pfpt_ClicksPermitted
        
        elif event_type == 'ClicksBlocked':
            HumioHECtoken =config.HumioHECtoken_pfpt_ClicksBlocked

        elif event_type == 'MessagesDelivered':
            HumioHECtoken =config.HumioHECtoken_pfpt_MessagesDelivered
        
        elif event_type == 'MessagesBlocked':
            HumioHECtoken =config.HumioHECtoken_pfpt_MessagesBlocked


        try:
            header = {"Authorization": "Bearer " + HumioHECtoken, "Content-Type": HumioHECcontent} 
            r = requests.post(url=HumioHECurl, headers=header, json=event_data, verify=HumioHECverify, timeout=300)
            transmit_result = r.status_code
            logging.debug('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Transmission status code for data push to HEC= '+ str(transmit_result))
            logging.debug('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Transmission results for data push to HEC= '+ str(r.json))

        except requests.exceptions.RequestException as e:
            error=str(e)
            logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Unable to evaluate and transmit sensor_data event: Error: ' + error)
            try:
                sys.exit('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: This is fatal error, please review and correct the issue - CrowdStrike Intel Indicators to Humio is shutting down')
            except:
                pass

        logging.info('PFPTSIEM2Humio v' + version + ' ' +event_type +' HEC: Sent ' + num_events + ' ' + event_type + ' events to Humio for processing')
