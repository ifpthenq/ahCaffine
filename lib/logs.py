"""
Module for logging 

"""
import os
import logging
from datetime import datetime
from logging import Handler,getLogger
import logging.handlers
import inspect


def getCaller():
    frame,filename,line_number,function_name,lines,index = inspect.stack()[-1]
    callerProgram = os.path.basename(filename)
    caller = str(callerProgram).replace('.py','')
    return caller
caller = getCaller()
path = "logs/{}".format(caller)
isExist = os.path.exists(path)
if not isExist:
    os.makedirs(path)

nameOfLog = 'main'

now_date = datetime.today().strftime('%Y%m%d')
print("log module loaded")

# ErrorHandler class is under the following copyright:
#   Copyright (c) 2008 Simplistix Ltd
class ErrorHandler(Handler):

    fired = False
    
    def __init__(self,level=logging.WARNING,logger='',install=True):
        Handler.__init__(self)
        self.level=level
        self.logger=logger
        if install:
            self.install()

    def install(self):
        self.setLevel(self.level)
        getLogger(self.logger).addHandler(self)
        
    def emit(self, record):
        self.fired=True

    def reset(self):
        self.fired=False

    def remove(self):
        getLogger().removeHandler(self)

SENDIT = 80
logging.addLevelName(SENDIT, 'SENDIT')
def sendit(self, message, *args, **kws):
    self.log(SENDIT, message, *args, **kws) 
logging.Logger.sendit = sendit




## Logging Configuration ##
#logfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), f"WD_EMPL-ADT_ATHENA_{now_date}.log")
logname = "{} - {}.log".format(nameOfLog, now_date)
errfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'logs/', "notifications.log")
logfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'logs/{}'.format(caller), logname)
print("Logfile name is {}".format(logfile))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set this level to control the master logging level.

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(logfile)
notification_handler = logging.FileHandler(errfile)
eh_notifications = ErrorHandler(logger=(__name__), level=logging.WARNING) #tripwire for notifications.

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)
notification_handler.setLevel(logging.WARNING)
smtp_handler = logging.handlers.SMTPHandler(mailhost='mailrelay.xxx.com',
                                            fromaddr='halla@xxx.com',
                                            toaddrs=['halla@xxx.com'],
                                            subject='{}'.format(caller))
smtp_handler.setLevel(SENDIT)                                           

#fmtr = logging.Formatter('%(asctime)s | [%(levelname)s] \t| (%(name)s) \t| %(message)s')
#fmtr = logging.Formatter('%(asctime)s | [%(levelname)s] \t|[%(filename)s:%(lineno)s] \t| (%(name)s) \t| %(message)s')
fmtr = logging.Formatter('[%(levelname)s] |[%(filename)s:%(lineno)s] \t| %(message)s')


file_handler.setFormatter(fmtr)
console_handler.setFormatter(fmtr)
notification_handler.setFormatter(fmtr)
smtp_handler.setFormatter(fmtr)

logger.addHandler(file_handler)
logger.addHandler(notification_handler)
logger.addHandler(eh_notifications)
logger.addHandler(console_handler) #disable this to stop console message output
logger.addHandler(smtp_handler)