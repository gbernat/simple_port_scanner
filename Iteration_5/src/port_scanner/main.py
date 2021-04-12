import socket
from multiprocessing.dummy import Pool as ThreadPool
import random
import time
import logging
import json
from . import conf


def shuffle_port_list(port_list=[]):
    """
    Returns the list of ports limiting MAX_CONSECUTIVE_PORT_SCAN elements in sequence.
    This is to avoid scans pattern detection by Firewalls 
    """
    logger = logging.getLogger()

    try:
        subgroup_lenght = conf.MAX_CONSECUTIVE_PORT_SCAN + 1

        # If port_list lenght is less than subgroup_lenght, just shuffle
        if len(port_list) < subgroup_lenght:
            random.shuffle(port_list)
            return port_list
    except TypeError as e:
        logger.error(e)
        return []    

    # Extract from the list every element stepped by subgroup_lenght, and append
    stepped = port_list[::subgroup_lenght]
    shuffled_list = list(filter(lambda l: l not in stepped, port_list))
    shuffled_list.extend(stepped)  

    return shuffled_list


def get_random_delays(cant=0):
    """
    Return a list of random delays between MIN & MAX_DELAY
    """ 
    logger = logging.getLogger()
    try:
        return [ round(random.uniform(conf.MIN_DELAY, conf.MAX_DELAY),1) for d in range(cant) ]
    except TypeError as e:
        logger.error(e)
        return []


def get_stealth_port_list(port_list=[]):
    """
    Shuffles ports list and calculates delays between scans
    This is to avoid scans pattern detection by Firewalls 
    """
    logger = logging.getLogger()

    ports = shuffle_port_list(port_list)
    delays = get_random_delays(len(port_list))

    stealth_list = []
    for p in ports:
        stealth_list.append( (p, delays.pop()) )

    logger.info('Stealth port list: {}'.format((stealth_list)))

    return stealth_list


def is_webserver(skt=None):
    """
    Determine if service is a webserver sending an HTTP GET stream
    """
    logger = logging.getLogger()

    try:
        skt.send(b'GET HTTP/1.1 \r\n')
        resp = str(skt.recv(300))

        logger.debug('Received: {}'.format(resp))
    except Exception as e:
        logger.error('Error trying to determine service. {}'.format(e))
        return False

    if 'doctype html' in resp.lower():
        return True
    else:
        return False


def check_port(dest=None):
    """
    Connect to target and check if port is open and if service is http
    """
    logger = logging.getLogger()

    try:
        target, port, delay = dest
    except (TypeError,ValueError) as e:
        logger.error(e)
        #return {'target': '', 'port': 0, 'status': ''}
        return {}

    res = {'target': target, 'port': port}

    logger.debug('Checking port: {} , sleeping: {}s'.format(port, delay))

    time.sleep(delay)

    # Try to establish connection to target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(conf.TIME_OUT)
    try:
        sock.connect((target, port))
        res['status'] = "open"

        # Try to detect if servide is a webserver
        res['web_server'] = is_webserver(sock)

    except:
        res['status'] = "closed"

    sock.close()
    return res


def print_results(results=[]):
    """
    Show results on stdout
    """
    logger = logging.getLogger()
    logger.debug('Scan results: {}'.format(str(results)))

    print('\nResults:')
    if not results:
        print('No ports were scanned')
    else:
        try:
            print('{} ports were scanned\n'.format(len(results)))
            opn = 0
            for res in results:
                if res['status'] is 'open':
                    opn += 1
                    if res['web_server']:
                        print('Port {}: {}  (http)'.format(str(res['port']), res['status']))
                    else:
                        print('Port {}: {}'.format(str(res['port']), res['status']))
            print('\n{} ports are open'.format(str(opn)))
        except TypeError as e:
            logger.error(e)


def export_results(results=[]):
    """
    Creates a json file with complete results, for programmatic use 
    """
    logger = logging.getLogger()

    try:
        filename = 'results_{}_{}.json'.format(results[0]['target'], time.strftime('%Y%M%d_%H%M'))
        with open(filename, 'w') as json_file:
            json.dump(results, json_file)
        print('\nFile {} has been created with scan results'.format(filename))            
        logger.info('File {} has been created with scan results'.format(filename))            
    except Exception as e:
        logger.error('Output json file could not be created. {}'.format(e))


def port_scanner(target_hostname, output_json, n_threads, stealth):
    """
    Execute ports scanning
    """
    logging.basicConfig(
        #level=logging.DEBUG,
        level= (conf.LOG_LEVEL).upper() if (conf.LOG_LEVEL).upper() in ['DEBUG','INFO','WARNING','ERROR','CRITICAL'] else 'ERROR',
        format='%(asctime)s - %(threadName)s - [%(levelname)s] %(message)s',
    )
    logger = logging.getLogger()

    # Prepare list of ports to scan
    # If stealth mode, list of ports is shuffled and a random delay is inserted between each one
    if stealth:
        ports = [ (target_hostname, prt, delay) for prt,delay in get_stealth_port_list(range(conf.PORTS_RANGE[0], conf.PORTS_RANGE[1]+1)) ]
    else:
        ports = [ (target_hostname, prt, 0) for prt in (range(conf.PORTS_RANGE[0], conf.PORTS_RANGE[1]+1)) ]

    logger.info('List of ports to scan (target,port,delay): {}'.format(str(ports)))

    # Launch threads of scans
    results = []
    pool = ThreadPool(n_threads)
    try:
        results = pool.map(check_port, ports)

    except KeyboardInterrupt:
        logger.info('Scan was interrupted by user Ctrl-C')
    except Exception as e:
        logger.error('Error on threads execution. {}'.format(str(e)))
        #results = []

    pool.close()
    pool.join()

    # Output results
    print_results(results)
    if output_json:
        export_results(results)

