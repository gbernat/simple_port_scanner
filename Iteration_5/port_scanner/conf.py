"""
Global configurations
"""

## Ports range to be scanned (first, last)
PORTS_RANGE = (1,1024)
#PORTS_RANGE = (10,85)

## Max timeout in seconds to testing a connection
#  If set to None, socket is put in blocking mode (wait until error or socket connection time out)
#  If set to 0, non-blocking mode. If connection doesn't responde immediatly, returns fail
#TIME_OUT = None
TIME_OUT = 2

## Firewall detection avoidance
#  Max consecutive ports to scan
MAX_CONSECUTIVE_PORT_SCAN = 2
#  Time range in seconds for waiting between port scans 
MIN_DELAY = 0.1     # 100ms
MAX_DELAY = 2



""""
Config parameters validation
"""
def check_configurations():
    msg = ''
    try:
        if PORTS_RANGE[0] > PORTS_RANGE[1]:
            msg = 'Incorrect order in PORTS_RANGE\n'    
    except:
        msg = 'PORTS_RANGE conf is missing\n'
    try:
        if TIME_OUT is not None and TIME_OUT < 0:
            msg += 'Invalid value for TIME_OUT\n' 
    except:
        msg += 'TIME_OUT conf is missing\n'
    try:
        if MAX_CONSECUTIVE_PORT_SCAN < 0:
            msg += 'Invalid value for MAX_CONSECUTIVE_PORT_SCAN\n' 
    except:
        msg += 'MAX_CONSECUTIVE_PORT_SCAN conf is missing\n'
    try:
        if MIN_DELAY > MAX_DELAY:
            msg += 'Incorrect order for MIN_DELAY and MAX_DELAY\n' 
    except:
        msg += 'MIN_DELAY and/or MAX_DELAY conf are missing\n'


    if msg:
        return '\nThere were the following errors in configuration file:\n{}\nCancelling scan.\n'.format(msg)
    else:
        return 'OK'
