import socket
from multiprocessing.dummy import Pool as ThreadPool
import time
import logging
import json
from . import conf


def check_port(dest):
    """
    Connect to target and check if port is open 
    """
    target, port = dest
    res = {'target': target, 'port': port}

    logger = logging.getLogger()
    logger.debug('Checking port: {}'.format(port))

    # Try to establish connection to target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(conf.TIME_OUT)
    try:
        sock.connect((target, port))
        res['status'] = "open"

    except:
        res['status'] = "closed"

    sock.close()
    return res


def print_results(results, output_json):
    """
    Show results on stdout
    """
    logger = logging.getLogger()
    logger.debug('Scan results: {}'.format(str(results)))

    print('\nResults:')
    if not results:
        print('No ports were scanned')
    else:
        print('{} ports were scanned\n'.format(len(results)))
        opn = 0
        for res in results:
            if res['status'] is 'open':
                opn += 1
                print('Port {}: {}'.format(str(res['port']), res['status']))
        print('\n{} ports are open'.format(str(opn)))

        # Creates a json file with complete results, for programmatic use 
        if output_json:
            filename = 'results_{}_{}.json'.format(results[0]['target'], time.strftime('%Y%M%d_%H%M'))
            try:
                with open(filename, 'w') as json_file:
                    json.dump(results, json_file)
                print('\nFile {} has been created with scan results'.format(filename))            
            except Exception as e:
                logger.error('Output json file could not be created. {}'.format(e))


def port_scanner(target_hostname, output_json, n_threads):
    """
    Execute ports scanning
    """
    logging.basicConfig(
        level=logging.DEBUG,
        #level=logging.WARNING,
        format='%(asctime)s - %(threadName)s - [%(levelname)s] %(message)s',
    )
    logger = logging.getLogger()

    # Prepare list of ports to scan
    ports = [ (target_hostname, prt) for prt in (range(conf.PORTS_RANGE[0], conf.PORTS_RANGE[1]+1)) ]

    logger.info('List of ports to scan (target,port): {}'.format(str(ports)))

    # Launch threads of scans
    pool = ThreadPool(n_threads)
    try:
        results = pool.map(check_port, ports)
    
    except Exception as e:
        logger.error('Error on threads execution. {}'.format(str(e)))
        results = []

    pool.close()
    pool.join()

    print_results(results, output_json)

