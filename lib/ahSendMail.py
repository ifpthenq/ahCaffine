from exchangelib import Credentials, Account
import keyring
import keyring.util.platform_ as keyring_platform
import logging
from lib import logs
import sys
from lib.ahConfig import ahConfig
from exchangelib import Message, Mailbox, FileAttachment, DELEGATE, Configuration
from exchangelib import HTMLBody


log = logging.getLogger('lib.logs.' + __name__)
log.info("== Loaded SendMail ==")
config = ahConfig()
cfg = config.get_config_section('config')
NAMESPACE = cfg['namespace']
ENTRY = cfg['entry']
cred = keyring.get_credential(NAMESPACE, ENTRY)
try:
    credentialname = cfg['credentialname']
    emailname = cfg['emailname']
except KeyError as e:
    log.critical("Unable to set credentialname or emailname from config.txt")
    sys.exit()
except Exception as e:
    log.critical("Unable to set values from config.txt for some other reason")
    sys.exit()

def sendNotifications(e):
    log.critical(e)
    
    try:
        alertList = cfg['alertlist'].split(',')
        automationname = cfg['automationname']
        scheduledtask = cfg['scheduledtask']
    except KeyError as e:
        log.critical("Unable to set alertlist, automationname, scheduledtask from config.txt")
        sys.exit()
    except Exception as e:
        log.critical("Unable to set values from config.txt in sendNotifications() for some other reason")
        sys.exit()
    
    try:
        password = cred.password
    except Exception as e:
        log.critical("Was not able to send notification email after error because I was unable to retrieve the password for the mail account")
        sys.exit("No password retrieved in sendNotifications. Exiting")
    
    try:
        credentials = Credentials(credentialname, password)
        
        account = Account(emailname, credentials=credentials, autodiscover=True)
        log.info("Successfully connected to email account to send notifications")
    except Exception as e:
        log.critical("Was not able to connecto to Exchange account to send notifications")
        sys.exit()
    
    body = HTMLBody('''
        <html>
            <body>
                <h2 style='color:red;'>
                    An automation has thrown a terminal error:
                </h2>
                <br>
                <ul>
                    <li> Automation Name : {}
                    <li> Scheduled Task : {}
                    <li> Error: {}
                </ul>
                
                To troubleshoot this error, find the automation on SRHC-RPA, 
                and review the logs in the logs folder. <br><br>
                
                The process may need be handeld manually until the error can be fixed.
                
            </body>
        </html>
    '''.format(automationname, scheduledtask, e))
    
    subject = "Error for automation: {}".format(automationname)
    
    m = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=body,
        to_recipients=alertList
    )
    
    m.send_and_save()
    
    log.info("sent notification alert")
    
def sendConfirmation1(htmlText):
    
    
    try:
        alertList = cfg['alertlist'].split(',')
        automationname = cfg['automationname']
        scheduledtask = cfg['scheduledtask']
    except KeyError as e:
        log.critical("Unable to set alertlist, automationname, scheduledtask from config.txt")
        sys.exit()
    except Exception as e:
        log.critical("Unable to set values from config.txt in sendNotifications() for some other reason")
        sys.exit()
    
    try:
        password = cred.password
    except Exception as e:
        log.critical("Was not able to send notification email after error because I was unable to retrieve the password for the mail account")
        sys.exit("No password retrieved in sendNotifications. Exiting")
    
    try:
        credentials = Credentials(credentialname, password)
        
        account = Account(emailname, credentials=credentials, autodiscover=True)
        log.info("Successfully connected to email account to send notifications")
    except Exception as e:
        log.critical("Was not able to connecto to Exchange account to send notifications")
        sys.exit()
    
    body = HTMLBody(htmlText)
    
    subject = "Automation Completed: {}".format(automationname)
    
    m = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=body,
        to_recipients=alertList
    )
    
    m.send_and_save()
    
    log.info("sent notification alert")
  
def sendPWNotify(htmlText, address):
    try:
        password = cred.password
        credentials = Credentials(credentialname, password)
        account = Account(emailname, credentials=credentials, autodiscover=True)
        log.info("succesfully connected to email account")
    except Exception as e:
        log.critical("Unable to connecto to Exchange")
        return 1
        
    body = HTMLBody(htmlText)
    subject = "Password Expiring Soon"
    
    m = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=body,
        to_recipients=address
    )
    m.send_and_save()
    log.info("Sent email notification to {}".format(address))
        