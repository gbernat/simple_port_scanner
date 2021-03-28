"""
Global configurations
"""

## Ports range to be scanned (first, last)
#PORTS_RANGE = (1,1024)
#PORTS_RANGE = (10,85)
PORTS_RANGE = (75,85)

## Max timeout in seconds to testing a connection
#  If set to None, socket is put in blocking mode (wait until error or socket connection time out)
#  If set to 0, non-blocking mode. If connection doesn't responde immediatly, returns fail
#TIME_OUT = None
TIME_OUT = 2



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


    if msg:
        return '\nThere were the following errors in configuration file:\n{}\nCancelling scan.\n'.format(msg)
    else:
        return 'OK'
