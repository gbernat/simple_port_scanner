#!/usr/bin/env python
import argparse
import time
import sys

from port_scanner import conf
from port_scanner.main import port_scanner


def banner(args):
    print("""\n\n\\\\\\ WILD PORT \\\\\\\\\n //// SCANNER ////\n\n""")
    print("I'm going to do:")
    print(' Target: {}'.format(args.target))
    print(' Range ports: {}'.format(str(conf.PORTS_RANGE)))
    print(' Max concurrent threads: {}'.format(str(args.threads)))
    print(' Firewall detection avoidance enabled: {}'.format(str(args.stealth)))
    print('\nLaunching scan...\n')


def main():
    parser = argparse.ArgumentParser(description='Port scanner')
    parser.add_argument(dest='target', type=str, help='Target hostname to scan')
    parser.add_argument('-o', '--output-json', required=False, dest='output_json', action='store_true', help='Creates a json file with scanning results in current path. Default: Disabled')
    parser.add_argument('-t', '--threads', required=False, dest='threads', default=5, type=int, help='Set max threads for concurrent execution. Default: 5')
    parser.add_argument('-f', '--disable-stealth', required=False, dest='stealth', action='store_false', help='Disable stealth feature. No random ports order and scanning intervalls changes will be performed to avoid firewall scanning pattern detection. Default: Enabled')
    argsh = parser.parse_args()

    conf_check = conf.check_configurations()
    if conf_check is not 'OK':
        print(conf_check)
        sys.exit()

    banner(argsh)

    t_init = time.time()

    # Run port scanning
    port_scanner(argsh.target, argsh.output_json, argsh.threads, argsh.stealth)

    t_delta = time.time() - t_init
    print('\nDone!\nTime consumed: {}m {}s\n'.format(str(time.gmtime(t_delta).tm_min), str(time.gmtime(t_delta).tm_sec)))

if __name__ == '__main__':
    main()
