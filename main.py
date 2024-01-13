import os
import sys
import time
import logging
from lib import logs
from lib.ahConfig import ahConfig

log = logging.getLogger('lib.logs.' + __name__)
log.info("==== INITIATE LOGFILE ====")

if __name__ == '__main__':
    log.info("BEGGINING MAIN")

    config = ahConfig()
    cfg = config.get_config_section('config')
    project_name = cfg['project_name']
